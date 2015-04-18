import re
import nltk
from nltk import PorterStemmer
from nltk.tokenize import RegexpTokenizer

measures = ['ounce','ounces','cup','cups','pound','pounds','kilos',\
            'grams','gram','kilo','bag','bags','teaspoon',\
            'teaspoons','tablespoon','tablespoons','tbsp','tbsps',\
            'lbs','kg','kilogram','kilograms','can','cans',\
            'tsp','tsps','oz','pint','pt','pints','pack','packs','packed',\
            'pinch']

english_sw = nltk.corpus.stopwords.words('english')

methods = ['grounded','crushed','chopped', 'cored', 'peeled', 'sliced',\
           'squeezed','diced','divided','softened','thawed','needed',\
           'drained','rinsed','beaten','husked','cleaned','mashed','melted',\
           'dried','processed','grated','frying','chopp','chuncked','chunk']



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

