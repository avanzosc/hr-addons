.. image:: https://img.shields.io/badge/license-AGPL--3-blue.svg
   :target: https://opensource.org/licenses/AGPL-3.0
   :alt: License: AGPL-3

==============================
HR Attendance User Menu Status
==============================

This module shows the attendance status of the logged user in the systray of
the main navigation bar, to the left of the other icons:

* A green dot when the employee of the user is checked in, so its hours are
  being counted.
* A red dot when the employee of the user is checked out, so its hours are not
  being counted.

Clicking the dot opens a panel with the hours worked today and a *Check in* or
*Check out* button, which creates or closes the attendance of the employee,
just like the buttons of *My Attendances*. The button is only shown to users
of the *Attendances / User* group.

The employee is the one of the user in the current company. Users without an
employee do not see any dot.

The dot is refreshed instantly whenever an attendance of the employee is
created, modified or deleted, wherever it is done (the systray, *My
Attendances*, kiosk mode, the attendance list...), in every open tab of the
user.

Bug Tracker
===========

Bugs are tracked on `GitHub Issues
<https://github.com/avanzosc/hr-addons/issues>`_. In case of trouble,
please check there if your issue has already been reported. If you spotted
it first, help us smash it by providing detailed and welcomed feedback.

Do not contact contributors directly about support or help with technical issues.

Credits
=======

Contributors
------------

* Ana Juaristi <anajuaristi@avanzosc.es>
* Lucía Echeverría <luciaecheverria@avanzosc.es>

For specific questions regarding this module, please contact the contributors. For support, please use the official issue tracker.

License
=======

This project is licensed under the AGPL-3 License. For more details, refer to the LICENSE file or visit <https://opensource.org/licenses/AGPL-3.0>.
