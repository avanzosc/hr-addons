{
    "name": "HR Attendance Custom Form",
    "version": "16.0.1.0.0",
    "category": "Human Resources",
    "summary": "Custom HR Attendance Form",
    "author": "Avanzosc",
    "license": "LGPL-3",
    "depends": ["hr_attendance", "web"],
    "website": "https://github.com/avanzosc/hr-addons",
    "assets": {
        "web.assets_backend": [
            "hr_attendance_custom_form/static/src/js/**/*",
            "hr_attendance_custom_form/static/src/xml/**/*",
        ],
    },
    "installable": True,
    "application": False,
    "auto_install": False,
}
