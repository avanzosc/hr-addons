odoo.define("your_module.fetch_unusual_days", function (require) {
  "use strict";

  const CalendarModel = require("@web/views/calendar/calendar_model");
  const {serializeDateTime} = require("@web/core/l10n/dates");

  /**
   * Modify the fetchUnusualDays method of the CalendarModel to add context properties
   */
  const originalFetchUnusualDays = CalendarModel.prototype.fetchUnusualDays;

  CalendarModel.prototype.fetchUnusualDays = function (data) {
    const meta = this.meta || {};
    const envContext = this.env && this.env.context ? this.env.context : {};

    const context = {
      ...envContext,
      active_id: (meta.context && meta.context.active_id) || envContext.active_id,
      model: meta.resModel || envContext.model,
    };

    // Call the original method (super) even if we don't use its result
    originalFetchUnusualDays.call(this, data);

    return this.orm.call(
      meta.resModel || "calendar.event",
      "get_unusual_days",
      [serializeDateTime(data.range.start), serializeDateTime(data.range.end)],
      {context}
    );
  };
});
