odoo.define("hr_attendance_reason_custom.my_attendances", function (require) {
  "use strict";
  const MyAttendances = require("hr_attendance.my_attendances");

  MyAttendances.include({
    update_attendance: function () {
      this.attendance_reason_id = parseInt(this.$(".o_hr_attendance_reason").val(), 10);

      const superCallback = this._super.bind(this);

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

            if (
              this.attendance_reason_id === 0 &&
              ((this.employee.attendance_state === "checked_out" && hasEntryReasons) ||
                (this.employee.attendance_state === "checked_in" && hasExitReasons))
            ) {
              superCallback();
            } else {
              this.employee.required_reason_on_attendance_screen = false;
              superCallback();
            }
          });
        } else {
          this.employee.required_reason_on_attendance_screen = false;
          superCallback();
        }
      });
    },
  });
});
