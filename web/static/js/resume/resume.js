define([], function(){
  var getData = function() {
    return {
      city: "New York",
      jobtype: "full time",
      eduBG_major: "Computer Science",
      eduBG_degree: "Master"
    }
  }

  return {
    getData: getData
  }
});