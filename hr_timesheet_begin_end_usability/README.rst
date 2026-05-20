.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
    :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
    :alt: License: AGPL-3

================================
Hr Timesheet Begin End Usability
================================

Extends ``hr_timesheet_begin_end`` with the following usability improvements:

* If the analytic line has no user, overlapping lines are allowed.
* If start time is greater than stop time, the stop time is treated as being
  on the next day (overnight entries), and ``date_end`` is set accordingly.
* The ``employee_id`` field is not required on the timesheet list view.

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

* Berezi Amubieta <bereziamubieta@avanzosc.es>
* Ana Juaristi <anajuaristi@avanzosc.es>
