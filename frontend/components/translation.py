"""
TradeForge AaaS - Translation Component
Author: Ary HH
Email: cateryatechnology@proton.me
GitHub: https://github.com/cateryatechnology
© 2026

Translation utilities for Streamlit frontend.
"""

from typing import Dict, Callable

# Supported languages
LANGUAGES = {
    "en": "🇬🇧 English",
    "id": "🇮🇩 Bahasa Indonesia"
}

# Translation dictionary (matches backend i18n)
TRANSLATIONS = {
    # Common
    "welcome": {
        "en": "Welcome to TradeForge AaaS",
        "id": "Selamat Datang di TradeForge AaaS"
    },
    "loading": {
        "en": "Loading...",
        "id": "Memuat..."
    },
    "success": {
        "en": "Success",
        "id": "Berhasil"
    },
    "error": {
        "en": "Error",
        "id": "Kesalahan"
    },
    "warning": {
        "en": "Warning",
        "id": "Peringatan"
    },
    "info": {
        "en": "Information",
        "id": "Informasi"
    },
    
    # Authentication
    "login": {
        "en": "Login",
        "id": "Masuk"
    },
    "logout": {
        "en": "Logout",
        "id": "Keluar"
    },
    "register": {
        "en": "Register",
        "id": "Daftar"
    },
    "email": {
        "en": "Email",
        "id": "Email"
    },
    "password": {
        "en": "Password",
        "id": "Kata Sandi"
    },
    "username": {
        "en": "Username",
        "id": "Nama Pengguna"
    },
    "login_success": {
        "en": "Login successful",
        "id": "Login berhasil"
    },
    "login_failed": {
        "en": "Login failed",
        "id": "Login gagal"
    },
    "register_success": {
        "en": "Registration successful!",
        "id": "Registrasi berhasil!"
    },
    
    # Dashboard
    "dashboard": {
        "en": "Dashboard",
        "id": "Dasbor"
    },
    "overview": {
        "en": "Overview",
        "id": "Ringkasan"
    },
    "portfolio": {
        "en": "Portfolio",
        "id": "Portofolio"
    },
    "balance": {
        "en": "Balance",
        "id": "Saldo"
    },
    "total_value": {
        "en": "Total Value",
        "id": "Nilai Total"
    },
    "profit_loss": {
        "en": "Profit/Loss",
        "id": "Untung/Rugi"
    },
    "today_pnl": {
        "en": "Today's P&L",
        "id": "P&L Hari Ini"
    },
    
    # Trading
    "backtest": {
        "en": "Backtest",
        "id": "Backtest"
    },
    "live_trading": {
        "en": "Live Trading",
        "id": "Trading Live"
    },
    "strategy": {
        "en": "Strategy",
        "id": "Strategi"
    },
    "buy": {
        "en": "Buy",
        "id": "Beli"
    },
    "sell": {
        "en": "Sell",
        "id": "Jual"
    },
    "run_backtest": {
        "en": "Run Backtest",
        "id": "Jalankan Backtest"
    },
    "backtest_running": {
        "en": "Backtest running...",
        "id": "Backtest berjalan..."
    },
    "backtest_complete": {
        "en": "Backtest completed",
        "id": "Backtest selesai"
    },
    "initial_capital": {
        "en": "Initial Capital",
        "id": "Modal Awal"
    },
    "final_capital": {
        "en": "Final Capital",
        "id": "Modal Akhir"
    },
    "total_return": {
        "en": "Total Return",
        "id": "Return Total"
    },
    "sharpe_ratio": {
        "en": "Sharpe Ratio",
        "id": "Rasio Sharpe"
    },
    "max_drawdown": {
        "en": "Max Drawdown",
        "id": "Drawdown Maksimum"
    },
    "win_rate": {
        "en": "Win Rate",
        "id": "Tingkat Menang"
    },
    "total_trades": {
        "en": "Total Trades",
        "id": "Total Trading"
    },
    "position_size": {
        "en": "Position Size",
        "id": "Ukuran Posisi"
    },
    "stop_loss": {
        "en": "Stop Loss",
        "id": "Stop Loss"
    },
    "take_profit": {
        "en": "Take Profit",
        "id": "Take Profit"
    },
    
    # DeFi
    "defi_operations": {
        "en": "DeFi Operations",
        "id": "Operasi DeFi"
    },
    "swap_tokens": {
        "en": "Swap Tokens",
        "id": "Tukar Token"
    },
    "add_liquidity": {
        "en": "Add Liquidity",
        "id": "Tambah Likuiditas"
    },
    "lend": {
        "en": "Lend",
        "id": "Pinjamkan"
    },
    "borrow": {
        "en": "Borrow",
        "id": "Pinjam"
    },
    "repay": {
        "en": "Repay",
        "id": "Bayar Kembali"
    },
    "token_in": {
        "en": "Token In",
        "id": "Token Masuk"
    },
    "token_out": {
        "en": "Token Out",
        "id": "Token Keluar"
    },
    "amount": {
        "en": "Amount",
        "id": "Jumlah"
    },
    "slippage": {
        "en": "Slippage Tolerance",
        "id": "Toleransi Slippage"
    },
    "swap_success": {
        "en": "Swap completed",
        "id": "Swap selesai"
    },
    
    # Settings
    "settings": {
        "en": "Settings",
        "id": "Pengaturan"
    },
    "api_keys": {
        "en": "API Keys",
        "id": "Kunci API"
    },
    "exchange": {
        "en": "Exchange",
        "id": "Exchange"
    },
    "wallet_address": {
        "en": "Wallet Address",
        "id": "Alamat Wallet"
    },
    "save": {
        "en": "Save",
        "id": "Simpan"
    },
    "cancel": {
        "en": "Cancel",
        "id": "Batal"
    },
    "language": {
        "en": "Language",
        "id": "Bahasa"
    },
    "english": {
        "en": "English",
        "id": "Bahasa Inggris"
    },
    "indonesian": {
        "en": "Indonesian",
        "id": "Bahasa Indonesia"
    },
    
    # Additional
    "select_strategy": {
        "en": "Select Strategy",
        "id": "Pilih Strategi"
    },
    "symbol": {
        "en": "Symbol",
        "id": "Simbol"
    },
    "timeframe": {
        "en": "Timeframe",
        "id": "Timeframe"
    },
    "start_date": {
        "en": "Start Date",
        "id": "Tanggal Mulai"
    },
    "end_date": {
        "en": "End Date",
        "id": "Tanggal Akhir"
    },
    "results": {
        "en": "Results",
        "id": "Hasil"
    },
}


class Translator:
    """Simple translator for Streamlit."""
    
    def __init__(self, language: str = "en"):
        self.language = language
    
    def __call__(self, key: str) -> str:
        """Translate a key."""
        if key in TRANSLATIONS:
            return TRANSLATIONS[key].get(self.language, key)
        return key


def get_translator(language: str = "en") -> Callable[[str], str]:
    """
    Get a translator function for the specified language.
    
    Args:
        language: Language code (en or id)
    
    Returns:
        Translator function
    """
    return Translator(language)


# Export
__all__ = ["LANGUAGES", "TRANSLATIONS", "Translator", "get_translator"]
