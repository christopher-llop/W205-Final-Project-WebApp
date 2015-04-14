import sys
from pymongo import MongoClient
import re
import nltk
from nltk import PorterStemmer
from nltk.tokenize import RegexpTokenizer
from bson.objectid import ObjectId

# Clean query - determine count of terms
# Stem query - stem query as needed
# Get inclusion postings
# Find overlap (inner join)
# Get metadata
# Rank
# Return results

def patch_ingred(ingredient):
    ingredient = ingredient.replace("&#174","")
    ingredient = re.sub(r'[\xf1]','n',ingredient)
    ingredient = re.sub(r'[^\x00-\x7F]',' ', ingredient)
    ingredient = re.sub(r'&nbsp','',ingredient)
    ingredient = re.sub(r'&#[0-9]+','',ingredient)
    ingredient = re.sub(r'&nbsp|&rarr|&larr','',ingredient)
    return ingredient

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

def extract_key_ingred(ingredient):
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

##eps2= coll.find({'ingredient': 'lemon' })
##Ingred2 = []for q in eps2:
#print q['postinglist']       Ingred2.append (q['postinglist'])

##S1 = set(Ingred1[0])
##S2 = set(Ingred2[0])
##Intersect = S1&S2

def query(query_string):
    MONGODB_URI = 'mongodb://recipe:recipe@ds053370.mongolab.com:53370/recipemaker'

    client = MongoClient(MONGODB_URI)

    #print client.database_names()
    db = client['recipemaker']
    print db.collection_names()
    inv_ind = db.recipe_index
    doc_info = db.recipeURLs

    #TODO: Will need to add exclusion parsing here, prior to string cleaning
    #TODO: Otherwise, we will lose "-" sign

    processed_search = extract_key_ingred(query_string)

    possible_documents = []
    for ingredient in processed_search:
        print "searching for " + str(ingredient)
        try:
            #get_documents = []
            get_documents = inv_ind.find_one({"ingredient":ingredient})[u'postinglist']
            if possible_documents == []:
                possible_documents = get_documents
            else:
                #S1 = set(possible_documents)
                #S2 = set(get_documents)
                #S3 = S1 & S2
                possible_documents = set(possible_documents) & set(get_documents)
        except:
            pass

    results = []
    i = 0
    for doc_id in possible_documents:
        #get_info = doc_info.find_one({"url":"http://www.simplyrecipes.com/recipes/broccoli_apple_soup/"})
        get_info = doc_info.find_one({"_id": ObjectId(doc_id)})
        get_info.pop(u'ingred',None)
        results.append(get_info)
        i += 1
        #print i
        if i >= 100:
            break

    return results


#query("lemon apple almonds")