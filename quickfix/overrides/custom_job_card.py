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

