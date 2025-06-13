odoo.define(
  "hr_attendance_custom_form.kiosk_confirm_patch",
  ["hr_attendance.kiosk_confirm", "web.core"],
  function (require) {
    "use strict";

    const KioskConfirm = require("hr_attendance.kiosk_confirm");

    KioskConfirm.include({
      events: Object.assign({}, KioskConfirm.prototype.events, {
        "click .o_hr_attendance_pin_pad_button_Go_to_employee_profile": function () {
          this.update_attendance((result) => {
            if (result?.warning) {
              this.displayNotification({ title: result.warning, type: "danger" });
            } else {
              this.do_action({
                type: "ir.actions.act_window",
                res_model: "hr.employee",
                res_id: this.employee_id,
                views: [[false, "form"]],
                target: "current",
                context: Object.assign({}, this.getSession().user_context, {
                  employee_id: this.employee_id,
                }),
                domain: [["id", "=", this.employee_id]],
              });
            }
          });
        },

        "click .o_hr_attendance_pin_pad_button_Go_to_calendar": function () {
          this.update_attendance((result) => {
            if (result?.warning) {
              this.displayNotification({ title: result.warning, type: "danger" });
            } else {
              this.do_action({
                type: "ir.actions.act_window",
                res_model: "hr.attendance",
                views: [[false, "calendar"]],
                target: "current",
                context: Object.assign({}, this.getSession().user_context, {
                  employee_id: this.employee_id,
                  search_default_employee_id: this.employee_id,
                  calendar_fields: {
                    date_start: "check_in",
                    date_stop: "check_out",
                  },
                }),
                domain: [["employee_id", "=", this.employee_id]],
                view_mode: "calendar",
                view_type: "calendar",
              });
            }
          });
        },
      }),
    });
  }
);
