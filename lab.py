"""
6.101 Lab:
Recipes
"""

import pickle
import sys
# import typing # optional import
# import pprint # optional import

sys.setrecursionlimit(20_000)
# NO ADDITIONAL IMPORTS!


def atomic_ingredient_costs(recipes_db):
    """
    Given a recipes database, a list containing compound and atomic food tuples,
    make and return a dictionary mapping each atomic food name to its cost.
    """
    atomic = {}
    for i in recipes_db:
        if(i[0]== "atomic"):
            atomic[i[1]] = i[2]
    return atomic



def compound_ingredient_possibilities(recipes_db):
    """
    Given a recipes database, a list containing compound and atomic food tuples,
    make and return a dictionary that maps each compound food name to a
    list of all the ingredient lists associated with that name.
    """
    compound = {}
    for item in recipes_db:
        if item[0] == "compound":
            name = item[1]
            ingredients = item[2]
            if name not in compound:
                compound[name] = [ingredients]  # wrap in a list
            else:
                compound[name].append(ingredients)  # add another list of ingredients
    return compound
                


def lowest_cost(recipes_db, food_name, forbidden = []):
    """
    Given a recipes database and the name of a food (str), return the lowest
    cost of a full recipe for the given food item or None if there is no way
    to make the food_item.
    """
    atomic = atomic_ingredient_costs(recipes_db)
    compound = compound_ingredient_possibilities(recipes_db)
    cost_arr = []
    g = forbidden
    if food_name in forbidden:
        return None
    if(len(forbidden) > 0):
        for i in forbidden:
            if(i in compound):
                del compound[i]
            if (i in atomic):
                del atomic[i]

    if food_name not in atomic and food_name not in compound:
        return None

    if food_name in atomic:
        return atomic[food_name]

    for lst in compound[food_name]:
        valid = True
        cost = 0
        for item in lst:
            ingredient_name, quantity = item
            sub_cost = lowest_cost(recipes_db, ingredient_name, g)
            if sub_cost is None:
                valid = False
                break
            cost += sub_cost * quantity
        if valid:
            cost_arr.append(cost)

    if len(cost_arr) == 0:
        return None

    return min(cost_arr)



               




def scaled_recipe(recipe_dict, n):
    """
    Given a dictionary of ingredients mapped to quantities needed, returns a
    new dictionary with the quantities scaled by n.
    """
    dic = {}
    for i in recipe_dict:
        dic[i] = recipe_dict[i] * n
    return dic


def add_recipes(recipe_dicts):
    """
    Given a list of recipe dictionaries that map food items to quantities,
    return a new dictionary that maps each ingredient name
    to the sum of its quantities across the given recipe dictionaries.

    For example,
        add_recipes([{'milk':1, 'chocolate':1}, {'sugar':1, 'milk':2}])
    should return:
        {'milk':3, 'chocolate': 1, 'sugar': 1}
    """
    dic = {}
    for recipies in recipe_dicts:
        for items in recipies:
            if(items not in dic):
                dic[items] = recipies[items]
            else:
                dic[items] = dic[items] + recipies[items]
    return dic



def cheapest_flat_recipe(recipes_db, food_name, forbidden = []):
    """
    Given a recipes database and the name of a food (str), return a dictionary
    (mapping atomic food items to quantities) representing the cheapest full
    recipe for the given food item.

    Returns None if there is no possible recipe.
    """
    atomic = atomic_ingredient_costs(recipes_db)
    compound = compound_ingredient_possibilities(recipes_db)
    
    if food_name in forbidden:
        return None

    # Remove forbidden items from atomic and compound dictionaries
    for item in forbidden:
        if item in atomic:
            del atomic[item]
        if item in compound:
            del compound[item]

    if food_name not in atomic and food_name not in compound:
        return None

    if food_name in atomic:
        return {food_name: 1}

    best_cost = None
    best_recipe = None

    for recipe in compound.get(food_name, []):
        subrecipes = []
        for ing_name, qty in recipe:
            subrecipe = cheapest_flat_recipe(recipes_db, ing_name, forbidden)
            if subrecipe is None:
                break
            subrecipes.append(scaled_recipe(subrecipe, qty))
        else:
            combined = add_recipes(subrecipes)
            cost = sum(combined[ing] * atomic[ing] for ing in combined)
            if best_cost is None or cost < best_cost:
                best_cost = cost
                best_recipe = combined

    return best_recipe


def combine_recipes(nested_recipes):
    """
    Given a list of lists of recipe dictionaries, where each inner list
    represents all the recipes for a certain ingredient, compute and return a
    list of recipe dictionaries that represent all the possible combinations of
    ingredient recipes.
    """
    if(len(nested_recipes) == 1):
        return nested_recipes[0]
    first = nested_recipes[0]
    rest_combined = combine_recipes(nested_recipes[1:])
    result = []
    for recipe1 in first:
        for recipe2 in rest_combined:
            combined = recipe1.copy()
            for key, values in recipe2.items():
                if(key in combined):
                    val = combined[key] + values
                    combined[key] = val
                else:
                    combined[key] = values
            result.append(combined)
    return result


def all_flat_recipes(recipes_db, food_name, forbidden = []):
    """
    Given a recipes database, the name of a food (str), produce a list (in any
    order) of all possible flat recipe dictionaries for that category.

    Returns an empty list if there are no possible recipes
    """
    if food_name in forbidden:
        return []
    
    atomic = atomic_ingredient_costs(recipes_db)
    compound = compound_ingredient_possibilities(recipes_db)
    if food_name in atomic:
        return [{food_name : 1}]
    
    if food_name not in compound:
        return []
    
    all_recipes = []
    for recipe in compound[food_name]:
        ingridient_combos = []
        for ingridient, qty in recipe:
            subrecipes = all_flat_recipes(recipes_db, ingridient, forbidden)
            if not subrecipes:
                break
            scaled = [scaled_recipe(r,qty) for r in subrecipes]
            ingridient_combos.append(scaled)
        else:
            all_recipes.extend(combine_recipes(ingridient_combos))
    return all_recipes



if __name__ == "__main__":
    # load example recipes from section 3 of the write-up
    with open("test_recipes/example_recipes.pickle", "rb") as f:
        example_recipes_db = pickle.load(f)
    # you are free to add additional testing code here!
    print(example_recipes_db)
