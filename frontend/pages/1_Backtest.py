"""
TradeForge AaaS - Backtest Page
Author: Ary HH
Email: aryhharyanto@proton.me
GitHub: https://github.com/AryHHAry
© 2026

Backtesting interface with strategy selection and results visualization.
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from datetime import datetime, timedelta
import sys
sys.path.append('..')
from components.translation import get_translator

st.set_page_config(page_title="Backtest - TradeForge", page_icon="📊", layout="wide")

# Get language from session state
if "language" not in st.session_state:
    st.session_state.language = "en"

t = get_translator(st.session_state.language)

# Page title
st.title("📊 " + t("backtest"))
st.markdown("---")

# Strategy selection
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader(t("select_strategy"))
    
    strategy = st.selectbox(
        t("strategy"),
        [
            "SMA Crossover",
            "EMA Crossover",
            "RSI Oversold/Overbought",
            "MACD Signal",
            "Bollinger Bands",
            "Custom Strategy (Code)"
        ]
    )

with col2:
    st.subheader(t("settings"))
    
    symbol = st.selectbox(
        t("symbol"),
        ["BTC/USDT", "ETH/USDT", "BNB/USDT", "SOL/USDT"]
    )
    
    timeframe = st.selectbox(
        t("timeframe"),
        ["1m", "5m", "15m", "1h", "4h", "1d"]
    )

# Backtest parameters
st.subheader("Parameters")

col1, col2, col3, col4 = st.columns(4)

with col1:
    initial_capital = st.number_input(
        t("initial_capital"),
        min_value=100.0,
        max_value=1000000.0,
        value=10000.0,
        step=100.0
    )

with col2:
    start_date = st.date_input(
        t("start_date"),
        value=datetime.now() - timedelta(days=365)
    )

with col3:
    end_date = st.date_input(
        t("end_date"),
        value=datetime.now()
    )

with col4:
    commission = st.number_input(
        "Commission (%)",
        min_value=0.0,
        max_value=1.0,
        value=0.1,
        step=0.01
    )

# Strategy-specific parameters
if strategy == "SMA Crossover":
    col1, col2 = st.columns(2)
    with col1:
        fast_period = st.slider("Fast SMA Period", 5, 50, 20)
    with col2:
        slow_period = st.slider("Slow SMA Period", 20, 200, 50)

elif strategy == "RSI Oversold/Overbought":
    col1, col2, col3 = st.columns(3)
    with col1:
        rsi_period = st.slider("RSI Period", 5, 30, 14)
    with col2:
        oversold = st.slider("Oversold Level", 10, 40, 30)
    with col3:
        overbought = st.slider("Overbought Level", 60, 90, 70)

# Run backtest button
st.markdown("---")

if st.button("🚀 " + t("run_backtest"), use_container_width=True, type="primary"):
    with st.spinner(t("backtest_running")):
        # Simulate backtest (replace with actual backtest logic)
        import time
        time.sleep(2)
        
        # Generate sample results
        dates = pd.date_range(start=start_date, end=end_date, periods=100)
        
        # Simulate price data
        np.random.seed(42)
        price_returns = np.random.normal(0.001, 0.02, len(dates))
        prices = initial_capital * np.cumprod(1 + price_returns)
        
        # Simulate portfolio value
        strategy_returns = np.random.normal(0.002, 0.015, len(dates))
        portfolio_values = initial_capital * np.cumprod(1 + strategy_returns)
        
        # Create results dataframe
        results_df = pd.DataFrame({
            'Date': dates,
            'Portfolio Value': portfolio_values,
            'Buy & Hold': prices
        })
        
        st.success(t("backtest_complete"))
        
        # Display results
        st.markdown("---")
        st.subheader(t("results"))
        
        # Metrics
        final_value = portfolio_values[-1]
        total_return = ((final_value - initial_capital) / initial_capital) * 100
        sharpe = np.random.uniform(0.5, 2.5)
        max_dd = np.random.uniform(5, 25)
        win_rate = np.random.uniform(45, 75)
        
        col1, col2, col3, col4, col5 = st.columns(5)
        
        with col1:
            st.metric(
                t("initial_capital"),
                f"${initial_capital:,.2f}"
            )
        
        with col2:
            st.metric(
                t("final_capital"),
                f"${final_value:,.2f}",
                delta=f"{total_return:+.2f}%"
            )
        
        with col3:
            st.metric(
                t("sharpe_ratio"),
                f"{sharpe:.2f}"
            )
        
        with col4:
            st.metric(
                t("max_drawdown"),
                f"{max_dd:.2f}%"
            )
        
        with col5:
            st.metric(
                t("win_rate"),
                f"{win_rate:.1f}%"
            )
        
        # Portfolio chart
        st.markdown("---")
        st.subheader("Portfolio Performance")
        
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=results_df['Date'],
            y=results_df['Portfolio Value'],
            mode='lines',
            name='Strategy',
            line=dict(color='#1f77b4', width=2)
        ))
        
        fig.add_trace(go.Scatter(
            x=results_df['Date'],
            y=results_df['Buy & Hold'],
            mode='lines',
            name='Buy & Hold',
            line=dict(color='#ff7f0e', width=2, dash='dash')
        ))
        
        fig.update_layout(
            title="Portfolio Value Over Time",
            xaxis_title="Date",
            yaxis_title="Portfolio Value ($)",
            hovermode='x unified',
            height=500
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Trade log (sample)
        st.markdown("---")
        st.subheader("Recent Trades (Sample)")
        
        trade_log = pd.DataFrame({
            'Date': dates[-10:],
            'Action': np.random.choice(['BUY', 'SELL'], 10),
            'Price': np.random.uniform(40000, 50000, 10),
            'Amount': np.random.uniform(0.01, 0.1, 10),
            'P&L': np.random.uniform(-200, 500, 10)
        })
        
        st.dataframe(
            trade_log.style.format({
                'Price': '${:,.2f}',
                'Amount': '{:.4f}',
                'P&L': '${:+.2f}'
            }),
            use_container_width=True
        )

# Info box
st.markdown("---")
st.info(
    "💡 **Tips:**\n"
    "- Always backtest multiple strategies and timeframes\n"
    "- Past performance does not guarantee future results\n"
    "- Consider transaction costs and slippage\n"
    "- Validate strategies with walk-forward analysis\n\n"
    "💡 **Tips (ID):**\n"
    "- Selalu backtest berbagai strategi dan timeframe\n"
    "- Performa masa lalu tidak menjamin hasil masa depan\n"
    "- Pertimbangkan biaya transaksi dan slippage\n"
    "- Validasi strategi dengan walk-forward analysis"
)
