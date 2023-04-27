from kazoo.client import KazooClient

def zk_tree(zk, path, ident=''):
    print(ident, path)
    nextident = ident + '  '
    for c in zk.get_children(path):
        nextpath = path + ('' if path.endswith('/') else '/') + c
        zk_tree(zk, nextpath, nextident)


zk = KazooClient(hosts='localhost')
zk.start()
zk.ensure_path('/mycluster/nodes')
zn_node = zk.create('/mycluster/nodes/', ephemeral=True, sequence=True, makepath=True)
print('zn_node = ', zn_node)
zk_tree(zk, '/mycluster')

zk2 = KazooClient(hosts='localhost')
zk2.start()
zk2.ensure_path('/mycluster/nodes')
zn_node2 = zk2.create('/mycluster/nodes/', ephemeral=True, sequence=True, makepath=True)
print('zn_node2 = ', zn_node2)
print('before zk2 stop')
zk_tree(zk, '/mycluster')
zk2.stop()

print('after zk2 stop')
zk_tree(zk, '/mycluster')

zk.stop()
print('after zk and zk2 stop')
zk3 = KazooClient(hosts='localhost')
zk3.start()
zk_tree(zk3, '/mycluster')
zk3.delete('/mycluster', recursive=True)
zk3.stop()

