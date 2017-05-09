define(["Backbone", "TEXT!resume/resume.tpl.html", "TEXT!resume/update.tpl.html", "TEXT!resume/preview.tpl.html", "underscore", "Resume"], 
  function(Backbone, ResumeTpl, UpdateTpl, PreviewTpl, _, Resume) {
  
  var ResumeView = Backbone.View.extend({
    el: "#resume_view",

    events: {
      "click #update_resume": "show_update_page",
      "click #preview_resume": "show_preview_page",
      "click #submit": "update_resume"
    },

    ResumeTemplate: _.template(ResumeTpl),
    UpdateTemplate: _.template(UpdateTpl),
    PreviewTemplate: _.template(PreviewTpl),

    initialize: function() {
      this.render_background();
      if (Resume.hasResume())
        this.show_preview_page();
      else
        this.show_update_page();
    },

    show_update_page: function() {
      this.$("#resume_window").html(this.UpdateTemplate({resume: Resume.getData()}));
    },

    show_preview_page: function() {
      this.$("#resume_window").html(this.PreviewTemplate({resume: Resume.getData()}));
    },

    update_resume: function() {
      Resume.update(this.getInputResume());
      window.location.href = "/resume";
    },

    getInputResume: function() {
      return {
        fn: this.$("#fn").val(),
        ln: this.$("#ln").val(),
        state: this.$("#state").val(),
        city: this.$("#city").val(),
        pbg: this.$("#pbg").val(),
        major: this.$("#major").val(),
        degree: this.$("#degree").val(),
        jobtype: this.$("#jobtype").val(),
        salary: parseFloat(this.$("#salary").val())
      }
    },

    render_background: function() {
      this.$el.html(this.ResumeTemplate());
    }

  });

  return ResumeView;

})