import tkinter as tk
from tkinter import ttk
import sys
from datetime import datetime
from budget_data import *

class LoanCalculatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Lånekalkulator og Budsjettanalyse")
        self.root.geometry("1400x900")
        
        # Set window icon
        try:
            self.root.iconbitmap('app_icon.ico')
        except:
            pass  # Icon file not found, continue without it
        
        # Colors
        self.PRIMARY_COLOR = "#2E7D32"      # Green
        self.SECONDARY_COLOR = "#1565C0"    # Blue
        self.ACCENT_COLOR = "#F57C00"       # Orange
        
        # Data storage
        self.loan_data = None
        self.budget_data = None
        
        self.setup_style()
        self.setup_ui()
    
    def setup_style(self):
        style = ttk.Style()
        style.theme_use('clam')
        
        # Green header
        style.configure('Header.TFrame', background=self.PRIMARY_COLOR)
        style.configure('Header.TLabel', background=self.PRIMARY_COLOR, foreground='white', font=('Arial', 12, 'bold'))
        
        # Blue section
        style.configure('Blue.TFrame', background=self.SECONDARY_COLOR)
        style.configure('Blue.TLabel', background=self.SECONDARY_COLOR, foreground='white', font=('Arial', 10, 'bold'))
        
        # Orange section
        style.configure('Orange.TFrame', background=self.ACCENT_COLOR)
        style.configure('Orange.TLabel', background=self.ACCENT_COLOR, foreground='white', font=('Arial', 10, 'bold'))
    
    def setup_ui(self):
        # Main header
        header_frame = tk.Frame(self.root, bg=self.PRIMARY_COLOR, height=50)
        header_frame.pack(fill=tk.X)
        header_frame.pack_propagate(False)
        
        title = tk.Label(header_frame, text="Lånekalkulator og Husholdningsbudsjett", 
                        font=("Arial", 16, "bold"), bg=self.PRIMARY_COLOR, fg="white")
        title.pack(pady=10)
        
        # Main container
        main_container = ttk.Frame(self.root)
        main_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Left panel - Loan Calculator
        left_panel = ttk.Frame(main_container)
        left_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))
        
        self.setup_loan_panel(left_panel)
        
        # Right panel - Budget Calculator
        right_panel = ttk.Frame(main_container)
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(5, 0))
        
        self.setup_budget_panel(right_panel)
    
    def setup_loan_panel(self, parent):
        # Header
        header = tk.Frame(parent, bg=self.SECONDARY_COLOR, height=40)
        header.pack(fill=tk.X)
        header.pack_propagate(False)
        
        title = tk.Label(header, text="Lånekalkulator", font=("Arial", 12, "bold"),
                        bg=self.SECONDARY_COLOR, fg="white")
        title.pack(pady=10)
        
        # Input frame
        input_frame = ttk.Frame(parent)
        input_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Loan amount
        ttk.Label(input_frame, text="Lånebeløp (kr):").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.loan_amount = ttk.Entry(input_frame, width=15)
        self.loan_amount.grid(row=0, column=1, pady=5, padx=5)
        self.loan_amount.insert(0, "3000000")
        
        # Interest rate
        ttk.Label(input_frame, text="Rentesats (% p.a.):").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.interest_rate = ttk.Entry(input_frame, width=15)
        self.interest_rate.grid(row=1, column=1, pady=5, padx=5)
        self.interest_rate.insert(0, "4.5")
        
        # Loan period
        ttk.Label(input_frame, text="Låneperiode (år):").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.loan_years = ttk.Entry(input_frame, width=15)
        self.loan_years.grid(row=2, column=1, pady=5, padx=5)
        self.loan_years.insert(0, "20")
        
        # Grace period
        ttk.Label(input_frame, text="Avdragsfrihet (mnd):").grid(row=3, column=0, sticky=tk.W, pady=5)
        self.grace_period = ttk.Entry(input_frame, width=15)
        self.grace_period.grid(row=3, column=1, pady=5, padx=5)
        self.grace_period.insert(0, "0")
        
        # Term fee
        ttk.Label(input_frame, text="Etableringsgebyr (kr):").grid(row=4, column=0, sticky=tk.W, pady=5)
        self.term_fee = ttk.Entry(input_frame, width=15)
        self.term_fee.grid(row=4, column=1, pady=5, padx=5)
        self.term_fee.insert(0, "2500")
        
        # Monthly fee (Termingebyr)
        ttk.Label(input_frame, text="Termingebyr (kr/mnd):").grid(row=5, column=0, sticky=tk.W, pady=5)
        self.monthly_fee = ttk.Entry(input_frame, width=15)
        self.monthly_fee.grid(row=5, column=1, pady=5, padx=5)
        self.monthly_fee.insert(0, "0")
        
        # Extra payment
        ttk.Label(input_frame, text="Ekstra betaling/år (kr):").grid(row=6, column=0, sticky=tk.W, pady=5)
        self.extra_payment = ttk.Entry(input_frame, width=15)
        self.extra_payment.grid(row=6, column=1, pady=5, padx=5)
        self.extra_payment.insert(0, "0")
        
        # Bind changes
        self.loan_amount.bind("<KeyRelease>", lambda e: self.calculate_loan())
        self.interest_rate.bind("<KeyRelease>", lambda e: self.calculate_loan())
        self.loan_years.bind("<KeyRelease>", lambda e: self.calculate_loan())
        self.grace_period.bind("<KeyRelease>", lambda e: self.calculate_loan())
        self.term_fee.bind("<KeyRelease>", lambda e: self.calculate_loan())
        self.monthly_fee.bind("<KeyRelease>", lambda e: self.calculate_loan())
        self.extra_payment.bind("<KeyRelease>", lambda e: self.calculate_loan())
        
        # Results frame
        results_frame = tk.Frame(parent, bg="#F5F5F5", relief=tk.SUNKEN, bd=1)
        results_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        tk.Label(results_frame, text="RESULTATER", font=("Arial", 10, "bold"),
                bg="#F5F5F5").pack(anchor=tk.W, padx=10, pady=(10, 5))
        
        self.result_monthly = tk.Label(results_frame, text="Månedsrate: 0 kr", font=("Arial", 9),
                                      bg="#F5F5F5", fg="#333")
        self.result_monthly.pack(anchor=tk.W, padx=20)
        
        self.result_interest = tk.Label(results_frame, text="Totale renter: 0 kr", font=("Arial", 9),
                                       bg="#F5F5F5", fg="#333")
        self.result_interest.pack(anchor=tk.W, padx=20)
        
        self.result_duration = tk.Label(results_frame, text="Løpetid: 0 år", font=("Arial", 9),
                                       bg="#F5F5F5", fg="#333")
        self.result_duration.pack(anchor=tk.W, padx=20)
        
        self.result_saved = tk.Label(results_frame, text="Sparing med ekstra bet.: 0 kr", font=("Arial", 9),
                                    bg="#F5F5F5", fg="#333")
        self.result_saved.pack(anchor=tk.W, padx=20)
        
        # Buttons
        button_frame = ttk.Frame(parent)
        button_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Button(button_frame, text="Nedbetalingsplan", 
                  command=self.show_repayment_plan).pack(side=tk.LEFT, padx=5)
        
        # Initial calculation
        self.calculate_loan()
    
    def setup_budget_panel(self, parent):
        # Create main container with two halves
        left_half = ttk.Frame(parent)
        left_half.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(5, 2.5))
        
        # Header
        header = tk.Frame(left_half, bg=self.ACCENT_COLOR, height=40)
        header.pack(fill=tk.X)
        header.pack_propagate(False)
        
        title = tk.Label(header, text="Husholdningsbudsjett", font=("Arial", 12, "bold"),
                        bg=self.ACCENT_COLOR, fg="white")
        title.pack(pady=10)
        
        # Create a canvas with scrollbar for all content
        canvas = tk.Canvas(left_half, bg="white", highlightthickness=0)
        scrollbar = ttk.Scrollbar(left_half, orient=tk.VERTICAL, command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Pack canvas and scrollbar
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y, pady=5)
        
        # Enable scrolling with mouse wheel
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        canvas.bind_all("<MouseWheel>", _on_mousewheel)
        
        input_frame = scrollable_frame
        
        # Income section with background color
        income_frame = tk.Frame(input_frame, bg="#E3F2FD", relief=tk.FLAT)
        income_frame.grid(row=0, column=0, columnspan=6, sticky="ew", padx=5, pady=5)
        
        ttk.Label(income_frame, text="Inntekt og skatt", font=("Arial", 10, "bold"), background="#E3F2FD").pack(anchor=tk.W, padx=10, pady=(5, 2))
        
        inner_frame = ttk.Frame(income_frame)
        inner_frame.pack(padx=10, pady=(2, 10), fill=tk.X)
        
        ttk.Label(inner_frame, text="Bruttoinntekt/mnd (kr):").grid(row=0, column=0, sticky=tk.W, pady=3)
        self.monthly_income = ttk.Entry(inner_frame, width=15)
        self.monthly_income.grid(row=0, column=1, pady=3, padx=5)
        self.monthly_income.insert(0, "60000")
        self.monthly_income.bind("<KeyRelease>", lambda e: self.calculate_budget())
        
        ttk.Label(inner_frame, text="Skattevalg:").grid(row=1, column=0, sticky=tk.W, pady=3)
        self.tax_mode = tk.StringVar(value="percent")
        tax_frame = ttk.Frame(inner_frame)
        tax_frame.grid(row=1, column=1, sticky=tk.W, padx=5)
        ttk.Radiobutton(tax_frame, text="% av inntekt", variable=self.tax_mode, 
                       value="percent", command=self.toggle_tax_mode).pack(side=tk.LEFT)
        ttk.Radiobutton(tax_frame, text="Fast beløp", variable=self.tax_mode, 
                       value="fixed", command=self.toggle_tax_mode).pack(side=tk.LEFT, padx=10)
        
        ttk.Label(inner_frame, text="Skatt (%):").grid(row=2, column=0, sticky=tk.W, pady=3)
        self.tax_input = ttk.Entry(inner_frame, width=15)
        self.tax_input.grid(row=2, column=1, pady=3, padx=5)
        self.tax_input.insert(0, "22")
        self.tax_input.bind("<KeyRelease>", lambda e: self.calculate_budget())
        
        # Adults section with background color
        adults_frame = tk.Frame(input_frame, bg="#F3E5F5", relief=tk.FLAT)
        adults_frame.grid(row=1, column=0, columnspan=6, sticky="ew", padx=5, pady=5)
        
        ttk.Label(adults_frame, text="Voksne", font=("Arial", 10, "bold"), background="#F3E5F5").pack(anchor=tk.W, padx=10, pady=(5, 2))
        
        inner_frame = ttk.Frame(adults_frame)
        inner_frame.pack(padx=10, pady=(2, 10), fill=tk.X)
        
        ttk.Label(inner_frame, text="Voksen 1 - Kjønn:").grid(row=0, column=0, sticky=tk.W, pady=3)
        self.adult1_gender = ttk.Combobox(inner_frame, values=["Kvinne", "Mann"], width=12, state="readonly")
        self.adult1_gender.grid(row=0, column=1, pady=3, padx=5)
        self.adult1_gender.set("Kvinne")
        self.adult1_gender.bind("<<ComboboxSelected>>", lambda e: self.calculate_budget())
        
        ttk.Label(inner_frame, text="Voksen 1 - Alder:").grid(row=1, column=0, sticky=tk.W, pady=3)
        self.adult1_age = ttk.Combobox(inner_frame, values=["18-30", "31-60", "61-74", "74+"], width=12, state="readonly")
        self.adult1_age.grid(row=1, column=1, pady=3, padx=5)
        self.adult1_age.set("31-60")
        self.adult1_age.bind("<<ComboboxSelected>>", lambda e: self.calculate_budget())
        
        ttk.Label(inner_frame, text="Voksen 2 - Kjønn:").grid(row=2, column=0, sticky=tk.W, pady=3)
        self.adult2_gender = ttk.Combobox(inner_frame, values=["Ingen", "Kvinne", "Mann"], width=12, state="readonly")
        self.adult2_gender.grid(row=2, column=1, pady=3, padx=5)
        self.adult2_gender.set("Ingen")
        self.adult2_gender.bind("<<ComboboxSelected>>", lambda e: self.calculate_budget())
        
        ttk.Label(inner_frame, text="Voksen 2 - Alder:").grid(row=3, column=0, sticky=tk.W, pady=3)
        self.adult2_age = ttk.Combobox(inner_frame, values=["18-30", "31-60", "61-74", "74+"], width=12, state="readonly")
        self.adult2_age.grid(row=3, column=1, pady=3, padx=5)
        self.adult2_age.set("31-60")
        self.adult2_age.bind("<<ComboboxSelected>>", lambda e: self.calculate_budget())
        
        # Children section with background color - all on one line
        children_frame = tk.Frame(input_frame, bg="#E8F5E9", relief=tk.FLAT)
        children_frame.grid(row=2, column=0, columnspan=6, sticky="ew", padx=5, pady=5)
        
        ttk.Label(children_frame, text="Barn (alle på samme linje)", font=("Arial", 10, "bold"), background="#E8F5E9").pack(anchor=tk.W, padx=10, pady=(5, 2))
        
        # Store children inputs in lists
        self.children_gender = []
        self.children_age = []
        
        # Create inputs for 6 children - all on one line in child_contents
        child_contents = ttk.Frame(children_frame)
        child_contents.pack(padx=10, pady=(2, 10), fill=tk.X)
        
        age_options = ["6-11 mnd", "1 år", "2-5", "6-9", "10-13", "14-17"]
        
        for i in range(6):
            child_col_frame = tk.Frame(child_contents, bg="#E8F5E9")
            child_col_frame.pack(side=tk.LEFT, padx=3, fill=tk.X, expand=True)
            
            # Child header
            ttk.Label(child_col_frame, text=f"Barn {i+1}:", font=("Arial", 8, "bold"), background="#E8F5E9").pack(anchor=tk.W, pady=(0, 3))
            
            # Gender
            ttk.Label(child_col_frame, text="Kjønn:", font=("Arial", 8)).pack(anchor=tk.W, pady=(2, 1))
            child_gender = ttk.Combobox(child_col_frame, values=["Ingen", "Gutt", "Jente"], width=9, state="readonly")
            child_gender.pack(fill=tk.X, pady=(0, 3))
            child_gender.set("Ingen")
            child_gender.bind("<<ComboboxSelected>>", lambda e: self.calculate_budget())
            self.children_gender.append(child_gender)
            
            # Age
            ttk.Label(child_col_frame, text="Alder:", font=("Arial", 8)).pack(anchor=tk.W, pady=(2, 1))
            child_age = ttk.Combobox(child_col_frame, values=age_options, width=9, state="readonly")
            child_age.pack(fill=tk.X)
            child_age.set("2-5")
            child_age.bind("<<ComboboxSelected>>", lambda e: self.calculate_budget())
            self.children_age.append(child_age)
        
        # Housing and car section
        other_frame = tk.Frame(input_frame, bg="#FFF3E0", relief=tk.FLAT)
        other_frame.grid(row=3, column=0, columnspan=6, sticky="ew", padx=5, pady=5)
        
        ttk.Label(other_frame, text="Bolig og kjøretøy", font=("Arial", 10, "bold"), background="#FFF3E0").pack(anchor=tk.W, padx=10, pady=(5, 2))
        
        inner_frame = ttk.Frame(other_frame)
        inner_frame.pack(padx=10, pady=(2, 10), fill=tk.X)
        
        ttk.Label(inner_frame, text="Bokostnader/mnd (kr):").grid(row=0, column=0, sticky=tk.W, pady=3)
        self.housing_costs = ttk.Entry(inner_frame, width=15)
        self.housing_costs.grid(row=0, column=1, pady=3, padx=5)
        self.housing_costs.insert(0, "4500")
        self.housing_costs.bind("<KeyRelease>", lambda e: self.calculate_budget())
        
        ttk.Label(inner_frame, text="Antall biler:").grid(row=1, column=0, sticky=tk.W, pady=3)
        self.num_cars = ttk.Combobox(inner_frame, values=["0", "1", "2", "3", "4", "5"], width=12, state="readonly")
        self.num_cars.grid(row=1, column=1, pady=3, padx=5)
        self.num_cars.set("1")
        self.num_cars.bind("<<ComboboxSelected>>", lambda e: self.update_car_inputs())
        
        # Car type inputs - will be created dynamically
        self.car_type_inputs = []
        self.car_type_frame = ttk.Frame(inner_frame)
        self.car_type_frame.grid(row=2, column=0, columnspan=2, sticky="ew", pady=(5, 0))
        
        # Initial car input
        self.update_car_inputs()
        
        # Separator
        ttk.Separator(input_frame, orient=tk.HORIZONTAL).grid(row=4, column=0, columnspan=6, sticky="ew", pady=10)
        
        # Results frame - inside the scrollable area with bright color
        results_frame = tk.Frame(input_frame, bg="#C8E6C9", relief=tk.SUNKEN, bd=2)
        results_frame.grid(row=5, column=0, columnspan=6, sticky="ew", padx=5, pady=10)
        
        tk.Label(results_frame, text="RESULTATER", font=("Arial", 11, "bold"),
                bg="#C8E6C9", fg="#1B5E20").pack(anchor=tk.W, padx=10, pady=(10, 5))
        
        self.result_net_income = tk.Label(results_frame, text="Netto inntekt: 0 kr", font=("Arial", 9),
                                         bg="#C8E6C9", fg="#1B5E20")
        self.result_net_income.pack(anchor=tk.W, padx=20, pady=2)
        
        self.result_total_expenses = tk.Label(results_frame, text="Totale utgifter: 0 kr", font=("Arial", 9),
                                             bg="#C8E6C9", fg="#1B5E20")
        self.result_total_expenses.pack(anchor=tk.W, padx=20, pady=2)
        
        self.result_surplus = tk.Label(results_frame, text="Overskudd/mnd: 0 kr", font=("Arial", 9),
                                      bg="#C8E6C9", fg="#1B5E20")
        self.result_surplus.pack(anchor=tk.W, padx=20, pady=2)
        
        self.result_surplus_yearly = tk.Label(results_frame, text="Overskudd/år: 0 kr", font=("Arial", 9),
                                             bg="#C8E6C9", fg="#1B5E20")
        self.result_surplus_yearly.pack(anchor=tk.W, padx=20, pady=(2, 10))
        
        # Buttons - outside scrollable area
        button_frame = ttk.Frame(left_half)
        button_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Button(button_frame, text="Detaljert budsjett", 
                  command=self.show_budget).pack(side=tk.LEFT, padx=2.5)
        ttk.Button(button_frame, text="Budsjettgraf", 
                  command=self.show_budget_chart).pack(side=tk.LEFT, padx=2.5)
        
        # Right half - placeholder for future features
        right_half = tk.Frame(parent, bg="#F5F5F5")
        right_half.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(2.5, 5))
        
        ttk.Label(right_half, text="", background="#F5F5F5").pack()
        
        # Initial calculation
        self.calculate_budget()
    
    def update_car_inputs(self):
        """Update car type inputs based on number of cars selected"""
        # Clear existing widgets
        for widget in self.car_type_frame.winfo_children():
            widget.destroy()
        self.car_type_inputs = []
        
        num_cars = int(self.num_cars.get())
        
        if num_cars > 0:
            for i in range(num_cars):
                ttk.Label(self.car_type_frame, text=f"Bil {i+1}:").grid(row=i, column=0, sticky=tk.W, pady=3, padx=(0, 5))
                car_type = ttk.Combobox(self.car_type_frame, values=["Bensinbil", "El-bil"], width=12, state="readonly")
                car_type.grid(row=i, column=1, sticky=tk.W, pady=3, padx=5)
                car_type.set("Bensinbil")
                car_type.bind("<<ComboboxSelected>>", lambda e: self.calculate_budget())
                self.car_type_inputs.append(car_type)
        
        self.calculate_budget()
    
    def get_float(self, entry):
        try:
            val = entry.get().replace(",", ".")
            return float(val) if val else 0
        except:
            return 0
    
    def format_currency(self, value):
        return f"{value:,.0f}".replace(",", " ").replace(".", ",")
    
    def calculate_loan(self):
        try:
            loan_amount = self.get_float(self.loan_amount)
            interest_rate = self.get_float(self.interest_rate)
            loan_years = self.get_float(self.loan_years)
            grace_period = int(self.get_float(self.grace_period))
            term_fee = self.get_float(self.term_fee)
            monthly_fee = self.get_float(self.monthly_fee)
            extra_payment = self.get_float(self.extra_payment) / 12
            
            if loan_amount <= 0 or interest_rate <= 0 or loan_years <= 0:
                return
            
            monthly_rate = interest_rate / 100 / 12
            planned_months = int(loan_years * 12)
            
            # Calculate monthly payment WITHOUT grace period (for comparison)
            if monthly_rate > 0:
                monthly_payment_no_grace = (loan_amount * monthly_rate * (1 + monthly_rate) ** planned_months) / \
                                 ((1 + monthly_rate) ** planned_months - 1)
            else:
                monthly_payment_no_grace = loan_amount / planned_months
            
            # Calculate monthly payment WITH grace period
            if grace_period > 0:
                payment_months = planned_months - grace_period
                balance_after_grace = loan_amount
                for month in range(1, grace_period + 1):
                    balance_after_grace = balance_after_grace * (1 + monthly_rate)
                
                if payment_months > 0 and monthly_rate > 0:
                    monthly_payment_with_grace = (balance_after_grace * monthly_rate * (1 + monthly_rate) ** payment_months) / \
                                      ((1 + monthly_rate) ** payment_months - 1)
                else:
                    monthly_payment_with_grace = balance_after_grace / max(payment_months, 1)
            else:
                monthly_payment_with_grace = monthly_payment_no_grace
            
            # Build payment schedule
            schedule = self.build_payment_schedule(
                loan_amount, monthly_rate, planned_months, term_fee, 
                monthly_fee, extra_payment, grace_period
            )
            
            self.loan_data = {
                'loan_amount': loan_amount,
                'interest_rate': interest_rate,
                'monthly_payment_base': monthly_payment_no_grace,
                'monthly_payment_grace': monthly_payment_with_grace,
                'grace_period': grace_period,
                'total_interest': schedule['total_interest'],
                'total_gebyrer': schedule['total_gebyrer'],
                'actual_months': len(schedule['payments']),
                'planned_months': planned_months,
                'schedule': schedule,
                'monthly_loan_payment': monthly_payment_with_grace + monthly_fee  # for budget integration
            }
            
            self.update_loan_display()
            self.calculate_budget()  # Update budget when loan changes
        except Exception as e:
            pass
    
    def build_payment_schedule(self, total_loan, monthly_rate, planned_months, term_fee, 
                              monthly_fee, extra_payment, grace_period=0):
        balance = total_loan
        payments = []
        year_count = 1
        month_in_year = 1
        
        # Calculate the payment months (after grace period)
        payment_months = planned_months - grace_period
        
        # Recalculate monthly payment considering grace period
        # During grace period, balance grows with interest
        balance_after_grace = total_loan
        for month in range(1, grace_period + 1):
            balance_after_grace = balance_after_grace * (1 + monthly_rate)
        
        # Now calculate the monthly payment for the remaining months
        if payment_months > 0 and monthly_rate > 0:
            monthly_payment_base = (balance_after_grace * monthly_rate * (1 + monthly_rate) ** payment_months) / \
                                  ((1 + monthly_rate) ** payment_months - 1)
        else:
            monthly_payment_base = balance_after_grace / max(payment_months, 1)
        
        balance = total_loan
        
        for month in range(1, planned_months + 1):
            interest = balance * monthly_rate
            
            # Establishment fee only on first month (month 1), always
            establishment_fee = term_fee if month == 1 else 0
            
            if month <= grace_period:
                # During grace period: only interest and establishment fee accrues, no principal payment
                principal = 0
                total_payment = interest + establishment_fee + monthly_fee
            else:
                # After grace period: normal amortization
                principal = min(monthly_payment_base + extra_payment - interest, balance)
                principal = max(0, principal)
                
                # Monthly fee is added every month
                total_payment = principal + interest + establishment_fee + monthly_fee
            
            balance = max(0, balance - principal)
            
            payments.append({
                'month': month_in_year,
                'year': year_count,
                'principal': principal,
                'interest': interest,
                'establishment_fee': establishment_fee,
                'monthly_fee': monthly_fee,
                'total': total_payment,
                'balance': balance
            })
            
            if balance <= 0:
                break
            
            month_in_year += 1
            if month_in_year > 12:
                month_in_year = 1
                year_count += 1
        
        # Calculate total gebyrer
        total_gebyrer = term_fee + sum(p['monthly_fee'] for p in payments)
        
        return {
            'payments': payments,
            'total_interest': sum(p['interest'] for p in payments),
            'total_gebyrer': total_gebyrer,
            'interest_saved': 0  # Will be calculated separately
        }
    
    def calculate_total_interest(self, loan, rate, months, extra):
        balance = loan
        total_interest = 0
        monthly_payment = (loan * rate * (1 + rate) ** months) / ((1 + rate) ** months - 1)
        
        for _ in range(months):
            interest = balance * rate
            principal = min(monthly_payment + extra - interest, balance)
            total_interest += interest
            balance -= principal
            if balance <= 0:
                break
        
        return total_interest
    
    def update_loan_display(self):
        """Update the loan results display with all required information"""
        monthly_base = self.loan_data['monthly_payment_base']
        monthly_grace = self.loan_data['monthly_payment_grace']
        grace = self.loan_data['grace_period']
        total_interest = self.loan_data['total_interest']
        total_gebyrer = self.loan_data['total_gebyrer']
        planned_months = self.loan_data['planned_months']
        
        # Calculate duration
        years = planned_months // 12
        remaining = planned_months % 12
        if years > 0 and remaining > 0:
            duration_text = f"Løpetid: {years} år {remaining} mnd"
        elif years > 0:
            duration_text = f"Løpetid: {years} år"
        else:
            duration_text = f"Løpetid: {remaining} mnd"
        
        # Update result labels
        if grace > 0:
            # Show both terminbeløp on separate lines (no extra indentation)
            text = f"Terminbeløp: {self.format_currency(monthly_base)} kr (uten avdragsfrihet)\n"
            text += f"Terminbeløp: {self.format_currency(monthly_grace)} kr (med {grace} mnd avdragsfrihet)"
            self.result_monthly.config(text=text, justify=tk.LEFT)
        else:
            self.result_monthly.config(text=f"Terminbeløp: {self.format_currency(monthly_base)} kr")
        
        self.result_interest.config(text=f"Totale renter: {self.format_currency(total_interest)} kr")
        self.result_duration.config(text=f"Total gebyrer: {self.format_currency(total_gebyrer)} kr")
        self.result_saved.config(text=duration_text)
    
    def toggle_tax_mode(self):
        self.calculate_budget()
    
    def calculate_budget(self):
        try:
            monthly_income = self.get_float(self.monthly_income)
            tax_input = self.get_float(self.tax_input)
            
            # Calculate tax based on mode
            if self.tax_mode.get() == "percent":
                monthly_tax = monthly_income * (tax_input / 100)
            else:
                monthly_tax = tax_input
            
            net_income = monthly_income - monthly_tax
            housing_costs = self.get_float(self.housing_costs)
            
            # Count household members
            num_adults = 1  # Always at least 1
            if self.adult2_gender.get() != "Ingen":
                num_adults += 1
            
            # Count all children (from 0-5 children inputs)
            num_children = 0
            for child_gender in self.children_gender:
                if child_gender.get() != "Ingen":
                    num_children += 1
            
            total_persons = num_adults + num_children
            
            # Calculate individual expenses
            individual_expenses = {'mat': 0, 'klaer': 0, 'pleie': 0, 'lek': 0, 'reise': 0}
            
            # Adult 1
            gender1 = "K" if self.adult1_gender.get() == "Kvinne" else "M"
            age1 = self.adult1_age.get()
            mat_key1 = f"{gender1} {age1}"
            if mat_key1 not in MAT_BUDGET:
                mat_key1 = f"{gender1} 18-30"
            
            individual_expenses['mat'] += MAT_BUDGET.get(mat_key1, 4000)
            individual_expenses['klaer'] += KLAER_BUDGET.get(f"{gender1} >17", 1070)
            individual_expenses['pleie'] += get_pleie_budget(age1, gender1)
            individual_expenses['reise'] += REISE_BUDGET.get("20-66", 985)
            
            # Adult 2
            if self.adult2_gender.get() != "Ingen":
                gender2 = "K" if self.adult2_gender.get() == "Kvinne" else "M"
                age2 = self.adult2_age.get()
                mat_key2 = f"{gender2} {age2}"
                if mat_key2 not in MAT_BUDGET:
                    mat_key2 = f"{gender2} 18-30"
                
                individual_expenses['mat'] += MAT_BUDGET.get(mat_key2, 4000)
                individual_expenses['klaer'] += KLAER_BUDGET.get(f"{gender2} >17", 1070)
                individual_expenses['pleie'] += get_pleie_budget(age2, gender2)
                individual_expenses['reise'] += REISE_BUDGET.get("20-66", 985)
            
            # Children (loop through all child inputs)
            for i, (child_gender_combo, child_age_combo) in enumerate(zip(self.children_gender, self.children_age)):
                if child_gender_combo.get() != "Ingen":
                    child_gender = "G" if child_gender_combo.get() == "Jente" else "J"
                    child_age = child_age_combo.get()
                    
                    individual_expenses['mat'] += MAT_BUDGET.get(child_age, 2500)
                    
                    if child_age in ["<1 år", "1 år", "2-5", "6-9"]:
                        individual_expenses['klaer'] += KLAER_BUDGET.get(child_age, 800)
                    else:
                        individual_expenses['klaer'] += KLAER_BUDGET.get(f"{child_gender} {child_age}", 900)
                    
                    individual_expenses['pleie'] += get_pleie_budget(child_age, "K")
                    individual_expenses['lek'] += get_lek_budget(child_age)
            
            # Household expenses
            household_size = get_household_size_category(total_persons)
            household_expenses = {
                'andre_dagligvarer': ANDRE_DAGLIGVARER.get(household_size, 600),
                'husholdningsartikler': HUSHOLDNINGSARTIKLER.get(household_size, 700),
                'mobler': MOBLER.get(household_size, 700),
                'mediebruk_fritid': MEDIEBRUK_FRITID.get(household_size, 2600)
            }
            
            # Car costs - calculate based on individual car types
            car_cost = 0
            num_cars = int(self.num_cars.get())
            
            if num_cars > 0 and len(self.car_type_inputs) == num_cars:
                size_category = "1-4 personer" if total_persons <= 4 else "5-7 personer"
                
                for car_type_combo in self.car_type_inputs:
                    car_type = car_type_combo.get()
                    if car_type == "Bensinbil":
                        car_cost += BILKOSTNADER["Bensinbil"].get(size_category, 3300)
                    else:  # El-bil
                        car_cost += BILKOSTNADER["El-bil"].get(size_category, 2195)
            
            # Monthly loan payment (use grace period payment if grace period is set)
            if self.loan_data:
                grace_period = self.loan_data.get('grace_period', 0)
                monthly_loan_payment = self.loan_data['monthly_payment_grace'] if grace_period > 0 else self.loan_data['monthly_payment_base']
                # Add monthly fee (termingebyr) to the payment
                monthly_fee = self.get_float(self.monthly_fee)
                monthly_loan_payment += monthly_fee
            else:
                monthly_loan_payment = 0
            
            # Total expenses
            individual_sum = sum(individual_expenses.values())
            household_sum = sum(household_expenses.values())
            total_expenses = individual_sum + household_sum + housing_costs + car_cost + monthly_loan_payment
            
            liquidity_surplus = net_income - total_expenses
            liquidity_surplus_yearly = liquidity_surplus * 12
            
            self.budget_data = {
                'monthly_income': monthly_income,
                'monthly_tax': monthly_tax,
                'net_income': net_income,
                'individual_expenses': individual_expenses,
                'household_expenses': household_expenses,
                'housing_costs': housing_costs,
                'car_cost': car_cost,
                'monthly_loan_payment': monthly_loan_payment,
                'total_expenses': total_expenses,
                'liquidity_surplus': liquidity_surplus,
                'liquidity_surplus_yearly': liquidity_surplus_yearly,
                'total_persons': total_persons,
                'num_adults': num_adults,
                'num_children': num_children
            }
            
            self.update_budget_display()
        except Exception as e:
            print(f"Budsjett-feil: {e}")
            import traceback
            traceback.print_exc()
    
    def update_budget_display(self):
        if not self.budget_data:
            return
        
        self.result_net_income.config(text=f"Netto inntekt: {self.format_currency(self.budget_data['net_income'])} kr")
        self.result_total_expenses.config(text=f"Totale utgifter: {self.format_currency(self.budget_data['total_expenses'])} kr")
        
        surplus = self.budget_data['liquidity_surplus']
        color = "#2E7D32" if surplus >= 0 else "#D32F2F"
        self.result_surplus.config(text=f"Overskudd/mnd: {self.format_currency(surplus)} kr", fg=color)
        self.result_surplus_yearly.config(text=f"Overskudd/år: {self.format_currency(self.budget_data['liquidity_surplus_yearly'])} kr", fg=color)
    
    def show_repayment_plan(self):
        if not self.loan_data:
            return
        
        plan_window = tk.Toplevel(self.root)
        plan_window.title("Nedbetalingsplan")
        plan_window.geometry("1400x950")
        
        # Header
        header = tk.Frame(plan_window, bg=self.SECONDARY_COLOR, height=50)
        header.pack(fill=tk.X)
        header.pack_propagate(False)
        
        title = tk.Label(header, text="Nedbetalingsplan og Avdrag/Renter fordeling", font=("Arial", 14, "bold"),
                        bg=self.SECONDARY_COLOR, fg="white")
        title.pack(pady=15)
        
        # Create notebook (tabs)
        notebook = ttk.Notebook(plan_window)
        notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Tab 1: Detailed table
        tab1 = ttk.Frame(notebook)
        notebook.add(tab1, text="Detaljert tabell")
        
        # Create frame with scrollbar for tab 1
        container = ttk.Frame(tab1)
        container.pack(fill=tk.BOTH, expand=True)
        
        scrollbar = ttk.Scrollbar(container)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Tree view with professional styling
        style = ttk.Style()
        style.configure('Treeview', rowheight=25, font=("Arial", 9))
        style.configure('Treeview.Heading', font=("Arial", 9, "bold"))
        
        tree = ttk.Treeview(container, columns=("Måned", "Avdrag", "Renter", "Etab.gebyr", "Term.gebyr", "Totalt", "Restgjeld"), 
                           yscrollcommand=scrollbar.set, height=30)
        scrollbar.config(command=tree.yview)
        tree.pack(fill=tk.BOTH, expand=True)
        
        tree.column("#0", width=0, stretch=tk.NO)
        tree.column("Måned", anchor=tk.W, width=100)
        tree.column("Avdrag", anchor=tk.E, width=120)
        tree.column("Renter", anchor=tk.E, width=120)
        tree.column("Etab.gebyr", anchor=tk.E, width=110)
        tree.column("Term.gebyr", anchor=tk.E, width=110)
        tree.column("Totalt", anchor=tk.E, width=130)
        tree.column("Restgjeld", anchor=tk.E, width=130)
        
        tree.heading("#0", text="")
        for col in ["Måned", "Avdrag", "Renter", "Etab.gebyr", "Term.gebyr", "Totalt", "Restgjeld"]:
            tree.heading(col, text=col)
        
        # Aggregate payments by year
        yearly_data = {}
        for payment in self.loan_data['schedule']['payments']:
            year = payment['year']
            if year not in yearly_data:
                yearly_data[year] = {
                    'principal': 0, 'interest': 0, 'establishment_fee': 0, 'monthly_fee': 0, 
                    'total': 0, 'months': []
                }
            yearly_data[year]['principal'] += payment['principal']
            yearly_data[year]['interest'] += payment['interest']
            yearly_data[year]['establishment_fee'] += payment['establishment_fee']
            yearly_data[year]['monthly_fee'] += payment['monthly_fee']
            yearly_data[year]['total'] += payment['total']
            yearly_data[year]['months'].append(payment)
        
        # Add Year 1 monthly details first
        if 1 in yearly_data:
            tree.insert("", "end", values=("År 1 - Månedlig oversikt", "", "", "", "", "", ""), open=True)
            for payment in yearly_data[1]['months']:
                tree.insert("", "end", values=(
                    f"  Mnd {payment['month']}",
                    self.format_currency(payment['principal']),
                    self.format_currency(payment['interest']),
                    self.format_currency(payment['establishment_fee']),
                    self.format_currency(payment['monthly_fee']),
                    self.format_currency(payment['total']),
                    self.format_currency(payment['balance'])
                ))
            
            # Add Year 1 summary
            tree.insert("", "end", values=(
                "År 1 - TOTALT",
                self.format_currency(yearly_data[1]['principal']),
                self.format_currency(yearly_data[1]['interest']),
                self.format_currency(yearly_data[1]['establishment_fee']),
                self.format_currency(yearly_data[1]['monthly_fee']),
                self.format_currency(yearly_data[1]['total']),
                ""
            ))
        
        # Add remaining years as collapsible summaries
        for year in sorted(yearly_data.keys()):
            if year == 1:
                continue
            
            data = yearly_data[year]
            # Get last month balance from this year
            last_balance = data['months'][-1]['balance'] if data['months'] else 0
            
            year_id = tree.insert("", "end", values=(
                f"År {year} - TOTALT (Klikk for detaljer)",
                self.format_currency(data['principal']),
                self.format_currency(data['interest']),
                self.format_currency(data['establishment_fee']),
                self.format_currency(data['monthly_fee']),
                self.format_currency(data['total']),
                self.format_currency(last_balance)
            ), open=False)
            
            # Add expandable monthly details
            for payment in data['months']:
                tree.insert(year_id, "end", values=(
                    f"  Mnd {payment['month']}",
                    self.format_currency(payment['principal']),
                    self.format_currency(payment['interest']),
                    self.format_currency(payment['establishment_fee']),
                    self.format_currency(payment['monthly_fee']),
                    self.format_currency(payment['total']),
                    self.format_currency(payment['balance'])
                ))
        
        # Tab 2: Chart
        tab2 = ttk.Frame(notebook)
        notebook.add(tab2, text="Avdrag/Renter fordeling")
        
        # Canvas for chart
        canvas = tk.Canvas(tab2, bg="white", highlightthickness=0)
        canvas.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Aggregate by year
        yearly_data_chart = {}
        for payment in self.loan_data['schedule']['payments']:
            year = payment['year']
            if year not in yearly_data_chart:
                yearly_data_chart[year] = {'principal': 0, 'interest': 0}
            yearly_data_chart[year]['principal'] += payment['principal']
            yearly_data_chart[year]['interest'] += payment['interest']
        
        # Draw chart
        canvas.create_text(700, 20, text="Fordeling av avdrag og renter per år", font=("Arial", 12, "bold"))
        
        years = sorted(yearly_data_chart.keys())
        max_total = max(yearly_data_chart[y]['principal'] + yearly_data_chart[y]['interest'] for y in years)
        
        x_start = 80
        bar_width = 40
        spacing = 60
        y_baseline = 350
        chart_height = 250
        
        for i, year in enumerate(years):
            x = x_start + i * spacing
            principal = yearly_data_chart[year]['principal']
            interest = yearly_data_chart[year]['interest']
            total = principal + interest
            
            # Calculate heights
            principal_height = (principal / max_total) * chart_height if max_total > 0 else 0
            interest_height = (interest / max_total) * chart_height if max_total > 0 else 0
            
            # Draw principal bar (green)
            canvas.create_rectangle(x, y_baseline - principal_height, x + bar_width, y_baseline, 
                                   fill="#4CAF50", outline="#333", width=2)
            
            # Draw interest bar (red) on top
            canvas.create_rectangle(x, y_baseline - principal_height - interest_height, x + bar_width, 
                                   y_baseline - principal_height, fill="#F44336", outline="#333", width=2)
            
            # Labels
            canvas.create_text(x + bar_width/2, y_baseline + 20, text=f"År {year}", font=("Arial", 9, "bold"))
            canvas.create_text(x + bar_width/2, y_baseline - principal_height - interest_height/2, 
                             text=self.format_currency(interest), font=("Arial", 7), fill="white")
            canvas.create_text(x + bar_width/2, y_baseline - principal_height/2, 
                             text=self.format_currency(principal), font=("Arial", 7), fill="white")
        
        # Legend
        canvas.create_rectangle(80, 30, 100, 50, fill="#4CAF50", outline="#333")
        canvas.create_text(110, 40, text="Avdrag", anchor=tk.W, font=("Arial", 9))
        
        canvas.create_rectangle(250, 30, 270, 50, fill="#F44336", outline="#333")
        canvas.create_text(280, 40, text="Renter", anchor=tk.W, font=("Arial", 9))
    
    def show_budget(self):
        if not self.budget_data:
            return
        
        budget_window = tk.Toplevel(self.root)
        budget_window.title("Detaljert Husholdningsbudsjett")
        budget_window.geometry("900x700")
        
        # Header
        header = tk.Frame(budget_window, bg=self.ACCENT_COLOR, height=50)
        header.pack(fill=tk.X)
        header.pack_propagate(False)
        
        title = tk.Label(header, text="Detaljert Husholdningsbudsjett 2025", font=("Arial", 14, "bold"),
                        bg=self.ACCENT_COLOR, fg="white")
        title.pack(pady=15)
        
        # Tree view
        tree = ttk.Treeview(budget_window, columns=("Kategori", "Beløp"), height=25)
        tree.column("#0", width=0, stretch=tk.NO)
        tree.column("Kategori", anchor=tk.W, width=400)
        tree.column("Beløp", anchor=tk.E, width=150)
        tree.heading("#0", text="")
        tree.heading("Kategori", text="Kategori")
        tree.heading("Beløp", text="Beløp/Måned")
        
        # Income
        tree.insert("", "end", values=("INNTEKTER", ""))
        tree.insert("", "end", values=("  Bruttoinntekt", self.format_currency(self.budget_data['monthly_income'])))
        tree.insert("", "end", values=("  Skatt", f"-{self.format_currency(self.budget_data['monthly_tax'])}"))
        tree.insert("", "end", values=("  Netto inntekt", self.format_currency(self.budget_data['net_income'])))
        
        tree.insert("", "end", values=("", ""))
        tree.insert("", "end", values=("INDIVIDUELLE UTGIFTER", ""))
        tree.insert("", "end", values=("  Mat og drikke", self.format_currency(self.budget_data['individual_expenses']['mat'])))
        tree.insert("", "end", values=("  Klær og sko", self.format_currency(self.budget_data['individual_expenses']['klaer'])))
        tree.insert("", "end", values=("  Personlig pleie", self.format_currency(self.budget_data['individual_expenses']['pleie'])))
        tree.insert("", "end", values=("  Lek og mediebruk", self.format_currency(self.budget_data['individual_expenses']['lek'])))
        tree.insert("", "end", values=("  Reisekostnader", self.format_currency(self.budget_data['individual_expenses']['reise'])))
        
        tree.insert("", "end", values=("", ""))
        tree.insert("", "end", values=("HUSHOLDSSPESIFIKKE UTGIFTER", ""))
        tree.insert("", "end", values=("  Andre dagligvarer", self.format_currency(self.budget_data['household_expenses']['andre_dagligvarer'])))
        tree.insert("", "end", values=("  Husholdningsartikler", self.format_currency(self.budget_data['household_expenses']['husholdningsartikler'])))
        tree.insert("", "end", values=("  Møbler", self.format_currency(self.budget_data['household_expenses']['mobler'])))
        tree.insert("", "end", values=("  Mediebruk og fritid", self.format_currency(self.budget_data['household_expenses']['mediebruk_fritid'])))
        
        tree.insert("", "end", values=("", ""))
        tree.insert("", "end", values=("ANDRE UTGIFTER", ""))
        tree.insert("", "end", values=("  Bokostnader", self.format_currency(self.budget_data['housing_costs'])))
        tree.insert("", "end", values=("  Bilkostnader", self.format_currency(self.budget_data['car_cost'])))
        tree.insert("", "end", values=("  Lånekostnader", self.format_currency(self.budget_data['monthly_loan_payment'])))
        
        tree.insert("", "end", values=("", ""))
        tree.insert("", "end", values=("TOTALT", ""))
        tree.insert("", "end", values=("  Totale utgifter", self.format_currency(self.budget_data['total_expenses'])))
        tree.insert("", "end", values=("  Overskudd/måned", self.format_currency(self.budget_data['liquidity_surplus'])))
        tree.insert("", "end", values=("  Overskudd/år", self.format_currency(self.budget_data['liquidity_surplus_yearly'])))
        
        tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    
    def show_budget_chart(self):
        if not self.budget_data:
            return
        
        chart_window = tk.Toplevel(self.root)
        chart_window.title("Budsjettgraf")
        chart_window.geometry("1100x700")
        
        # Header
        header = tk.Frame(chart_window, bg=self.ACCENT_COLOR, height=50)
        header.pack(fill=tk.X)
        header.pack_propagate(False)
        
        title = tk.Label(header, text="Budsjettfordeling - Grafisk Oversikt", font=("Arial", 12, "bold"),
                        bg=self.ACCENT_COLOR, fg="white")
        title.pack(pady=10)
        
        # Main container with top (chart) and bottom (summary) sections
        main_frame = tk.Frame(chart_window, bg="white")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Top section - Chart
        top_frame = tk.Frame(main_frame, bg="white")
        top_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=0, pady=(0, 20))
        
        tk.Label(top_frame, text="Utgiftsfordeling (Månedsbudsjett)", font=("Arial", 11, "bold"), bg="white").pack(anchor=tk.W, pady=(0, 10))
        
        canvas = tk.Canvas(top_frame, bg="white", highlightthickness=0)
        canvas.pack(fill=tk.BOTH, expand=True)
        
        budget = self.budget_data
        total = budget['total_expenses']
        
        categories = [
            ("Mat og drikke", budget['individual_expenses']['mat'], "#4CAF50"),
            ("Personlig pleie", budget['individual_expenses']['pleie'], "#2196F3"),
            ("Bokostnader", budget['housing_costs'], "#FF9800"),
            ("Bilkostnader", budget['car_cost'], "#F44336"),
            ("Lånekostnad", budget['monthly_loan_payment'], "#9C27B0"),
        ]
        
        y_start = 20
        for cat, amount, color in categories:
            if amount > 0:
                width = (amount / total) * 400 if total > 0 else 0
                canvas.create_rectangle(20, y_start, 20 + width, y_start + 25, fill=color, outline="#333")
                percentage = (amount / total) * 100 if total > 0 else 0
                canvas.create_text(25, y_start + 12, text=f"{cat}", anchor=tk.W, font=("Arial", 9, "bold"), fill="white")
                canvas.create_text(430, y_start + 12, text=f"{self.format_currency(amount)} ({percentage:.1f}%)", anchor=tk.W, font=("Arial", 9))
                y_start += 45
        
        # Bottom section - Summary in a frame
        bottom_frame = tk.Frame(main_frame, bg="#F5F5F5", relief=tk.SUNKEN, bd=2)
        bottom_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=0, pady=0)
        
        tk.Label(bottom_frame, text="SAMMENDRAG", font=("Arial", 10, "bold"), bg="#F5F5F5", fg="#1B5E20").pack(anchor=tk.W, padx=15, pady=(10, 5))
        
        surplus = budget['liquidity_surplus']
        surplus_color = "#2E7D32" if surplus >= 0 else "#D32F2F"
        
        summary_items = [
            (f"Mat og drikke:", self.format_currency(budget['individual_expenses']['mat'])),
            (f"Personlig pleie:", self.format_currency(budget['individual_expenses']['pleie'])),
            (f"Bokostnader:", self.format_currency(budget['housing_costs'])),
            (f"Bilkostnader:", self.format_currency(budget['car_cost'])),
            (f"Lånekostnad:", self.format_currency(budget['monthly_loan_payment'])),
        ]
        
        # Create a frame for summary items
        items_frame = tk.Frame(bottom_frame, bg="#F5F5F5")
        items_frame.pack(fill=tk.X, padx=15, pady=(0, 5))
        
        for label, value in summary_items:
            item_frame = tk.Frame(items_frame, bg="#F5F5F5")
            item_frame.pack(fill=tk.X, pady=1)
            tk.Label(item_frame, text=label, font=("Arial", 9), bg="#F5F5F5", width=20).pack(side=tk.LEFT, anchor=tk.W)
            tk.Label(item_frame, text=value, font=("Arial", 9), bg="#F5F5F5").pack(side=tk.LEFT, anchor=tk.E)
        
        # Separators and totals
        ttk.Separator(bottom_frame, orient=tk.HORIZONTAL).pack(fill=tk.X, padx=15, pady=5)
        
        total_frame = tk.Frame(bottom_frame, bg="#F5F5F5")
        total_frame.pack(fill=tk.X, padx=15, pady=2)
        tk.Label(total_frame, text="TOTAL UTGIFTER:", font=("Arial", 10, "bold"), bg="#F5F5F5", width=20).pack(side=tk.LEFT, anchor=tk.W)
        tk.Label(total_frame, text=self.format_currency(total), font=("Arial", 10, "bold"), bg="#F5F5F5").pack(side=tk.LEFT, anchor=tk.E)
        
        ttk.Separator(bottom_frame, orient=tk.HORIZONTAL).pack(fill=tk.X, padx=15, pady=5)
        
        surplus_frame = tk.Frame(bottom_frame, bg="#F5F5F5")
        surplus_frame.pack(fill=tk.X, padx=15, pady=(2, 10))
        tk.Label(surplus_frame, text="OVERSKUDD/MND:", font=("Arial", 10, "bold"), bg="#F5F5F5", fg=surplus_color, width=20).pack(side=tk.LEFT, anchor=tk.W)
        tk.Label(surplus_frame, text=self.format_currency(surplus), font=("Arial", 10, "bold"), bg="#F5F5F5", fg=surplus_color).pack(side=tk.LEFT, anchor=tk.E)
        
        yearly_surplus_frame = tk.Frame(bottom_frame, bg="#F5F5F5")
        yearly_surplus_frame.pack(fill=tk.X, padx=15, pady=(0, 10))
        tk.Label(yearly_surplus_frame, text="OVERSKUDD/ÅR:", font=("Arial", 10, "bold"), bg="#F5F5F5", fg=surplus_color, width=20).pack(side=tk.LEFT, anchor=tk.W)
        tk.Label(yearly_surplus_frame, text=self.format_currency(budget['liquidity_surplus_yearly']), font=("Arial", 10, "bold"), bg="#F5F5F5", fg=surplus_color).pack(side=tk.LEFT, anchor=tk.E)


if __name__ == "__main__":
    root = tk.Tk()
    app = LoanCalculatorApp(root)
    root.mainloop()
