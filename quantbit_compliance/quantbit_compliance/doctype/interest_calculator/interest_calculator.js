// Copyright (c) 2024, abub.patel@erpdata.in and contributors
// For license information, please see license.txt

frappe.ui.form.on('Interest Calculator', {
	get_chart: function(frm) {
		frm.call({
			method: 'get_chart',
			doc: frm.doc
		})
	}
});
