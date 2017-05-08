from flask import *
from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search, Q
import collections


es = Elasticsearch(['localhost'], http_auth=('elastic', 'changeme'), port=9200)
app = Flask(__name__)

@app.route("/")
# show the query page
def search():
    return render_template('homepage.html')


@app.route("/results", methods=['POST'])
# do the searching and show the first 10 results
def results():
    try:

        # get the query from user
        Title = request.form['Job Title']
        Description = request.form['Job Description']
        Company = request.form['Company']
        Type = request.form['Job Type']
        State = request.form['State']
        City = request.form['City']
        ZipCode = request.form['ZipCode']
        Salary = request.form['Salary']
        Date = request.form['Date']

        print Title

        # # store the queries in SearchResult class
        # if query == "Keywords":
        #     query = ""
        # result.set_query(query)
        # if starring.find("Starring") >= 0:
        #     starring = ""
        # result.set_starring(starring)
        # result.set_genre(genre)
        # if runtimemax == "Upperbound":
        #     runtimemax = ""
        # if runtimemin == "Lowerbound":
        #     runtimemin = ""
        #
        # result.set_runtime(runtimemax,runtimemin)
        #
        # # if the user did not input any query, redirect to query page
        # if query == "" and starring == "" and genre == "" and runtimemax == "" and runtimemin == "":
        #     return render_template('index.html')
        #
        # # Form Query
        # s = Search(using=es)
        # s = s.index('imdb')
        # s = s.source(includes=['text', 'title', 'country', 'id']) # setup the reuturned data fields of hits
        # s = s.query(Q('match_all'))
        # q0 = Q('match_all') # used for genre query
        # q1 = Q('match_all') # used for starring query
        #
        #
        # # dealing with starring query
        # if starring != "":
        #     for cast in result.get_starringlist():
        #         # if there is only one name, then search the name
        #         if q1 == Q('match_all'):
        #             q1 = Q('match_phrase', starring= cast)
        #         # if there are multiple names, then do disjunctive search over the names
        #         else:
        #             q1 = q1 | Q('match_phrase', starring= cast)
        #
        # # dealing with runtime query by using range query
        # filter = Q('range', runtime = {'gte': result.get_runtime()[1], 'lte' : result.get_runtime()[0]})
        #
        # # dealing with genre query
        # if genre != "":
        #     q0 = Q('match', categories = genre)
        #
        # # dealing with keyword query
        # if query != "":
        #     s = result.buildquery(query, s)
        #
        # # join all queries together and set the highlight option
        # s = s.query(q0)
        # s = s.query(q1)
        # s = s.query(filter)
        # print s.to_dict()
        # s = s.highlight_options(order='score').highlight('text', fragment_size=100000, number_of_fragments=1)
        #
        # # save the final query in SearchResult class
        # result.set_search(s)
        #
        # # do the search
        # ret = s.execute()
        #
        # # save the total hits' number and highlighted texts in SearchResult class
        # resultlist = get_movies(ret.hits)
        # result.set_highlighttext(resultlist)
        # result.set_totalhits(ret.hits.total)
        #
        # # get the introduction for first 10 results
        # intro = buildIntro(resultlist)
        #
        # # show in the web page
        # return render_template('result.html', keyword = result.get_query(), num = result.get_totalhits(), results=intro,
        #                        id = 0, starring = starring, max = result.get_runtime()[0], min = result.get_runtime()[1], genre = genre)
    except KeyError:
        return "Problem"

# The function is used to preprocess the highlighted text
#  extract all the required informaion and save them in an array
def get_movies(hits):
    resultlist = []
    for r in hits:
        # extract metaid
        r._d_['metaid'] = r.meta.id

        # set hightlight tags
        if hasattr(r.meta, 'highlight'):
            r._d_['text'] = r.meta.highlight['text'][0]
        r._d_['text'] = r._d_['text'].replace("<em>", "<mark>")
        r._d_['text'] = r._d_['text'].replace("</em>", "</mark>")

        # get the first 200 characters of the text field
        r._d_['intro'] = r._d_['text'][0:200] + "..."

        # extract score
        r._d_['score'] = r.meta.score

        # if the movie does not have a title, then set its "Unknown"
        if len(r._d_['title']) <= 1:
            r._d_['title'] = 'Unknown'

        # append the movie at the end of the array
        if r.meta.score > 0:
            resultlist.append(r.to_dict())
    return resultlist


