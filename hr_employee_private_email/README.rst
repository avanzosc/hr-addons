.. image:: https://img.shields.io/badge/license-AGPL--3-blue.svg
   :target: https://opensource.org/licenses/AGPL-3.0
   :alt: License: AGPL-3

=========================
HR Employee Private Email
=========================

In Odoo 16 the private email of an employee is the email of its private
address, and its work email is the email of its work contact. When the private
address is the work contact, both are the same field and overwrite each other.

This module keeps the private email on the employee, so it no longer depends on
the private address. It can be edited from the employee form and from the user 
preferences, without changing the work email or any contact.

On installation, the email of the private address of each employee is copied
to its private email. The private address itself is not changed.

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
