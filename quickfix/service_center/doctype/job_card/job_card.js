// Copyright (c) 2026, Praveenkumar-Dhanasekar and contributors
// For license information, please see license.txt

// frappe.ui.form.on("Job Card", {
//     onload(frm) {
//         frappe.db.get_single_value("QuickFix Settings", "default_labour_charge")
//             .then(value => {
//                 const labour = value || 0
//                 frm.set_value("labour_charge", labour)
//                 calculate_total_amount(frm)
//             })
//     },

//     labour_charge(frm) {
//         calculate_total_amount(frm)
//     }
// })

// frappe.ui.form.on("Part Usage Entry", {
//     part(frm,cdt,cdn){
//         calculate_row_total(frm, cdt, cdn)
//     },
//     quantity(frm, cdt, cdn) {
//         calculate_row_total(frm, cdt, cdn)
//     }
// })

// function calculate_row_total(frm, cdt, cdn) {
//     const row = locals[cdt][cdn]

//     total_price = (row.quantity || 0) * (row.unit_price || 0)
//     frappe.model.set_value(cdt,cdn,"total",total_price)
//     frm.refresh_field("parts_used")
//     calculate_total_amount(frm)
// }

// function calculate_total_amount(frm) {
//     let  parts_total = 0;
    
//     (frm.doc.parts_used || []).forEach(d => {
//         parts_total += d.total_price || 0
//     })

//     const labour = frm.doc.labour_charge || 0

//     frm.set_value("parts_total", parts_total)
//     frm.set_value("final_amount", parts_total + labour)
// }

frappe.realtime.on("job_ready", async function(data) {
    console.log("222222222222222222222222222");
    // frappe.msgprint("ytcdytcytfy");
    console.log(data);
});