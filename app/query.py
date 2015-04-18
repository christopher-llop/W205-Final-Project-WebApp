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
    measures = ['ounce','ounces','cup','cups','pound','pounds','kilos',
            'grams','gram','kilo','bag','bags','teaspoon',
            'teaspoons','tablespoon','tablespoons','tbsp','tbsps',
            'lbs','kg','kilogram','kilograms','can','cans',
            'tsp','tsps','oz','pint','pt','pints','pack','packs','packed',
            'pinch']

    english_sw = nltk.corpus.stopwords.words('english')

    methods = ['grounded','crushed','chopped', 'cored', 'peeled', 'sliced',
               'squeezed','diced','divided','softened','thawed','needed',
               'drained','rinsed','beaten','husked','cleaned','mashed','melted',
               'dried','processed','grated','frying','chopp','chuncked','chunk']

    ingredient = ingredient.strip().lower()
    ingredient = patch_ingred(ingredient)
    #print "original ingredients {}".format(ingredient)
    tokenizer = RegexpTokenizer(r'\w+')
    tkn = tokenizer.tokenize(ingredient)
    ps = PorterStemmer()
    tkn = [ps.stem(t) for t in tkn if t not in measures and t not in methods and t not in english_sw]
    tagged = nltk.pos_tag(tkn)
    key_words = [w for w,tag in tagged if tag != 'LS' and tag != 'CD']
    np = [w for w,tag in tagged if tag == 'NN'] # noun phrase
    np = ' '.join(np)
    if np not in key_words and len(np) > 0 and len(np.split()) <= 3:
        key_words.append(np)
    return key_words

    return 0

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

