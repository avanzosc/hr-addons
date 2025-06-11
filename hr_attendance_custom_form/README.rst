.. image:: https://img.shields.io/badge/license-LGPL--3-blue.svg
   :target: https://www.gnu.org/licenses/lgpl-3.0.html
   :alt: License: LGPL-3

===============================================================================
HR Attendance Custom Form
===============================================================================

Overview
========

The **HR Attendance Custom Form** module customizes the default HR attendance kiosk interface in Odoo. It hides the default Odoo navigation elements (like the control panel and navbar) and extends the attendance kiosk screen with new buttons that provide quick access to the employee form and attendance calendar.

Features
========

- Hides the Odoo **NavBar**, **ControlPanel**, and **FormControlPanel** when in kiosk mode.
- Replaces the numeric keypad layout in the kiosk attendance view.
- Adds the following custom buttons to the kiosk interface:
  
  - **"Go to employee profile"**: Opens the current employee's form view.
  - **"Go to calendar"**: Opens a calendar view of the employee's attendances.

Usage
=====

1. Navigate to the **Attendances > Kiosk Mode**.
2. Enter your PIN to confirm attendance.
3. On the confirmation screen, the keypad will be customized and will show:
   - Number pad and OK button
   
   - New buttons:
   
     - **Go to employee profile**: Takes you to the HR employee record.
   
     - **Go to calendar**: Opens a calendar showing the employee’s attendance records.

These buttons are especially useful for HR or team leads to quickly verify employee records or schedules from the kiosk.

Technical Details
=================

- This module uses `t-extend` to modify the `HrAttendanceKioskConfirm` template.
- OWL templates and JavaScript are used to add behavior to the new buttons.
- Inherited templates (`web.ControlPanel`, `web.FormControlPanel`, `web.NavBar`) are overridden to hide standard UI elements during kiosk mode.

Configuration
=============

No additional configuration is needed. Simply install the module and open the **Kiosk Mode** view.

Bug Tracker
===========

If you encounter any issues, please report them on the issue tracker:
`GitHub Issues <https://github.com/avanzosc/odoo-addons/issues>`_.

Credits
=======

Contributors
------------

* Ana Juaristi <anajuaristi@avanzosc.es>
* Unai Beristain <unaiberistain@avanzosc.es>

License
=======

This project is licensed under the LGPL-3 License.  
See: https://www.gnu.org/licenses/lgpl-3.0.html
