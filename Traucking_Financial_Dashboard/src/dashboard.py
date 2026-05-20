#!/usr/bin/env python
"""
Date: 2026-05-19
Script Name: dashboard.py
Author: omegazyph
Updated On: 2026-05-19

Description:
    An interactive Tkinter desktop financial dashboard designed for tracking 
    trucking logistics, fuel efficiency, cost-per-mile (CPM), and net profit.
    This version applies a premium, custom dark theme across both the Tkinter 
    user interface elements and the embedded bottom-left Matplotlib vertical 
    bar chart for optimal low-light visibility.
"""

import os
import json
import tkinter as tk
from tkinter import ttk, messagebox

# Import Matplotlib engineering modules for Tkinter canvas integration
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure


class TruckingDashboard(tk.Tk):

    def __init__(self):
        super().__init__()

        # Define explicit pathing landmarks relative to this execution script
        self.script_directory = os.path.dirname(os.path.abspath(__file__))
        self.project_root = os.path.dirname(self.script_directory)
        self.config_directory = os.path.join(self.project_root, "config")
        self.config_filepath = os.path.join(self.config_directory, "config.json")

        # Initialize core hardcoded fallback values in case the JSON file is unreadable
        self.fallback_defaults = {
            "gross_revenue": 3500.00,
            "total_miles": 1200.0,
            "fuel_price": 3.85,
            "mpg": 6.5,
            "fixed_costs": 800.00,
            "misc_costs": 250.00,
            "window_width": 1200,
            "window_height": 800
        }

        # Load dynamic settings profile from the external JSON file
        self.app_settings = self.load_configuration_file()

        # Configure the main window properties based on configuration values
        self.title("Omegazyph Logistics - Dark Financial Dashboard")
        window_w = self.app_settings.get("window_width", 1200)
        window_h = self.app_settings.get("window_height", 800)
        self.geometry(f"{window_w}x{window_h}")
        self.minsize(1100, 700)

        # Set up a clean, modern dark theme styling palette
        self.configure(bg="#1e1e1e")
        self.style = ttk.Style()
        self.style.theme_use("clam")

        # Overwrite standard clam layout styles with dark theme values
        self.style.configure(".", background="#1e1e1e", foreground="#ffffff")
        self.style.configure("TFrame", background="#1e1e1e")
        self.style.configure("TLabelframe", background="#1e1e1e", foreground="#458588")
        self.style.configure("TLabelframe.Label", background="#1e1e1e", foreground="#8ec07c", font=("Arial", 11, "bold"))
        self.style.configure("TLabel", background="#1e1e1e", foreground="#ffffff")
        
        # Style entries with dark backgrounds and white text
        self.style.configure("TEntry", fieldbackground="#2d2d2d", foreground="#ffffff", insertcolor="#ffffff")
        
        # Style flat, dark buttons with accent hover adjustments
        self.style.configure("TButton", background="#3a3a3a", foreground="#ffffff", borderwidth=1, focuscolor="none")
        self.style.map("TButton", background=[("active", "#4a4a4a")])

        # Initialize Tkinter operational variables using parsed JSON attributes
        self.var_gross_revenue = tk.DoubleVar(value=self.app_settings.get("gross_revenue"))
        self.var_total_miles = tk.DoubleVar(value=self.app_settings.get("total_miles"))
        self.var_fuel_price = tk.DoubleVar(value=self.app_settings.get("fuel_price"))
        self.var_mpg = tk.DoubleVar(value=self.app_settings.get("mpg"))
        self.var_fixed_costs = tk.DoubleVar(value=self.app_settings.get("fixed_costs"))
        self.var_misc_costs = tk.DoubleVar(value=self.app_settings.get("misc_costs"))

        # Trace modifications to automatically update calculations when inputs change
        for tracking_variable in [
            self.var_gross_revenue,
            self.var_total_miles,
            self.var_fuel_price,
            self.var_mpg,
            self.var_fixed_costs,
            self.var_misc_costs,
        ]:
            tracking_variable.trace_add("write", self.calculate_metrics)

        # Output/Result display strings
        self.res_fuel_cost = tk.StringVar()
        self.res_total_cost = tk.StringVar()
        self.res_net_profit = tk.StringVar()
        self.res_rev_per_mile = tk.StringVar()
        self.res_cost_per_mile = tk.StringVar()
        self.res_profit_per_mile = tk.StringVar()

        # Build the user interface components
        self.create_widgets()

        # Perform initial calculation on startup
        self.calculate_metrics()

    def load_configuration_file(self):
        """Reads application settings from JSON file or handles self-healing creation."""
        if not os.path.exists(self.config_filepath):
            try:
                if not os.path.exists(self.config_directory):
                    os.makedirs(self.config_directory)
                
                with open(self.config_filepath, "w") as write_file:
                    json.dump(self.fallback_defaults, write_file, indent=4)
                return self.fallback_defaults
            except Exception as creation_error:
                print(f"Warning: Failed to create default configuration file: {creation_error}")
                return self.fallback_defaults

        try:
            with open(self.config_filepath, "r") as read_file:
                parsed_json = json.load(read_file)
                for key, fallback_value in self.fallback_defaults.items():
                    if key not in parsed_json:
                        parsed_json[key] = fallback_value
                return parsed_json
        except Exception as reading_error:
            print(f"Warning: Failed parsing configuration JSON file, falling back to defaults: {reading_error}")
            return self.fallback_defaults

    def save_current_as_defaults(self):
        """Gathers runtime states and commits them back to disk as current standard properties."""
        try:
            updated_settings = {
                "gross_revenue": self.var_gross_revenue.get(),
                "total_miles": self.var_total_miles.get(),
                "fuel_price": self.var_fuel_price.get(),
                "mpg": self.var_mpg.get(),
                "fixed_costs": self.var_fixed_costs.get(),
                "misc_costs": self.var_misc_costs.get(),
                "window_width": self.winfo_width(),
                "window_height": self.winfo_height()
            }

            with open(self.config_filepath, "w") as update_file:
                json.dump(updated_settings, update_file, indent=4)
            
            messagebox.showinfo("Configuration Updated", "Current operational values saved successfully as default configuration settings.")
        except Exception as save_error:
            messagebox.showerror("Save Failure", f"An error occurred while saving the configuration settings:\n{save_error}")

    def create_widgets(self):
        """Creates the grid layout, entry panels, KPI displays, and embedded Matplotlib canvas."""
        # Main Layout: Left control panel, Right financial readout panel
        self.grid_columnconfigure(0, weight=1, minsize=450)
        self.grid_columnconfigure(1, weight=2, minsize=600)
        self.grid_rowconfigure(0, weight=1)

        # ==========================================
        # LEFT PANEL: INPUT CONTROLS & CHART
        # ==========================================
        left_frame = ttk.Frame(self, padding="20")
        left_frame.grid(row=0, column=0, sticky="nsew")
        
        # Configure layout inside left panel to support the input area and the chart area
        left_frame.grid_columnconfigure(0, weight=1)
        left_frame.grid_rowconfigure(0, weight=0)  # Inputs
        left_frame.grid_rowconfigure(1, weight=0)  # Buttons
        left_frame.grid_rowconfigure(2, weight=1)  # Dynamic Chart Canvas

        # Input Group container box
        input_container = ttk.Frame(left_frame)
        input_container.grid(row=0, column=0, sticky="ew", pady=(0, 10))

        input_header = ttk.Label(
            input_container,
            text="Load & Operational Inputs",
            font=("Arial", 16, "bold"),
            foreground="#8ec07c"
        )
        input_header.pack(anchor="w", pady=(0, 10))

        def create_input_field(parent, label_text, variable):
            frame = ttk.Frame(parent)
            frame.pack(fill="x", pady=4)
            lbl = ttk.Label(frame, text=label_text, font=("Arial", 11), foreground="#ffffff")
            lbl.pack(side="left")
            ent = ttk.Entry(
                frame, textvariable=variable, font=("Arial", 11), width=12, style="TEntry"
            )
            ent.pack(side="right")
            return frame

        create_input_field(input_container, "Gross Revenue ($):", self.var_gross_revenue)
        create_input_field(input_container, "Total Trip Miles (mi):", self.var_total_miles)
        create_input_field(input_container, "Fuel Price per Gallon ($):", self.var_fuel_price)
        create_input_field(input_container, "Truck Fuel Economy (MPG):", self.var_mpg)
        create_input_field(input_container, "Fixed Costs (Truck/Ins) ($):", self.var_fixed_costs)
        create_input_field(input_container, "Misc Costs (Tolls/Maint) ($):", self.var_misc_costs)

        # Control utilities row
        btn_frame = ttk.Frame(left_frame)
        btn_frame.grid(row=1, column=0, sticky="ew", pady=(5, 15))
        btn_frame.grid_columnconfigure(0, weight=1)
        btn_frame.grid_columnconfigure(1, weight=1)

        reload_btn = ttk.Button(
            btn_frame, text="Reload JSON Config", command=self.reload_from_disk
        )
        reload_btn.grid(row=0, column=0, padx=(0, 5), sticky="ew")

        save_btn = ttk.Button(
            btn_frame, text="Save Current to JSON", command=self.save_current_as_defaults
        )
        save_btn.grid(row=0, column=1, padx=(5, 0), sticky="ew")

        # Bottom-Left Chart Placement Container Frame
        self.chart_container = ttk.LabelFrame(left_frame, text=" Dollar Allocation Breakdown ($) ", padding="10")
        self.chart_container.grid(row=2, column=0, sticky="nsew")
        
        # Initialize the Matplotlib structural objects matching the UI dark theme background (#1e1e1e)
        self.figure = Figure(figsize=(4, 3.5), dpi=100, facecolor="#1e1e1e")
        self.ax = self.figure.add_subplot(111)
        self.ax.set_facecolor("#1e1e1e")
        
        self.canvas = FigureCanvasTkAgg(self.figure, master=self.chart_container)
        self.canvas.get_tk_widget().pack(fill="both", expand=True)

        # ==========================================
        # RIGHT PANEL: FINANCIAL PERFORMANCE READOUT
        # ==========================================
        right_frame = ttk.Frame(self, padding="20")
        right_frame.grid(row=0, column=1, sticky="nsew")

        right_header = ttk.Label(
            right_frame, text="Financial Performance", font=("Arial", 16, "bold"), foreground="#8ec07c"
        )
        right_header.pack(anchor="w", pady=(0, 20))

        totals_group = ttk.LabelFrame(
            right_frame, text=" Trip Ledger Totals ", padding="15"
        )
        totals_group.pack(fill="x", pady=10)

        def create_kpi_row(parent, title, text_var, highlight=False, highlight_color="#ffffff"):
            frame = ttk.Frame(parent)
            frame.pack(fill="x", pady=6)
            
            if highlight:
                font_style = ("Arial", 12, "bold")
                lbl_color = highlight_color
                val_color = highlight_color
            else:
                font_style = ("Arial", 11)
                lbl_color = "#b0b0b0"
                val_color = "#ffffff"

            lbl = ttk.Label(frame, text=title, font=font_style, foreground=lbl_color)
            lbl.pack(side="left")
            val = ttk.Label(frame, textvariable=text_var, font=font_style, foreground=val_color)
            val.pack(side="right")

        create_kpi_row(totals_group, "Calculated Fuel Cost:", self.res_fuel_cost)
        create_kpi_row(totals_group, "Total Operating Expenses:", self.res_total_cost)
        create_kpi_row(
            totals_group, "Net Trip Profit:", self.res_net_profit, highlight=True, highlight_color="#b8bb26"
        )

        mile_group = ttk.LabelFrame(
            right_frame, text=" Mileage Breakdowns ", padding="15"
        )
        mile_group.pack(fill="x", pady=10)

        create_kpi_row(mile_group, "Gross Revenue Per Mile:", self.res_rev_per_mile)
        create_kpi_row(mile_group, "Total Cost Per Mile (CPM):", self.res_cost_per_mile)
        create_kpi_row(
            mile_group,
            "Net Profit Per Mile:",
            self.res_profit_per_mile,
            highlight=True,
            highlight_color="#b8bb26"
        )

        info_box = ttk.LabelFrame(right_frame, text=" System Configurations Info ", padding="12")
        info_box.pack(fill="both", expand=True, pady=(20, 0))

        info_text = (
            f"• Full system wide Premium Dark Theme integrated successfully.\n"
            f"• Vertical bar chart configured to match the dark aesthetic elements.\n"
            f"• Net Profit bar automatically tracks into deep red values if costs exceed gains."
        )
        info_lbl = ttk.Label(
            info_box, text=info_text, font=("Arial", 10), justify="left", wraplength=550, foreground="#b0b0b0"
        )
        info_lbl.pack(anchor="w")

    def calculate_metrics(self, *args):
        """Safely executes financial calculations and refreshes text fields and bar charts."""
        try:
            # Safely fetch values from UI inputs
            gross = self.var_gross_revenue.get()
            miles = self.var_total_miles.get()
            fuel_p = self.var_fuel_price.get()
            mpg = self.var_mpg.get()
            fixed = self.var_fixed_costs.get()
            misc = self.var_misc_costs.get()

            # Prevent division by zero errors for unconfigured loads
            if miles <= 0 or mpg <= 0:
                self.set_blank_results("Enter Valid Inputs")
                self.clear_chart_canvas()
                return

            # Compute Trip Financials
            calculated_fuel = (miles / mpg) * fuel_p
            total_expenses = calculated_fuel + fixed + misc
            net_profit = gross - total_expenses

            # Compute Per-Mile Averages
            rev_per_mile = gross / miles
            cost_per_mile = total_expenses / miles
            profit_per_mile = net_profit / miles

            # Assign formatted text to variables linked to UI elements
            self.res_fuel_cost.set(f"${calculated_fuel:,.2f}")
            self.res_total_cost.set(f"${total_expenses:,.2f}")
            self.res_net_profit.set(f"${net_profit:,.2f}")

            self.res_rev_per_mile.set(f"${rev_per_mile:.2f} / mi")
            self.res_cost_per_mile.set(f"${cost_per_mile:.2f} / mi")
            self.res_profit_per_mile.set(f"${profit_per_mile:.2f} / mi")

            # Update the bottom-left bar chart visualization panel
            self.update_chart_visualization(calculated_fuel, fixed, misc, net_profit)

        except tk.TclError:
            # Gracefully handle incomplete or malformed numerical input while typing
            self.set_blank_results("Typing...")
            self.clear_chart_canvas()

    def update_chart_visualization(self, fuel, fixed, misc, net):
        """Re-plots data to the embedded canvas using a vertical, bottom-up dark layout."""
        self.ax.clear()

        # Establish categorical data boundaries
        categories = ["Fuel", "Fixed", "Misc", "Net Profit"]
        values = [fuel, fixed, misc, net]
        
        # Determine profit bar color dynamically depending on health status
        profit_color = "#b8bb26" if net >= 0 else "#fb4934"
        colors = ["#fe8019", "#83a598", "#fabd2f", profit_color]

        # Draw vertical bars rising from the bottom up
        bars = self.ax.bar(categories, values, color=colors, width=0.55)
        
        # Configure grid layouts and label styling to look clean against dark colors
        self.ax.spines["top"].set_visible(False)
        self.ax.spines["right"].set_visible(False)
        self.ax.spines["left"].set_color("#504945")
        self.ax.spines["bottom"].set_color("#504945")
        self.ax.yaxis.grid(True, linestyle="--", alpha=0.3, color="#a89984")
        self.ax.set_axisbelow(True)
        
        # Set tick label color to white for contrast
        self.ax.tick_params(axis="both", labelsize=9, colors="#ffffff")

        # Add an explicit dark horizontal zero line to clearly denote positive vs negative profit
        self.ax.axhline(0, color="#7c6f64", linewidth=0.8)

        # Draw raw value callouts directly on top of (or below) each matching bar
        for bar in bars:
            height = bar.get_height()
            # Position logic checks for negative values to ensure proper spacing
            if height >= 0:
                text_position_y = height + (max(values) * 0.02)
                text_alignment = "bottom"
            else:
                text_position_y = height - (max(values) * 0.06)
                text_alignment = "top"
                
            self.ax.text(
                bar.get_x() + bar.get_width() / 2,
                text_position_y,
                f"${height:,.0f}",
                va=text_alignment,
                ha="center",
                fontsize=8,
                fontweight="bold",
                color="#ffffff"
            )

        # Set chart boundaries with padding on the vertical Y-axis
        min_y = min(0, net) * 1.25 if net < 0 else 0
        max_y = max(values) * 1.20
        self.ax.set_ylim(min_y, max_y)

        if net < 0:
            self.ax.set_title("Operating at a Loss", color="#fb4934", fontname="Arial", fontsize=11, fontweight="bold")

        self.figure.tight_layout()
        self.canvas.draw()

    def clear_chart_canvas(self):
        """Wipes chart elements during typing intervals or invalid entry configurations."""
        self.ax.clear()
        self.ax.axis("off")
        self.canvas.draw()

    def set_blank_results(self, message):
        """Fills readout strings with a fallback status indicator flag."""
        self.res_fuel_cost.set(message)
        self.res_total_cost.set(message)
        self.res_net_profit.set(message)
        self.res_rev_per_mile.set(message)
        self.res_cost_per_mile.set(message)
        self.res_profit_per_mile.set(message)

    def reload_from_disk(self):
        """Re-reads the local JSON structure to overwrite current fields."""
        self.app_settings = self.load_configuration_file()
        self.var_gross_revenue.set(self.app_settings.get("gross_revenue"))
        self.var_total_miles.set(self.app_settings.get("total_miles"))
        self.var_fuel_price.set(self.app_settings.get("fuel_price"))
        self.var_mpg.set(self.app_settings.get("mpg"))
        self.var_fixed_costs.set(self.app_settings.get("fixed_costs"))
        self.var_misc_costs.set(self.app_settings.get("misc_costs"))
        self.calculate_metrics()


if __name__ == "__main__":
    app = TruckingDashboard()
    app.mainloop()