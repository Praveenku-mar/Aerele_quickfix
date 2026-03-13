# Copyright (c) 2026, Praveenkumar-Dhanasekar and Contributors
# See license.txt

import frappe
from frappe.tests.utils import FrappeTestCase
from frappe.utils import nowdate


def make_device(dev_name="_test_smartphone"):
	if frappe.db.exists("Device Type", {"device_type": dev_name}):
		return frappe.get_doc("Device Type", {"device_type": dev_name})

	doc = frappe.new_doc("Device Type")
	doc.device_type = dev_name
	doc.description = "test device"
	doc.insert()
	return doc


def make_technician(name="_test_tech", emp_id="EMP-0001"):
	if frappe.db.exists("Technician", {"employee_id": emp_id}):
		return frappe.get_doc("Technician", {"employee_id": emp_id})

	doc = frappe.new_doc("Technician")
	doc.technician_name = name
	doc.employee_id = emp_id
	doc.specialization = "_test_smartphone"
	doc.status = "Active"
	doc.insert()
	return doc


def make_spare_part(**kwargs):
	part_code = kwargs.get("part_code","_test_part")
	stock_qty = kwargs.get("stock_qty",10)
	unit_cost = kwargs.get("u_cost",100)
	selling_cost =kwargs.get("s_cost",110)

	if frappe.db.exists("Spare Part", {"part_code": part_code}):
		return frappe.get_doc("Spare Part", {"part_code": part_code})

	data = {
		"doctype":"Spare Part",
		"part_name":"_test",
		"part_code":part_code,
		"stock_qty":stock_qty,
		"unit_cost":unit_cost,
		"selling_price":selling_cost
	}
	data.update(kwargs)
	doc = frappe.get_doc(data)
	doc.insert()
	return doc


def make_job_card(**kwargs):

	device = make_device()
	tech = make_technician()
	part = make_spare_part()

	data = {
		"doctype": "Job Card",
		"customer_name": "Test Customer",
		"customer_phone": kwargs.get("customer_phone",9999999999) ,
		"customer_email": "22bad098@gmail.com",
		"device_type": device.name,
		"device_brand": "Samsung",
		"imei_or_serial": "IMEI123",
		"problem_description": "Screen broken",
		"assigned_technician": tech.name,
		"diagnosis_notes": "Replace screen",
		"estimated_cost": 500,
		"delivery_date": nowdate(),
		"parts_used": [
			{
				"part": part.name,
				"part_name": part.part_name,
				"unit_price": part.selling_price,
				"quantity": 1,
				"total_price": part.selling_price,
			}
		],
		"parts_total": part.selling_price,
		"labour_charge": 200,
		"final_amount": part.selling_price + 200,
		"status":kwargs.get("status", "Draft")
	}

	data.update(kwargs)

	doc = frappe.get_doc(data)
	doc.insert()
	return doc


