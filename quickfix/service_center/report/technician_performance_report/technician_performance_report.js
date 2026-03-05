// Copyright (c) 2026, Praveenkumar-Dhanasekar and contributors
// For license information, please see license.txt

frappe.query_reports["Technician Performance Report"] = {
	formatter: function(value, row, column, data, default_formatter) {

        value = default_formatter(value, row, column, data);

        if (column.fieldname === "completion_rate" && data) {

            if (data.completion_rate < 70) {
                value = `<span style="color:red;font-weight:bold">${value}</span>`;
            }

            if (data.completion_rate >= 90) {
                value = `<span style="color:green;font-weight:bold">${value}</span>`;
            }
        }

        return value;
    },
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
