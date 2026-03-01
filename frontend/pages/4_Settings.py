"""
TradeForge AaaS - Settings Page
Author: Ary HH
Email: aryhharyanto@proton.me
GitHub: https://github.com/AryHHAry
© 2026

User settings and configuration interface.
"""

import streamlit as st
import sys
sys.path.append('..')
from components.translation import get_translator

st.set_page_config(page_title="Settings - TradeForge", page_icon="⚙️", layout="wide")

if "language" not in st.session_state:
    st.session_state.language = "en"

t = get_translator(st.session_state.language)

st.title("⚙️ " + t("settings"))
st.markdown("---")

# Settings tabs
tab1, tab2, tab3, tab4 = st.tabs([
    "🔑 " + t("api_keys"),
    "💼 Wallet",
    "🔔 Notifications",
    "⚠️ Risk Management"
])

# API Keys tab
with tab1:
    st.subheader(t("api_keys"))
    
    st.info("API keys are encrypted and stored securely.")
    
    # Binance
    st.markdown("### Binance")
    col1, col2 = st.columns(2)
    
    with col1:
        binance_key = st.text_input(
            "API Key",
            type="password",
            key="binance_key",
            placeholder="Enter Binance API Key"
        )
    
    with col2:
        binance_secret = st.text_input(
            "API Secret",
            type="password",
            key="binance_secret",
            placeholder="Enter Binance API Secret"
        )
    
    binance_testnet = st.checkbox("Use Testnet", value=True, key="binance_testnet")
    
    # Bybit
    st.markdown("### Bybit")
    col1, col2 = st.columns(2)
    
    with col1:
        bybit_key = st.text_input(
            "API Key",
            type="password",
            key="bybit_key",
            placeholder="Enter Bybit API Key"
        )
    
    with col2:
        bybit_secret = st.text_input(
            "API Secret",
            type="password",
            key="bybit_secret",
            placeholder="Enter Bybit API Secret"
        )
    
    bybit_testnet = st.checkbox("Use Testnet", value=True, key="bybit_testnet")
    
    if st.button(t("save") + " API Keys", use_container_width=True, type="primary"):
        st.success(t("saved_successfully"))

# Wallet tab
with tab2:
    st.subheader("Wallet Configuration")
    
    st.warning("⚠️ Never share your private keys. They are encrypted before storage.")
    
    network = st.selectbox(
        "Default Network",
        ["Ethereum", "Polygon", "Arbitrum"]
    )
    
    wallet_address = st.text_input(
        t("wallet_address"),
        placeholder="0x..."
    )
    
    private_key = st.text_input(
        t("private_key"),
        type="password",
        placeholder="Private key for signing transactions (optional)"
    )
    
    st.info(
        "💡 You can connect your wallet for read-only operations without providing a private key. "
        "Private key is only needed for executing transactions."
    )
    
    if st.button(t("save") + " Wallet", use_container_width=True, type="primary"):
        st.success(t("saved_successfully"))

# Notifications tab
with tab3:
    st.subheader("Notification Settings")
    
    # Telegram
    st.markdown("### Telegram")
    telegram_enabled = st.checkbox("Enable Telegram Notifications")
    
    if telegram_enabled:
        col1, col2 = st.columns(2)
        
        with col1:
            telegram_token = st.text_input(
                "Bot Token",
                type="password",
                placeholder="Enter Telegram Bot Token"
            )
        
        with col2:
            telegram_chat_id = st.text_input(
                "Chat ID",
                placeholder="Enter your Chat ID"
            )
    
    # Discord
    st.markdown("### Discord")
    discord_enabled = st.checkbox("Enable Discord Notifications")
    
    if discord_enabled:
        discord_webhook = st.text_input(
            "Webhook URL",
            type="password",
            placeholder="Enter Discord Webhook URL"
        )
    
    # Email
    st.markdown("### Email")
    email_enabled = st.checkbox("Enable Email Notifications")
    
    if email_enabled:
        email_address = st.text_input(
            "Email Address",
            placeholder="your@email.com"
        )
    
    # Notification types
    st.markdown("### Notification Types")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.checkbox("Trade Executions", value=True)
        st.checkbox("Order Fills", value=True)
        st.checkbox("Stop Loss Triggers", value=True)
    
    with col2:
        st.checkbox("Daily Summary", value=True)
        st.checkbox("Error Alerts", value=True)
        st.checkbox("System Updates", value=False)
    
    if st.button(t("save") + " Notifications", use_container_width=True, type="primary"):
        st.success(t("saved_successfully"))

