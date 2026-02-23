# 6.1010 Recipes Lab

This project explores tree recursion to calculate the paths, compositions, and costs related to combining and breaking down compound food items into their atomic ingredients.

## Features
- **Atomic and Compound Costs**: Evaluate the atomic ingredients needed to build a given complex recipe and map them to their specific costs.
- **Lowest Recipe Cost**: Calculate the most optimal, cheapest cost to build a given food item from scratch.
- **Cheapest Flat Recipe**: Find the most cost-effective dictionary of base atomic items necessary for a specific food.
- **All Flat Recipes**: Output all valid flattened configuration paths (as dictionaries) to successfully put together a recipe without duplicate traversal.

## Core Files
- `lab.py`: Core logic and recursive functions for processing the recipe database.
- `test.py`: Unit tests checking edge cases and function correctness.
- `test_recipes/`: Directory containing various pre-built recipe databases serialized via `pickle` (e.g. `dairy_recipes.pickle`, `cookie_recipes.pickle`).

## Usage
Simply run python on the `lab.py` file to test outputs, or run `pytest test.py` to evaluate overall functionality and correctness.
