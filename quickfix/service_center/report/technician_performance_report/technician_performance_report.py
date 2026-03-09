# Copyright (c) 2026, Praveenkumar-Dhanasekar and contributors
# For license information, please see license.txt

import frappe

from frappe.utils import date_diff

def execute(filters=None):
    if not filters:
        filters = {}

    columns = get_columns()
    data = get_data(filters)
    chart = get_chart(data)
    frappe.log_error("111111",data)
    return columns, data, None, chart,get_report_summary(data)

def get_columns():
    cols = [
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
            "fieldtype":"Int",
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
            "fieldtype":"Percentage",
            "label":"Completion Rate",
            "precision": 2,
            "width":200
        }
    ]
    for dt in frappe.get_list("Device Type", fields=["name"]):
        fieldname = dt.name.lower()

        cols.append({
            "label": dt.name,
            "fieldname": fieldname,
            "fieldtype": "Int",
            "width": 100
        })
    return cols

def get_data(filters):

    job_filters = {}

    if filters.get("technician"):
        job_filters["assigned_technician"] = filters.get("technician")

    if filters.get("from_date") and filters.get("to_date"):
        job_filters["creation"] = ["between", [filters.get("from_date"), filters.get("to_date")]]

    device_types = frappe.get_list("Device Type",fields=["name"],debug=True)
    device_map = {
        dt.name: dt.name.lower()
        for dt in device_types
    }
    jobs = frappe.get_list(
        "Job Card",
        filters=job_filters,
        fields=[
            "assigned_technician",
            "status",
            "final_amount",
            "labour_charge",
            "device_type",
            "creation",
            "delivery_date"
        ]
    )
    frappe.log_error("job",jobs)

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
                "completion_rate": 0,
            }
            for fieldname in device_map.values():
                result[tech][fieldname] = 0

        result[tech]["total_jobs"] += 1

        # Count device type
        if job.device_type in device_map:
            fieldname = device_map[job.device_type]
            result[tech][fieldname] += 1


        if job.status == "Delivered":
            result[tech]["completed_jobs"] += 1
            result[tech]["revenue"] += job.final_amount
            result[tech]["total_labour_charge"] += job.labour_charge

            # Calculate turnaround days
            turnaround = date_diff(job.delivery_date, job.creation)
            result[tech]["total_turnaround_days"] += turnaround

    # Final Calculations
    for tech in result:
        total = result[tech]["total_jobs"]
        completed = result[tech]["completed_jobs"]

        # Completion Rate
        result[tech]["completion_rate"] = round((completed / total) * 100,2) if total else 0

        # Average Turnaround
        if completed > 0:
            result[tech]["avg_turnaround_days"] = (
                result[tech]["total_turnaround_days"] / completed
            )
    return list(result.values())


def get_chart(data):

    labels = []
    total_jobs = []
    completed_jobs = []

    for row in data:
        labels.append(row.get("technician"))
        total_jobs.append(row.get("total_jobs"))
        completed_jobs.append(row.get("completed_jobs"))

    chart = {
        "data": {
            "labels": labels,
            "datasets": [
                {
                    "name": "Total Jobs",
                    "values": total_jobs
                },
                {
                    "name": "Completed Jobs",
                    "values": completed_jobs
                }
            ]
        },
        "type": "bar",
        "colors": ["#3b5bdb", "#2f9e44"]
    }

    return chart

def get_report_summary(data):
    if not data:
        return []

    total_jobs = 0
    total_revenue = 0
    best_technician = None
    best_rate = -1
    
    for row in data:
        rate = row.get("completion_rate") or 0
        frappe.log_error("rate",rate)
        if rate > best_rate:
            best_rate = rate
            best_technician = row.get("technician")
            total_revenue = row.get("revenue") or 0
            total_jobs = row.get("total_jobs") or 0

    return [
        {
            "label": "Total Jobs",
            "value": total_jobs,
            "indicator": "Blue"
        },
        {
            "label": "Total Revenue",
            "value": total_revenue,
            "indicator": "Green",
            "datatype": "Currency"
        },
        {
            "label": "Best Technician",
            "value": best_technician or "N/A",
            "indicator": "Green" if best_rate >= 90 else "Orange"
        }
    ]