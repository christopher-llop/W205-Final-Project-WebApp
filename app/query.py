import re
import nltk
from nltk import PorterStemmer
from nltk.tokenize import RegexpTokenizer
from pymongo import MongoClient
from bson.objectid import ObjectId

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

    english_sw = [
        'i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you',  'your',
        'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she',
        'her', 'hers', 'herself', 'it', 'its', 'itself', 'they', 'them', 'their',
        'theirs', 'themselves', 'what', 'which', 'who', 'whom', 'this', 'that',
        'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being',
        'have', 'has', 'had',  'having', 'do', 'does', 'did', 'doing', 'a', 'an',
        'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while', 'of',
        'at', 'by', 'for', 'with', 'about', 'against', 'between', 'into', 'through',
        'during', 'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down',
        'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then',
        'once', 'here', 'there', 'when', 'where', 'why', 'how', 'all', 'any',
        'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor',
        'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 's', 't', 'can',
        'will', 'just', 'don', 'should', 'now'
    ]

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
    #tagged = nltk.pos_tag(tkn)
    #key_words = [w for w,tag in tagged if tag != 'LS' and tag != 'CD']
    #np = [w for w,tag in tagged if tag == 'NN'] # noun phrase
    #np = ' '.join(np)
    #if np not in key_words and len(np) > 0 and len(np.split()) <= 3:
    #    key_words.append(np)
    key_words = tkn
    return key_words


def query(query_string):
    MONGODB_URI = 'mongodb://recipe:recipe@ds053370.mongolab.com:53370/recipemaker'
    client = MongoClient(MONGODB_URI)

    db = client['recipemaker']
    print db.collection_names()
    inv_ind = db.recipe_index
    #doc_info = db.recipeURLs

    #TODO: Will need to add exclusion parsing here, prior to string cleaning
    #TODO: Otherwise, we will lose "-" sign

    processed_search = extract_key_ingred(query_string)

    possible_documents = []
    for ingredient in processed_search:
        print "searching for " + str(ingredient)
        try:
            get_documents = inv_ind.find_one({"ingredient":ingredient})[u'postinglist']
            if possible_documents == []:
                possible_documents = get_documents
            else:
                possible_documents = set(possible_documents) & set(get_documents)
        except:
            pass
    return possible_documents




def ranked_query(query_string):
    #MONGODB_URI = 'mongodb://recipe:recipe@ds053370.mongolab.com:53370/recipemaker'
    MONGODB_URI = 'mongodb://query:query@ds029142-a0.mongolab.com:29142/scraper'
    client = MongoClient(MONGODB_URI)
    #db = client['recipemaker']
    db = client['scraper']

    ranked_ind = db.rank3
    processed_search = extract_key_ingred(query_string)
    print processed_search

    possible_documents = []
    #Part 1: Pull doc data from MongoDB
    #1. We only need to keep one copy of doc-specific ranks.
    #2. For each doc, count the # of matched terms
    #3. For each doc, sum the ingredient IDF
    query_results = dict()
    max_results_count = 0
    max_matched_IDF = 0
    for ingredient in processed_search:
        print "searching for " + str(ingredient)
        try:
            query_ingredient = ranked_ind.find_one({"ingredient":ingredient})
            # For each result
            for k, v in query_ingredient[u'postinglistIDFRankCount'].iteritems():
                # If this document was not part of a previous query ingredient, get the doc-specific array
                query_results[k] = query_results.get(k, v)
                # Inflate the array to have 5 values
                while len(query_results[k]) < 5:
                    query_results[k].append(0)
                # Add the ingredient IDFs together
                query_results[k][3] += query_ingredient[u'ingredIDF']
                # Count the number of ingredients that returend that doc
                query_results[k][4] += 1
                # Array is: [DocIDF, DocRank, DocIngredients, MatchedIDF, MatchedIngredients]
            max_results_count += 1
            max_matched_IDF += query_ingredient[u'ingredIDF']

        except:
            print "query pass"
            pass

    #Part 2: Rank and Sort
    ranked_results = dict()
    n = 0
    try:
        for k, v in query_results.iteritems():
            n += 1
            ranked_results[k] = n
    except:
        print "rank pass"
        pass


    ranked_docs = sorted(query_results, key=query_results.__getitem__, reverse=True)


    print ranked_docs
    return ranked_docs

def fetch_details(post_list):
    print "fetching details"
    MONGODB_URI = 'mongodb://query:query@ds029142-a0.mongolab.com:29142/scraper'
    #MONGODB_URI = 'mongodb://recipe:recipe@ds053370.mongolab.com:53370/recipemaker'

    client = MongoClient(MONGODB_URI)

    db = client['scraper']
    #db = client['recipemaker']
    doc_info = db.recipeURLs

    details = []
    for doc_id in post_list:
        try:
            get_info = doc_info.find_one({"_id": ObjectId(doc_id)})
            get_info.pop(u'ingred',None)
            details.append(get_info)
        except:
            pass

    return details

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

