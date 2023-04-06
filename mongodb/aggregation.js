use("restaurants")

pipeline = [
    { $match: { rating: {$gt: 4.0}} },
    { $group: { _id: "$category", total: { $sum: "$votes"}} }
]

db.recipe.aggregate(pipeline)
