from quickfix.service_center.doctype.job_card.job_card import JobCard

class CustomJobCard(JobCard):
    def validate(self):
        super().validate()
        self._check_urgent_unassigned()

    def _check_urgent_unassigned(self):
        if self.priority == "Urgent" and not self.assigned_technician:
            settings = frappe.get_single("QuickFix Settings")
            frappe.enqueue(
                "quickfix.utils.send_urgent_alert",
                job_card = self.name,manager= settings.manager_email
            )

# what is Method Resolution Order (MRO), and why calling super() is non-negotiable

# 1. **MRO (Method Resolution Order)** defines the exact order Python searches classes during inheritance.
# 2. Python uses C3 linearization to maintain consistent, predictable method lookup order.
# 3. `super()` ensures parent class logic executes according to MRO.
# 4. Skipping `super()` can bypass core validations and break framework behavior.
# 5. In frameworks like Frappe, not calling `super()` risks data integrity and hidden bugs.


# Write a comment block explaining: when would you choose override_doctype_class over doc_events?


# Use override_doctype_class when you need full control over a DocType’s core behavior.
# Choose it if you must replace standard methods, change internal logic deeply,
# modify validation flow entirely, or alter submit/cancel mechanics.
# It replaces the original controller class.
#
# Use doc_events for small extensions like adding validation,
# sending notifications, or running extra logic during lifecycle events.
# Prefer doc_events unless a complete behavioral override is absolutely necessary.

def after_app_install():
    data = [
        {
         "average_repair_hours": 24,
         "description": "A smartphone is a mobile device that combines the functionality of a traditional mobile phone with advanced computing capabilities, effectively serving as a handheld computer.",
         "device_type": "Smartphone",
        },
        {
         "average_repair_hours": 48,
         "description": "A laptop is a portable personal computer designed for mobile use, integrating all essential components—such as a display, keyboard, touchpad, battery, and speakers—into a single compact, clamshell-shaped unit.",
         "device_type": "Laptop",
        },
        {
         "average_repair_hours": 24,
         "description": "A tablet is a portable, wireless computing device with a touchscreen interface, typically ranging from 7 to 12 inches in screen size. ",
         "device_type": "Tablet",
        }
    ] 
    for row in data:
        if not frappe.get_doc("Device Type",row.device_type):
            device = frappe.new_doc("Device Type")
            device.device_type = row.device_type
            device.description = row.description
            device.average_repair_hours = row.average_repair_hours
            device.insert(ignore_permissions=True)      