# Copyright (c) 2026, Praveenkumar-Dhanasekar and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
import re
from datetime import datetime

class JobCard(Document):
	def validate(self):
		self.validate_phone()
		self.check_assign_tech()
		self.set_total_part_cost()
		self.set_total_cost()

	def before_submit(self):
		self.validate_submit()
		self.check_stock()	

	def on_submit(self):
		self.stock_update()
		self.create_invoice()
		self.notify_job_complete()
		self.send_job_ready_mail()
	
	def on_cancel(self):
		self.status = "Cancelled"
		self.roll_back_parts()



	#Validate Hook
	def validate_phone(self):
		phone = self.customer_phone
		if not re.fullmatch(r"\d{10}",phone):
			frappe.throw("Customer phone number must contain exactly 10 digits.")

	def check_assign_tech(self):
		req_satuts = ["In Repair","Ready For Delivery","Delivered","Cancelled"]
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

	#Before save hook
	def validate_submit(self):
		if not self.status == "Ready For Delivery":
			frappe.throw("Job is not ready for delivery.")

	def check_stock(self):
		for row in self.parts_used:
			qty = row.quantity
			aval_qty = frappe.db.get_value("Spare Part",row.part,"stock_qty")
			if aval_qty < qty:
				frappe.throw(f"Available stock for {row.part} is {aval_qty}.")
	
	#On submit Hook
	def stock_update(self):
		for row in self.parts_used:
			aval_qty = frappe.db.get_value("Spare Part",row.part,"stock_qty")
			frappe.db.set_value("Spare Part",row.part,"stock_qty",aval_qty - row.quantity,ignore_permissions=True)

	
	def create_invoice(self):
		invoice = frappe.new_doc("Service Invoice")
		invoice.job_card = self.name
		invoice.invoice_date = datetime.now()
		invoice.labour_charge = self.labour_charge
		invoice.parts_total = self.parts_total
		invoice.final_amount = self.final_amount
		invoice.payment_status = "Unpaid"
		invoice.insert(ignore_permissions=True)

	def notify_job_complete(self):
		frappe.publish_realtime(
			"job_ready",
			message={
				"job_card":self.name,
				"status":"Completed",
				"message":f"Job Card {self.name} is ready for delivery."
			},
			user=frappe.session.user
		)

	def send_job_ready_mail(self):
		frappe.enqueue(
			method="quickfix.api.send_job_ready_email",
			queue="short",         
			timeout=300,
			job_name=f"Send Job Ready Email - {self.name}",
			job_card=self.name
		)

	#On cancel Hook

	def roll_back_parts(self):
		for row in self.parts_used:
			aval_qty = frappe.db.get_value("Spare Part",row.part,"stock_qty")
			frappe.db.set_value("Spare Part",row.part,"stock_qty",aval_qty + row.quantity)

	

	
