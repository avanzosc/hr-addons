/** @odoo-module **/

import { NavBar as parentNavBar } from "@web/webclient/navbar/navbar";
import { patch } from "@web/core/utils/patch";

patch(parentNavBar.prototype, "hr_attendance_custom_form.systray_items_patch", {
    get systrayItems() {
        const menuItems = this._super();
        console.log("Original systrayItems:", menuItems);
        if (!Array.isArray(menuItems)) {
            console.warn("systrayItems is not an array or is undefined:", menuItems);
            return [];
        }
        const filteredItems = menuItems.filter(item => item.key === "web.user_menu");
        console.log("Filtered systrayItems (web.user_menu):", filteredItems);
        return filteredItems;
    }
});