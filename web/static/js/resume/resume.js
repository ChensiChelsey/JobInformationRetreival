define([], function(){
  var getData = function() {
    if (!hasResume()) 
      return {fn: "", ln: "", state: "", city: "", pbg: "", major: "", degree: "", jobtype: "", salary: ""}
    var resume = localStorage.getItem("resume");
    return JSON.parse(resume);
  }

  var hasResume = function() {
    return !(localStorage.getItem("resume") == null);
  }

  var getBriefHTML = function() {
    return " <p class=\"w3-white\">Breif Resume HTML Content. </p>"
  }

  var update = function(newResume) {
    localStorage.setItem("resume", JSON.stringify(newResume));
  }

  return {
    getData: getData,
    hasResume: hasResume,
    getBriefHTML: getBriefHTML,
    update: update
  }
});