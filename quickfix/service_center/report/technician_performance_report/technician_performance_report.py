# Copyright (c) 2026, Praveenkumar-Dhanasekar and contributors
# For license information, please see license.txt

import frappe


def execute(filters=None):
	
	return get_columns(),get_data(filters)



def get_columns():
	return[
		{
			"fieldname":"technician",
			"fieldtype":"Link",
			"label":"Technician",
			"options":"Technician",
			"width":200
		},
		{
			"fieldname":"total_jobs",
			"fieldtype":"Int",
			"label":"Total Jobs",
			"width":200
		},
		{
			"fieldname":"completed_jobs",
			"fieldtype":"Int",
			"label":"Completed",
			"width":200
		},
		{
			"fieldname":"avg_turnaround_days",
			"fieldtype":"Currency",
			"label":"Avg Turnaround Days",
			"width":200
		},
		{
			"fieldname":"revenue",
			"fieldtype":"Currency",
			"label":"Revenue",
			"width":200
		},
		{
			"fieldname":"completion_rate",
			"fieldtype":"Float",
			"label":"Completion Rate",
			"width":200
		}
	]
def get_data(filters):

    job_filters = {"docstatus": 1}

    if filters.get("technician"):
        job_filters["assigned_technician"] = filters.get("technician")

    if filters.get("from_date") and filters.get("to_date"):
        job_filters["creation"] = ["between", [filters.get("from_date"), filters.get("to_date")]]

    jobs = frappe.get_all(
        "Job Card",
        filters=job_filters,
        fields=[
            "assigned_technician",
            "status",
            "final_amount",
            "labour_charge",
            "creation",
            "modified"
        ]
    )

    result = {}

    for job in jobs:
        tech = job.assigned_technician
        if not tech:
            continue

        if tech not in result:
            result[tech] = {
                "technician": tech,
                "total_jobs": 0,
                "completed_jobs": 0,
                "total_labour_charge": 0,
                "revenue": 0,
                "total_turnaround_days": 0,
                "avg_turnaround_days": 0,
                "completion_rate": 0
            }

        result[tech]["total_jobs"] += 1

        if job.status == "Delivered":
            result[tech]["completed_jobs"] += 1
            result[tech]["revenue"] += flt(job.final_amount)
            result[tech]["total_labour_charge"] += flt(job.labour_charge)

            # Calculate turnaround days
            turnaround = date_diff(job.modified, job.creation)
            result[tech]["total_turnaround_days"] += flt(turnaround)

    # Final Calculations
    for tech in result:
        total = result[tech]["total_jobs"]
        completed = result[tech]["completed_jobs"]

        # Completion Rate
        result[tech]["completion_rate"] = (completed / total) * 100 if total else 0

        # Average Turnaround
        if completed > 0:
            result[tech]["avg_turnaround_days"] = (
                result[tech]["total_turnaround_days"] / completed
            )

        # Remove helper field (not needed in report)
        result[tech].pop("total_turnaround_days", None)

    return list(result.values())