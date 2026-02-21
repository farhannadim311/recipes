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
    


def lowest_cost(recipes_db, food_name, forbidden_item = None):
    """
    Given a recipes database and the name of a food (str), return the lowest
    cost of a full recipe for the given food item or None if there is no way
    to make the food_item.
    """
    atomic_dic = atomic_ingredient_costs(recipes_db)
    compound_dic = compound_ingredient_possibilities(recipes_db)
    if(forbidden_item != None):
        for items in forbidden_item:
            if(items in atomic_dic):
                del atomic_dic[items]
            if(items in compound_dic):
                del compound_dic[items]
    def helper(f):
        min_cost = 9999999
        if(f not in atomic_dic and f not in compound_dic):
            return
        if(f in atomic_dic):
            return atomic_dic[f]
        else:
            if(f in compound_dic):
                for recipe in compound_dic[f]:
                    cost = 0
                    ingridient_missing = False
                    for ingridient in recipe:
                        catch = helper(ingridient[0]) 
                        if(catch == None):
                            ingridient_missing = True 
                            break 
                        cost = cost + catch * ingridient[1]
                    if(not(ingridient_missing)):
                        if (cost < min_cost):
                            min_cost = cost
        if(min_cost != 0 and min_cost != 9999999):                
            return min_cost
    return helper(food_name)






def scaled_recipe(recipe_dict, n):
    """
    Given a dictionary of ingredients mapped to quantities needed, returns a
    new dictionary with the quantities scaled by n.
    """
    new_dic = {}
    for key, values in recipe_dict.items():
        new_dic[key] = values * n
    return new_dic



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
    new_dic = {}
    for dic in recipe_dicts:
        for key, value in dic.items():
            if(key in new_dic):
                new_dic[key] += value
            else:
                new_dic[key] = value
    return new_dic


def cheapest_flat_recipe(recipes_db, food_name, forbidden_item = None):
    """
    Given a recipes database and the name of a food (str), return a dictionary
    (mapping atomic food items to quantities) representing the cheapest full
    recipe for the given food item.

    Returns None if there is no possible recipe.
    """
    #Observation - right now you are finding local minimum sure, as in the cheapest way to make the ingridients of a burger but there might be a burger with cheaper ingridients
    # Deleting the item in dictionary is weak because the ingridients can be compound as well
    atomic_dic = atomic_ingredient_costs(recipes_db)
    compound_dic = compound_ingredient_possibilities(recipes_db)
    master_dic = {}
    atomic_list = []
    if(forbidden_item != None):
        for items in forbidden_item:
            if(items in atomic_dic):
                del atomic_dic[items]
            if(items in compound_dic):
                del compound_dic[items]
    if(food_name in atomic_dic):
        return {food_name : 1}
    def helper(f):
        min_cost = 9999999
        if(f not in atomic_dic and f not in compound_dic):
            return
        if(f in atomic_dic):
            return atomic_dic[f]
        else:
            if(f in compound_dic):
                for recipe in compound_dic[f]:
                    cost = 0
                    ingridient_missing = False
                    for ingridient in recipe:
                        catch = helper(ingridient[0]) 
                        if(catch == None):
                            ingridient_missing = True 
                            break 
                        cost = cost + catch * ingridient[1]
                    if(not(ingridient_missing)):
                        if (cost < min_cost):
                            min_cost = cost
                            for key,value in recipe:
                                master_dic[f] = {key: value}
        if(min_cost != 0 and min_cost != 9999999):                
            return min_cost
    helper(food_name)
    masterfood = master_dic[food_name]
    def subhelper(food, scale):
        tmp = {}
        for key, value in food.items():
            if(key in atomic_dic):
                tmp[key] = value * scale
            else:
                subhelper(master_dic[key], value)
        atomic_list.append(tmp)
    
    subhelper(masterfood, 1)
    result = add_recipes(atomic_list)
    return result






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

def _filter_graph(graph, elts):
    elts = set(elts)
    return [i for i in graph if i[1] not in elts]

