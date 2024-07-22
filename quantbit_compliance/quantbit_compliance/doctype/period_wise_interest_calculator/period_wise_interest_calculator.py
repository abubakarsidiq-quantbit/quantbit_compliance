# Copyright (c) 2024, abub.patel@erpdata.in and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from datetime import date, datetime, timedelta

class PeriodWiseInterestCalculator(Document):
	@frappe.whitelist()
	def calculate_interest(self):
		if self.period == 'Custom':
			self.get_custom_interest()
		else:
			date_format = "%Y-%m-%d"
			start_date = datetime.strptime(self.date, date_format)
			self.interest_bifurcation.clear()
			if self.period == 'Quarterly':
				periods, duration = 4, 3
			elif self.period == 'Half Yearly':
				periods, duration = 2, 6
			elif self.period == 'Yearly':
				periods, duration = 1, 12
			else:
				frappe.throw("Select Valid Period")

			tot_days, tot_int_amount = 0, 0
			for _ in range(periods):
				end_date = self.calculate_end_date(start_date, duration)
				days = (end_date - start_date.date()).days
				interest_amount = self.amount * self.rate_of_interest * days / 365 / 100
				end_date = datetime.strptime(str(end_date), date_format)
				
				self.append('interest_bifurcation', {
					'start_date': start_date,
					'end_date': end_date - timedelta(days=1),
					'no_of_days': days,
					'rate_of_interest': self.rate_of_interest,
					'interest_amount': interest_amount
				})
				tot_int_amount += interest_amount
				tot_days += days
				start_date = end_date
			
			self.no_of_days = tot_days
			self.total_interest_amount = tot_int_amount

	def calculate_end_date(self, start_date, months):
		"""
		Calculate the end date based on the start date and the number of months.
		"""
		month = start_date.month - 1 + months
		year = start_date.year + month // 12
		month = month % 12 + 1
		day = min(start_date.day, [31, 29 if year % 4 == 0 and not year % 100 == 0 or year % 400 == 0 else 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31][month - 1])
		return date(year, month, day)

	def get_custom_interest(self):
		"""
		Calculate custom interest based on custom periods defined in interest_bifurcation.
		"""
		tot_days, tot_int_amount = 0, 0
		for i in self.interest_bifurcation:
			if not i.start_date or not i.end_date:
				frappe.throw("Select Custom Start And End Date In Child Table")
			date_format = "%Y-%m-%d"
			start_date = datetime.strptime(i.start_date, date_format)
			end_date = datetime.strptime(i.end_date, date_format)
			days = (end_date.date() - start_date.date()).days + 1
			i.no_of_days = days
			i.rate_of_interest = self.rate_of_interest
			i.interest_amount = self.amount * self.rate_of_interest * days / 365 / 100
			tot_int_amount += i.interest_amount
			tot_days += days
		
		self.no_of_days = tot_days
		self.total_interest_amount = tot_int_amount