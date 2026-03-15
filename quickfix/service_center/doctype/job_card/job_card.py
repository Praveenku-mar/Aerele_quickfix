# Copyright (c) 2026, Praveenkumar-Dhanasekar and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
import re
from datetime import datetime
from frappe.utils.pdf import get_pdf
from frappe.utils.file_manager import get_file

class JobCard(Document):
	def validate(self):
		self.final = self.final_amount or 0
		self.validate_phone()
		self.check_technician()
		self.set_total_part_cost()
		self.set_total_cost()
		self.estimated_cost_validation()

	def before_submit(self):
		if not self.delivery_date:
			frappe.throw("Please select the delivery date.")

		if self.status != "Ready For Delivery":
			frappe.throw("Job is not ready for delivery.")
		self.validate_submit()
		self.check_stock()	
		self.status = "Delivered"

	def on_submit(self):
		
		self.stock_update()
		self.create_invoice()
		self.notify_job_complete()
		self.send_job_ready_mail()
		self.send_pft_job()
		# frappe.db.commit()
	
	def on_cancel(self):
		self.status = "Cancelled"
		self.roll_back_parts()
		self.cancel_invoice()

	def on_trash(self):
		if self.status != "Cancelled" and self.status != "Draft":
			frappe.throw("You can only delete Draft or Cancelled Job Cards.",frappe.ValidationError)

		invoice = frappe.get_doc("Service Invoice",{"job_card",self.name})
		invoice.delete()

	def before_print(self, print_settings=None):
		self.print_summary = f"{self.customer_name} - {self.device_type} {self.device_brand}"

	def on_update(self):
		frappe.cache.delete_value("job_card_status_chart")

	#Validate Hook
	def validate_phone(self):
		phone = str(self.customer_phone or "")
		if not re.fullmatch(r"\d{10}",phone):
			frappe.throw("Customer phone number must contain exactly 10 digits.")

	@frappe.whitelist()
	def check_technician(self):

		# if not self.assigned_technician:
		# 	frappe.throw("")
		required_status = ["In Repair", "Ready For Delivery", "Delivered"]

		if self.status in required_status and not self.assigned_technician:
			frappe.throw("Assigned Technician is mandatory for this status.")


		exists = frappe.db.exists(
			"Technician",
			{
				"name": self.assigned_technician,
				"status": "Active"
			}
		)

		if not exists:
			frappe.throw(f"{self.assigned_technician} Technician is on Leave.")

		

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

	def estimated_cost_validation(self):
		if self.status == "In Repair" and not self.estimated_cost:
			frappe.throw("Estimated Cost is required")

	#Before save hook
	def validate_submit(self):
		if not self.status == "Ready For Delivery":
			frappe.throw("Job is not ready for delivery.")

	def check_stock(self):
		for row in self.parts_used:
			qty = row.quantity
			if qty <= 0:
				frappe.throw("Quantity must be greater than zero",frappe.ValidationError)
			aval_qty = frappe.db.get_value("Spare Part",row.part,"stock_qty")
			if aval_qty < qty:
				frappe.throw(f"Available stock for {row.part} is {aval_qty}.",frappe.ValidationError)
	
	#On submit Hook
	def stock_update(self):
		for row in self.parts_used:
			stock = frappe.db.get_value("Spare Part",row.part,"stock_qty")
			frappe.db.set_value("Spare Part",row.part,"stock_qty",stock - row.quantity)

	
	def create_invoice(self):
		exists = frappe.db.exists("Service Invoice",{"job_card":self.name})
		if exists:
			return

	
		invoice = frappe.new_doc("Service Invoice")
		invoice.job_card = self.name
		invoice.invoice_date = datetime.now()
		invoice.labour_charge = self.labour_charge
		invoice.parts_total = self.parts_total
		invoice.total_amount = self.final_amount
		invoice.payment_status = "Unpaid"
		invoice.insert(ignore_permissions=True)
		invoice.submit()

	def notify_job_complete(self):
		# frappe.publish_realtime(
		# 	"job_ready",
		# 	{
		# 		"job_card":self.name
		# 	}
		# 	# message={
		# 	# 	"job_card":self.name,
		# 	# 	"status":"Completed",
		# 	# 	"message":f"Job Card {self.name} is ready for delivery."
		# 	# },
		# 	# user=frappe.session.user
		# )
		frappe.publish_realtime(
		"job_ready",
		{"job_card": self.name},
		after_commit=True
	)
		

	def send_job_ready_mail(self):
		#skip during automated tests
		if frappe.flags.in_test:
			return
		frappe.enqueue(
			method="quickfix.api.send_job_ready_email",
			queue="short",         
			timeout=300,
			job_name=f"Send Job Ready Email - {self.name}",
			job_card=self.name
		)

	def send_pft_job(self):
		#skip during automated tests
		if frappe.flags.in_test:
			# pdf = b"test pdf"
			return

		else:
			pdf = frappe.get_print(self.doctype, self.name, print_format="Job Card Receipt", as_pdf=True)
		frappe.log_error("1111")
		# pdf = get_pdf(message)
		frappe.sendmail(recipients=[self.customer_email],
			subject="Job Card Submitted",
			message="Please find the attached Job Card PDF.",
			attachments=[{
				"fname":f"{self.name}-invoice.pdf",
				"fcontent":pdf
			}]
		)

	#On cancel Hook
	def roll_back_parts(self):
		for row in self.parts_used:
			aval_qty = frappe.db.get_value("Spare Part",row.part,"stock_qty")
			frappe.db.set_value("Spare Part",row.part,"stock_qty",aval_qty + row.quantity)

	def cancel_invoice(self):
		invoice = frappe.get_doc("Service Invoice",{"job_card":self.name})
		# invoice = frappe.get_doc("Service Invoice",in_name)

		if not invoice:
			return 
		if invoice.docstatus == 1:
			invoice.cancel()
	
	@frappe.whitelist()
	def show_alert(self):
		frappe.log_error("11111111")
		frappe.publish_realtime("job_ready",{'message':"This Job Card is Ready for Delivery"})
		return {"ok": True}

		

	

