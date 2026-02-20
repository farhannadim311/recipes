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
    recipe_to_cost = {}
    for recipie in recipes_db:
        if(recipie[0] == 'atomic'):
            recipe_to_cost[recipie[1]] = recipie[2]
    return recipe_to_cost


def compound_ingredient_possibilities(recipes_db):
    """
    Given a recipes database, a list containing compound and atomic food tuples,
    make and return a dictionary that maps each compound food name to a
    list of all the ingredient lists associated with that name.
    """
    recipe_to_ingridient = {}
    for recipie in recipes_db:
        if(recipie[0] == 'compound'):
            if(recipie[1] in recipe_to_ingridient):
                recipe_to_ingridient[recipie[1]].append(recipie[2])
            else:
                recipe_to_ingridient[recipie[1]] = []
                recipe_to_ingridient[recipie[1]].append(recipie[2])
    return recipe_to_ingridient
    


def lowest_cost(recipes_db, food_name):
    """
    Given a recipes database and the name of a food (str), return the lowest
    cost of a full recipe for the given food item or None if there is no way
    to make the food_item.
    """
    atomic_dic = atomic_ingredient_costs(recipes_db)
    compound_dic = compound_ingredient_possibilities(recipes_db)
    def helper(f):
        cost = 0
        min_cost = 9999999
        if(f in atomic_dic):
            return atomic_dic[f]
        else:
            if(f in compound_dic):
                for recipe in compound_dic[f]:
                    for ingridient in recipe:
                        for i in range(ingridient[1]):
                            cost = cost + helper(ingridient[0])
                    if (cost < min_cost):
                        min_cost = cost
        if(min_cost != 0):                
            return cost
    
    return helper(food_name)






def scaled_recipe(recipe_dict, n):
    """
    Given a dictionary of ingredients mapped to quantities needed, returns a
    new dictionary with the quantities scaled by n.
    """
    raise NotImplementedError


def add_recipes(recipe_dicts):
    """
    Given a list of recipe dictionaries that map atomic food items to quantities,
    return a new dictionary that maps each ingredient name
    to the sum of its quantities across the given recipe dictionaries.

    For example,
        add_recipes([{'milk':1, 'chocolate':1}, {'sugar':1, 'milk':2}])
    should return:
        {'milk':3, 'chocolate': 1, 'sugar': 1}
    """
    raise NotImplementedError


def cheapest_flat_recipe(recipes_db, food_name):
    """
    Given a recipes database and the name of a food (str), return a dictionary
    (mapping atomic food items to quantities) representing the cheapest full
    recipe for the given food item.

    Returns None if there is no possible recipe.
    """
    raise NotImplementedError


def combine_recipes(nested_recipes):
    """
    Given a list of lists of recipe dictionaries, where each inner list
    represents all the recipes for a certain ingredient, compute and return a
    list of recipe dictionaries that represent all the possible combinations of
    ingredient recipes.
    """
    raise NotImplementedError


def all_flat_recipes(recipes_db, food_name):
    """
    Given a recipes database, the name of a food (str), produce a list (in any
    order) of all possible flat recipe dictionaries for that category.

    Returns an empty list if there are no possible recipes
    """
    raise NotImplementedError


if __name__ == "__main__":
    # load recipe databases from the write-up
    with open("test_recipes/example_recipes.pickle", "rb") as f:
        example_recipes_db = pickle.load(f)

    with open("test_recipes/dairy_recipes.pickle", "rb") as f:
        dairy_recipes_db = pickle.load(f)

    with open("test_recipes/cookie_recipes.pickle", "rb") as f:
        cookie_recipes_db = pickle.load(f)
    print(lowest_cost(example_recipes_db, "cheese"))
