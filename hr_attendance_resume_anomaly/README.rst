.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

============================
Hr attendance resume anomaly
============================

* This module performs anomaly control in the attendances summary. These are
  the anomalies that are controlled:
  
  - "There are attendances in day that do not apply". No turn or has
    vacationed. 
  - "Have absence". The worker has worked, and has absent.
  - "Festive worked". The worker has worked on festive day.
  - "There is an approved absence and there is no attendance". The worker has
    not imputed, and is absent.
  - "Entry without exit". The worker forgot to impute in at the exit.
  - "Attendances very often". Imputations very often, less than 1 minute.
  - "There is no attendance in day that corresponds". The worker should to have
    imputed on this day, and has not done so.
  - "Real working day greater or less than the percentage over the planned day"
    Actual day greater or lesser than the percentage of expected day
    (provided there are no approved absences). The percentages are defined in
    the calendar, one for excess, and another defect.

Bug Tracker
===========

Bugs are tracked on `GitHub Issues
<https://github.com/avanzosc/hr-addons/issues>`_. In case of trouble, please
check there if your issue has already been reported. If you spotted it first,
help us smash it by providing detailed and welcomed feedback.

Credits
=======

Contributors
------------
* Ana Juaristi <anajuaristi@avanzosc.es>
* Alfredo de la Fuente <alfredodelafuente@avanzosc.es>

Do not contact contributors directly about support or help with technical issues.
