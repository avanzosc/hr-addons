// Copyright 2025 Ane Gurruchaga - AvanzOSC
// License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
/* global window */

import {KioskGreetings} from "@hr_attendance/components/greetings/greetings";
import {patch} from "@web/core/utils/patch";

const AUTO_GOODBYE_DELAY = 5000;

patch(KioskGreetings.prototype, {
    setup() {
        super.setup();
        window.clearTimeout(this.kiosk_delay);
        this.kiosk_delay = window.setTimeout(() => {
            this.props.kioskReturn(true);
        }, AUTO_GOODBYE_DELAY);
    },
});
