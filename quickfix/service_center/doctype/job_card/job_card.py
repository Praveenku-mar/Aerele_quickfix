# Copyright (c) 2026, Praveenkumar-Dhanasekar and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
import re

class JobCard(Document):
	def validate(self):
		self.validate_phone()
		self.check_assign_tech()
		self.set_total_part_cost()
		self.set_total_cost()


	def validate_phone(self):
		phone = self.customer_phone
		if not re.fullmatch(r"\d{10}",phone):
			frappe.throw("Customer phone number must contain exactly 10 digits.")

	def check_assign_tech(self):
		req_satuts = ["In Repair","Ready","For Delivery","Delivered","Cancelled"]
		if self.status in req_satuts and not self.assigned_technician:
			frappe.throw("Assigned Technician is mandatory for this status.")

	def set_total_part_cost(self):
		for row in self.parts_used:
			qty = row.quantity
			rate = row.unit_price 
			row.total_price = rate * qty
	
	def set_total_cost(self):
		lab_cost = frappe.db.get_single_value("QuickFix Settings","default_labour_charge")
		total = 0
		for row in self.parts_used:
			total += row.total_price

		self.labour_charge = lab_cost
		self.parts_total = total
		self.final_amount = lab_cost + total

		

	
