# Copyright (c) 2026, Praveenkumar-Dhanasekar and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from datetime import datetime


class SparePart(Document):
	def autoname(self):
		part_code = (self.part_code).upper()
		count = frappe.db.count("Spare Part")
		self.name = f"{part_code}-PART-{datetime.now().year}-{count + 1}"

	def validate(self):
		if self.selling_price <= self.unit_cost:
			frappe.throw("Selling Price must be greater than the Unit Cost")

	