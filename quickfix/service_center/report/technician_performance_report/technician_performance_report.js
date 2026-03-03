// Copyright (c) 2026, Praveenkumar-Dhanasekar and contributors
// For license information, please see license.txt

frappe.query_reports["Technician Performance Report"] = {
	"filters": [
		{
			"fieldname":"from_date",
			"fieldtype":'Date',
			"label":"From Date"
		},
		{
			"fieldname":"to_date",
			"fieldtype":'Date',
			"label":"To Date"
		},
		{
			"fieldname":"technician",
			"fieldtype":"Link",
			"label":"Technician",
			"options":'Technician'
		}

	]
};
