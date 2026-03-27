odoo.define(
    "hr_attendance_custom_form.kiosk_confirm_patch",
    ["hr_attendance.kiosk_confirm", "web.core", "web.session"],
    function (require) {
        "use strict";

        const KioskConfirm = require("hr_attendance.kiosk_confirm");
        const core = require("web.core");
        const session = require("web.session");
        const _t = core._t;

        KioskConfirm.include({
            events: Object.assign({}, KioskConfirm.prototype.events, {
                "click .o_hr_attendance_pin_pad_button_Go_to_employee_profile": function () {
                    this._handle_action_after_pin("profile");
                },

                "click .o_hr_attendance_pin_pad_button_Go_to_calendar": function () {
                    this._handle_action_after_pin("calendar");
                },
            }),

            _handle_action_after_pin: function (target) {
                this.attendance_reason_id = parseInt(this.$(".o_hr_attendance_reason").val(), 0);
                if (
                    this.employee.required_reason_on_attendance_screen &&
                    this.attendance_reason_id === 0
                ) {
                    this.displayNotification({
                        title: _t("Please, select a reason"),
                        type: "danger",
                    });
                    return;
                }

                var self = this;
                this._sendPinWithResult().then(function (result) {
                    if (result && result.action) {
                        if (target === "profile") {
                            self.do_action({
                                type: "ir.actions.act_window",
                                res_model: "hr.employee.public",
                                res_id: self.employee_id,
                                views: [[false, "form"]],
                                target: "current",
                                context: session.user_context,
                            }).catch(function (error) {
                                self.displayNotification({
                                    title: _t("Error opening profile"),
                                    message: error.message || _t("An error occurred"),
                                    type: "danger",
                                });
                            });
                        } else if (target === "calendar") {
                            self.do_action({
                                type: "ir.actions.act_window",
                                res_model: "hr.leave",
                                views: [[false, "calendar"]],
                                target: "current",
                                context: Object.assign({}, session.user_context, {
                                    search_default_employee_id: self.employee_id,
                                    calendar_fields: {
                                        date_start: "check_in",
                                        date_stop: "check_out",
                                    },
                                }),
                                view_mode: "calendar",
                                view_type: "calendar",
                            }).catch(function (error) {
                                self.displayNotification({
                                    title: _t("Error opening calendar"),
                                    message: error.message || _t("An error occurred"),
                                    type: "danger",
                                });
                            });
                        }
                    } else {
                        self.displayNotification({
                            title: _t("Invalid response"),
                            message: _t("Wrong PIN"),
                            type: "danger",
                        });
                    }
                }).catch(function (error) {
                    self.displayNotification({
                        title: _t("Error processing PIN"),
                        message: error.message || _t("An error occurred"),
                        type: "danger",
                    });
                });
            },

            _sendPinWithResult: function () {
                var self = this;
                this.$(".o_hr_attendance_pin_pad_button_ok").attr("disabled", "disabled");
                const result = this._rpc({
                    model: "hr.employee",
                    method: "attendance_manual_custom_form",
                    args: [
                        [this.employee_id],
                        this.next_action,
                        this.$(".o_hr_attendance_PINbox").val(),
                    ],
                    context: session.user_context,
                }).then(function (result) {
                    self.pin_is_send = true;
                    return result;
                });
                return result;
            },
            init: function (parent, action) {
                this._super.apply(this, arguments);
            },
        });
    }
);