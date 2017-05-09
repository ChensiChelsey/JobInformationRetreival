require.config({
  baseUrl: "/static/js",
  paths: {
    underscore: "underscore-1.8.3",
    Backbone: "backbone",
    jquery: "jquery.min-2.1.4",
    TEXT: "text-2.0.14",
    Jobs: "jobs/jobs.model",
    SearchView: "jobs/search.view",
    Resume: "resume/resume"
  },
  waitSeconds: 10
})

require(["SearchView"], function(SearchView) {
  var search_view = new SearchView();
  search_view.display_recommends();
})

