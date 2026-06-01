# Crypto Automator

## High-Reliability Automated Trading Engine

A professional-grade Python trading bot built for the Crypto.com exchange (via CCXT). This project focuses on high uptime, data integrity, and real-time dashboarding for Bollinger Band mean-reversion strategies.

---

## 🛠 Features

- **Automated Trading:** Uses the CCXT library to interface with Crypto.com for seamless order execution.
- **Mean-Reversion Logic:** Implements a Bollinger Band strategy with configurable entry/exit thresholds.
- **Real-Time Dashboard:** A custom-built terminal UI featuring:
  - Live Price Monitoring
  - Current Position Status
  - Dynamic P/L Tracking
- **Hardware-Level Reliability:**
  - **Physical Disk Sync:** Uses `os.fsync()` to ensure trade logs are written to the physical drive immediately, preventing data loss during power failures.
  - **Uptime Management:** Integrated Windows API calls to prevent the system from entering sleep mode during active trading loops.
- **Dynamic Configuration:** Controlled via an external `config.json`, allowing for strategy adjustments without modifying the core source code.

## 📁 Project Structure

/CRYPTOAUTOMATOR
    /src
        main_loop.py       # Core trading logic and dashboard
    config.json.example    # Template for strategy settings
    requirements.txt       # Project dependencies
    .gitignore             # Security gate for private data
    README.md              # Project documentation

## 🚀 Technical Skills Demonstrated

    Python Programming: Advanced loops, error handling, and environment management.

    API Integration: REST API communication with financial exchanges.

    Data Persistence: Managing CSV logs with low-level file system synchronization.

    System Administration: Windows environment optimization for long-running scripts.

## 🔒 Security & Privacy

Note: The core trading logic and private configuration files (API keys and live balances) are kept in a private repository to protect proprietary strategy details and financial security. This repository serves as a portfolio demonstration of the system's architecture and capabilities.

Author: omegazyph
Updated: 2026-04-22
