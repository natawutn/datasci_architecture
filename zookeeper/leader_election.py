#
from kazoo.client import KazooClient
from kazoo.exceptions import NodeExistsError
import time


class GroupMember:
    def __init__(self, hostname, base_path):
        self._base_path = base_path
        self._members_path = base_path + '/members/'
        self._leader_znode_name = base_path + '/leader'
        self._nmember = 0
        self._is_leader = False
        self._zk = KazooClient(hosts=hostname)
        self._zk.start()

    def get_id(self):
        return self._id

    def get_leader(self):
        if self._zk.exists(self._leader_znode_name):
            value, stats = self._zk.get(self._leader_znode_name, watch=self.watch_leader)
            leader_id = value.decode('utf-8')        
        else:
            leader_id = None
        return leader_id
    
    def is_leader(self):
        return self._is_leader
    
    def get_nmember(self):
        return self._nmember
        
    def join(self):
        self._zn = self._zk.create(self._members_path, ephemeral=True, sequence=True, makepath=True)
        self._id = self._zn.split('/')[-1]
        # set watch for member changes
        self._nmember = len(self._zk.get_children(self._members_path, watch=self.watch_members))

    def watch_members(self, event):
        # set watch for member changes
        n = len(self._zk.get_children(self._members_path, watch=self.watch_members))
        if n > self._nmember:
            print('A new member just joined')
        else:
            print('A member just left')
        self._nmember = n

    def watch_leader(self, event):
        print('Re-election')
        self.election(self.election_listener)

    def election(self, election_listener=None):
        self.election_listener = election_listener

        # we must ensure all writes have been committed
        self._is_leader = False
        self._zk.sync(self._leader_znode_name)
        try:
            self._zk.create(self._leader_znode_name, ephemeral=True, sequence=False, makepath=True)
            self._zk.set(self._leader_znode_name, bytes(self._id, 'utf-8'))  
            self._is_leader = True
        except NodeExistsError as e:
            pass
        
        if self._is_leader:
            # I want to become a leader
            print('{}: I am the leader'.format(self._id))
        else:
            leader_id = self.get_leader()
            self._zk.get(self._leader_znode_name, watch=self.watch_leader)
            print('{}: found leader {}'.format(self._id, leader_id))

        return self._is_leader


base_path = '/mycluster'
g = GroupMember('localhost', base_path)
g.join()
g.election()
while True:
    print('id = {}, leader = {}, members = {}'.format(g.get_id(), g.get_leader(), g.get_nmember()))
    time.sleep(3)