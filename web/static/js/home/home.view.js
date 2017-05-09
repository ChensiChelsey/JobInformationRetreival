define(["Backbone", "Jobs", "TEXT!home/home.tpl.html", "TEXT!jobs/job.tpl.html", "underscore", "Resume"], 
  function(Backbone, Jobs, HomeTpl, JobTpl, _, Resume) {
  
  var HomeView = Backbone.View.extend({
    el: "#home_view",

    events: {
      "click #search": "search",
      "click #load_more": "load_more",
      "click #manager_resume": "navto_resume"
    },

    template: _.template(HomeTpl),
    template_job: _.template(JobTpl),

    initialize: function() {
      this.render_background();
      this.jobs = new Jobs();
      this.listenTo(this.jobs, "append", this.append_jobs);
      this.listenTo(this.jobs, "refresh", this.refresh_jobs);
      this.jobs_number = 0;
    },

    display_recommends: function() {
      this.jobs.setType("recommend");
      this.jobs.reset();
      this.jobs.setData(Resume.getData());
      this.query(true);
    },

    load_more: function() {
      this.query(false);
    },

    navto_resume: function() {
      window.location.href = "/resume"
    },

    query: function(is_new) {
      if (is_new) this.offset = 0;
      var that = this;
      this.jobs.getJobs({
        offset: this.jobs.length,
        success: function(collection, resp, options) {
          if (is_new) collection.trigger("refresh");
          else collection.trigger("append");
        }
      });
    },

    render_background: function() {
      this.$el.html(this.template());
    },

    append_jobs: function() {
      for (var i = this.jobs_number; i < this.jobs.length; i ++)
        this.$("#job_list").append(this.template_job({job: this.jobs.at(i).toJSON()}));
      this.jobs_number = this.jobs.length;
    },

    refresh_jobs: function() {
      this.$("#job_list").html("");
      this.jobs_number = 0;
      this.append_jobs();
    }

  });

  return HomeView;

})