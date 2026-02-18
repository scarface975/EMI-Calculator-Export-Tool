from __future__ import annotations

import argparse
import csv
from dataclasses import dataclass
from typing import List, Dict, Iterable
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import tkinter.font as tkFont


def monthly_payment(principal: float, annual_rate_percent: float, n_months: int) -> float:
	"""Formula:
	  payment = P * r * (1+r)**n / ((1+r)**n - 1)
	"""
	if n_months <= 0:
		raise ValueError("n_months must be > 0")
	if principal == 0:
		return 0.0

	monthly_rate = annual_rate_percent / 100.0 / 12.0
	if monthly_rate == 0:
		return principal / n_months
	r = monthly_rate
	denom = (1 + r) ** n_months - 1
	payment = principal * r * (1 + r) ** n_months / denom
	return payment


def amortization_schedule(principal: float, annual_rate_percent: float, n_months: int) -> List[Dict]:
	payment = monthly_payment(principal, annual_rate_percent, n_months)
	balance = principal
	monthly_rate = annual_rate_percent / 100.0 / 12.0
	schedule: List[Dict] = []

	for m in range(1, n_months + 1):
		interest = balance * monthly_rate
		principal_paid = payment - interest
		# Handle final payment rounding: ensure balance doesn't go negative
		if principal_paid > balance:
			principal_paid = balance
			payment = interest + principal_paid
		balance = balance - principal_paid
		schedule.append({
			"month": m,
			"payment": round(payment, 10),
			"interest": round(interest, 10),
			"principal": round(principal_paid, 10),
			"balance": round(max(balance, 0.0), 10),
		})
	return schedule


def format_currency(value: float) -> str:
	return f"${value:,.2f}"


def print_schedule(schedule: Iterable[Dict]):
	header = f"{'Month':>5} {'Payment':>12} {'Interest':>12} {'Principal':>12} {'Balance':>14}"
	print(header)
	print("-" * len(header))
	for row in schedule:
		print(f"{row['month']:5d} {row['payment']:12,.2f} {row['interest']:12,.2f} {row['principal']:12,.2f} {row['balance']:14,.2f}")


def write_csv(schedule: Iterable[Dict], filename: str):
	fieldnames = ["month", "payment", "interest", "principal", "balance"]
	with open(filename, "w", newline="", encoding="utf-8") as f:
		writer = csv.DictWriter(f, fieldnames=fieldnames)
		writer.writeheader()
		for row in schedule:
			writer.writerow(row)


def parse_args():
	p = argparse.ArgumentParser(description="Loan amortization calculator")
	p.add_argument("-p", "--principal", type=float, required=True, help="Loan principal amount")
	p.add_argument("-r", "--rate", type=float, required=True, help="Annual interest rate (percent)")
	group = p.add_mutually_exclusive_group(required=True)
	group.add_argument("--years", type=float, help="Loan term in years (can be fractional)")
	group.add_argument("-m", "--months", type=int, help="Loan term in months")
	p.add_argument("--csv", type=str, help="Optional output CSV file for schedule")
	return p.parse_args()


def main():
	args = parse_args()
	principal = args.principal
	rate = args.rate
	if args.months:
		n_months = args.months
	else:
		n_months = int(round(args.years * 12))

	payment = monthly_payment(principal, rate, n_months)
	schedule = amortization_schedule(principal, rate, n_months)
	total_paid = sum(r["payment"] for r in schedule)
	total_interest = sum(r["interest"] for r in schedule)

	print(f"Loan amount: {format_currency(principal)}")
	print(f"Annual rate: {rate:.4g}%")
	print(f"Term: {n_months} months")
	print(f"Monthly payment: {format_currency(payment)}")
	print()
	print_schedule(schedule)
	print()
	print(f"Total paid:    {format_currency(total_paid)}")
	print(f"Total interest:{format_currency(total_interest)}")

	if args.csv:
		write_csv(schedule, args.csv)
		print(f"Schedule written to {args.csv}")


