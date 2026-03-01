"""
TradeForge AaaS - Live Trading Page
Author: Ary HH
Email: aryhharyanto@proton.me
GitHub: https://github.com/AryHHAry
© 2026

Live trading interface with order execution and position management.
"""

import streamlit as st
import sys
sys.path.append('..')
from components.translation import get_translator

st.set_page_config(page_title="Live Trading - TradeForge", page_icon="🤖", layout="wide")

if "language" not in st.session_state:
    st.session_state.language = "en"

t = get_translator(st.session_state.language)

st.title("🤖 " + t("live_trading"))
st.markdown("---")

# Warning
st.warning(
    "⚠️ **LIVE TRADING MODE**\n\n"
    "This will execute real trades with real money. Make sure you understand the risks.\n\n"
    "Ini akan mengeksekusi trading nyata dengan uang sungguhan. Pastikan Anda memahami risikonya."
)

# Exchange selection
col1, col2 = st.columns(2)

with col1:
    exchange = st.selectbox(
        t("exchange"),
        ["Binance", "Bybit", "Coinbase", "Kraken", "Alpaca (Testnet)"]
    )

with col2:
    symbol = st.selectbox(
        t("symbol"),
        ["BTC/USDT", "ETH/USDT", "BNB/USDT", "SOL/USDT"]
    )

# Order panel
st.markdown("---")
st.subheader("Order Panel")

tab1, tab2 = st.tabs([t("buy"), t("sell")])

with tab1:
    col1, col2 = st.columns(2)
    
    with col1:
        buy_amount = st.number_input(
            t("amount"),
            min_value=0.0,
            value=0.01,
            step=0.001,
            key="buy_amount"
        )
    
    with col2:
        buy_price = st.number_input(
            "Price (USDT)",
            min_value=0.0,
            value=50000.0,
            step=100.0,
            key="buy_price"
        )
    
    buy_stop_loss = st.number_input(
        t("stop_loss") + " (%)",
        min_value=0.0,
        max_value=100.0,
        value=2.0,
        step=0.1
    )
    
    buy_take_profit = st.number_input(
        t("take_profit") + " (%)",
        min_value=0.0,
        max_value=100.0,
        value=5.0,
        step=0.1
    )
    
    if st.button("🟢 " + t("buy"), use_container_width=True, type="primary"):
        st.success(f"Buy order placed: {buy_amount} {symbol} @ ${buy_price}")

with tab2:
    col1, col2 = st.columns(2)
    
    with col1:
        sell_amount = st.number_input(
            t("amount"),
            min_value=0.0,
            value=0.01,
            step=0.001,
            key="sell_amount"
        )
    
    with col2:
        sell_price = st.number_input(
            "Price (USDT)",
            min_value=0.0,
            value=50000.0,
            step=100.0,
            key="sell_price"
        )
    
    if st.button("🔴 " + t("sell"), use_container_width=True):
        st.success(f"Sell order placed: {sell_amount} {symbol} @ ${sell_price}")

# Open positions
st.markdown("---")
st.subheader("Open Positions")

if st.button("🔄 Refresh"):
    st.rerun()

# Sample positions (replace with actual API data)
import pandas as pd

positions_df = pd.DataFrame({
    'Symbol': ['BTC/USDT', 'ETH/USDT'],
    'Side': ['LONG', 'SHORT'],
    'Amount': [0.05, 1.2],
    'Entry Price': [48500.00, 3200.00],
    'Current Price': [49000.00, 3150.00],
    'P&L': ['+$25.00', '-$60.00'],
    'P&L %': ['+1.03%', '-1.56%']
})

st.dataframe(positions_df, use_container_width=True)

# Recent orders
st.markdown("---")
st.subheader("Recent Orders")

orders_df = pd.DataFrame({
    'Time': ['2026-02-11 10:30', '2026-02-11 10:15', '2026-02-11 10:00'],
    'Symbol': ['BTC/USDT', 'ETH/USDT', 'BTC/USDT'],
    'Side': ['BUY', 'SELL', 'BUY'],
    'Amount': [0.05, 1.0, 0.03],
    'Price': [48500.00, 3200.00, 48400.00],
    'Status': ['Filled', 'Filled', 'Filled']
})

st.dataframe(orders_df, use_container_width=True)

# Risk metrics
st.markdown("---")
st.subheader("Risk Metrics")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Account Balance", "$10,000")

with col2:
    st.metric("Used Margin", "$1,250", "-2.5%")

with col3:
    st.metric("Available Margin", "$8,750")

with col4:
    st.metric("Daily P&L", "+$125.50", "+1.26%")

# Info
st.markdown("---")
st.info(
    "💡 **Important Notes:**\n"
    "- All trades are subject to exchange fees\n"
    "- Prices shown are indicative and may differ at execution\n"
    "- Always use stop-loss to manage risk\n"
    "- Never risk more than you can afford to lose"
)
