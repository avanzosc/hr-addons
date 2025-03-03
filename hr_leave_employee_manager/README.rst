.. image:: https://img.shields.io/badge/license-LGPL--3-blue.svg
   :target: https://opensource.org/licenses/LGPL-3.0
   :alt: License: LGPL-3

=========================
HR Leave Employee Manager
=========================

Overview
========

The **HR Leave Employee Manager** module enhances the leave request process in Odoo by modifying the domain applied to the `employee_id` field. With this module, the field only shows:

- The current employee (if the user is linked to an employee record).
- Employees managed by the current employee (employees for whom the current employee is the `leave_manager_id`).

This ensures that managers can only create leave requests for their own team, improving usability and enforcing better data control.

Features
========

- The `employee_id` field on leave requests (model `hr.leave`) is restricted to:

    - The current user’s employee record.

    - Employees for whom the current user is the `leave_manager_id`.

- Form view inheritance to ensure the `employee_id` field is always visible and applies the correct domain dynamically.

Usage
=====

1. **Install the Module**:

    - Install the **HR Leave Employee Manager** module from the Apps menu.

2. **Go to Leave Requests**:

    - Navigate to *Time Off > Managers > Time Off*.

    - Create a new leave request.

    - In the *Employee* field, you will only see:

        - Yourself (if you are an employee).

        - Employees who have you set as their *Leave Manager*.

3. **Simplified Selection**:
    - Managers will only see their team members, simplifying the creation of requests on behalf of employees.

Configuration
=============

No additional configuration is required to use this module.

Testing
=======

1. Link a user to an employee record.

2. Set that employee as the `leave_manager_id` of some other employees.

3. Log in with that user and try to create a leave request.

4. Verify that the `employee_id` field only shows:

    - The current employee.

    - The employees managed by that employee.

Bug Tracker
===========

If you encounter any issues, please report them on the GitHub repository at `GitHub Issues <https://github.com/avanzosc/hr-addons/issues>`_.

Credits
=======

Contributors
------------

* Ana Juaristi <anajuaristi@avanzosc.es>
* Unai Beristain <unaiberistain@avanzosc.es>

For specific questions or support, please contact the contributors.

License
=======

This project is licensed under the LGPL-3 License. For more details, refer to the LICENSE file or visit <https://opensource.org/licenses/LGPL-3.0>.
