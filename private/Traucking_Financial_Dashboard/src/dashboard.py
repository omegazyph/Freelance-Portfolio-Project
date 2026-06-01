#!/usr/bin/env python
"""
Date: 2026-05-20
Script Name: dashboard.py
Author: omegazyph
Updated On: 2026-05-20

Description:
    An interactive Tkinter desktop financial dashboard designed for tracking 
    trucking logistics, fuel efficiency, cost-per-mile (CPM), and net profit.
    This advanced version dynamically generates all revenue and deduction 
    entry fields on-the-fly based on lists defined inside an external JSON 
    configuration file. Entry boxes are embedded with auto-highlight event bindings
    to eliminate the need for manual backspacing when modifying data fields.
    The dashboard automatically sorts and saves database entries in chronological 
    order by date inside the load history spreadsheet file, and provides a 
    running Year-to-Date (YTD) business performance summary.
"""

import os
import json
import csv
from datetime import datetime
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
        
        # Paths for configuration file
        self.config_directory = os.path.join(self.project_root, "config")
        self.config_filepath = os.path.join(self.config_directory, "config.json")
        
        # Paths for CSV historical tracking file
        self.data_directory = os.path.join(self.project_root, "data")
        self.csv_filepath = os.path.join(self.data_directory, "load_history.csv")

        # Load dynamic settings profile from the external JSON file
        self.app_settings = self.load_configuration_file()
        
        # Explicitly verify or initialize the historical CSV ledger storage
        self.initialize_csv_file()

        # Configure the main window properties based on configuration values
        self.title("Omegazyph Logistics - Dynamic Statement Dashboard")
        window_width_value = self.app_settings.get("window_width", 1350)
        window_height_value = self.app_settings.get("window_height", 950)
        self.geometry(f"{window_width_value}x{window_height_value}")

        # Set up a clean, modern dark theme styling palette
        self.configure(bg="#1e1e1e")
        self.style = ttk.Style()
        self.style.theme_use("clam")

        # Overwrite standard clam layout styles with dark theme values
        self.style.configure(".", background="#1e1e1e", foreground="#ffffff")
        self.style.configure("TFrame", background="#1e1e1e")
        self.style.configure("TLabelframe", background="#1e1e1e", foreground="#458588")
        self.style.configure("TLabelframe.Label", background="#1e1e1e", foreground="#8ec07c", font=("Arial", 10, "bold"))
        self.style.configure("TLabel", background="#1e1e1e", foreground="#ffffff")
        
        # Style entries with dark backgrounds and white text
        self.style.configure("TEntry", fieldbackground="#2d2d2d", foreground="#ffffff", insertcolor="#ffffff")
        
        # Style flat, dark buttons with accent hover adjustments
        self.style.configure("TButton", background="#3a3a3a", foreground="#ffffff", borderwidth=1, focuscolor="none")
        self.style.map("TButton", background=[("active", "#4a4a4a")])

        # Custom configuration style rules for historical treeview display matrix
        self.style.configure("Treeview", background="#2d2d2d", foreground="#ffffff", fieldbackground="#2d2d2d", rowheight=25)
        self.style.configure("Treeview.Heading", background="#3a3a3a", foreground="#ffffff", relief="flat")
        self.style.map("Treeview.Heading", background=[("active", "#4a4a4a")])

        # Initialize tracking dictionaries for data collection
        self.revenue_variables = {}
        self.charge_variables = {}

        # Initialize Tkinter core operational metadata variables
        self.var_order_number = tk.StringVar(value="E930309")
        core_metrics = self.app_settings.get("core_metrics", {"pickup_date": "2026-05-20", "loaded_miles": 967.0, "empty_miles": 0.0, "total_gallons": 150.0})
        
        self.var_pickup_date = tk.StringVar(value=core_metrics.get("pickup_date", "2026-05-20"))
        self.var_loaded_miles = tk.DoubleVar(value=core_metrics.get("loaded_miles", 967.0))
        self.var_empty_miles = tk.DoubleVar(value=core_metrics.get("empty_miles", 0.0))
        self.var_total_gallons = tk.DoubleVar(value=core_metrics.get("total_gallons", 150.0))

        # Attach standard validation change traces to core miles/gallons inputs
        self.var_loaded_miles.trace_add("write", self.calculate_metrics)
        self.var_empty_miles.trace_add("write", self.calculate_metrics)
        self.var_total_gallons.trace_add("write", self.calculate_metrics)

        # Dynamically instantiate DoubleVars based on JSON definitions
        for revenue_item in self.app_settings.get("revenue_line_items", []):
            item_key = revenue_item.get("key")
            item_default = revenue_item.get("default_value", 0.0)
            variable_object = tk.DoubleVar(value=item_default)
            variable_object.trace_add("write", self.calculate_metrics)
            self.revenue_variables[item_key] = variable_object

        for charge_item in self.app_settings.get("charge_line_items", []):
            item_key = charge_item.get("key")
            item_default = charge_item.get("default_value", 0.0)
            variable_object = tk.DoubleVar(value=item_default)
            variable_object.trace_add("write", self.calculate_metrics)
            self.charge_variables[item_key] = variable_object

        # Output/Result display strings for the current active load
        self.res_calculated_mpg = tk.StringVar()
        self.res_price_per_gallon = tk.StringVar()
        self.res_gross_due_owner = tk.StringVar()
        self.res_total_cost = tk.StringVar()
        self.res_net_profit = tk.StringVar()
        self.res_revenue_per_mile = tk.StringVar()
        self.res_cost_per_mile = tk.StringVar()
        self.res_break_even_cpm = tk.StringVar()
        self.res_profit_per_mile = tk.StringVar()

        # Cumulative business (Year-to-Date) dashboard tracking variables
        self.res_ytd_gross_revenue = tk.StringVar(value="$0.00")
        self.res_ytd_total_expenses = tk.StringVar(value="$0.00")
        self.res_ytd_net_profit = tk.StringVar(value="$0.00")
        self.res_ytd_fuel_cost = tk.StringVar(value="$0.00")
        self.res_ytd_loaded_miles = tk.StringVar(value="0.0 mi")
        self.res_ytd_empty_miles = tk.StringVar(value="0.0 mi")
        self.res_ytd_overall_cost_per_mile = tk.StringVar(value="$0.00 / mi")

        # Build the user interface components
        self.create_widgets()

        # Render data rows imported from loaded CSV tracking records and compute totals
        self.refresh_historical_ledger_display()

        # Perform initial calculation on startup
        self.calculate_metrics()

    def load_configuration_file(self):
        """Reads configuration settings from JSON file or throws a fatal alert if corrupted."""
        if not os.path.exists(self.config_filepath):
            if not os.path.exists(self.config_directory):
                os.makedirs(self.config_directory)
            messagebox.showerror("Configuration Error", "The config.json file was not found in the config folder.")
            self.destroy()
            return {}

        try:
            with open(self.config_filepath, "r") as read_file:
                return json.load(read_file)
        except Exception as reading_error:
            messagebox.showerror("JSON Error", f"Failed to parse your config.json file:\n{reading_error}")
            self.destroy()
            return {}

    def initialize_csv_file(self):
        """Ensures the data directory and target load history CSV file exist with correct headers."""
        try:
            if not os.path.exists(self.data_directory):
                os.makedirs(self.data_directory)
            if not os.path.exists(self.csv_filepath):
                with open(self.csv_filepath, mode="w", newline="", encoding="utf-8") as csv_file:
                    writer = csv.writer(csv_file)
                    writer.writerow([
                        "Pickup Date", "Order Number", "Gross Revenue", "Loaded Miles", 
                        "Empty Miles", "Fuel Cost", "Total Expenses", "Break-Even CPM", "Net Profit"
                    ])
        except Exception as csv_error:
            print(f"Warning: Failed to initialize spreadsheet ledger file: {csv_error}")

    def save_current_as_defaults(self):
        """Gathers dynamic and static states and dumps them back to the configuration JSON file."""
        try:
            self.app_settings["core_metrics"]["pickup_date"] = self.var_pickup_date.get()
            self.app_settings["core_metrics"]["loaded_miles"] = self.var_loaded_miles.get()
            self.app_settings["core_metrics"]["empty_miles"] = self.var_empty_miles.get()
            self.app_settings["core_metrics"]["total_gallons"] = self.var_total_gallons.get()
            self.app_settings["window_width"] = self.winfo_width()
            self.app_settings["window_height"] = self.winfo_height()

            # Map dynamic input fields state changes back to default keys lists
            for revenue_item in self.app_settings.get("revenue_line_items", []):
                item_key = revenue_item.get("key")
                if item_key in self.revenue_variables:
                    revenue_item["default_value"] = self.revenue_variables[item_key].get()

            for charge_item in self.app_settings.get("charge_line_items", []):
                item_key = charge_item.get("key")
                if item_key in self.charge_variables:
                    charge_item["default_value"] = self.charge_variables[item_key].get()

            with open(self.config_filepath, "w") as update_file:
                json.dump(self.app_settings, update_file, indent=4)
            messagebox.showinfo("Configuration Saved", "Current entry field values committed as new JSON defaults.")
        except Exception as save_error:
            messagebox.showerror("Save Failure", f"An error occurred saving configuration variables:\n{save_error}")

    def create_widgets(self):
        """Creates the split grid layout, dynamic control fields, and historical display trees."""
        self.grid_columnconfigure(0, weight=1, minsize=480)
        self.grid_columnconfigure(1, weight=2, minsize=740)
        self.grid_rowconfigure(0, weight=1)

        # ==========================================
        # LEFT PANEL: DYNAMIC SCROLLABLE ENTRY FIELDS
        # ==========================================
        left_canvas_frame = ttk.Frame(self, padding="10")
        left_canvas_frame.grid(row=0, column=0, sticky="nsew")
        
        input_scroll_canvas = tk.Canvas(left_canvas_frame, bg="#1e1e1e", highlightthickness=0)
        scrollbar_widget = ttk.Scrollbar(left_canvas_frame, orient="vertical", command=input_scroll_canvas.yview)
        scrollable_input_frame = ttk.Frame(input_scroll_canvas)

        scrollable_input_frame.bind(
            "<Configure>",
            lambda event: input_scroll_canvas.configure(scrollregion=input_scroll_canvas.bbox("all"))
        )
        input_scroll_canvas.create_window((0, 0), window=scrollable_input_frame, anchor="nw")
        input_scroll_canvas.configure(yscrollcommand=scrollbar_widget.set)

        input_scroll_canvas.pack(side="left", fill="both", expand=True)
        scrollbar_widget.pack(side="right", fill="y")

        scrollable_input_frame.grid_columnconfigure(0, weight=1)

        input_header = ttk.Label(
            scrollable_input_frame, text="Dynamic Statement Matrix", font=("Arial", 14, "bold"), foreground="#8ec07c"
        )
        input_header.pack(anchor="w", pady=(0, 10))

        def auto_highlight_entry_contents(event):
            """Triggered when user clicks/tabs into entry box; highlights all characters for swift overwriting."""
            event.widget.selection_range(0, tk.END)

        def append_rendered_input_row(parent_frame, title, variable_hook):
            row_frame = ttk.Frame(parent_frame)
            row_frame.pack(fill="x", pady=2)
            label_widget = ttk.Label(row_frame, text=title, font=("Arial", 9), foreground="#ffffff")
            label_widget.pack(side="left")
            entry_widget = ttk.Entry(row_frame, textvariable=variable_hook, font=("Arial", 9), width=12, style="TEntry")
            entry_widget.pack(side="right")
            
            # Attach operational event bindings to handle quick entry behaviors
            entry_widget.bind("<FocusIn>", auto_highlight_entry_contents)

        # Render Tracking Metadata
        metadata_group = ttk.LabelFrame(scrollable_input_frame, text=" Core Load Tracking ", padding="8")
        metadata_group.pack(fill="x", pady=4)
        append_rendered_input_row(metadata_group, "Order / Load #:", self.var_order_number)
        append_rendered_input_row(metadata_group, "Pickup Date (YYYY-MM-DD):", self.var_pickup_date)
        append_rendered_input_row(metadata_group, "Loaded Trip Miles (mi):", self.var_loaded_miles)
        append_rendered_input_row(metadata_group, "Empty / Deadhead Miles (mi):", self.var_empty_miles)
        append_rendered_input_row(metadata_group, "Total Gallons (gal):", self.var_total_gallons)

        # Dynamically build revenue rows from configuration arrays
        revenue_group = ttk.LabelFrame(scrollable_input_frame, text=" Revenue Statement Line-Items ", padding="8")
        revenue_group.pack(fill="x", pady=4)
        for revenue_item in self.app_settings.get("revenue_line_items", []):
            item_key = revenue_item.get("key")
            item_label = revenue_item.get("label", "Unknown Revenue")
            if item_key in self.revenue_variables:
                append_rendered_input_row(revenue_group, item_label, self.revenue_variables[item_key])

        # Dynamically build charges rows from configuration arrays
        charges_group = ttk.LabelFrame(scrollable_input_frame, text=" Charges & Deductions Line-Items ", padding="8")
        charges_group.pack(fill="x", pady=4)
        for charge_item in self.app_settings.get("charge_line_items", []):
            item_key = charge_item.get("key")
            item_label = charge_item.get("label", "Unknown Charge")
            if item_key in self.charge_variables:
                append_rendered_input_row(charges_group, item_label, self.charge_variables[item_key])

        # Control Buttons
        button_frame = ttk.Frame(scrollable_input_frame)
        button_frame.pack(fill="x", pady=10)
        button_frame.grid_columnconfigure(0, weight=1)
        button_frame.grid_columnconfigure(1, weight=1)

        reload_button = ttk.Button(button_frame, text="Reload Config File", command=self.reload_from_disk)
        reload_button.grid(row=0, column=0, padx=(0, 2), sticky="ew")

        save_button = ttk.Button(button_frame, text="Save Fields to Config", command=self.save_current_as_defaults)
        save_button.grid(row=0, column=1, padx=(2, 0), sticky="ew")

        # Visualization Chart Area
        self.chart_container = ttk.LabelFrame(scrollable_input_frame, text=" Settlement Allocation Breakdown ($) ", padding="5")
        self.chart_container.pack(fill="both", expand=True, pady=5)
        
        self.figure = Figure(figsize=(4, 2.8), dpi=100, facecolor="#1e1e1e")
        self.ax = self.figure.add_subplot(111)
        self.ax.set_facecolor("#1e1e1e")
        
        self.canvas = FigureCanvasTkAgg(self.figure, master=self.chart_container)
        self.canvas.get_tk_widget().pack(fill="both", expand=True)

        # ==========================================
        # RIGHT PANEL: LOGISTICS LEDGER & PERFORMANCE
        # ==========================================
        right_frame = ttk.Frame(self, padding="15")
        right_frame.grid(row=0, column=1, sticky="nsew")
        
        right_header = ttk.Label(
            right_frame, text="Financial Performance & History", font=("Arial", 15, "bold"), foreground="#8ec07c"
        )
        right_header.pack(anchor="w", pady=(0, 10))

        kpi_container_frame = ttk.Frame(right_frame)
        kpi_container_frame.pack(fill="x", pady=(0, 5))
        kpi_container_frame.grid_columnconfigure(0, weight=1)
        kpi_container_frame.grid_columnconfigure(1, weight=1)

        totals_group = ttk.LabelFrame(kpi_container_frame, text=" Active Load Settlement Totals ", padding="10")
        totals_group.grid(row=0, column=0, sticky="nsew", padx=(0, 5))

        create_kpi_row(totals_group, "Calculated Gross Due Owner:", self.res_gross_due_owner, highlight=True, highlight_color="#83a598")
        create_kpi_row(totals_group, "Calculated Trip MPG:", self.res_calculated_mpg, highlight=True, highlight_color="#8ec07c")
        create_kpi_row(totals_group, "Avg Price Per Gallon:", self.res_price_per_gallon)
        create_kpi_row(totals_group, "Total Settlement Deductions:", self.res_total_cost)
        create_kpi_row(totals_group, "Net Take-Home Check Profit:", self.res_net_profit, highlight=True, highlight_color="#b8bb26")

        mile_group = ttk.LabelFrame(kpi_container_frame, text=" Active Load Mileage Performance ", padding="10")
        mile_group.grid(row=0, column=1, sticky="nsew", padx=(5, 0))

        create_kpi_row(mile_group, "Gross Revenue Per Mile:", self.res_revenue_per_mile)
        create_kpi_row(mile_group, "Break-Even Cost Per Mile:", self.res_break_even_cpm, highlight=True, highlight_color="#fabd2f")
        create_kpi_row(mile_group, "Total Cost Per Mile (CPM):", self.res_cost_per_mile)
        create_kpi_row(mile_group, "Net Profit Per Mile:", self.res_profit_per_mile, highlight=True, highlight_color="#b8bb26")

        # Cumulative business metrics panel (YTD totals compiled from CSV rows)
        ytd_summary_group = ttk.LabelFrame(right_frame, text=" Cumulative Business Performance Summary (YTD Ledger Totals) ", padding="10")
        ytd_summary_group.pack(fill="x", pady=(5, 10))
        
        ytd_column_1 = ttk.Frame(ytd_summary_group)
        ytd_column_1.pack(side="left", expand=True, fill="x", padx=5)
        create_kpi_row(ytd_column_1, "Total Gross Rev:", self.res_ytd_gross_revenue, highlight=True, highlight_color="#83a598")
        create_kpi_row(ytd_column_1, "Total Expenses:", self.res_ytd_total_expenses)

        ytd_column_2 = ttk.Frame(ytd_summary_group)
        ytd_column_2.pack(side="left", expand=True, fill="x", padx=5)
        create_kpi_row(ytd_column_2, "Total Net Profit:", self.res_ytd_net_profit, highlight=True, highlight_color="#b8bb26")
        create_kpi_row(ytd_column_2, "Total Fuel Cost:", self.res_ytd_fuel_cost)

        ytd_column_3 = ttk.Frame(ytd_summary_group)
        ytd_column_3.pack(side="left", expand=True, fill="x", padx=5)
        create_kpi_row(ytd_column_3, "Total Loaded Mi:", self.res_ytd_loaded_miles)
        create_kpi_row(ytd_column_3, "Total Empty Mi:", self.res_ytd_empty_miles)

        ytd_column_4 = ttk.Frame(ytd_summary_group)
        ytd_column_4.pack(side="left", expand=True, fill="x", padx=5)
        create_kpi_row(ytd_column_4, "Overall Business CPM:", self.res_ytd_overall_cost_per_mile, highlight=True, highlight_color="#fabd2f")

        # Historical tree matrix panel
        history_group = ttk.LabelFrame(right_frame, text=" Year-to-Date CSV Load Registry ", padding="10")
        history_group.pack(fill="both", expand=True)

        ledger_action_bar = ttk.Frame(history_group)
        ledger_action_bar.pack(fill="x", pady=(0, 8))

        commit_load_button = ttk.Button(ledger_action_bar, text="Commit Current Load to CSV", command=self.append_current_load_to_csv)
        commit_load_button.pack(side="left", padx=(0, 5))

        remove_load_button = ttk.Button(ledger_action_bar, text="Delete Selected Record", command=self.delete_selected_csv_record)
        remove_load_button.pack(side="left")

        treeview_columns = ("date", "order_id", "gross", "loaded_miles", "empty_miles", "fuel_cost", "total_cost", "break_even", "net_profit")
        self.ledger_treeview = ttk.Treeview(history_group, columns=treeview_columns, show="headings", selectmode="browse")
        
        self.ledger_treeview.heading("date", text="Pickup Date")
        self.ledger_treeview.heading("order_id", text="Order / Load #")
        self.ledger_treeview.heading("gross", text="Gross Rev")
        self.ledger_treeview.heading("loaded_miles", text="Loaded Mi")
        self.ledger_treeview.heading("empty_miles", text="Empty Mi")
        self.ledger_treeview.heading("fuel_cost", text="Fuel Cost")
        self.ledger_treeview.heading("total_cost", text="Total Deduct")
        self.ledger_treeview.heading("break_even", text="Break-Even")
        self.ledger_treeview.heading("net_profit", text="Net Take-Home")

        self.ledger_treeview.column("date", width=90, anchor="center")
        self.ledger_treeview.column("order_id", width=95, anchor="center")
        self.ledger_treeview.column("gross", width=90, anchor="center")
        self.ledger_treeview.column("loaded_miles", width=75, anchor="center")
        self.ledger_treeview.column("empty_miles", width=75, anchor="center")
        self.ledger_treeview.column("fuel_cost", width=90, anchor="center")
        self.ledger_treeview.column("total_cost", width=90, anchor="center")
        self.ledger_treeview.column("break_even", width=90, anchor="center")
        self.ledger_treeview.column("net_profit", width=105, anchor="center")

        tree_scroll = ttk.Scrollbar(history_group, orient="vertical", command=self.ledger_treeview.yview)
        self.ledger_treeview.configure(yscrollcommand=tree_scroll.set)

        tree_scroll.pack(side="right", fill="y")
        self.ledger_treeview.pack(fill="both", expand=True)

    def calculate_metrics(self, *args):
        """Processes calculations loop by parsing dynamic storage dictionaries accurately."""
        try:
            loaded_miles = self.var_loaded_miles.get()
            empty_miles = self.var_empty_miles.get()
            gallons = self.var_total_gallons.get()
            
            total_miles = loaded_miles + empty_miles

            base_revenue_val = self.revenue_variables.get("base_revenue", tk.DoubleVar()).get()
            owner_percentage_rate = self.revenue_variables.get("owner_rate", tk.DoubleVar()).get()

            # Process baseline gross contractual percentages 
            gross_due_owner = base_revenue_val * owner_percentage_rate
            for key, tkinter_variable in self.revenue_variables.items():
                if key not in ["base_revenue", "owner_rate"]:
                    gross_due_owner += tkinter_variable.get()

            # Sum up dynamic charges variables array elements
            total_expenses = 0.0
            for key, tkinter_variable in self.charge_variables.items():
                total_expenses += tkinter_variable.get()

            net_profit = gross_due_owner - total_expenses

            if total_miles <= 0:
                self.set_blank_results("Enter Valid Inputs")
                self.res_gross_due_owner.set(f"${gross_due_owner:,.2f}")
                self.clear_chart_canvas()
                return

            # Safety handling when there are no gallons logged for the load
            if gallons > 0:
                calculated_mpg = total_miles / gallons
                self.res_calculated_mpg.set(f"{calculated_mpg:.2f} MPG")
            else:
                self.res_calculated_mpg.set("$0.00 (No Fuel)")

            tch_fuel_cost = self.charge_variables.get("charge_tch_fuel", tk.DoubleVar()).get()
            
            # Safety handling when no gallons or fuel charges exist to prevent zero division
            if gallons > 0 and tch_fuel_cost > 0:
                price_per_gallon = tch_fuel_cost / gallons
                self.res_price_per_gallon.set(f"${price_per_gallon:.3f} / gal")
            else:
                self.res_price_per_gallon.set("$0.000 / gal")

            revenue_per_mile = gross_due_owner / total_miles
            cost_per_mile = total_expenses / total_miles
            break_even_cpm = total_expenses / total_miles
            profit_per_mile = net_profit / total_miles

            self.res_gross_due_owner.set(f"${gross_due_owner:,.2f}")
            self.res_total_cost.set(f"${total_expenses:,.2f}")
            self.res_net_profit.set(f"${net_profit:,.2f}")

            self.res_revenue_per_mile.set(f"${revenue_per_mile:.2f} / mi")
            self.res_cost_per_mile.set(f"${cost_per_mile:.2f} / mi")
            self.res_break_even_cpm.set(f"${break_even_cpm:.2f} / mi")
            self.res_profit_per_mile.set(f"${profit_per_mile:.2f} / mi")

            misc_fees_val = self.charge_variables.get("charge_misc", tk.DoubleVar()).get() if "charge_misc" in self.charge_variables else 0.0
            
            # Sum up transaction fees if present to separate them cleanly in the visualization
            tch_cwe_val = self.charge_variables.get("charge_tch_cwe_sc", tk.DoubleVar()).get() if "charge_tch_cwe_sc" in self.charge_variables else 0.0
            tch_trans_val = self.charge_variables.get("charge_tch_transact_sc", tk.DoubleVar()).get() if "charge_tch_transact_sc" in self.charge_variables else 0.0
            combined_misc_fees = misc_fees_val + tch_cwe_val + tch_trans_val

            fixed_holds_sum = total_expenses - tch_fuel_cost - combined_misc_fees
            self.update_chart_visualization(tch_fuel_cost, fixed_holds_sum, combined_misc_fees, net_profit)

        except tk.TclError:
            self.set_blank_results("Typing...")
            self.clear_chart_canvas()

    def update_chart_visualization(self, fuel, fixed, misc, net):
        """Plots current metrics array onto the embedded canvas framework elements."""
        self.ax.clear()

        categories = ["Fuel Cost", "Holds/Ins", "Misc/Fees", "Net Check"]
        values = [fuel, fixed, misc, net]
        
        profit_color = "#b8bb26" if net >= 0 else "#fb4934"
        colors = ["#fe8019", "#83a598", "#fabd2f", profit_color]

        bars = self.ax.bar(categories, values, color=colors, width=0.55)
        
        self.ax.spines["top"].set_visible(False)
        self.ax.spines["right"].set_visible(False)
        self.ax.spines["left"].set_color("#504945")
        self.ax.spines["bottom"].set_color("#504945")
        self.ax.yaxis.grid(True, linestyle="--", alpha=0.3, color="#a89984")
        self.ax.set_axisbelow(True)
        
        self.ax.tick_params(axis="both", labelsize=8, colors="#ffffff")
        self.ax.axhline(0, color="#7c6f64", linewidth=0.8)

        for bar in bars:
            height = bar.get_height()
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

        min_y = min(0, net) * 1.25 if net < 0 else 0
        max_y = max(values) * 1.20
        self.ax.set_ylim(min_y, max_y)
        self.figure.tight_layout()
        self.canvas.draw()

    def append_current_load_to_csv(self):
        """Extracts values and builds ledger outputs into the history spreadsheet storage in date order."""
        try:
            order_id = self.var_order_number.get().strip()
            pickup_date = self.var_pickup_date.get().strip()
            loaded_miles = self.var_loaded_miles.get()
            empty_miles = self.var_empty_miles.get()
            gallons = self.var_total_gallons.get()
            
            total_miles = loaded_miles + empty_miles

            if not order_id:
                messagebox.showwarning("Validation Error", "Please provide a valid Order / Load Number reference.")
                return

            if not pickup_date:
                messagebox.showwarning("Validation Error", "Please provide a valid Pickup Date reference.")
                return

            if total_miles <= 0:
                messagebox.showwarning("Calculation Error", "Verify operational tracking mileage criteria is greater than zero.")
                return

            base_revenue_val = self.revenue_variables.get("base_revenue", tk.DoubleVar()).get()
            owner_percentage_rate = self.revenue_variables.get("owner_rate", tk.DoubleVar()).get()
            gross_due_owner = base_revenue_val * owner_percentage_rate
            for key, tkinter_variable in self.revenue_variables.items():
                if key not in ["base_revenue", "owner_rate"]:
                    gross_due_owner += tkinter_variable.get()

            total_expenses = 0.0
            for key, tkinter_variable in self.charge_variables.items():
                total_expenses += tkinter_variable.get()

            break_even_cpm = total_expenses / total_miles
            net_profit = gross_due_owner - total_expenses
            tch_fuel_cost = self.charge_variables.get("charge_tch_fuel", tk.DoubleVar()).get()

            new_row_data = [
                pickup_date, order_id, f"{gross_due_owner:.2f}", f"{loaded_miles:.1f}", f"{empty_miles:.1f}",
                f"{tch_fuel_cost:.2f}", f"{total_expenses:.2f}",
                f"{break_even_cpm:.2f}", f"{net_profit:.2f}"
            ]

            # Read all existing rows to sort them on disk with the new entry
            all_records = []
            header = ["Pickup Date", "Order Number", "Gross Revenue", "Loaded Miles", "Empty Miles", "Fuel Cost", "Total Expenses", "Break-Even CPM", "Net Profit"]
            
            if os.path.exists(self.csv_filepath):
                with open(self.csv_filepath, mode="r", newline="", encoding="utf-8") as csv_file:
                    reader = csv.reader(csv_file)
                    try:
                        header = next(reader)
                    except StopIteration:
                        pass
                    for row in reader:
                        if row:
                            all_records.append(row)

            all_records.append(new_row_data)

            # Sort records chronologically before writing back to disk
            def parse_row_date(data_row):
                try:
                    return datetime.strptime(data_row[0].strip(), "%Y-%m-%d")
                except ValueError:
                    return datetime.min

            all_records.sort(key=parse_row_date)

            with open(self.csv_filepath, mode="w", newline="", encoding="utf-8") as csv_file:
                writer = csv.writer(csv_file)
                writer.writerow(header)
                writer.writerows(all_records)

            self.refresh_historical_ledger_display()
            messagebox.showinfo("Ledger Updated", f"Load record {order_id} committed and sorted successfully in CSV ledger.")

        except tk.TclError:
            messagebox.showerror("Parsing Failure", "Ensure all configuration box fields are valid numbers before logging.")

    def delete_selected_csv_record(self):
        """Removes selected indexed row nodes entries from database history ledger file."""
        selected_row = self.ledger_treeview.selection()
        if not selected_row:
            messagebox.showwarning("Selection Required", "Please click a row inside the spreadsheet matrix.")
            return

        target_row_index = self.ledger_treeview.index(selected_row[0])
        
        try:
            all_records = []
            with open(self.csv_filepath, mode="r", newline="", encoding="utf-8") as csv_file:
                reader = csv.reader(csv_file)
                header = next(reader)
                for row in reader:
                    if row:
                        all_records.append(row)

            # Keep synchronization aligned with chronological sorting order
            def parse_row_date_for_index(data_row):
                try:
                    return datetime.strptime(data_row[0].strip(), "%Y-%m-%d")
                except ValueError:
                    return datetime.min

            all_records.sort(key=parse_row_date_for_index)

            if 0 <= target_row_index < len(all_records):
                del all_records[target_row_index]
            
            with open(self.csv_filepath, mode="w", newline="", encoding="utf-8") as csv_file:
                writer = csv.writer(csv_file)
                writer.writerow(header)
                writer.writerows(all_records)

            self.refresh_historical_ledger_display()
            messagebox.showinfo("Record Dropped", "Target load record removed successfully.")
        except Exception as removal_error:
            messagebox.showerror("Deletion Error", f"An anomaly occurred modifying CSV database rows:\n{removal_error}")

    def refresh_historical_ledger_display(self):
        """Parses row values, sorts them chronologically by date, sums cumulative values, and updates components."""
        self.ledger_treeview.delete(*self.ledger_treeview.get_children())
        if not os.path.exists(self.csv_filepath):
            return

        try:
            collected_rows = []
            with open(self.csv_filepath, mode="r", newline="", encoding="utf-8") as csv_file:
                reader = csv.reader(csv_file)
                next(reader)  # Skip CSV header line
                
                for row in reader:
                    if len(row) >= 9:
                        collected_rows.append(row)
            
            # Sorting engine key function to handle date format safely
            def parse_entry_date(data_row):
                try:
                    return datetime.strptime(data_row[0].strip(), "%Y-%m-%d")
                except ValueError:
                    return datetime.min  # Fallback for unparseable entries

            # Sort row array records from oldest date to newest date
            collected_rows.sort(key=parse_entry_date)

            # Initialize tracking containers for cumulative summaries
            running_gross_revenue = 0.0
            running_total_expenses = 0.0
            running_net_profit = 0.0
            running_fuel_cost = 0.0
            running_loaded_miles = 0.0
            running_empty_miles = 0.0

            # Populate Treeview matrix with the ordered records and gather sums
            for row in collected_rows:
                self.ledger_treeview.insert(
                    "", "end",
                    values=(
                        row[0], row[1], f"${float(row[2]):,.2f}", f"{float(row[3]):,.1f} mi", f"{float(row[4]):,.1f} mi",
                        f"${float(row[5]):,.2f}", f"${float(row[6]):,.2f}",
                        f"${float(row[7]):.2f} / mi", f"${float(row[8]):,.2f}"
                    )
                )
                try:
                    running_gross_revenue += float(row[2])
                    running_loaded_miles += float(row[3])
                    running_empty_miles += float(row[4])
                    running_fuel_cost += float(row[5])
                    running_total_expenses += float(row[6])
                    running_net_profit += float(row[8])
                except ValueError:
                    pass

            # Update the user interface cumulative summary tracking variables
            self.res_ytd_gross_revenue.set(f"${running_gross_revenue:,.2f}")
            self.res_ytd_total_expenses.set(f"${running_total_expenses:,.2f}")
            self.res_ytd_net_profit.set(f"${running_net_profit:,.2f}")
            self.res_ytd_fuel_cost.set(f"${running_fuel_cost:,.2f}")
            self.res_ytd_loaded_miles.set(f"{running_loaded_miles:,.1f} mi")
            self.res_ytd_empty_miles.set(f"{running_empty_miles:,.1f} mi")

            running_total_miles = running_loaded_miles + running_empty_miles
            if running_total_miles > 0:
                overall_cost_per_mile = running_total_expenses / running_total_miles
                self.res_ytd_overall_cost_per_mile.set(f"${overall_cost_per_mile:.2f} / mi")
            else:
                self.res_ytd_overall_cost_per_mile.set("$0.00 / mi")

        except Exception as read_error:
            print(f"Warning: Failed reading load_history.csv ledger data: {read_error}")

    def clear_chart_canvas(self):
        """Wipes plot states fields area nodes from interface view display frame windows."""
        self.ax.clear()
        self.ax.axis("off")
        self.canvas.draw()

    def set_blank_results(self, message):
        """Sets result outputs data parameters values strings to processing statuses placeholders."""
        self.res_calculated_mpg.set(message)
        self.res_price_per_gallon.set(message)
        self.res_total_cost.set(message)
        self.res_net_profit.set(message)
        self.res_revenue_per_mile.set(message)
        self.res_cost_per_mile.set(message)
        self.res_break_even_cpm.set(message)
        self.res_profit_per_mile.set(message)

    def reload_from_disk(self):
        """Destroys current configuration instances runtime frames and forces application reboot refresh."""
        messagebox.showinfo("Reloading Settings", "Re-reading configuration parameters. This window will now refresh.")
        self.destroy()
        reboot_instance = TruckingDashboard()
        reboot_instance.mainloop()


def create_kpi_row(parent, title, text_var, highlight=False, highlight_color="#ffffff"):
    """Helper method to draw consistently stylized tracking value labels."""
    frame = ttk.Frame(parent)
    frame.pack(fill="x", pady=4)
    font_style = ("Arial", 10, "bold") if highlight else ("Arial", 10)
    lbl_color = highlight_color if highlight else "#b0b0b0"
    val_color = highlight_color if highlight else "#ffffff"

    label_widget = ttk.Label(frame, text=title, font=font_style, foreground=lbl_color)
    label_widget.pack(side="left")
    value_widget = ttk.Label(frame, textvariable=text_var, font=font_style, foreground=val_color)
    value_widget.pack(side="right")


if __name__ == "__main__":
    app = TruckingDashboard()
    app.mainloop()