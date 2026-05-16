"""
Date: 2026-01-05
Script Name: main_bot_loop.py
Author: omegazyph
Updated: 2026-05-01
Description: 
    Wayne's LIVE Trading Bot for Crypto.com.
    Strategy: Buy at Lower Bollinger Band with Trailing Buy bounce.
    Strategy: Sell at Upper Bollinger Band with Trailing Stop drop.
"""

import ccxt
import time
import os
import json
import csv
import pandas as pd
import ctypes
from pathlib import Path
from dotenv import load_dotenv
from colorama import init, Fore, Style

# Initialize Colorama for the terminal display
init(autoreset=True, strip=False)

# --- WINDOWS POWER MANAGEMENT ---
EXECUTION_STATE_CONTINUOUS = 0x80000000
EXECUTION_STATE_SYSTEM_REQUIRED = 0x00000001
def prevent_system_sleep():
    if os.name == 'nt':
        try:
            # Re-enabled the thread state to ensure your Lenovo Legion stays awake
            ctypes.windll.kernel32.SetThreadExecutionState(EXECUTION_STATE_SYSTEM_REQUIRED | EXECUTION_STATE_CONTINUOUS)
        except Exception:
            pass

def allow_system_sleep():
    if os.name == 'nt':
        try:
            ctypes.windll.kernel32.SetThreadExecutionState(EXECUTION_STATE_CONTINUOUS)
        except Exception:
            pass

# --- DIRECTORY AND FILE PATHS ---
current_script_path = Path(__file__).resolve()
project_root_directory = current_script_path.parent.parent
environment_file_path = project_root_directory / ".env"
load_dotenv(dotenv_path=environment_file_path)

class InterfaceColors:
    HEADER_CYAN = Fore.CYAN + Style.BRIGHT
    SUCCESS_GREEN = Fore.GREEN + Style.BRIGHT
    WARNING_YELLOW = Fore.YELLOW
    DANGER_RED = Fore.RED + Style.BRIGHT
    INFO_BLUE = Fore.BLUE + Style.BRIGHT
    RESET_STYLE = Style.RESET_ALL

def clear_terminal_screen():
    if os.name == 'nt':
        os.system("cls")
    else:
        os.system("clear")

def get_required_file_paths():
    configuration_file_path = project_root_directory / "config.json"
    trading_activity_log_path = project_root_directory / "live_trade_log.csv"
    error_log_path = project_root_directory / "error_log.csv"
    return configuration_file_path, trading_activity_log_path, error_log_path

def load_trading_configuration():
    configuration_path, _, _ = get_required_file_paths()
    with open(configuration_path, mode="r", encoding="utf-8") as file:
        return json.load(file)

def record_successful_trade(symbol, side, amount, price, remaining_balance, note):
    _, log_path, _ = get_required_file_paths()
    time_full = time.strftime("%Y-%m-%d %H:%M:%S")
    file_exists = os.path.isfile(log_path)
    
    with open(log_path, mode="a", newline="", encoding="utf-8") as csv_file:
        writer = csv.writer(csv_file)
        if not file_exists:
            writer.writerow(["Timestamp", "Symbol", "Side", "Amount", "Price", "Wallet", "Note"])
        
        writer.writerow([time_full, symbol, side, f"{amount:.8f}", f"{price:.8f}", f"{remaining_balance:.2f}", note])
        csv_file.flush()
        os.fsync(csv_file.fileno())

