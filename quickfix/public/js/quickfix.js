frappe.ready(function() {
    if (frappe.boot.quickfix_shop_name) {
        $(".navbar-brand").append(
            `<span class="ml-2 text-muted">
                ${frappe.boot.quickfix_shop_name}
            </span>`
        );
    }
});
