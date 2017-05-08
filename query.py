from flask import *
from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search, Q
import collections
import os


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

@app.route('/resume')
def check_resume():
    filename = r'resume.json'
    if os.path.exists(filename):
        with open(filename, 'r') as f:
            data = json.load(f)
        return render_template('resume_result.html', data)
    else:
        return render_template('update_resume.html')


@app.route('/save_resume')
# save the user's resume into a json-file
def save_resume():
    try:
        # get the query from user
        resume = {}
        resume['FirstName'] = request.form['First name']
        resume['LastName'] = request.form['First name']
        resume['Address']['State'] = request.form['State']
        resume['Address']['City'] = request.form['City']
        resume['Address']['ZipCode'] = request.form['ZipCode']
        resume['ProfessionalBackground'] = request.form['Professional Background']
        resume['EducationBackground']['Degree'] = request.form['Degree']
        resume['EducationBackground']['Major'] = request.form['Major']
        resume['JobType'] = request.form['JobType']
        resume['ExpectedSalary'] = request.form['Expected Salary']
        f = open("resume.json", "w+")
        jsontext = json.dumps(resume, ensure_ascii=False, indent=4)
        f.write(jsontext)
        return render_template('resume_result.html', resume)
    except:
        print "Problem"

@app.route('/detail/<string:id>')
# show the detailed information of a doc, inclues the title, id, infobox and text
def page_detail(id):
    try:
        # search the document based on its metaid
        s = Search(using=es)
        s = s.index('job_index')
        s = s.filter('term', _id=id)
        ret = s.execute()
        job=get_job_detail(ret.hits[0].to_dict(),id)

        return render_template('detail.html', job)
    except KeyError:
        return "Problem"

# This function is used to get the detailed information of the movie in a dictionary
def get_job_detail(hit, id):
    print 'detail'
    job = {}
    job['title'] = hit['title']
    job['summary'] = hit['summary']
    job['url'] = 'www.indeed.com' + hit['url']
    job['company'] = hit['company']
    job['location'] = hit['location']
    if hit['salary'] == '':
        job['salary'] = 'Unknown'
    else:
        job['salary'] = hit['salary']
    job['jobtype'] = hit['jobtype']
    return job


if __name__ == "__main__":
    # initialize the SearchResult class
    # create a Elasticsearch client, run the web UI

    app.run(debug=True, host='127.0.0.1', port=5000)