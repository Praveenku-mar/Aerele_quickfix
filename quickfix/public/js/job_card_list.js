frappe.listview_settings["Job Card"] = {

    add_fields: ["status", "docstatus", "final_amount", "priority"],

    color_map: {
        "Diagnosis": "orange",
        "In Repair": "blue",
        "Ready For Delivery": "green",
        "Delivered": "gray",
        "Cancelled": "red"
    },

    get_indicator(doc) {
        if (!doc.status) return;

        const color = this.color_map[doc.status] || "gray";

        return [
            doc.status,
            color,
            `status,=,${doc.status}`
        ];
    },

    formatters: {
        final_amount(value) {
            if (!value) return "";

            return format_currency(
                value,
                frappe.defaults.get_default("currency")
            );
        }
    },

    button: {

        show(doc) {
            return doc.status === "In Repair" && doc.docstatus === 0;
        },

        get_label() {
            return "Mark as Ready";
        },

        get_description() {
            return "Change status to Ready For Delivery";
        },

        action(doc) {

            frappe.confirm(
                `Mark ${doc.name} as Ready For Delivery?`,
                () => {

                    frappe.call({
                        method: "quickfix.service_center.doctype.job_card.job_card.mark_delivered",
                        args: {
                            doctype: "Job Card",
                            name: doc.name,
                            fieldname: "status",
                            value: "Ready For Delivery"
                        },
                        callback: function (r) {
                            if (!r.exc) {
                                frappe.show_alert({
                                    message: "Status Updated",
                                    indicator: "green"
                                });
                                frappe.listview.refresh();
                            }
                        }
                    });

                }
            );
        }
    }
};