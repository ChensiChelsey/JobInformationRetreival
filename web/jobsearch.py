import json
from flask import *
import queryBuilder


app = Flask(__name__)
job_fields = ["job_title", "description", "company", "type", "state", "city", "salary", "date"]
resume_fields = ["city", "state", "jobtype", "major", "pbg", "degree", "salary"]
mock_job_list = [{
    "score": 1.0,
    "title": "title 1",
    "summary": "job summary",
    "url": "url",
    "company": "indeed",
    "location": "Waltham",
    "postingdate": "2017-3-2"
}] * 10


@app.route("/")
@app.route("/home")
def home_page():
    return render_template("home.html")


@app.route("/resume")
def resume_page():
    return render_template("resume.html")


@app.route("/searchpage")
def search_page():
    return render_template("search.html")


@app.route("/job<int:job_id>")
def job_page():
    # TODO: embed job information
    return render_template("job.html")


@app.route("/search")
def general_search():
    params = {}
    for field in job_fields:
        if field in request.form:
            params[field] = request.form[field]
    job_list = general_search_ela(params)
    return json.dumps(job_list)


@app.route("/recommend")
def recommend_Search():
    params = {}
    for field in resume_fields:
        if field in request.form:
            params[field] = request.form[field]
    job_list = recommend_search_ela(params)
    return json.dumps(job_list)


def general_search_ela(params, mock=False):
    if mock:
        return [{
            "score": 1.0,
            "title": "title 1",
            "summary": "job summary",
            "url": "url",
            "company": "indeed",
            "location": "Waltham",
            "postingdate": "2017-3-2"
        }] * 10
    else:
        job_list = queryBuilder.generalSearch(params)
        return job_list


def recommend_search_ela(params, modk=False):
    if mock:
        return [{
            "score": 1.0,
            "title": "title 1",
            "summary": "job summary",
            "url": "url",
            "company": "indeed",
            "location": "Waltham",
            "postingdate": "2017-3-2"
        }] * 10
    else:
        job_list = queryBuilder.recommendationSearch(params)
        return job_list


if __name__ == "__main__":
    app.run()
