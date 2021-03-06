import json
from flask import *
import queryBuilder


app = Flask(__name__)
job_fields = ["jobtitle", "description", "company", "type", "state", "city", "salary", "date"]
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


@app.route("/jobs/<string:job_id>")
def job_page(job_id):
    # TODO: embed job information
    job = queryBuilder.jobdetail(job_id)
    job["summary"] = job["summary"].replace("\n", "</br></br>")
    return render_template("jobdetail.tpl", job=job)


@app.route("/search")
def general_search():
    params = {}
    for field in job_fields + ["offset", "sort_by_date"]:
        if field in request.args:
            params[field] = request.args[field]
    params["sort_by_date"] = True if params["sort_by_date"] == "true" else False
    job_list_with_total = general_search_ela(params)
    return json.dumps(job_list_with_total)


@app.route("/recommend")
def recommend_Search():
    params = {}
    for field in resume_fields + ["offset"]:
        if field in request.args:
            params[field] = request.args[field]
    job_list = recommend_search_ela(params)
    return json.dumps(job_list)


@app.route("/samecompany")
def search_by_company():
    params = {
        "offset": request.args["offset"],
        "company": request.args["company"]
    }
    job_list = queryBuilder.companySearch(params)
    return json.dumps(job_list)


def general_search_ela(params, mock=False):
    if mock:
        return mock_job_list
    job_list = queryBuilder.generalSearch(params)
    return job_list


def recommend_search_ela(params, mock=False):
    if mock:
        return mock_job_list
    job_list = queryBuilder.recommendationSearch(params)
    return job_list


if __name__ == "__main__":
    app.run()
