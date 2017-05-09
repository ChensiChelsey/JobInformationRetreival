require.config({
  baseUrl: "/static/js",
  paths: {
    underscore: "underscore-1.8.3",
    Backbone: "backbone",
    jquery: "jquery.min-2.1.4",
    TEXT: "text-2.0.14",
    ResumeView: "resume/resume.view",
    Resume: "resume/resume",
  },
  waitSeconds: 10
})

require(["ResumeView"], function(ResumeView) {
  var resume_view = new ResumeView();
})