if __name__ == "__main__":
	# Create GUI
	root = tk.Tk()
	root.title("EMI Calculator & Export Tool")
	root.geometry("750x750")
	
	# Create main frame
	main_frame = ttk.Frame(root, padding="20")
	main_frame.pack(fill=tk.BOTH, expand=True)
	
	# Title
	title_font = tkFont.Font(family="Helvetica", size=14, weight="bold")
	title_label = ttk.Label(main_frame, text="Loan Eligibility & Amortization", font=title_font)
	title_label.pack(pady=(0, 20))
	
	# Input Frame
	input_frame = ttk.LabelFrame(main_frame, text="Loan Details", padding="15")
	input_frame.pack(fill=tk.X, pady=(0, 20))
	
	# Monthly Salary
	ttk.Label(input_frame, text="Monthly Salary (₹):").grid(row=0, column=0, sticky=tk.W, pady=8)
	salary_var = tk.StringVar(value="2000000")
	salary_entry = ttk.Entry(input_frame, textvariable=salary_var, width=30)
	salary_entry.grid(row=0, column=1, sticky=tk.EW, padx=10)
	
	# Loan Amount
	ttk.Label(input_frame, text="Loan Amount (₹):").grid(row=1, column=0, sticky=tk.W, pady=8)
	loan_var = tk.StringVar(value="20000000")
	loan_entry = ttk.Entry(input_frame, textvariable=loan_var, width=30)
	loan_entry.grid(row=1, column=1, sticky=tk.EW, padx=10)
	
	# Interest Rate
	ttk.Label(input_frame, text="Interest Rate (%):").grid(row=2, column=0, sticky=tk.W, pady=8)
	rate_var = tk.StringVar(value="10")
	rate_entry = ttk.Entry(input_frame, textvariable=rate_var, width=30)
	rate_entry.grid(row=2, column=1, sticky=tk.EW, padx=10)
	
	# Tenure
	ttk.Label(input_frame, text="Tenure (Years):").grid(row=3, column=0, sticky=tk.W, pady=8)
	tenure_var = tk.StringVar(value="10")
	tenure_entry = ttk.Entry(input_frame, textvariable=tenure_var, width=30)
	tenure_entry.grid(row=3, column=1, sticky=tk.EW, padx=10)
	
	input_frame.columnconfigure(1, weight=1)
	
	# Button Frame
	button_frame = ttk.Frame(main_frame)
	button_frame.pack(fill=tk.X, pady=10)
	
	# Calculate EMI Button
	def calculate_emi():
		try:
			salary = float(salary_var.get())
			principal = float(loan_var.get())
			rate = float(rate_var.get())
			tenure_years = float(tenure_var.get())
			n_months = int(round(tenure_years * 12))
			
			if principal <= 0 or rate < 0 or tenure_years <= 0 or salary <= 0:
				messagebox.showerror("Error", "Please enter valid positive values.")
				return
			
			payment = monthly_payment(principal, rate, n_months)
			emi_percentage = (payment / salary) * 100
			
			# Check if EMI is less than 50% of salary
			if payment > salary * 0.5:
				status_text = "NOT AFFORDABLE"
				status_color = "#d32f2f"
				result_text = f"Monthly EMI: ₹{payment:,.2f}\nStatus: {status_text} (EMI exceeds 50% of salary)"
			else:
				status_text = "SAFE (Affordable)"
				status_color = "#388e3c"
				result_text = f"Monthly EMI: ₹{payment:,.2f}\nStatus: {status_text}"
			
			# Update results
			result_label.config(text="Financial Analysis")
			emi_label.config(text=f"Monthly EMI: ₹{payment:,.2f}")
			status_label.config(text=f"Status: {status_text} ({emi_percentage:.1f}% of salary)", foreground=status_color)
			
			# Store schedule for view
			calculate_emi.schedule = amortization_schedule(principal, rate, n_months)
			calculate_emi.payment = payment
			calculate_emi.principal = principal
			calculate_emi.rate = rate
			calculate_emi.n_months = n_months
			
		except ValueError:
			messagebox.showerror("Error", "Please enter valid numeric values.")
	
	calculate_btn = ttk.Button(button_frame, text="Calculate EMI", command=calculate_emi)
	calculate_btn.pack(side=tk.LEFT, padx=5)
	
	# View Schedule Button
	def view_schedule():
		if not hasattr(calculate_emi, 'schedule'):
			messagebox.showwarning("Warning", "Please calculate EMI first.")
			return
		
		# Create new window
		schedule_win = tk.Toplevel(root)
		schedule_win.title("Amortization Schedule")
		schedule_win.geometry("900x600")
		
		# Create treeview
		columns = ("Month", "Payment", "Interest", "Principal", "Balance")
		tree = ttk.Treeview(schedule_win, columns=columns, height=20, show='headings')
		
		for col in columns:
			tree.column(col, width=150, anchor=tk.CENTER)
			tree.heading(col, text=col)
		
		# Add scrollbar
		scrollbar = ttk.Scrollbar(schedule_win, orient=tk.VERTICAL, command=tree.yview)
		tree.configure(yscroll=scrollbar.set)
		scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
		tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
		
		# Insert data
		for row in calculate_emi.schedule:
			tree.insert('', 'end', values=(
				row['month'],
				f"₹{row['payment']:,.2f}",
				f"₹{row['interest']:,.2f}",
				f"₹{row['principal']:,.2f}",
				f"₹{row['balance']:,.2f}"
			))
		
		# Summary frame
		summary_frame = ttk.Frame(schedule_win)
		summary_frame.pack(fill=tk.X, padx=10, pady=10)
		
		total_paid = sum(r["payment"] for r in calculate_emi.schedule)
		total_interest = sum(r["interest"] for r in calculate_emi.schedule)
		
		ttk.Label(summary_frame, text=f"Total Paid: ₹{total_paid:,.2f}", font=("Helvetica", 10, "bold")).pack(anchor=tk.W)
		ttk.Label(summary_frame, text=f"Total Interest: ₹{total_interest:,.2f}", font=("Helvetica", 10, "bold")).pack(anchor=tk.W)
	
	view_btn = ttk.Button(button_frame, text="View Schedule", command=view_schedule)
	view_btn.pack(side=tk.LEFT, padx=5)
	
	# Export CSV Button
	def export_csv():
		if not hasattr(calculate_emi, 'schedule'):
			messagebox.showwarning("Warning", "Please calculate EMI first.")
			return
		
		file_path = filedialog.asksaveasfilename(
			defaultextension=".csv",
			filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
			initialfile="loan_amortization.csv"
		)
		
		if file_path:
			write_csv(calculate_emi.schedule, file_path)
			messagebox.showinfo("Success", f"Schedule exported to:\n{file_path}")
	
	export_btn = ttk.Button(button_frame, text="Export CSV", command=export_csv)
	export_btn.pack(side=tk.LEFT, padx=5)
	
	# Clear Button
	def clear_fields():
		salary_var.set("2000000")
		loan_var.set("20000000")
		rate_var.set("10")
		tenure_var.set("10")
		result_label.config(text="")
		emi_label.config(text="")
		status_label.config(text="")
	
	clear_btn = ttk.Button(button_frame, text="Clear", command=clear_fields)
	clear_btn.pack(side=tk.LEFT, padx=5)
	
	# Results Frame
	result_frame = ttk.LabelFrame(main_frame, text="", padding="15")
	result_frame.pack(fill=tk.BOTH, expand=True, pady=10)
	
	result_label = ttk.Label(result_frame, text="", font=("Helvetica", 11, "bold"), foreground="#1976d2")
	result_label.pack(pady=(0, 10))
	
	emi_label = ttk.Label(result_frame, text="", font=("Helvetica", 18, "bold"))
	emi_label.pack(pady=10)
	
	status_label = ttk.Label(result_frame, text="", font=("Helvetica", 12))
	status_label.pack(pady=10)
	
	root.mainloop()
