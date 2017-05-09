require.config({
  baseUrl: "/static/js",
  paths: {
    underscore: "underscore-1.8.3",
    Backbone: "backbone",
    jquery: "jquery.min-2.1.4",
    TEXT: "text-2.0.14",
    Jobs: "jobs/jobs.model",
    HomeView: "home/home.view",
    Resume: "resume/resume"
  },
  waitSeconds: 10
})

require(["HomeView", "Resume"], function(HomeView, Resume) {
  var home_view = new HomeView();
  if (Resume.hasResume())
    home_view.display_recommends();
})

