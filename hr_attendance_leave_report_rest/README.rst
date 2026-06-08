.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
    :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
    :alt: License: AGPL-3

===============================
Hr attendance leave report rest
===============================

* In "Attendances And Absences" new field "rest_hours" with the sum of
  attendances that are rest.
* If the rest time is longer than 15 minutes: hours worked = hours worked -
  (rest time - 15 minutes).
* If the rest time is longer than 15 minutes: Non Remunerated Hours =
  Non Remunerated Hours + (rest time - 15 minutes).


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
* Alfredo de la Fuente <alfredodelafuente@avanzosc.es>
