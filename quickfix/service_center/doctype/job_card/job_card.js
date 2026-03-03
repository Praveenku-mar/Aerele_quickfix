// // Copyright (c) 2026, Praveenkumar-Dhanasekar and contributors
// // For license information, please see license.txt

// frappe.ui.form.on("Job Card", {
//     refresh(frm){
//         if (!frappe.user.has_role("QF Manager")) {
//             frm.set_df_property("customer_phone", "hidden", 1);
//         }
//         if(frm.doc.status){
//             // console.log("condition")
//             let color_map ={
//                 "Diagnosis" : "orange",
//                 "In Repair":"blue",
//                 "Ready For Delivery":"green",
//                 "Delivered":"gray",
//                 "Cancelled":"red"
//             };
//             frm.dashboard.add_indicator(
//                 frm.doc.status,
//                 color_map[frm.doc.status]
//             );
//         }

//         if(frm.doc.status === "Ready For Delivery" && frm.doc.docstatus === 1 ){
//             // console.log("Button")
//             frm.add_custom_button("Mark as Delivered",()=>{
//                 // frm.set_value("status","Delivered");
//             });
//         }


//         //Set shop_name
//         if(frappe.boot.quickfix_shop_name){
//             console.log("set intro")
//             frm.set_intro(
//                 `Service Center: ${frappe.boot.quickfix_shop_name}`,
//                 "blue"
//             );
//         }

//         //Reject job
//         if(frm.doc.status != "Cancelled"){
//         frm.add_custom_button(("Reject Job"), ()=>{
//             console.log("reject")
//             console.log(frm.doc.device_type)
//             let dialog = new frappe.ui.Dialog({
//                 title:"Reject Job",
//                 fields:[
//                     {
//                         label:"Rejection Reason",
//                         fieldname:"reason",
//                         fieldtype:"Small Text",
//                         reqd:1,
//                         // get_query: () => ({
// 					    //     filters: {
// 						//         specialization: frm.doc.device_type,
// 					    //     },
// 				        // }),
//                     }
//                 ],
//                 primary_action_label: "Submit",
//                 primary_action(values){
//                     frappe.call({
//                         method:"quickfix.service_center.doctype.job_card.job_card.reject_job",
//                         args:{
//                             name : frm.doc.name,
//                             reason : values.reason
//                         },
//                         callback: function(){
//                             dialog.hide();
//                             frm.reload_doc();
//                         }
//                     });
//                 }
//             });
//             dialog.show();
//         }).addClass("btn-danger");
//     }
    

//     //Transfer Technician

//     frm.add_custom_button(("Transfer Technician"), () =>{
//         frappe.prompt(
//             [
//                 {
//                     fieldname:"technician",
//                     fieldtype:"Link",
//                     label:"Technician",
//                     options:"Technician",
//                     reqd:1,
//                         get_query: () => ({
// 					        filters: {
// 						        specialization: frm.doc.device_type,
// 					        },
// 				        }),

//                 }
//             ],
            
//             function(data){
//                 frappe.confirm(`Are you sure you want change the technician to ${data.technician}?`,
//                     () =>{
                            
//                             frappe.call({
//                             method:"quickfix.service_center.doctype.job_card.job_card.assign_technician",
//                             args:{
//                                 name : frm.doc.name,
//                                 technician : data.technician
//                             },
//                             // freeze: true,
//                             // freeze_message : "Reassigning Technician......",
//                             callback: function(r){
//                                 if(!r.exc){
//                                     frappe.msgprint({
//                                         title:"Success",
//                                         message:"Reassigned Technician",
//                                         indicator:"green"
//                                     });
//                                 }
                                
//                             }
//                         });
//                         frm.trigger("assigned_technician")
//                     }   
//                 )  
//             }
//         )
//     })
    
//     },
//     onload(frm) {
//         frappe.db.get_single_value("QuickFix Settings", "default_labour_charge")
//             .then(value => {
//                 const labour = value || 0
//                 frm.set_value("labour_charge", labour)
//                 calculate_total_amount(frm)
//             });
//         console.log("onload")
//         frappe.call({
//             method:"quickfix.service_center.doctype.job_card.job_card.show_alert"
//         });
//         frappe.realtime.on("job_ready",function(data){
//             frappe.show_alert({
//                 message:"This Job Card is Ready for Delivery",
//                 indicator:"green"
//             },10);
//         })
//     },
//     assigned_technician(frm){
//         frm.call("check_technician");
//     },
//     labour_charge(frm) {
//         calculate_total_amount(frm)
//     },
//     device_type(frm){
//         if (!frm.doc.device_type) return;
//         frappe.call({
//             method: "quickfix.service_center.doctype.job_card.job_card.get_technician",
//             args: {
//                 device_type: frm.doc.device_type
//             },
//             callback: function(r) {
//                 if (r.message) {
//                     console.log(r.message);
//                     let technician = r.message
//                     console.log(technician)
//                     frm.set_query("assigned_technician", () =>{
//                          return {
//                         filters: {
//                             name: ["in", technician]
//                         }
//                     };
//                     });
//                 }
//             }
//         });
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
//     console.log("111111111");
//     const row = locals[cdt][cdn]
//     console.log("222222222222");
//     console.log(row);

//     total_price = (row.quantity || 0) * (row.unit_price || 0)
//     frappe.model.set_value(cdt,cdn,"total_price",total_price)
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

// // frappe.realtime.on("job_ready", async function(data) {
// //     console.log("222222222222222222222222222");
// //     // frappe.msgprint("ytcdytcytfy");
// //     console.log(data);
// // });