class TestJobCard(FrappeTestCase):

	def setUp(self):
		self.device = make_device()
		self.tech = make_technician()
		self.part = make_spare_part()
		self.job = make_job_card()

	def test_job_card_created(self):
		self.assertEqual(self.job.docstatus, 0)

	def test_job_card_status(self):
		self.assertEqual(self.job.status, "Draft")

	def test_job_card_device_link(self):
		self.assertEqual(self.job.device_type, self.device.name)

	def test_job_card_technician_link(self):
		self.assertEqual(self.job.assigned_technician, self.tech.name)

	def test_spare_part_stock(self):
		part = make_spare_part()
		self.assertGreaterEqual(part.stock_qty, 0)

	def test_job_card_submit(self):
		self.job.status = "Ready For Delivery"
		print(nowdate())
		self.job.delivery_date = nowdate()
		self.job.save()
		self.job.submit()

		self.assertEqual(self.job.docstatus, 1)

	def test_invoice_creation(self):
		self.job.status = "Ready For Delivery"
		print(nowdate())
		self.job.delivery_date = nowdate()
		self.job.save()
		self.job.submit()

		invoice_name = frappe.db.get_value(
        	"Service Invoice",
        	{"job_card": self.job.name},
        	"name"
    	)
		invoice = frappe.get_doc("Service Invoice",invoice_name)
		self.assertIsNotNone(invoice)
		self.assertEqual(invoice.docstatus,0)

	def test_happy_path_insert(self):
		self.assertTrue(frappe.db.exists("Job Card",self.job.name))
		self.assertEqual(self.job.docstatus,0)


	#Phone Validation Boundary cases
	def test_phone_validation(self):
		invalid_numbers=[
			"12344",
			"1234267460979643",
			"98765ABCD1"
		]

		for phone in invalid_numbers:
			with self.assertRaises(frappe.ValidationError):
				make_job_card(customer_phone=phone)
		
		job = make_job_card(customer_phone="9092837965")
		self.assertTrue(frappe.db.exists("Job Card",job.name))


	#Spare part selling price constraint
	def test_spare_part_price_constraints(self):
		with self.assertRaises(frappe.ValidationError):
			spare_equal = make_spare_part(part_code="_equal_test",
				stock_qty=5,
				u_cost = 500,
				s_cost=500
			)
		
		with self.assertRaises(frappe.ValidationError):
			spare_lower = make_spare_part(part_code="_lower_test",
				stock_qty=5,
				u_cost = 500,
				s_cost=400
			)

		spare_valid = spare_lower = make_spare_part(part_code="_valid_test",
				stock_qty=5,
				u_cost = 500,
				s_cost=501
			)

		self.assertTrue(spare_valid.name)

	#Final Amount Computation
	def test_final_amount_computation(self):
		job = make_job_card()
		expected_parts_total = 1 * self.job.parts_used[0].unit_price
		expected_final_amount = expected_parts_total + job.labour_charge

		self.assertEqual(job.parts_total, expected_parts_total)
		self.assertEqual(job.final_amount,expected_final_amount)

	#Status Transition Guard
	def test_in_repair_status_transition_guard(self):
		self.job.status = "In Repair"
		self.job.assigned_technician = None   # deliberately remove the technician
 
		with self.assertRaises(frappe.ValidationError):
			self.job.save()

	def test_in_repair_tech_status_transition_guard(self):
		self.job.status = "In Repair"
		self.job.assigned_technician = self.tech.name
		self.job.save()
		
		self.assertEqual(self.job.status,"In Repair")
	
	def test_estimated_cost_requires(self):
		self.job.status = "In Repair"
		self.job.estimated_cost = 0
		with self.assertRaises(frappe.ValidationError):
			self.job.save()


	def test_child_row_computation(self):
		part = make_spare_part()
		tech = make_technician()
		device = make_device()

		job = frappe.get_doc({
			"doctype": "Job Card",
			"customer_name": "Test Customer",
			"customer_phone": "9788636286",
			"customer_email": "test@example.com",
			"device_type": device.name,
			"device_brand": "Samsung",
			"imei_or_serial": "IMEI123",
			"problem_description": "Screen broken",
			"assigned_technician": tech.name,
			"diagnosis_notes": "Replace screen",
			"estimated_cost": 500,
			"delivery_date": nowdate(),
			"parts_used": [
				{
					"part": part.name,
					"part_name": part.part_name,
					"unit_price": part.selling_price,
					"quantity": 1
				},
				{
					"part": part.name,
					"part_name": part.part_name,
					"unit_price": part.selling_price,
					"quantity": 2
				}
			],
			"status": "Draft"
		}).insert()

		row1_total = 1 * part.selling_price
		row2_total = 2 * part.selling_price

		self.assertEqual(job.parts_used[0].total_price, row1_total)
		self.assertEqual(job.parts_used[1].total_price, row2_total)

		expected_total = row1_total + row2_total
		self.assertEqual(job.parts_total, expected_total)

	def tearDown(self):
		frappe.db.rollback()