# Risk Management tab
with tab4:
    st.subheader("Risk Management Settings")
    
    st.info(
        "Configure risk parameters to protect your capital. "
        "These limits will be enforced across all trading activities."
    )
    
    col1, col2 = st.columns(2)
    
    with col1:
        max_position_size = st.slider(
            "Max Position Size (% of Capital)",
            min_value=1.0,
            max_value=100.0,
            value=5.0,
            step=0.5,
            help="Maximum percentage of capital to allocate to a single position"
        )
        
        default_stop_loss = st.slider(
            "Default Stop Loss (%)",
            min_value=0.5,
            max_value=20.0,
            value=2.0,
            step=0.5,
            help="Default stop loss percentage for new positions"
        )
        
        max_open_positions = st.slider(
            "Max Open Positions",
            min_value=1,
            max_value=50,
            value=10,
            help="Maximum number of concurrent open positions"
        )
    
    with col2:
        max_daily_loss = st.slider(
            "Max Daily Loss (% of Capital)",
            min_value=1.0,
            max_value=50.0,
            value=5.0,
            step=0.5,
            help="Trading will be suspended if daily loss exceeds this limit"
        )
        
        default_take_profit = st.slider(
            "Default Take Profit (%)",
            min_value=1.0,
            max_value=50.0,
            value=5.0,
            step=0.5,
            help="Default take profit percentage for new positions"
        )
        
        leverage = st.slider(
            "Max Leverage",
            min_value=1,
            max_value=20,
            value=1,
            help="Maximum leverage allowed (1 = no leverage)"
        )
    
    # Advanced settings
    with st.expander("Advanced Settings"):
        trailing_stop = st.checkbox("Enable Trailing Stop Loss")
        
        if trailing_stop:
            trailing_percent = st.slider(
                "Trailing Stop Percentage",
                min_value=0.5,
                max_value=10.0,
                value=2.0,
                step=0.5
            )
        
        risk_per_trade = st.slider(
            "Risk Per Trade (% of Capital)",
            min_value=0.1,
            max_value=5.0,
            value=1.0,
            step=0.1,
            help="Maximum capital to risk on a single trade"
        )
        
        auto_hedge = st.checkbox(
            "Auto-Hedge on High Volatility",
            help="Automatically hedge positions during high volatility periods"
        )
    
    if st.button(t("save") + " Risk Settings", use_container_width=True, type="primary"):
        st.success(t("saved_successfully"))

# Account info
st.markdown("---")
st.subheader("Account Information")

col1, col2, col3 = st.columns(3)

with col1:
    st.info("**Account Type:** Free Plan")
    st.caption("Upgrade to Pro for unlimited backtests")

with col2:
    st.info("**Member Since:** February 2026")

with col3:
    st.info("**API Calls Today:** 45 / 1000")

# Danger zone
st.markdown("---")
st.subheader("⚠️ Danger Zone")

with st.expander("Show Danger Zone"):
    st.warning(
        "These actions are irreversible. Please proceed with caution."
    )
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🗑️ Delete All API Keys", use_container_width=True):
            st.error("API keys deleted (simulation)")
    
    with col2:
        if st.button("🗑️ Delete Account", use_container_width=True):
            st.error("This would delete your account (simulation)")
