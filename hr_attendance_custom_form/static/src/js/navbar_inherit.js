odoo.define(
  "hr_attendance_custom_form.systray_items_patch",
  ["web.NavBar", "web.utils"],
  function (require) {
    "use strict";

    const NavBar = require("web.NavBar");
    const {patch} = require("web.utils");

    patch(NavBar.prototype, "hr_attendance_custom_form.systray_items_patch", {
      get systrayItems() {
        const menuItems = this._super(...arguments);
        console.log("Original systrayItems:", menuItems);
        if (!Array.isArray(menuItems)) {
          console.warn("systrayItems is not an array or is undefined:", menuItems);
          return [];
        }
        const filteredItems = menuItems.filter((item) => item.key === "web.user_menu");
        console.log("Filtered systrayItems (web.user_menu):", filteredItems);
        return filteredItems;
      },
    });
  }
);
