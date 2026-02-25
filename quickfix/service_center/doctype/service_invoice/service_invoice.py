# Copyright (c) 2026, Praveenkumar-Dhanasekar and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


class ServiceInvoice(Document):
	pass


def check_has_permission(doc,user):
	if user == "Administrator":
		return True
	if "QF Manager" not in frappe.get_roles(user):
		return False
	if doc.job_card and doc.payment_status != "Paid":
		return False
	

