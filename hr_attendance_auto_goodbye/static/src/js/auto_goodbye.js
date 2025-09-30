odoo.define("hr_attendance_auto_goodbye.FarewellPatch", function (require) {
  "use strict";
  var GreetingMessage = require("hr_attendance.greeting_message");
  GreetingMessage.include({
    farewell_message: function () {
      var res = this._super.apply(this, arguments);
      var self = this;
      setTimeout(function () {
        if (self.$(".o_hr_attendance_warning_message:visible").length) {
          setTimeout(function () {
            self.do_action(self.next_action, {clear_breadcrumbs: true});
          }, 5000);
        }
      }, 300);

      return res;
    },
  });
});
