# Copyright (c) 2026, Praveenkumar-Dhanasekar and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from datetime import datetime

class AuditLog(Document):
	def autoname(self):
		count = frappe.db.count("Audit Log")
		self.name = f"AL-{datetime.now().year}-{count+1:05d}"
		
