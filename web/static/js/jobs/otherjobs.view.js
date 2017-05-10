define(["Backbone", "Jobs", "TEXT!jobs/otherjobs.tpl.html", "TEXT!jobs/job_snippet.tpl.html", "underscore"], 
  function(Backbone, Jobs, OtherJobsTpl, JobTpl, _) {

  var OtherJobsView = Backbone.View.extend({
    el: "#otherjobs_view",

    events: {
      "click #load_more": "query"
    },

    template: _.template(OtherJobsTpl),
    template_job: _.template(JobTpl),

    initialize: function(company) {
      this.render_background();
      this.company = company;
      this.jobs = new Jobs();
      this.jobs.setType("company");
      this.jobs.setData({company: company});
      this.listenTo(this.jobs, "append", this.append_jobs);
      this.jobs_number = 0;
    },

    query: function() {
      this.jobs.getJobs({
        offset: this.jobs.length,
        success: function(collection, resp, options) {
          collection.trigger("append");
        }
      })
    },

    render_background: function() {
      this.$el.html(this.template());
    },

    append_jobs: function() {
      for (var i = this.jobs_number; i < this.jobs.length; i ++)
        this.$("#job_list").append(this.template_job({job: this.jobs.at(i).toJSON()}));
      this.jobs_number = this.jobs.length;
      // this.$("#load_more").show();
    }

  });

  return OtherJobsView;

}); 