# This function is used for build the introduction of the movie, which is shown on the result page
def buildIntro(movies):
    # Inorder to maintain the scoreranking, use ordered dictionary
    intro = collections.OrderedDict()
    # save the introductions part as an array
    for movie in movies:
        intro[movie['metaid']] = []
        intro[movie['metaid']].append(movie['id'])
        intro[movie['metaid']].append(movie['title'])
        if type(movie['country']) == list:
            intro[movie['metaid']].append(', '.join(movie['country']))
        else:
            intro[movie['metaid']].append(movie['country'])
        intro[movie['metaid']].append(movie['intro'])
        intro[movie['metaid']].append(movie['score'])
    return intro


@app.route("/result/<int:id>")
# show the result page based on the id, each page contains at most 10 results
def getpage(id):
    try:
        print 'getpage'
        # id = int(id)
        # if (id <= result.get_totalhits() / 10) & (id >= 0):
        #     s = result.get_search()
        #     # get the rank range of the result documents
        #     s = s[id * 10: (id+1) * 10]
        #     ret = s.execute()
        #     # get the introduction of the hits
        #     resultlist = get_movies(ret.hits)
        #     result.set_highlighttext(resultlist)
        #     intro = buildIntro(resultlist)
        #     return render_template('result.html', keyword = result.get_query(), num=result.get_totalhits(), results=intro, id = id
        #                            , starring=result.get_starring(), max=result.get_runtime()[0], min=result.get_runtime()[1], genre=result.get_genre())
        # else:
        #     return "no such pages"
    except KeyError:
        return "Problem"



@app.route('/detail/<string:id>')
# show the detailed information of a doc, inclues the title, id, infobox and text
def page_detail(id):
    try:
        # search the document based on its metaid
        s = Search(using=es)
        s = s.index('imdb')
        s = s.filter('term', _id=id)
        ret = s.execute()
        movie=get_movie_detail(ret.hits[0].to_dict(),id)

        return render_template('detail.html',title = movie['title'], infobox = movie['infobox'], text = movie['text'], id = movie['id'])
    except KeyError:
        return "Problem"

# This function is used to get the detailed information of the movie in a dictionary
def get_movie_detail(hit, id):
    print 'detail'
    # movie = {}
    # movie['title'] = hit['title']
    # movie['text'] = result.get_highlighttext(id)
    # if movie['text'] == "":
    #     movie['text'] = hit['text']
    # movie['id'] = hit['id']
    # movie['infobox'] = {}
    #
    # # for some of the data fields are a list of terms, so make them to a string
    # if type(hit['language']) == list:
    #     movie['infobox']['language'] = ', '.join(hit['language'])
    # else:
    #     movie['infobox']['language'] = hit['language']
    # if type(hit['country']) == list:
    #     movie['infobox']['country'] = ', '.join(hit['country'])
    # else:
    #     movie['infobox']['country'] = hit['country']
    # if type(hit['director']) == list:
    #     movie['infobox']['director'] = ', '.join(hit['director'])
    # else:
    #     movie['infobox']['director'] = hit['director']
    # if type(hit['location']) == list:
    #     movie['infobox']['location'] = ', '.join(hit['location'])
    # else:
    #     movie['infobox']['location'] = hit['location']
    # if type(hit['starring']) == list:
    #     casts = ', '.join(hit['starring'])
    # else:
    #     casts = hit['starring']
    #
    # # highlight the query terms in starring
    # for cast in result.get_starringlist():
    #     casts = casts.replace(cast, "<mark>" + cast + "</mark>")
    # movie['infobox']['starring'] = casts
    # if type(hit['categories']) == list:
    #     movie['infobox']['categories'] = ', '.join(hit['categories'])
    # movie['infobox']['runtime'] = hit['runtime']
    # return movie


if __name__ == "__main__":
    # initialize the SearchResult class
    # create a Elasticsearch client, run the web UI

    app.run(debug=True, host='127.0.0.1', port=5000)