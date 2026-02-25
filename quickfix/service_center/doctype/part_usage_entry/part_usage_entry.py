# Copyright (c) 2026, Praveenkumar-Dhanasekar and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


class PartUsageEntry(Document):
	pass
# `merge=True` dangerous because two separate records become
# permanently combined. Data may mix incorrectly, 
# linked documents update automatically, and original identity is lost.
#  Mistakes are hard to reverse without backup.