if __name__ == "__main__":
    # load recipe databases from the write-up
    with open("test_recipes/example_recipes.pickle", "rb") as f:
        example_recipes_db = pickle.load(f)

    with open("test_recipes/dairy_recipes.pickle", "rb") as f:
        dairy_recipes_db = pickle.load(f)

    with open("test_recipes/cookie_recipes.pickle", "rb") as f:
        cookie_recipes_db = pickle.load(f)
    
    graph = graph = [
        ('atomic', 'sc', 34), ('atomic', 'uw', 16), ('atomic', 'hm', 14),
        ('compound', 'wq', [('dx', 4), ('vf', 1), ('mc', 4), ('uw', 3), ('lf', 1), ('mt', 11), ('os', 3)]),
        ('atomic', 'vk', 21), ('atomic', 'kv', 5), ('atomic', 'rx', 38), ('atomic', 'fm', 44),
        ('atomic', 'mc', 21), ('atomic', 'dx', 25),
        ('compound', 'hl', [('qu', 4), ('dj', 3), ('wl', 1), ('er', 1), ('wz', 2), ('tw', 7), ('ur', 3), ('kx', 3), ('xn', 5)]),
        ('atomic', 'gg', 4), ('atomic', 'bh', 30), ('atomic', 'ox', 18),
        ('compound', 'er', [('fm', 5), ('hc', 3), ('vk', 3), ('si', 2), ('ap', 6), ('ku', 7)]),
        ('atomic', 'xz', 17), ('atomic', 'cr', 13),
        ('compound', 'ru', [('ap', 7), ('gg', 3), ('mt', 2), ('tw', 4)]),
        ('atomic', 'om', 10), ('atomic', 'cx', 12), ('atomic', 'mr', 33), ('atomic', 'zp', 31),
        ('atomic', 'nk', 23), ('atomic', 'wl', 39), ('atomic', 'vh', 46), ('atomic', 'sq', 15),
        ('atomic', 'kp', 31), ('atomic', 'tp', 50), ('atomic', 'dk', 15), ('atomic', 'hc', 45),
        ('compound', 'oi', [('vf', 4), ('dx', 7), ('xz', 7), ('lf', 7)]),
        ('compound', 'ru', [('lf', 5), ('ue', 1), ('cx', 4)]), # <--- THE CHEAPEST RU
        ('compound', 'oi', [('kf', 6), ('cb', 5), ('kh', 7)]),
        ('atomic', 'cb', 45), ('atomic', 'lb', 48),
        ('compound', 'ru', [('kf', 3), ('tw', 5), ('en', 4), ('fw', 7)]),
        ('atomic', 'le', 2),
        ('compound', 'ru', [('fm', 5), ('se', 4), ('yz', 6), ('jl', 5), ('tw', 6), ('gq', 1), ('wl', 5)]),
        ('atomic', 'jp', 14), ('atomic', 'xn', 28),
        ('compound', 'fz', [('ue', 1), ('wl', 5)]),
        ('atomic', 'ap', 45), ('atomic', 'rl', 12), ('atomic', 'qu', 24), ('atomic', 'tx', 27),
        ('atomic', 'yz', 14), ('atomic', 'kf', 50), ('atomic', 'cg', 20), ('atomic', 'ob', 21),
        ('atomic', 'tf', 21), ('atomic', 'qj', 14), ('atomic', 'pe', 34), ('atomic', 'gq', 40),
        ('atomic', 'en', 6), ('atomic', 'lf', 18), ('atomic', 'ea', 44), ('atomic', 'mt', 14),
        ('atomic', 'no', 15), ('atomic', 'tw', 19),
        ('compound', 'ru', [('mr', 7), ('cb', 3), ('jp', 3), ('lb', 4), ('jl', 7)]),
        ('atomic', 'bu', 9), ('atomic', 'ca', 22), ('atomic', 'si', 1), ('atomic', 'kh', 36),
        ('atomic', 'py', 26),
        ('compound', 'fk', [('ap', 3), ('kp', 5), ('ur', 4), ('bh', 6), ('jd', 7), ('gg', 5), ('ox', 3), ('om', 5)]),
        ('atomic', 'ag', 19), ('atomic', 'vc', 31), ('atomic', 'kn', 39), ('atomic', 'bp', 34),
        ('compound', 'qp', [('ru', 2)]), # <--- TARGET
        ('compound', 'hl', [('xn', 4), ('kp', 5), ('fm', 3)]),
        ('atomic', 'vi', 45), ('atomic', 'ut', 20), ('atomic', 'sr', 47), ('atomic', 'vf', 7),
        ('atomic', 'dj', 44), ('atomic', 'se', 44),
        ('compound', 'pu', [('ok', 3), ('vc', 2), ('en', 4), ('jy', 4)]),
        ('atomic', 'ku', 14), ('atomic', 'bo', 18),
        ('compound', 'fk', [('si', 3), ('gq', 2), ('en', 1), ('ru', 7), ('jl', 5)]),
        ('atomic', 'kw', 20), ('atomic', 'vd', 21), ('atomic', 'ue', 45), ('atomic', 'xs', 8),
        ('atomic', 'ef', 27),
        ('compound', 'ah', [('ca', 4), ('rx', 4), ('jp', 6), ('vi', 1), ('jl', 2)]),
        ('atomic', 'fi', 34), ('atomic', 'ep', 40), ('atomic', 'ne', 18), ('atomic', 'jd', 50),
        ('atomic', 'wz', 49), ('atomic', 'yt', 27), ('atomic', 'xa', 38), ('atomic', 'fo', 18),
        ('atomic', 'dg', 22), ('atomic', 'sh', 4), ('atomic', 'ur', 25),
        ('compound', 'fk', [('oi', 6), ('fw', 3), ('sq', 1), ('ku', 6), ('cr', 4), ('ap', 3), ('fm', 5), ('qj', 4)]),
        ('atomic', 'jl', 2), ('atomic', 'ok', 20),
        ('compound', 'oi', [('cg', 3), ('ep', 2), ('nk', 5), ('xs', 7), ('cb', 2), ('gg', 2), ('ob', 7), ('yz', 3), ('xn', 6)]),
        ('compound', 'os', [('ut', 2), ('lb', 3), ('xn', 4), ('dx', 6), ('xa', 5), ('si', 7)]),
        ('atomic', 'kx', 39), ('atomic', 'fw', 16),
        ('compound', 'ru', [('lf', 7), ('yz', 5), ('vh', 1), ('hm', 4)]),
        ('atomic', 'jy', 23),
        ('compound', 'yo', [('fm', 1), ('ag', 2), ('le', 5), ('gq', 4), ('fw', 5)])
    ]

    tst = cheapest_flat_recipe(graph, "qp")
    result     = {'cx': 8, 'lf': 10, 'ue': 2}
    print(tst)
    print(tst == result)