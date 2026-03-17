# Copyright (c) 2026, Praveenkumar-Dhanasekar and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.query_builder import DocType
from datetime import datetime, timedelta


class ServiceInvoice(Document):
	pass


def check_has_permission(doc,user):
	if user == "Administrator":
		return True

	roles = frappe.get_roles(user)

	if "QF Manager" in roles:
		return True
	if doc.job_card:
		job_card = frappe.get_doc("Job Card", doc.job_card)
		if job_card.payment_status != "Paid":
			return False

	return True



def get_overdue_jobs():
    JobCard = DocType("Job Card")

    seven_days_ago = datetime.now() - timedelta(days=7)

    query = (
        frappe.qb.from_(JobCard)
        .select(
            JobCard.name,
            JobCard.customer_name,
            JobCard.assigned_technician,
            JobCard.creation
        )
        .where(
            (JobCard.status.isin(["Pending Diagnosis", "In Repair"])) &
            (JobCard.creation < seven_days_ago)
        )
        .orderby(JobCard.creation, order=frappe.qb.asc)
    )

    return query.run(as_dict=True)






