define(["Backbone", "underscore"], function(Backbone, _) {
  var Job = Backbone.Model.extend({
    parse: function(job, options) {
      return job;
    }
  });

  var Jobs = Backbone.Collection.extend({
    model: Job,

    setType: function(type) {
      this.type = type;
      if (type == "recommend") this.url = "/recommend";
      else if (type == "search") this.url = "/search";
      else this.url = "/samecompany";
    },

    setData: function(data) {
      this.queryParams = data;
    },

    getJobs: function(options) {
      data = _.extend({offset: options.offset}, this.queryParams);
      options = {
        data: data,
        success: options.success
      }
      this.fetch(options);
    },

    beforeParse: function(resp) {
      return resp;
    },

    parse: function(joblist_with_total, options) {
      if (joblist_with_total instanceof Array)
        return this.toJSON().concat(joblist_with_total);
      localStorage.setItem("total", joblist_with_total["hitsnum"])
      return this.toJSON().concat(joblist_with_total["joblist"])
    }
  });

  return Jobs;
})