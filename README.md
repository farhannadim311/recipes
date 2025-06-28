# 🍲 Recursive Recipe Cost Calculator & Expansion Engine

This Python project implements a recursive system for managing and computing information about recipes from a structured database. It can calculate the **lowest cost** to produce a food item, and generate **all valid flattened recipes** for compound items based on their ingredients.

---

## 📌 Features

- ✅ **Atomic & Compound Food Representation**
  - Atomic: `('atomic', 'item name', cost)`
  - Compound: `('compound', 'item name', [('ingredient', quantity), ...])`

- 🔁 **Supports Multiple Recipes per Item**
  - Handles multiple ways to make the same compound item

- 🧠 **Recursively Resolves Ingredient Trees**
  - Computes nested ingredient costs and combinations

- 💸 **`lowest_cost(recipes_db, food_name)`**
  - Recursively finds the cheapest way to make a food item using atomic ingredients

- 📦 **`all_flat_recipes(recipes_db, food_name, forbidden=[])`**
  - Returns **all possible flat recipe dictionaries**
  - Supports `forbidden` ingredients for exclusion logic

- ⚙️ **Helper Functions**
  - `combine_recipes(...)` – merges all ingredient recipe combos
  - `scaled_recipe(...)` – multiplies ingredient quantities
  - `add_recipes(...)` – merges recipe dictionaries

---

## 🧪 Example Usage

```python
example_db = [
    ('compound', 'cookie sandwich', [('cookie', 2), ('ice cream scoop', 3)]),
    ('compound', 'cookie', [('chocolate chips', 3)]),
    ('compound', 'cookie', [('sugar', 10)]),
    ('atomic', 'chocolate chips', 200),
    ('atomic', 'sugar', 5),
    ('compound', 'ice cream scoop', [('vanilla ice cream', 1)]),
    ('compound', 'ice cream scoop', [('chocolate ice cream', 1)]),
    ('atomic', 'vanilla ice cream', 20),
    ('atomic', 'chocolate ice cream', 30),
]

lowest_cost(example_db, 'cookie sandwich')
# Output: 160 or similar (depending on cheapest ingredient path)

all_flat_recipes(example_db, 'cookie sandwich')
# Output: List of dictionaries like:
# [{'chocolate chips': 6, 'vanilla ice cream': 3}, {'sugar': 20, 'chocolate ice cream': 3}, ...]
