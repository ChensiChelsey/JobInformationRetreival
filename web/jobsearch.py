import json
from flask import *
# import collections
# import os


app = Flask(__name__)
job_fields = ["job_title", "description", "company", "type", "state", "city", "salary", "date"]

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
def search():
    params = {}
    for field in job_fields:
        if field in request.form:
            params[field] = request.form[field]
    job_list = search_jobs_by_params(params, mock=True)
    return json.dumps(job_list)


def search_jobs_by_params(params, mock=False):
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


if __name__ == "__main__":
    app.run()
