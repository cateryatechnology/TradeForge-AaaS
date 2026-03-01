"""
TradeForge AaaS - Internationalization (i18n) Module
Author: Ary HH
Email: cateryatechnology@proton.me
GitHub: https://github.com/cateryatechnology
© 2026

Simple bilingual support for English and Bahasa Indonesia.
"""

from typing import Dict, Literal
from enum import Enum


class Language(str, Enum):
    """Supported languages."""
    ENGLISH = "en"
    INDONESIAN = "id"


# Translation dictionary
TRANSLATIONS: Dict[str, Dict[str, str]] = {
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
        "en": "Login failed. Please check your credentials.",
        "id": "Login gagal. Silakan periksa kredensial Anda."
    },
    "register_success": {
        "en": "Registration successful! Please login.",
        "id": "Registrasi berhasil! Silakan login."
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
    "open_position": {
        "en": "Open Position",
        "id": "Buka Posisi"
    },
    "close_position": {
        "en": "Close Position",
        "id": "Tutup Posisi"
    },
    "order_placed": {
        "en": "Order placed successfully",
        "id": "Order berhasil ditempatkan"
    },
    "order_failed": {
        "en": "Failed to place order",
        "id": "Gagal menempatkan order"
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
    
    # Backtesting
    "run_backtest": {
        "en": "Run Backtest",
        "id": "Jalankan Backtest"
    },
    "backtest_running": {
        "en": "Backtest is running...",
        "id": "Backtest sedang berjalan..."
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
    "remove_liquidity": {
        "en": "Remove Liquidity",
        "id": "Hapus Likuiditas"
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
    "gas_price": {
        "en": "Gas Price",
        "id": "Harga Gas"
    },
    "swap_success": {
        "en": "Swap completed successfully",
        "id": "Swap berhasil diselesaikan"
    },
    "swap_failed": {
        "en": "Swap failed",
        "id": "Swap gagal"
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
    "private_key": {
        "en": "Private Key",
        "id": "Kunci Pribadi"
    },
    "save": {
        "en": "Save",
        "id": "Simpan"
    },
    "cancel": {
        "en": "Cancel",
        "id": "Batal"
    },
    "saved_successfully": {
        "en": "Saved successfully",
        "id": "Berhasil disimpan"
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
    
    # Risk Management
    "risk_management": {
        "en": "Risk Management",
        "id": "Manajemen Risiko"
    },
    "max_position_size": {
        "en": "Max Position Size",
        "id": "Ukuran Posisi Maksimal"
    },
    "max_daily_loss": {
        "en": "Max Daily Loss",
        "id": "Kerugian Harian Maksimal"
    },
    "max_open_positions": {
        "en": "Max Open Positions",
        "id": "Posisi Terbuka Maksimal"
    },
    "daily_loss_limit_reached": {
        "en": "Daily loss limit reached. Trading suspended.",
        "id": "Batas kerugian harian tercapai. Trading ditangguhkan."
    },
    
    # Errors
    "invalid_credentials": {
        "en": "Invalid email or password",
        "id": "Email atau kata sandi tidak valid"
    },
    "user_not_found": {
        "en": "User not found",
        "id": "Pengguna tidak ditemukan"
    },
    "user_already_exists": {
        "en": "User with this email already exists",
        "id": "Pengguna dengan email ini sudah ada"
    },
    "insufficient_balance": {
        "en": "Insufficient balance",
        "id": "Saldo tidak mencukupi"
    },
    "invalid_amount": {
        "en": "Invalid amount",
        "id": "Jumlah tidak valid"
    },
    "connection_error": {
        "en": "Connection error. Please try again.",
        "id": "Kesalahan koneksi. Silakan coba lagi."
    },
    "server_error": {
        "en": "Server error. Please contact support.",
        "id": "Kesalahan server. Silakan hubungi dukungan."
    },
    
    # Notifications
    "notifications": {
        "en": "Notifications",
        "id": "Notifikasi"
    },
    "enable_telegram": {
        "en": "Enable Telegram Alerts",
        "id": "Aktifkan Alert Telegram"
    },
    "enable_discord": {
        "en": "Enable Discord Alerts",
        "id": "Aktifkan Alert Discord"
    },
    "enable_email": {
        "en": "Enable Email Alerts",
        "id": "Aktifkan Alert Email"
    },
    
    # Subscription
    "subscription": {
        "en": "Subscription",
        "id": "Langganan"
    },
    "current_plan": {
        "en": "Current Plan",
        "id": "Paket Saat Ini"
    },
    "upgrade": {
        "en": "Upgrade",
        "id": "Tingkatkan"
    },
    "free_plan": {
        "en": "Free Plan",
        "id": "Paket Gratis"
    },
    "pro_plan": {
        "en": "Pro Plan",
        "id": "Paket Pro"
    },
    "enterprise_plan": {
        "en": "Enterprise Plan",
        "id": "Paket Enterprise"
    },
}


class Translator:
    """Simple translator class for bilingual support."""
    
    def __init__(self, language: Language = Language.ENGLISH):
        """
        Initialize translator with default language.
        
        Args:
            language: Default language (en or id)
        """
        self.language = language
    
    def set_language(self, language: Language | str) -> None:
        """
        Set the current language.
        
        Args:
            language: Language to set (en or id)
        """
        if isinstance(language, str):
            language = Language(language)
        self.language = language
    
    def translate(self, key: str, language: Language | str | None = None) -> str:
        """
        Translate a key to the specified language.
        
        Args:
            key: Translation key
            language: Target language (defaults to current language)
        
        Returns:
            Translated string or key if translation not found
        """
        if language is None:
            language = self.language
        
        if isinstance(language, str):
            language = Language(language)
        
        if key in TRANSLATIONS:
            return TRANSLATIONS[key].get(language.value, key)
        
        return key
    
    def t(self, key: str, language: Language | str | None = None) -> str:
        """
        Shorthand for translate method.
        
        Args:
            key: Translation key
            language: Target language (defaults to current language)
        
        Returns:
            Translated string
        """
        return self.translate(key, language)
    
    def get_all_translations(self, language: Language | str) -> Dict[str, str]:
        """
        Get all translations for a specific language.
        
        Args:
            language: Target language
        
        Returns:
            Dictionary of all translations
        """
        if isinstance(language, str):
            language = Language(language)
        
        return {
            key: translations.get(language.value, key)
            for key, translations in TRANSLATIONS.items()
        }


# Singleton instance
translator = Translator()


def t(key: str, language: Language | str | None = None) -> str:
    """
    Global translation function.
    
    Args:
        key: Translation key
        language: Target language (defaults to current language)
    
    Returns:
        Translated string
    """
    return translator.translate(key, language)


def set_language(language: Language | str) -> None:
    """
    Set global language.
    
    Args:
        language: Language to set (en or id)
    """
    translator.set_language(language)


# Export for convenience
__all__ = [
    "Language",
    "Translator",
    "translator",
    "t",
    "set_language",
    "TRANSLATIONS",
]