@frappe.whitelist()
def show_alert():
	frappe.publish_realtime("job_ready", {"message": "This Job Card is Ready for Delivery"})
	return {"ok": True}


def check_access_permission(user):
	if user == "Administrator":
		return ""
	if "QF Technician" in frappe.get_roles(user):
		technician_name = frappe.db.exists(
			"Technician",
			{"user": user}
		)
		if technician_name:
			return f"""
				`tabJob Card`.assigned_technician IN (
					SELECT name FROM `tabTechnician`
				WHERE user = {frappe.db.escape(user)}
			)
			"""
		return "1=0"

@frappe.whitelist()
def get_technician(device_type):
	return frappe.get_all(
		"Technician",
		filters={
			"specialization":device_type,
			"status":"Active"
		},pluck="name"
	)

# @frappe.whitelist()
# def check_technician(device_type,technician):
# 	exits = frappe.db.exists("Technician",
# 		{
# 			"name":technician,
# 			"specialization":device_type,
# 			"status":"Active"
# 		}
# 	)
# 	if not exits:
# 		frappe.show_alert("Technician specialization not matching with device type or is on Leave.")





@frappe.whitelist()
def reject_job(name,reason):
	frappe.log_error("reject_job function")
	frappe.db.set_value("Job Card",name,
		{
			"status":"Cancelled",
			"remarks":reason
		})
	# rej_doc = frappe.get_doc("Job Card",name)
	# rej_doc.status = "Cancelled"
	# rej_doc.remarks = reason
	# rej_doc.save()
	# frappe.db.commit()

@frappe.whitelist()
def assign_technician(name,technician):
	frappe.db.set_value("Job Card",name,"assigned_technician",technician)
	doc = frappe.get_doc("Job Card",name)
	# doc.assigned_technician = technician
	# doc.save()
	# frappe.db.commit()

@frappe.whitelist()
def mark_delivered(doctype,name,fieldname,value):
	frappe.set_value(doctype,name,fieldname,value)


# @frappe.whitelist()
# def back_ground():
# 	frappe.enqueue(method="quickfix.service_center.doctype.job_card.job_card.get_job",queue="short",timeout=500,retry=Retry(max=3))

# def get_job():
# 	return frappe.get_doc("job Card","JC-2026-00001")