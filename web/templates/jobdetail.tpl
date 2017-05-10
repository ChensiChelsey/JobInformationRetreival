<!doctype html>
<html>
<head>
  <meta charset="utf-8">
  <title>Job Search</title>
  <link href="../static/css/bootstrap.min.css" rel="stylesheet">
  <link href="../static/css/w3.css" rel="stylesheet" >
  <link href="https://fonts.googleapis.com/css?family=Inconsolata" rel="stylesheet" >
  <link href="../static/css/style.css" rel="stylesheet">
</head>
<body>
  <div class="container-fluid">
    <div class="row w3-top">
      <div class="w3-row w3-padding w3-black">
        <div class="w3-col s4">
          <a href="/home" class="w3-button w3-block w3-black nav-option" >HOME</a>
        </div>
        <div class="w3-col s4">
          <a href="/resume" class="w3-button w3-block w3-black nav-option">RESUME</a>
        </div>
        <div class="w3-col s4">
          <a href="/searchpage" class="w3-button w3-block w3-black nav-option">SEARCH</a>
        </div>
      </div>
    </div>

    <div class="row main-content" >
      <div class="col-md-12">
        <!-- <h1 class="w3-center w3-padding-48">
          <span class="w3-tag w3-wide">HomePage</span>
        </h1> -->
        <div class="row">
          <div class="col-md-1">
          </div>
          <div class="col-md-10">

            <div class="row">
              <div class="col-md-9">
                <!-- right -->
                <!-- Job Detail -->
                <h3 style="margin-bottom:20px">
                  <span class="w3-tag w3-wide">
                    {% if job["title"] != "" %} {{job["title"]}} {% else %} Unknown {% endif %}
                  </span>
                </h3>
                {% if job['company'] != '' %} 
                  <label class="w3-text-grey job-tag">Company</label>
                  <p class="w3-text-white" id="company">{{job['company']}}</p> 
                {% endif %}
                {% if job['jobtype'] != '' %} 
                  <label class="w3-text-grey job-tag">JobType</label>
                  <p class="w3-text-white">{{job['jobtype']}}</p> 
                {% endif %}
                {% if job['location'] != '' %} 
                  <label class="w3-text-grey job-tag">Location</label>
                  <p class="w3-text-white">{{job['location']}}</p> 
                {% endif %}
                {% if job['salary'] != 0.0 %} 
                  <label class="w3-text-grey job-tag">Salary</label> 
                  <p class="w3-text-white">{{job['salary']}}</p> 
                {% endif %}
                <label class="w3-text-grey job-tag">Summary</label>
                <p class="w3-text-white">
                  {{job['summary']}}
                </p>
                {% if job['url'] != '' %} 
                  <a href="{{'http://' + job['url']}}" target="_blank"><button class="btn btn-info">See Job On Indeed</button></a>
                {% endif %}
              </div>

              <div class="col-md-3">
                <div class="c-sidebar" id="otherjobs_view">

                  
                </div>
              </div>
            </div>

          </div>
          <div class="col-md-1">
          </div>
        </div>
      </div>
    </div>
  </div>
  <footer class="w3-center w3-light-grey w3-padding-16 w3-large">
    <p>Powered by COSI132 JOB SEARCH GROUP</p>
  </footer>
  <script src="../static/js/jquery.min-2.1.4.js"></script>
  <script src="../static/js/require-1.0.8.js" data-main="../static/js/jobdetail_main"></script>
</body>
</html>