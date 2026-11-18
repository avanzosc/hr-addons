/** @odoo-module **/

import {Component, useState} from "@odoo/owl";
import {useBus, useService} from "@web/core/utils/hooks";
import {Dropdown} from "@web/core/dropdown/dropdown";
import {DropdownItem} from "@web/core/dropdown/dropdown_item";
import {_lt} from "@web/core/l10n/translation";
import {deserializeDateTime} from "@web/core/l10n/dates";
import {registry} from "@web/core/registry";

const {DateTime} = luxon;

const NOTIFICATION_TYPE = "hr_attendance_user_menu_status/update";

const STATUS_TITLES = {
  checked_in: _lt("Checked in: your hours are being counted"),
  checked_out: _lt("Checked out: your hours are not being counted"),
};

export class AttendanceUserMenuStatus extends Component {
  setup() {
    this.orm = useService("orm");
    this.formatFloatTime = registry.category("formatters").get("float_time");
    this.state = useState({
      employeeId: false,
      attendanceState: false,
      canCheckInOut: false,
      checking: false,
      hoursToday: "",
      hoursPreviouslyToday: "",
      lastAttendanceWorkedHours: "",
      lastCheckIn: "",
      isFirstAttendance: true,
    });
    useBus(useService("bus_service"), "notification", this.onAttendanceNotification);
    this.loadStatus();
  }

  get checkedIn() {
    return this.state.attendanceState === "checked_in";
  }

  get statusTitle() {
    const title = STATUS_TITLES[this.state.attendanceState];
    return title ? title.toString() : "";
  }

  async loadStatus() {
    const status = await this.orm.call(
      "res.users",
      "get_attendance_user_menu_status",
      []
    );
    this.updateState(status);
  }

  updateState(status) {
    this.state.employeeId = status.employee_id || false;
    this.state.attendanceState = status.attendance_state || false;
    this.state.canCheckInOut = status.can_check_in_out || false;
    if (!this.state.employeeId) {
      return;
    }
    this.state.hoursToday = this.formatFloatTime(status.hours_today);
    this.state.hoursPreviouslyToday = this.formatFloatTime(
      status.hours_previously_today
    );
    this.state.lastAttendanceWorkedHours = this.formatFloatTime(
      status.last_attendance_worked_hours
    );
    this.state.lastCheckIn = status.last_check_in
      ? deserializeDateTime(status.last_check_in).toLocaleString(DateTime.TIME_SIMPLE)
      : "";
    this.state.isFirstAttendance = status.hours_previously_today === 0;
  }

  onAttendanceNotification({detail: notifications}) {
    for (const {type, payload} of notifications) {
      if (
        type === NOTIFICATION_TYPE &&
        this.state.employeeId &&
        payload.employee_id === this.state.employeeId
      ) {
        this.state.attendanceState = payload.attendance_state;
      }
    }
  }

  async checkInOut() {
    if (this.state.checking) {
      return;
    }
    this.state.checking = true;
    try {
      const status = await this.orm.call(
        "res.users",
        "attendance_user_menu_check_in_out",
        []
      );
      this.updateState(status);
    } finally {
      this.state.checking = false;
    }
  }
}

AttendanceUserMenuStatus.template =
  "hr_attendance_user_menu_status.AttendanceUserMenuStatus";
AttendanceUserMenuStatus.components = {Dropdown, DropdownItem};
AttendanceUserMenuStatus.props = {};

registry
  .category("systray")
  .add(
    "hr_attendance_user_menu_status.AttendanceUserMenuStatus",
    {Component: AttendanceUserMenuStatus},
    {sequence: 101}
  );
