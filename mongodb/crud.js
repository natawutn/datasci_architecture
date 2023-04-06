use("restaurants")

db.recipe.insertOne(
    {
      name: "Pad Thai",
      cuisine: "Thai",
      category: "Noodle",
      rating: 4.7,
      votes: 9301,
      ingredients: [
        { item: "noodle", quantity: "125", unit: "g" },
        { item: "chicken", quantity: "150", unit: "g" },
        { item: "brown sugar", quantity: "3", unit: "tbsp" }
      ]
    }
  )

db.recipe.insertMany([ 
    { name: "Tom Yum", cuisine: "Thai", category: "Soup", rating: 4.3, votes: 13450, ingredients: [ { item: "shrimp", quantity: "200", unit: "g" }, { item: "water", quantity: "500", unit: "cc" }, { item: "lemon grass", quantity: "10", unit: "g" } ] },
    { name: "Chick Rice", cuisine: "Chinese", category: "Rice", rating: 3.5, votes: 7116, ingredients: [ { item: "rice", quantity: "300", unit: "g" }, { item: "chicken", quantity: "150", unit: "g" } ] },
    { name: "Salmon Sushi", cuisine: "Japanese", category: "Rice", rating: 4.1, votes: 5593, ingredients: [ { item: "salmon", quantity: "25", unit: "g" }, { item: "rice", quantity: "50", unit: "g" }, { item: "vinegar", quantity: "1", unit: "tsp" } ] },
    { name: "Miso Soup", cuisine: "Japanese", category: "Soup", rating: 3.7, votes: 6082, ingredients: [ { item: "tofu", quantity: "50", unit: "g" }, { item: "water", quantity: "200", unit: "cc" }, { item: "miso paste", quantity: "2", unit: "tsp" } ] }
])

db.recipe.find(
    { cuisine: "Thai", rating: { $gt: 4.4 } },
    { name: 1, rating: 1, category: 1 }
).limit(2)