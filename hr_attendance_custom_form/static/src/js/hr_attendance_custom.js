/** @odoo-module **/

import KioskConfirm from "hr_attendance.kiosk_confirm";
import {_t} from "web.core";

KioskConfirm.include({
  events: Object.assign({}, KioskConfirm.prototype.events, {
    "click .o_hr_attendance_pin_pad_button_Go_to_employee_profile": function () {
      console.log("Go to employee profile clicked for employee ID:", this.employee_id);
      this.do_action({
        type: "ir.actions.act_window",
        res_model: "hr.employee",
        res_id: this.employee_id,
        views: [[false, "form"]],
        target: "current",
        context: this.getSession().user_context,
      });
    },
    "click .o_hr_attendance_pin_pad_button_Go_to_calendar": function () {
      console.log("Go to calendar clicked for employee ID:", this.employee_id);
      this.do_action({
        type: "ir.actions.act_window",
        res_model: "hr.attendance",
        views: [[false, "list"]],
        target: "current",
        context: Object.assign({}, this.getSession().user_context, {
          search_default_employee_id: this.employee_id,
          calendar_fields: {
            date_start: "check_in",
            date_stop: "check_out",
          },
        }),
        view_mode: "calendar",
        view_type: "calendar",
      });
    },
  }),
});
