// Copyright (c) 2026, Praveenkumar-Dhanasekar and contributors
// For license information, please see license.txt

frappe.query_reports["Spare Parts Inventory"] = {
	formatter: function(value, row, column, data, default_formatter) {

		value = default_formatter(value, row, column, data);
		// console.log(data.stock_qty,data.reorder_level)
		if (
			data &&
			Number(data.stock_qty) <= Number(data.reorder_level)
		) {
			// console.log(data.stock_qty,data.recorder_level)
			return `<div style="background-color:#ffcccc;
				font-weight:bold;
				padding:4px;">
				${value}
			</div>`;
		}
		if (data && data.part_name === "Total") {
            value = `<b>${value}</b>`;
        }

		return value;
	},

	filters: [
		{
			fieldname: "item",
			fieldtype: "Link",
			label: "Item",
			options: "Spare Part"
		}
	]
};