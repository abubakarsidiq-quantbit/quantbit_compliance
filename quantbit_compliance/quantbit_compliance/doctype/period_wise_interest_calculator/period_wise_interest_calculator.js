// Copyright (c) 2024, abub.patel@erpdata.in and contributors
// For license information, please see license.txt
// hello
frappe.ui.form.on('Period Wise Interest Calculator', {
	calculate_interest: function(frm) {
		if(frm.doc.amount && frm.doc.rate_of_interest && frm.doc.date && frm.doc.period){
			frm.call({
				method: 'calculate_interest',
				doc: frm.doc
			})
		}
		else{
			frappe.throw("Check Amount or Rate or Date or Period is Set Properly.......")
		}
	},
	setup: function(frm) {
        frm.set_query("account", function() {
			return {
				filters: [["Account", "company", '=', frm.doc.company]]
			};
		});
	}
});
