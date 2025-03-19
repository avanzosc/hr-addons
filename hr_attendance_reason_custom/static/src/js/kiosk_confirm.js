odoo.define("hr_attendance_reason_custom.kiosk_confirm", function (require) {
  "use strict";

  const KioskConfirm = require("hr_attendance.kiosk_confirm");

  KioskConfirm.include({
    update_attendance: function (event_func) {
      this.attendance_reason_id = parseInt(this.$(".o_hr_attendance_reason").val(), 10);

      const superCallback = this._super ? this._super.bind(this) : function () {};

      // Save the current value of required_reason_on_attendance_screen
      const wasRequiredReason = this.employee.required_reason_on_attendance_screen;

      this._rpc({
        model: "hr.attendance",
        method: "search_read",
        domain: [["employee_id", "=", this.employee.id]],
        fields: ["attendance_reason_ids"],
      }).then((attendances) => {
        let hasEntryReasons = false;
        let hasExitReasons = false;

        const reasonIds = attendances.flatMap((att) => att.attendance_reason_ids);

        if (reasonIds.length > 0) {
          this._rpc({
            model: "hr.attendance.reason",
            method: "search_read",
            domain: [
              ["id", "in", reasonIds],
              ["show_on_attendance_screen", "=", true],
            ],
            fields: ["action_type"],
          }).then((reasons) => {
            hasEntryReasons = reasons.some(
              (reason) => reason.action_type === "sign_in"
            );
            hasExitReasons = reasons.some(
              (reason) => reason.action_type === "sign_out"
            );

            // Fetch the employee details, including attendance_state
            this._rpc({
              model: "hr.employee",
              method: "search_read",
              domain: [["id", "=", this.employee.id]],
              fields: ["attendance_state"],
            }).then((employeeData) => {
              const employee = employeeData[0];
              
              if (
                // Attendance_reason_id being 0 means no reason has been selected
                this.attendance_reason_id === 0 &&
                ((employee.attendance_state === "checked_out" && hasEntryReasons) ||
                  (employee.attendance_state === "checked_in" && hasExitReasons))
              ) {
                superCallback(event_func);
              } else {
                this.employee.required_reason_on_attendance_screen = false;
                superCallback(event_func);
                // Restore the original value of required_reason_on_attendance_screen
                this.employee.required_reason_on_attendance_screen = wasRequiredReason;
              }
            });
          });
        } else {
          this.employee.required_reason_on_attendance_screen = false;
          superCallback(event_func);

          // Restore the original value of required_reason_on_attendance_screen
          this.employee.required_reason_on_attendance_screen = wasRequiredReason;
        }
      });
    },
  });
});
