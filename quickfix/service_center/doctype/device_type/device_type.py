# Copyright (c) 2026, Praveenkumar-Dhanasekar and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document



class DeviceType(Document):
	def validate(self):
		frappe.utils.logger.set_log_level("INFO")
		
		logger = frappe.logger("quickfix", allow_site=True, file_count=50)
		# frappe.log_error("validate",logger)
		logger.info("Dummyyyyyyyyyyyyyyy")
		logger.warning("webhook warning")
		logger.error("webhook error")

