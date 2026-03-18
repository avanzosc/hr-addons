.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

==================
Machine Manager HR
==================

Machine Manager HR is a companion module for **Machine Manager** that
connects your machinery records with Odoo's Human Resources module. It
creates a direct link between machines and the employees who operate them,
giving you full visibility in both directions — from the machine and from
the employee.
 
This module requires both **Machine Manager** and the **Employees** (hr)
module to be installed. Once both are present, Machine Manager HR activates
automatically.
 
Features
========
 
Assign Employees to Machines
------------------------------
 
A new **Machine Users** tab is added to every machine record. From there
you can assign one or more employees who work with or are responsible for
that machine. The list shows each employee by name and can hold as many
users as needed.
 
Assign Machines to Employees
------------------------------
 
A new **Machines** tab is added to every employee record, listing all the
machines that employee is linked to. This lets you see at a glance what
equipment a given person works with, without having to check each machine
individually.
 
Bidirectional Relationship
---------------------------
 
The link between machines and employees works in **both directions**. If
you assign an employee to a machine from the machine record, that machine
will automatically appear in the employee's profile, and vice versa. You
never need to update both sides manually.
 
Machine List — Employees Column
---------------------------------
 
In the machine list view, a new optional column **Machine Users** is
available. When enabled, it shows the assigned employees directly in the
list as tags, giving you a quick overview of all your equipment and who
operates each one without opening individual records.
 
Employee List — Machines Column
---------------------------------
 
In the employee list view, a new optional column **Machines** is available.
When enabled, it displays the machines linked to each employee as tags,
making it easy to spot unassigned equipment or overloaded operators at
a glance.
 
Configuration
=============
 
No additional configuration is required. Once the module is installed:
 
1. Go to **Machine Manager → Configuration → Machines**, open any machine
   and use the **Machine Users** tab to assign employees.
 
2. Alternatively, go to **Employees → Employees**, open any employee
   profile and use the **Machines** tab to assign machines directly from
   the employee side.
 
Both approaches produce the same result thanks to the bidirectional
relationship.

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
* Daniel Campos <danielcampos@avanzosc.es>
* Pedro M. Baeza <pedro.baeza@serviciobaeza.com>
* Ana Juaristi <ajuaristio@gmail.com>
* Oihane Crucelaegui <oihanecrucelaegi@avanzosc.es>
* Esther Martín <esthermartin@avanzosc.es>