def record_error_to_log(error_type, error_message):
    """Saves errors to a structed CSV file for troubleshooting."""
    _, _, error_log_path = get_required_file_paths()
    time_stamp = time.strftime("%Y-%m-%d %H:%M:%S")
    file_exists = os.path.isfile(error_log_path)

    #------ new code -----
    # --cleaning Logic ---
    # Takes only the frist line of error to avid massive HTML 502/Cloud fare blocks
    msg_str = str(error_message).strip()
    clean_msg = msg_str.split('\n')[0]
    if len(clean_msg) > 150:
        clean_msg = clean_msg[:147] + "..."
    #--------------------------------------------

    try:
        # Append the new error
        with open(error_log_path, mode="a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            
            # add the header only if the file is being created for the first time
            if not file_exists:
                writer.writerow(["Timestamp", "Error Type", "Message"])
            writer.writerow([time_stamp, error_type, clean_msg])

        # self-cleaning: keep only last 50 errors
        if os.path.exists(error_log_path):
            with open(error_log_path, mode="r", encoding="utf-8") as f:
                lines = list(csv.reader(f))

                #if log exceeds 50 error (plus header), rewrite with only the newest 50
                if len(lines) > 51:
                    header = lines[0]
                    new_data = lines[-50:]
                    with open(error_log_path, mode="w", newline="", encoding="utf-8") as f_new:
                        writer = csv.writer(f_new)
                        writer.writerow(header)
                        writer.writerows(new_data)

    except Exception:
        pass # Prevent the bot from crashing if the disk is busy

def get_recent_activity_from_csv():
    _, log_path, _ = get_required_file_paths()
    recent_lines = []
    if not os.path.isfile(log_path):
        return recent_lines
    try:
        with open(log_path, mode="r", encoding="utf-8") as file:
            reader = list(csv.reader(file))
            if len(reader) <= 1:
                return recent_lines
            data_rows = reader[1:]
            for row in data_rows[-10:]:
                timestamp = row[0].split(" ")[1]
                side = row[2]
                symbol = row[1]
                note = row[6]
                color = InterfaceColors.SUCCESS_GREEN if "BUY" in side else InterfaceColors.DANGER_RED
                recent_lines.insert(0, f"[{timestamp}] {color}{side:<10}{InterfaceColors.RESET_STYLE} {symbol} {note}")
    except Exception as error_message:
        print(f"Activity Log Error {error_message}")
        record_error_to_log("Activity_LOG", str(error_message))
            
    return recent_lines

def restore_portfolio_from_log():
    _, log_path, _ = get_required_file_paths()
    active_holdings = {}
    if not os.path.isfile(log_path):
        return active_holdings
    try:
        with open(log_path, mode="r", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for row in reader:
                symbol = row["Symbol"].strip()
                side = row["Side"].strip()
                price = float(row["Price"])
                amount = float(row["Amount"])

                if side == "LIVE_BUY":
                    if symbol not in active_holdings:
                        active_holdings[symbol] = {
                            "status": "HOLDING", 
                            "coins": 0.0, 
                            "total_cost": 0.0,
                            "highest_seen": 0.0,
                            "lowest_seen_price": 0.0
                        }
                    active_holdings[symbol]["status"] = "HOLDING"
                    active_holdings[symbol]["coins"] += amount
                    active_holdings[symbol]["total_cost"] += (amount * price)
                elif side == "LIVE_SELL":
                    active_holdings[symbol] = {
                        "status": "WAITING", 
                        "coins": 0.0, 
                        "total_cost": 0.0,
                        "highest_seen": 0.0,
                        "lowest_seen_price": 0.0
                    }
    except Exception as error_message:
        print(f"somthing worng in restore_portfolio_from_log {error_message}")
        record_error_to_log("RESTORE_ERROR", str(error_message))
    return active_holdings

def calculate_bollinger_bands(exchange, symbol, timeframe='15m', window=20):
    try:
        ohlcv = exchange.fetch_ohlcv(symbol, timeframe)
        df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
        df['sma'] = df['close'].rolling(window=window).mean()
        df['std'] = df['close'].rolling(window=window).std()
        df['upper'] = df['sma'] + (df['std'] * 2)
        df['lower'] = df['sma'] - (df['std'] * 2)
        latest = df.iloc[-1]
        return latest['lower'], latest['upper'], latest['close']
    except Exception as error_message:
        print(f"Bollinger Band Error: {error_message}")
        record_error_to_log("Bollinger Band Error", str(error_message))
        return None, None, None

def run_trading_engine():
    prevent_system_sleep()
    exchange_client = ccxt.cryptocom({
        "apiKey": os.getenv("CRYPTO_COM_KEY"),
        "secret": os.getenv("CRYPTO_COM_SECRET"),
        "enableRateLimit": True
    })

    # --- STARTUP Config ---
    current_portfolio = restore_portfolio_from_log()
    recent_activity_ram = get_recent_activity_from_csv()
    settings = load_trading_configuration()

    while True:
        try:
            
            trading_pairs_list = settings["trading_pairs"]
            global_settings = settings.get("global_settings", {})

            starting_bal = global_settings.get("starting_balance", 0.0)
            trade_dollar_amount = global_settings.get("trade_dollar_amount")
            check_interval_seconds = global_settings.get("check_interval_seconds")
            
            # gets the triling stop enable and disab;e form the json file
            trailing_stop_enabled = global_settings.get("trailing_stop_enabled", False)

            max_open_positions = global_settings.get("max_open_positions")

            trailing_buy_percentage = global_settings.get("trailing_buy_percentage", 1.0)

            # loads the value of the safety net
            safety_net = global_settings.get("safety_net")
            balance_response = exchange_client.fetch_balance()
            settled_usd = balance_response.get('total', {}).get("USD", 0.0)
            instant_credit = balance_response.get('total', {}).get("USD-CREDIT", 0.0)
            available_usd_cash = float(settled_usd + instant_credit)
            
            total_unrealized_profit_loss = 0.0
            dashboard_data_rows = []
            insufficient_funds_warning_active = False

            for pair_info in trading_pairs_list:
                if not pair_info.get("enabled", True):
                    continue
                
                symbol = pair_info["symbol"]
                base_asset = symbol.split('/')[0]
                active_symbol = f"{base_asset}/USD"
                
                lower_band, upper_band, current_price = calculate_bollinger_bands(exchange_client, active_symbol)
                
                if lower_band is None:
                    continue

                if active_symbol not in current_portfolio:
                    current_portfolio[active_symbol] = {
                        "status": "WAITING", 
                        "coins": 0.0, 
                        "total_cost": 0.0,
                        "highest_seen": 0.0,
                        "lowest_seen_price": 0.0
                    }
                
                state = current_portfolio[active_symbol]

                # --- WAITING STATE (SEARCHING FOR BUY) ---
                if state["status"] == "WAITING":
                    dashboard_data_rows.append(
                        f"{active_symbol:<10} "
                        f"{InterfaceColors.INFO_BLUE}{'SEARCHING':<15}{InterfaceColors.RESET_STYLE} "
                        f"${current_price:<11,.4f} "
                        f"BUY AT: ${lower_band:<10,.4f}"
                    )
                    
                    
                    
                    if current_price <= lower_band:
                        if current_price < state.get("lowest_seen_price", 999999.0):
                            state["lowest_seen_price"] = current_price

                    lowest_recorded_price = state.get("lowest_seen_price", 0.0)
                    if lowest_recorded_price > 0:
                        buy_trigger_level = lowest_recorded_price * (1 + (trailing_buy_percentage / 100))
                        
                        if trailing_stop_enabled and current_price >= buy_trigger_level:
                            coins_held = sum(1 for s in current_portfolio.values() if s["status"] == "HOLDING")
                            if available_usd_cash >= trade_dollar_amount and coins_held < max_open_positions:
                                try:
                                    quantity_to_purchase = trade_dollar_amount / current_price
                                    order_response = exchange_client.create_market_buy_order(active_symbol, quantity_to_purchase)
                                    
                                    execution_price = order_response.get('price') if order_response.get('price') else current_price
                                    execution_quantity = order_response.get('amount') if order_response.get('amount') else quantity_to_purchase

                                    record_successful_trade(
                                        active_symbol, 
                                        "LIVE_BUY", 
                                        execution_quantity, 
                                        execution_price, 
                                        available_usd_cash - trade_dollar_amount, 
                                        f"Trailing Buy: {trailing_buy_percentage}% bounce"
                                    )
                                    state["status"] = "HOLDING"
                                    state["coins"] = execution_quantity
                                    state["total_cost"] = execution_quantity * execution_price
                                    state["lowest_seen_price"] = 0.0

                                    # update the ram activity list
                                    timestamp = time.strftime("%H:%M:%S")
                                    recent_activity_ram.insert(0, f"[{timestamp}] {InterfaceColors.SUCCESS_GREEN}LIVE_BUY {InterfaceColors.RESET_STYLE} {active_symbol} Trailing Buy: {trailing_buy_percentage}% bounce")
                                    recent_activity_ram = recent_activity_ram[:10]


                                except Exception as error_message:
                                    print(f"Buy Error for {active_symbol}: {error_message}")
                                    record_error_to_log("BUY_ORDER", f"[{active_symbol}] {str(error_message)}")
                                    
                            else:
                                insufficient_funds_warning_active = True

                # --- HOLDING STATE (SEARCHING FOR SELL) ---
                elif state["status"] == "HOLDING":
                    average_entry = state["total_cost"] / state["coins"]
                    current_value = state["coins"] * current_price
                    pnl_dollars = current_value - state["total_cost"]
                    total_unrealized_profit_loss += pnl_dollars
                    pnl_pct = (pnl_dollars / state["total_cost"]) * 100

                    # Fixed: Pulling correct key 'trailing_stop_pct' from config
                    trailing_stop_percentage = global_settings.get("trailing_stop_pct")

                    # 1. Track peak
                    if current_price >= upper_band and pnl_pct >= safety_net:
                        if current_price > state.get("highest_seen", 0.0):
                            state["highest_seen"] = current_price

                    # 2. Check for drop from peak using percentage from config
                    highest_price = state.get("highest_seen", 0.0)
                    if highest_price > 0:
                        sell_trigger_level = highest_price * (1 - (trailing_stop_percentage / 100))
                        
                        if trailing_stop_enabled and current_price <= sell_trigger_level:
                            try:
                                sell_quantity = state["coins"]
                                order = exchange_client.create_market_sell_order(active_symbol, sell_quantity)
                                execution_price = order.get('price') if order.get('price') else current_price
                                
                                record_successful_trade(
                                    active_symbol, 
                                    "LIVE_SELL", 
                                    sell_quantity, 
                                    execution_price, 
                                    available_usd_cash + (sell_quantity * execution_price), 
                                    f"Trailing Stop Hit: {trailing_stop_percentage}% drop"
                                )
                                state["status"] = "WAITING"
                                state["coins"] = 0.0
                                state["total_cost"] = 0.0
                                state["highest_seen"] = 0.0

                                # Update the RAM activity list
                                timestamp = time.strftime("%H:%M:%S")
                                recent_activity_ram.insert(0, f"[{timestamp}] {InterfaceColors.DANGER_RED}LIVE_SELL {InterfaceColors.RESET_STYLE} {active_symbol} Trailing Stop Hit: {trailing_stop_percentage}% drop")
                                recent_activity_ram = recent_activity_ram[:10] # Keep only 10

                            except Exception as error_message:
                                print(f"Sell Error for {active_symbol}: {error_message}")
                                record_error_to_log("SELL_ORDER", f"[{active_symbol}] {str(error_message)}")

                    color = InterfaceColors.SUCCESS_GREEN if pnl_pct >= 0 else InterfaceColors.DANGER_RED
                    dashboard_data_rows.append(
                        f"{active_symbol:<10} "
                        f"{InterfaceColors.SUCCESS_GREEN}{'HOLDING':<15}{InterfaceColors.RESET_STYLE} "
                        f"AVG: ${average_entry:<10,.4f} "
                        f"SELL AT: ${upper_band:<10,.4f} "
                        f"{color}{pnl_pct:>+6.2f}%"
                    )

            clear_terminal_screen()
            total_pnl_color = InterfaceColors.SUCCESS_GREEN if total_unrealized_profit_loss >= 0 else InterfaceColors.DANGER_RED
            print(f"{InterfaceColors.HEADER_CYAN}===========================================================================")
            print(f" {InterfaceColors.HEADER_CYAN}WAYNE'S SENTINEL LOOP | Started: ${starting_bal:.2f} | {time.strftime('%H:%M:%S')}")
            print(f" {InterfaceColors.HEADER_CYAN}CASH: {InterfaceColors.RESET_STYLE}${available_usd_cash:.2f} | "
                  f"{InterfaceColors.HEADER_CYAN}UNREALIZED P/L: {total_pnl_color}${total_unrealized_profit_loss:+.2f}{InterfaceColors.RESET_STYLE}")
            print(f"{InterfaceColors.HEADER_CYAN}===========================================================================")
            print(f"{'SYMBOL':<10} {'STATUS':<15} {'DETAILS':<32} {'P/L %'}")
            print("-" * 75)
            for row in dashboard_data_rows:
                print(row)
            
            if insufficient_funds_warning_active:
                print(f"\n{InterfaceColors.WARNING_YELLOW}* ALERT: USD balance insufficient for trade.")

            
            if recent_activity_ram:
                print(f"\n{InterfaceColors.HEADER_CYAN}RECENT TRADES (FROM RAM):")
                for line in recent_activity_ram:
                    print(f" {line}")

            time.sleep(check_interval_seconds)

        except KeyboardInterrupt:
            allow_system_sleep()
            break
        except Exception as error_message:
            print(f"\n{InterfaceColors.DANGER_RED}!!! CRITICAL LOOP ERROR: {error_message}")
            record_error_to_log("CRITICAL", str(error_message))
            print(f"{InterfaceColors.WARNING_YELLOW}Re-attempting in 10 seconds...")
            time.sleep(10)

if __name__ == "__main__":
    run_trading_engine()