import re
import nltk
from nltk import PorterStemmer
from nltk.tokenize import RegexpTokenizer


def patch_ingred(ingredient):
    ingredient = ingredient.replace("&#174","")
    ingredient = re.sub(r'[\xf1]','n',ingredient)
    ingredient = re.sub(r'[^\x00-\x7F]',' ', ingredient)
    ingredient = re.sub(r'&nbsp','',ingredient)
    ingredient = re.sub(r'&#[0-9]+','',ingredient)
    ingredient = re.sub(r'&nbsp|&rarr|&larr','',ingredient)
    return ingredient

def extract_key_ingred(ingredient):
    key_words = "wtf"
    return key_words


##eps2= coll.find({'ingredient': 'lemon' })
##Ingred2 = []for q in eps2:
#print q['postinglist']       Ingred2.append (q['postinglist'])

##S1 = set(Ingred1[0])
##S2 = set(Ingred2[0])
##Intersect = S1&S2

def query(query_string):

    #TODO: Will need to add exclusion parsing here, prior to string cleaning
    #TODO: Otherwise, we will lose "-" sign

    processed_search = extract_key_ingred(query_string)

    return processed_search


def dead_query(query_string):
    results = []
    if query_string == "test1":
        results = [{'title':'Omelette Du Fromage', 'url':'http://www.urbandictionary.com/define.php?term=Omelette+du+fromage'},
           {'title':'Chicken Parmesan', 'url':'http://www.simplyrecipes.com/recipes/chicken_parmesan/'},
           {'title':'Franks Wing Dip', 'url':'https://www.franksredhot.com/recipes/franks-redhot-buffalo-chicken-dip-RE1242-1'},
           {'title':'Omelette Du Fromage', 'url':'http://www.urbandictionary.com/define.php?term=Omelette+du+fromage'},
           {'title':'Chicken Parmesan', 'url':'http://www.simplyrecipes.com/recipes/chicken_parmesan/'},
           {'title':'Franks Wing Dip', 'url':'https://www.franksredhot.com/recipes/franks-redhot-buffalo-chicken-dip-RE1242-1'},
           {'title':'Omelette Du Fromage', 'url':'http://www.urbandictionary.com/define.php?term=Omelette+du+fromage'},
           {'title':'Chicken Parmesan', 'url':'http://www.simplyrecipes.com/recipes/chicken_parmesan/'},
           {'title':'Franks Wing Dip', 'url':'https://www.franksredhot.com/recipes/franks-redhot-buffalo-chicken-dip-RE1242-1'},
           {'title':'Omelette Du Fromage', 'url':'http://www.urbandictionary.com/define.php?term=Omelette+du+fromage'},
           {'title':'Chicken Parmesan', 'url':'http://www.simplyrecipes.com/recipes/chicken_parmesan/'},
           {'title':'Franks Wing Dip', 'url':'https://www.franksredhot.com/recipes/franks-redhot-buffalo-chicken-dip-RE1242-1'},
           {'title':'Omelette Du Fromage', 'url':'http://www.urbandictionary.com/define.php?term=Omelette+du+fromage'},
           {'title':'Chicken Parmesan', 'url':'http://www.simplyrecipes.com/recipes/chicken_parmesan/'},
           {'title':'Franks Wing Dip', 'url':'https://www.franksredhot.com/recipes/franks-redhot-buffalo-chicken-dip-RE1242-1'},
           {'title':'Franks Wing Dip', 'url':'https://www.franksredhot.com/recipes/franks-redhot-buffalo-chicken-dip-RE1242-1'},
           ]
    elif query_string == "test2":
        results = [{'title':'Sample Title', 'url':'http://www.christopherllop.com'},
           {'title':'Sample Title 2', 'url':'http://www.christopherllop.com'},
           {'title':'Sample Title 3', 'url':'http://www.christopherllop.com'},
           {'title':'Sample Title 4', 'url':'http://www.christopherllop.com'},
           {'title':'Sample Title 5', 'url':'http://www.christopherllop.com'},
           {'title':'Sample Title 6', 'url':'http://www.christopherllop.com'},
           {'title':'Sample Title 7', 'url':'http://www.christopherllop.com'},
           {'title':'Sample Title 8', 'url':'http://www.christopherllop.com'},
           {'title':'Sample Title 9', 'url':'http://www.christopherllop.com'},
           {'title':'Sample Title 10', 'url':'http://www.christopherllop.com'},
           {'title':'Sample Title 11', 'url':'http://www.christopherllop.com'},
           {'title':'Sample Title 12', 'url':'http://www.christopherllop.com'},
           {'title':'Sample Title 13', 'url':'http://www.christopherllop.com'},
           {'title':'Sample Title 14', 'url':'http://www.christopherllop.com'},
           {'title':'Sample Title 15', 'url':'http://www.christopherllop.com'},
           {'title':'Sample Title 16', 'url':'http://www.christopherllop.com'},
           {'title':'Sample Title 17', 'url':'http://www.christopherllop.com'},
           {'title':'Sample Title 18', 'url':'http://www.christopherllop.com'},
           {'title':'Sample Title 19', 'url':'http://www.christopherllop.com'}
           ]
    return results

