import tkinter as tk
from tkinter import messagebox
from math import pow

class ArtGalleryExhibition:
    def __init__(self, name, kloc, initial_investment, projected_cash_flows, discount_rate, object_points):
        self.name = name
        self.kloc = kloc
        self.initial_investment = initial_investment
        self.projected_cash_flows = projected_cash_flows
        self.discount_rate = discount_rate
        self.object_points = object_points

    def calculate_function_points(self, inputs, outputs, user_interactions, files):
        return inputs + outputs + user_interactions + files

    def calculate_effort_cocomo(self):
        a, b, c, d = 2.4, 1.05, 2.5, 0.38
        effort = a * pow(self.kloc, b)
        development_time = c * pow(effort, d)
        return effort, development_time

    def calculate_effort_strs(self):
        effort_per_object_point = 2.94
        return self.object_points * effort_per_object_point

    def calculate_financial_metrics(self):
        npv = sum(cf / pow(1 + self.discount_rate, year) for year, cf in enumerate(self.projected_cash_flows, start=1))
        total_profit = sum(self.projected_cash_flows) - self.initial_investment
        roi = (total_profit / self.initial_investment) * 100
        cumulative_cash_flow = 0
        payback_period = None
        for year, cf in enumerate(self.projected_cash_flows, start=1):
            cumulative_cash_flow += cf
            if cumulative_cash_flow >= self.initial_investment:
                payback_period = year
                break
        return npv, roi, payback_period, total_profit

    def earned_value_analysis(self, pv, ev, ac):
        sv = ev - pv
        cv = ev - ac
        spi = ev / pv if pv != 0 else 0
        cpi = ev / ac if ac != 0 else 0
        return sv, cv, spi, cpi


# Tkinter GUI
class ArtGalleryGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Art Gallery Exhibition Management System")
        self.root.geometry("600x600")

        # Exhibition Information
        tk.Label(root, text="Art Gallery Exhibition Management", font=("Arial", 16, "bold")).pack(pady=10)
        tk.Label(root, text="Enter Exhibition Details:", font=("Arial", 12)).pack(anchor="w", padx=20)

        # KLOC and Investment Inputs
        tk.Label(root, text="KLOC (in thousands):").pack(anchor="w", padx=20)
        self.kloc_entry = tk.Entry(root)
        self.kloc_entry.pack(padx=20, pady=5, anchor="w")

        tk.Label(root, text="Initial Investment ($):").pack(anchor="w", padx=20)
        self.investment_entry = tk.Entry(root)
        self.investment_entry.pack(padx=20, pady=5, anchor="w")

        # Financial Projections and Rate
        tk.Label(root, text="Projected Cash Flows (comma-separated):").pack(anchor="w", padx=20)
        self.cash_flows_entry = tk.Entry(root)
        self.cash_flows_entry.pack(padx=20, pady=5, anchor="w")

        tk.Label(root, text="Discount Rate (%):").pack(anchor="w", padx=20)
        self.discount_rate_entry = tk.Entry(root)
        self.discount_rate_entry.pack(padx=20, pady=5, anchor="w")

        tk.Label(root, text="Object Points for STRS:").pack(anchor="w", padx=20)
        self.object_points_entry = tk.Entry(root)
        self.object_points_entry.pack(padx=20, pady=5, anchor="w")

        # Buttons for Calculations
        tk.Button(root, text="Calculate Function Points", command=self.calculate_function_points).pack(pady=10)
        tk.Button(root, text="Calculate COCOMO Effort", command=self.calculate_cocomo).pack(pady=5)
        tk.Button(root, text="Calculate STRS Effort", command=self.calculate_strs).pack(pady=5)
        tk.Button(root, text="Calculate Financial Metrics", command=self.calculate_financial_metrics).pack(pady=5)
        tk.Button(root, text="Earned Value Analysis", command=self.calculate_earned_value_analysis).pack(pady=5)

    def calculate_function_points(self):
        inputs, outputs, interactions, files = 10, 5, 3, 2
        function_points = inputs + outputs + interactions + files
        messagebox.showinfo("Function Points", f"Total Function Points: {function_points}")

    def calculate_cocomo(self):
        try:
            kloc = float(self.kloc_entry.get())
            effort = 2.4 * pow(kloc, 1.05)
            time = 2.5 * pow(effort, 0.38)
            messagebox.showinfo("COCOMO Effort", f"Effort: {effort:.2f} PM, Time: {time:.2f} months")
        except ValueError:
            messagebox.showerror("Error", "Invalid KLOC input.")

    def calculate_strs(self):
        try:
            object_points = int(self.object_points_entry.get())
            effort = object_points * 2.94
            messagebox.showinfo("STRS Effort", f"Effort: {effort:.2f} person-hours")
        except ValueError:
            messagebox.showerror("Error", "Invalid Object Points input.")

    def calculate_financial_metrics(self):
        try:
            investment = float(self.investment_entry.get())
            cash_flows = list(map(float, self.cash_flows_entry.get().split(',')))
            discount_rate = float(self.discount_rate_entry.get()) / 100
            npv = sum(cf / pow(1 + discount_rate, i) for i, cf in enumerate(cash_flows, start=1))
            total_profit = sum(cash_flows) - investment
            roi = (total_profit / investment) * 100
            payback_period = next((i + 1 for i, cf in enumerate(cash_flows) if sum(cash_flows[:i + 1]) >= investment), "N/A")
            messagebox.showinfo("Financial Metrics", f"NPV: ${npv:.2f}, ROI: {roi:.2f}%, Payback Period: {payback_period} years, Profit: ${total_profit:.2f}")
        except ValueError:
            messagebox.showerror("Error", "Invalid financial data input.")

    def calculate_earned_value_analysis(self):
        try:
            pv, ev, ac = 10000, 9500, 11000
            sv = ev - pv
            cv = ev - ac
            spi = ev / pv if pv != 0 else 0
            cpi = ev / ac if ac != 0 else 0
            messagebox.showinfo("Earned Value Analysis", f"SV: ${sv:.2f}, CV: ${cv:.2f}, SPI: {spi:.2f}, CPI: {cpi:.2f}")
        except ValueError:
            messagebox.showerror("Error", "Invalid earned value data.")

# Initialize the app
root = tk.Tk()
app = ArtGalleryGUI(root)
root.mainloop()
