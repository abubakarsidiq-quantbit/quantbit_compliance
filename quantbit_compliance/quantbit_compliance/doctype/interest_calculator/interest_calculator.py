import frappe
from frappe.model.document import Document

class InterestCalculator(Document):
    @frappe.whitelist()
    def get_chart(self):
        try:
            amount = self.amount
            period_months = self.period * 12
            monthly_rate = (self.rate / 100) / 12
            self.payment = self.calculate_pmt(monthly_rate, period_months, amount)
            balance = amount
            tot_int = tot_pri = 0
            self.interest_chart.clear()
            for month in range(1, int(period_months) + 1):
                interest = balance * monthly_rate
                principal = self.payment - interest
                ending_balance = balance - principal
                self.append('interest_chart', {
                    'month': month,
                    'beginning': balance,
                    'payment': self.payment,
                    'interest': interest,
                    'principal': principal,
                    'balance': ending_balance
                })
                tot_int += interest
                tot_pri += principal
                balance = ending_balance
            self.total_interest_amount = tot_int
            self.total_principal_amount = tot_pri

        except Exception as e:
            frappe.msgprint(f"Error generating interest chart: {str(e)}")
            frappe.log_error(message=str(e), title="Interest Chart Generation Error")
            
    def calculate_pmt(self,rate, nper, pv):
        if rate != 0:
            pmt = (rate * pv) / (1 - (1 + rate) ** -nper)
        else:
            pmt = pv / nper
        return pmt

