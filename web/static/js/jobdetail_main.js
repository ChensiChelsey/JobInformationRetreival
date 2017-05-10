require.config({
  baseUrl: "/static/js",
  paths: {
    underscore: "underscore-1.8.3",
    Backbone: "backbone",
    jquery: "jquery.min-2.1.4",
    TEXT: "text-2.0.14",
    Jobs: "jobs/jobs.model",
    OtherJobsView: "jobs/otherjobs.view"
  },
  waitSeconds: 10
})

require(["OtherJobsView"], function(OtherJobsView) {
  var company = $("#company").text();
  var otherjobs_view = new OtherJobsView(company);
  otherjobs_view.query();
});
