/** @odoo-module **/

import {onMounted, useState} from "@odoo/owl";
import {useBus, useService} from "@web/core/utils/hooks";
import {UserMenu} from "@web/webclient/user_menu/user_menu";
import {_lt} from "@web/core/l10n/translation";
import {patch} from "@web/core/utils/patch";

const NOTIFICATION_TYPE = "hr_attendance_user_menu_status/update";

const STATUS_TITLES = {
  checked_in: _lt("Checked in: your hours are being counted"),
  checked_out: _lt("Checked out: your hours are not being counted"),
};

patch(UserMenu.prototype, "hr_attendance_user_menu_status.UserMenu", {
  setup() {
    this._super(...arguments);
    this.orm = useService("orm");
    this.attendanceStatus = useState({employeeId: false, state: false});
    useBus(
      useService("bus_service"),
      "notification",
      this.onAttendanceStatusNotification
    );
    onMounted(() => this.loadAttendanceStatus());
  },

  async loadAttendanceStatus() {
    const status = await this.orm.call(
      "res.users",
      "get_attendance_user_menu_status",
      []
    );
    this.attendanceStatus.employeeId = status.employee_id || false;
    this.attendanceStatus.state = status.attendance_state || false;
  },

  onAttendanceStatusNotification({detail: notifications}) {
    for (const {type, payload} of notifications) {
      if (
        type === NOTIFICATION_TYPE &&
        this.attendanceStatus.employeeId &&
        payload.employee_id === this.attendanceStatus.employeeId
      ) {
        this.attendanceStatus.state = payload.attendance_state;
      }
    }
  },

  getAttendanceStatusTitle() {
    return STATUS_TITLES[this.attendanceStatus.state] || "";
  },
});
