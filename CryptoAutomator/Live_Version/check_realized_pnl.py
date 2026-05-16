"""
Date: 2026-01-05
Script Name: check_realized_pnl.py
Author: omegazyph
Updated: 2026-05-16
Description: 
    On-demand standalone script to safely read live_trade_log.csv,
    calculate total lifetime realized profit/loss, and display the metrics.
    Keeps main_bot_loop.py clean and minimizes SSD drive wear.
"""

import os
import csv
from pathlib import Path
from colorama import init, Fore, Style

# Initialize Colorama for clean terminal feedback
init(autoreset=True, strip=False)

class DisplayColors:
    HEADER_CYAN = Fore.CYAN + Style.BRIGHT
    SUCCESS_GREEN = Fore.GREEN + Style.BRIGHT
    DANGER_RED = Fore.RED + Style.BRIGHT
    RESET_STYLE = Style.RESET_ALL

def calculate_lifetime_metrics():
    """Reads the trade log precisely once to calculate and print net realized gains."""
    base_directory = Path(__file__).resolve().parent
    log_path = base_directory / "live_trade_log.csv"
    
    if not os.path.isfile(log_path):
        print(f"{DisplayColors.DANGER_RED}Error: live_trade_log.csv not found in {base_directory}")
        return

    lifetime_pnl = 0.0
    completed_trades_count = 0
    running_buy_costs = {}

    print(f"\n{DisplayColors.HEADER_CYAN}==========================================================================")
    print(f" {DisplayColors.HEADER_CYAN}WAYNE'S SENTINEL LEDGER | CLOSED POSITIONS AUDIT")
    print(f"{DisplayColors.HEADER_CYAN}==========================================================================")
    print(f"{'SYMBOL':<12} {'COST BASIS':<15} {'REVENUE':<15} {'NET PROFIT/LOSS'}")
    print("-" * 74)

    try:
        with open(log_path, mode="r", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            
            for row in reader:
                symbol = row["Symbol"].strip()
                side = row["Side"].strip()
                price = float(row["Price"])
                amount = float(row["Amount"])
                
                if side == "LIVE_BUY":
                    if symbol not in running_buy_costs:
                        running_buy_costs[symbol] = []
                    running_buy_costs[symbol].append({"amount": amount, "price": price})
                
                elif side == "LIVE_SELL":
                    if symbol in running_buy_costs and running_buy_costs[symbol]:
                        sell_value = amount * price
                        allocated_buy_cost = 0.0
                        remaining_sell_amount = amount
                        
                        while remaining_sell_amount > 0 and running_buy_costs[symbol]:
                            oldest_buy = running_buy_costs[symbol][0]
                            if oldest_buy["amount"] <= remaining_sell_amount:
                                allocated_buy_cost += oldest_buy["amount"] * oldest_buy["price"]
                                remaining_sell_amount -= oldest_buy["amount"]
                                running_buy_costs[symbol].pop(0)
                            else:
                                allocated_buy_cost += remaining_sell_amount * oldest_buy["price"]
                                oldest_buy["amount"] -= remaining_sell_amount
                                remaining_sell_amount = 0.0
                        
                        trade_pnl = sell_value - allocated_buy_cost
                        lifetime_pnl += trade_pnl
                        completed_trades_count += 1
                        
                        pnl_color = DisplayColors.SUCCESS_GREEN if trade_pnl >= 0 else DisplayColors.DANGER_RED
                        print(f"{symbol:<12} ${allocated_buy_cost:<14.2f} ${sell_value:<14.2f} {pnl_color}${trade_pnl:+.2f}")
                        
    except Exception as error_message:
        print(f"{DisplayColors.DANGER_RED}Error parsing file: {error_message}")
        return

    total_pnl_color = DisplayColors.SUCCESS_GREEN if lifetime_pnl >= 0 else DisplayColors.DANGER_RED
    print(f"{DisplayColors.HEADER_CYAN}==========================================================================")
    print(f" Total Completed Trades Audited: {completed_trades_count}")
    print(f" Net Lifetime Realized Profit:   {total_pnl_color}${lifetime_pnl:+.2f}{DisplayColors.RESET_STYLE}")
    print(f"{DisplayColors.HEADER_CYAN}==========================================================================")

if __name__ == "__main__":
    calculate_lifetime_metrics()