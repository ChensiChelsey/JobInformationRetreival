define(["Backbone", "Jobs", "TEXT!jobs/search.tpl.html", "TEXT!jobs/job.tpl.html", "underscore", "Resume"], 
  function(Backbone, Jobs, SearhTpl, JobTpl, _, Resume) {
  
  var SearchView = Backbone.View.extend({
    el: "#search_view",

    events: {
      "click #search_relevance": "search_relevance",
      "click #search_date": "search_date",
      "click #load_more": "load_more"
    },

    template: _.template(SearhTpl),
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

    search_date: function() {
      this.$("#search_relevance").removeClass("btn-success");
      this.$("#search_date").addClass("btn-success");
      this.search(true);
    },

    search_relevance: function() {
      this.$("#search_date").removeClass("btn-success");
      this.$("#search_relevance").addClass("btn-success");
      this.search(false);
    },

    search: function(sort_by_date) {
      this.jobs.setType("search");
      this.jobs.reset();
      this.jobs.setData(_.extend({sort_by_date: sort_by_date}, this.getQueryParams()));
      this.query(true);
    },

    load_more: function() {
      this.query(false);
    },

    query: function(is_new) {
      if (is_new) this.offset = 0;
      var that = this;
      this.jobs.getJobs({
        offset: this.jobs.length,
        success: function(collection, resp, options) {
          if (is_new) collection.trigger("refresh");
          else collection.trigger("append");
          if (that.jobs.type == "search")
            that.$("#result_title").text(localStorage.getItem("total") + " results");
        }
      });
    },

    render_background: function() {
      this.$el.html(this.template());
    },

    getQueryParams: function() {
      var params = {};
      if (this.$("#jobtitle").val() != "") params["jobtitle"] = this.$("#jobtitle").val();
      if (this.$("#job_description").val() != "") params["description"] = this.$("#job_description").val();
      if (this.$("#company").val() != "") params["company"] = this.$("#company").val();
      if (this.$("#job_type").val() != "") params["type"] = this.$("#job_type").val();
      if (this.$("#state").val() != "") params["state"] = this.$("#state").val();
      if (this.$("#city").val() != "") params["city"] = this.$("#city").val();
      if (this.$("#salary").val() != "") params["salary"] = this.$("#salary").val();
      if (this.$("#date").val() != "") params["date"] = this.$("#date").val();
      return params;
    },

    append_jobs: function() {
      for (var i = this.jobs_number; i < this.jobs.length; i ++)
        this.$("#job_list").append(this.template_job({job: this.jobs.at(i).toJSON()}));
      this.jobs_number = this.jobs.length;
      this.$("#load_more").show();
    },

    refresh_jobs: function() {
      this.$("#job_list").html("");
      this.jobs_number = 0;
      this.append_jobs();
    }

  });

  return SearchView;

})