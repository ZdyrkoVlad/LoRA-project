#!/usr/bin/env python
# coding: utf-8

# In[13]:


# JY, - Import dictionaries
# Import OWLReady
import owlready2
from owlready2 import *
from itertools import chain
import rdflib
# import sparql
from SPARQLWrapper import SPARQLWrapper, JSON
from rdflib import Graph, Literal, RDF, URIRef
from rdflib.namespace import FOAF, XSD

graph = default_world.as_rdflib_graph()

# Import Pandas, Numpy
import pandas as pd
from pprint import pprint
import numpy as np
import re

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)

print('ok - import dictionaries')

# In[15]:


import owlready2
from owlready2 import *
from itertools import chain
import rdflib
# import sparql
from SPARQLWrapper import SPARQLWrapper, JSON
from rdflib import Graph, Literal, RDF, URIRef
from rdflib.namespace import FOAF, XSD

graph = default_world.as_rdflib_graph()

onto = get_ontology("http://test.org/onto.owl")

with onto:
    class Food(Thing):
        pass


    class Vegetable(Food):
        pass


    class Fruit(Food):
        pass


    class Meat(Food):
        pass


    class Fish(Food):
        pass


    class Grain(Food):
        pass


    class Dairy(Food):
        pass


    class Tool(Thing):
        pass


    class Kitchenware(Tool):
        pass


    class Tableware(Tool):
        pass


    class Taste(Thing):
        pass


    class Country(Thing):
        pass


    class Color(Thing):
        pass


    class Nutrition(Thing):
        pass


    class Function(Thing):
        pass


    class Shape(Thing):
        pass


    class original_from(ObjectProperty):
        domain = [Food]
        range = [Country]


    class has_taste(ObjectProperty):
        domain = [Food]
        range = [Taste]


    class has_child_food(ObjectProperty):
        domain = [Food]
        range = [Food]


    class has_color(ObjectProperty):
        domain = [Food]
        range = [Color]


    class has_nutrition(ObjectProperty):
        domain = [Food]
        range = [Nutrition]


    class has_function(ObjectProperty):
        domain = [Tool]
        range = [Function]


    class has_shape(ObjectProperty):
        domain = [Tool]
        range = [Shape]


    class has_sub_function(ObjectProperty):
        domain = [Tool]
        range = [Tool]


    juicy = Taste('juicy')
    sweet = Taste('sweet')
    sour = Taste('sour')
    bitter = Taste('bitter')
    salty = Taste('salty')
    spicy = Taste('spicy')
    fruity = Taste('fruity')
    grassy = Taste('grassy')
    woody = Taste('woody')
    pungent = Taste('pungent')
    meaty = Taste('meaty')
    fishy = Taste('fishy')
    tangy = Taste('tangy')

    australia = Country('australia')
    new_zealand = Country('new_zealand')
    china = Country('china')
    canada = Country('canada')
    mexica = Country('mexica')
    america = Country('america')
    europe = Country('europe')
    asia = Country('asia')
    egypt = Country('egypt')
    india = Country('india')

    green = Color('green')
    red = Color('red')
    yellow = Color('yellow')
    white = Color('white')
    purple = Color('purple')

    protein = Nutrition('protein')
    fat = Nutrition('fat')

    fry = Function('fry')
    boil = Function('boil')
    drinking = Function('drinking')
    poking = Function('poking')
    stabbing = Function('stabbing')
    cutting = Function('cutting')
    servefood = Function('servefood')

    long = Shape('long')
    round = Shape('round')
    circular = Shape('circular')
    solid = Shape('solid')
    liquid = Shape('liquid')

    tomato = Vegetable("tomato", has_shape=[round], has_color=[red], has_taste=[juicy, sweet], original_from=[america])
    broccoli = Vegetable("broccoli", has_color=[green], has_taste=[juicy, sweet])
    bean = Vegetable("bean", has_color=[green], original_from=[australia, new_zealand])
    chilli = Vegetable("chilli", has_taste=[spicy], has_color=[green, red, yellow], original_from=[america])
    carrot = Vegetable("carrot", has_shape=[long], has_color=[yellow], has_taste=[woody])
    capsicum = Vegetable("capsicum", has_taste=[spicy], has_color=[green, red, yellow], original_from=[america])
    cucumber = Vegetable("cucumber", has_shape=[long], has_color=[green], has_taste=[juicy], original_from=[india])
    squash = Vegetable("squash", has_shape=[long], has_color=[green])
    cabbage = Vegetable("cabbage", has_taste=[sweet])
    ginger = Vegetable("ginger", has_taste=[pungent], original_from=[asia])
    garlic = Vegetable("garlic", has_color=[white], has_taste=[pungent], original_from=[asia])
    leek = Vegetable("leek", has_taste=[pungent], original_from=[australia, new_zealand])
    lettuce = Vegetable("lettuce", has_shape=[round], has_color=[green], original_from=[egypt])
    mushroom = Vegetable("mushroom", has_color=[white])
    onion = Vegetable("onion", has_shape=[round], has_color=[yellow, purple], has_taste=[pungent],
                      original_from=[australia, new_zealand])
    potato = Vegetable("potato", has_taste=[sweet], original_from=[america])
    pumpkin = Vegetable("pumpkin", has_taste=[sweet], has_color=[yellow], original_from=[mexica])
    parsley = Vegetable("parsley", has_color=[green], original_from=[mexica])
    green_onion = Vegetable("green_onion", has_shape=[long], has_color=[white, green], has_taste=[pungent],
                            original_from=[australia, new_zealand])
    eggplant = Vegetable("eggplant", has_shape=[long], has_color=[purple], has_taste=[sweet])
    asparagus = Vegetable("asparagus", has_shape=[long], has_color=[green], has_taste=[sweet])
    pepper = Vegetable("pepper", has_color=[green, red, yellow], has_taste=[spicy])

    orange = Fruit("orange", has_color=[yellow], has_for_taste=[sweet, sour, juicy])
    apple = Fruit("apple", has_color=[green, red], has_for_taste=[sweet], original_from=[america])
    banana = Fruit("banana", has_shape=[long], has_color=[yellow], has_for_taste=[sweet])
    lemon = Fruit("lemon", has_color=[yellow], has_taste=[sweet, sour, juicy], original_from=[china])
    plum = Fruit("plum", has_color=[purple], has_taste=[sweet, sour, juicy], original_from=[china])
    lime = Fruit("lime", has_color=[green], has_taste=[sweet, sour, juicy], original_from=[china])

    melon = Fruit("melon", has_taste=[sweet])
    kiwifruit = Fruit("kiwifruit", has_shape=[round], has_color=[green], original_from=[new_zealand])
    strawberry = Fruit("strawberry", has_color=[red], has_taste=[sweet])
    raspberry = Fruit("raspberry", has_color=[red], has_taste=[sweet])
    pineapple = Fruit("pineapple", has_color=[yellow], has_taste=[sweet])
    mandarin = Fruit("mandarin", has_color=[yellow], has_taste=[sweet, juicy])
    avocado = Fruit("avocado", has_shape=[round], has_color=[green], has_taste=[grassy], original_from=[america])
    watermelon = Fruit("watermelon", has_color=[green, red], has_taste=[sweet, juicy])
    grape = Fruit("grape", has_color=[green, red], has_taste=[juicy, sweet])
    cherry = Fruit("cherry", has_color=[red], has_taste=[sweet])
    pear = Fruit("pear", has_shape=[round], has_color=[green, yellow], has_taste=[juicy, sweet])

    green_apple = Fruit("green_apple", has_color=[green], has_taste=[sweet], original_from=[america])
    red_apple = Fruit("red_apple", has_color=[red], has_taste=[sweet], original_from=[america])

    apple = Fruit("apple", has_child_food=[red_apple])
    apple = Fruit("apple", has_child_food=[green_apple])

    beaf = Meat("beaf", has_taste=[meaty], has_color=[red])
    chicken = Meat("chicken", has_taste=[meaty], has_color=[white])
    lamb = Meat("lamb", has_taste=[meaty], has_color=[red])
    pork = Meat("pork", has_taste=[meaty], has_color=[red])

    salmon = Fish("salmon", has_taste=[fishy], has_nutrition=[fat, protein])
    shrimp = Fish("shrimp", has_taste=[fishy], has_nutrition=[protein])
    squid = Fish("squid", has_taste=[fishy], has_nutrition=[protein])
    fillet = Fish("fillet", has_taste=[fishy], has_nutrition=[fat, protein])

    egg = Dairy("egg", has_nutrition=[protein])
    yoghurt = Dairy("yoghurt", has_taste=[sweet], has_nutrition=[protein])
    cheese = Dairy("cheese", has_nutrition=[protein, fat])
    milk = Dairy("milk", has_nutrition=[protein, fat], has_taste=[sweet])

    rice = Grain("rice", has_shape=[round, long])
    noodle = Grain("noodle", has_shape=[long])
    pasta = Grain("pasta", has_shape=[round, long])
    bread = Grain("bread", has_shape=[long], has_taste=[tangy])
    corn = Grain("corn", has_color=[yellow], original_from=[america])

    pan = Kitchenware('pan', has_function=[fry], has_color=[red])
    pot = Kitchenware('pot', has_function=[boil], has_color=[red])
    chopping_board = Kitchenware('chopping_board', has_function=[cutting])

    spoon = Tableware('spoon', has_function=[drinking])
    fork = Tableware('fork', has_function=[poking, stabbing])
    knife = Tableware('knife', has_function=[cutting])
    plate = Tableware('plate', has_function=[servefood], has_shape=[circular])

    plate = Tableware('plate', has_function=[servefood], has_shape=[circular], has_sub_function=[chopping_board])

    print('ok-onto1')

# In[19]:

print('all objects')
print(list(onto.individuals()))

food = set(Food.instances())
print(f'{food=}')

kitchenware = set(Kitchenware.instances())
print(f'{kitchenware=}')