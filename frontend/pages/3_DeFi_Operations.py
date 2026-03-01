"""
TradeForge AaaS - DeFi Operations Page
Author: Ary HH
Email: aryhharyanto@proton.me
GitHub: https://github.com/AryHHAry
© 2026

DeFi operations interface for Uniswap V3, Aave V3, and more.
"""

import streamlit as st
import sys
sys.path.append('..')
from components.translation import get_translator

st.set_page_config(page_title="DeFi Operations - TradeForge", page_icon="🌐", layout="wide")

if "language" not in st.session_state:
    st.session_state.language = "en"

t = get_translator(st.session_state.language)

st.title("🌐 " + t("defi_operations"))
st.markdown("---")

# Network selection
col1, col2 = st.columns(2)

with col1:
    network = st.selectbox(
        "Blockchain Network",
        ["Ethereum", "Polygon", "Arbitrum"]
    )

with col2:
    wallet = st.text_input(
        t("wallet_address"),
        placeholder="0x...",
        help="Your wallet address for DeFi operations"
    )

# Wallet balance
if wallet:
    st.markdown("---")
    st.subheader("Wallet Balance")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("ETH", "2.5 ETH", "$7,500")
    
    with col2:
        st.metric("USDC", "5,000 USDC")
    
    with col3:
        st.metric("WBTC", "0.15 WBTC", "$6,750")
    
    with col4:
        st.metric("DAI", "2,500 DAI")

# DeFi operations tabs
st.markdown("---")

tab1, tab2, tab3, tab4 = st.tabs([
    "🔄 " + t("swap_tokens"),
    "💰 " + t("add_liquidity"),
    "🏦 " + t("lend"),
    "💳 " + t("borrow")
])

# Swap tab
with tab1:
    st.subheader(t("swap_tokens") + " (Uniswap V3)")
    
    col1, col2 = st.columns(2)
    
    with col1:
        token_in = st.selectbox(
            t("token_in"),
            ["ETH", "USDC", "WBTC", "DAI", "USDT"],
            key="swap_token_in"
        )
        
        amount_in = st.number_input(
            t("amount"),
            min_value=0.0,
            value=1.0,
            step=0.1,
            key="swap_amount_in"
        )
    
    with col2:
        token_out = st.selectbox(
            t("token_out"),
            ["USDC", "ETH", "WBTC", "DAI", "USDT"],
            key="swap_token_out"
        )
        
        st.info(f"Estimated output: ~3,000 {token_out}")
    
    col1, col2 = st.columns(2)
    
    with col1:
        slippage = st.slider(
            t("slippage") + " (%)",
            min_value=0.1,
            max_value=5.0,
            value=0.5,
            step=0.1
        )
    
    with col2:
        fee_tier = st.selectbox(
            "Fee Tier",
            ["0.05% (Most Liquid)", "0.3% (Standard)", "1% (Exotic)"]
        )
    
    if st.button("🔄 " + t("swap_tokens"), use_container_width=True, type="primary"):
        with st.spinner("Processing swap..."):
            import time
            time.sleep(2)
            st.success(t("swap_success") + f": {amount_in} {token_in} → {token_out}")

# Add liquidity tab
with tab2:
    st.subheader(t("add_liquidity") + " (Uniswap V3)")
    
    col1, col2 = st.columns(2)
    
    with col1:
        lp_token_a = st.selectbox(
            "Token A",
            ["ETH", "USDC", "WBTC", "DAI"],
            key="lp_token_a"
        )
        
        lp_amount_a = st.number_input(
            "Amount A",
            min_value=0.0,
            value=1.0,
            key="lp_amount_a"
        )
    
    with col2:
        lp_token_b = st.selectbox(
            "Token B",
            ["USDC", "ETH", "WBTC", "DAI"],
            key="lp_token_b"
        )
        
        lp_amount_b = st.number_input(
            "Amount B",
            min_value=0.0,
            value=3000.0,
            key="lp_amount_b"
        )
    
    col1, col2 = st.columns(2)
    
    with col1:
        price_range_min = st.number_input(
            "Price Range Min",
            min_value=0.0,
            value=2800.0
        )
    
    with col2:
        price_range_max = st.number_input(
            "Price Range Max",
            min_value=0.0,
            value=3200.0
        )
    
    st.info(
        "💡 Concentrated liquidity allows you to provide liquidity within a specific price range "
        "for better capital efficiency."
    )
    
    if st.button("💰 " + t("add_liquidity"), use_container_width=True, type="primary"):
        st.success(f"Liquidity added: {lp_amount_a} {lp_token_a} + {lp_amount_b} {lp_token_b}")

# Lend tab (Aave V3)
with tab3:
    st.subheader(t("lend") + " (Aave V3)")
    
    col1, col2 = st.columns(2)
    
    with col1:
        lend_asset = st.selectbox(
            "Asset to Lend",
            ["USDC", "DAI", "USDT", "ETH", "WBTC"]
        )
        
        lend_amount = st.number_input(
            t("amount"),
            min_value=0.0,
            value=1000.0,
            key="lend_amount"
        )
    
    with col2:
        st.metric("Current APY", "3.5%", "+0.2%")
        st.metric("Your Deposits", "$5,000")
    
    st.info(
        f"You will receive a{lend_asset} tokens representing your deposit. "
        "These tokens earn interest over time and can be redeemed anytime."
    )
    
    if st.button("🏦 " + t("lend"), use_container_width=True, type="primary"):
        st.success(f"Deposited {lend_amount} {lend_asset} to Aave V3")

# Borrow tab (Aave V3)
with tab4:
    st.subheader(t("borrow") + " (Aave V3)")
    
    col1, col2 = st.columns(2)
    
    with col1:
        borrow_asset = st.selectbox(
            "Asset to Borrow",
            ["USDC", "DAI", "USDT", "ETH", "WBTC"],
            key="borrow_asset"
        )
        
        borrow_amount = st.number_input(
            t("amount"),
            min_value=0.0,
            value=500.0,
            key="borrow_amount"
        )
        
        interest_mode = st.radio(
            "Interest Rate Mode",
            ["Variable (Lower APY)", "Stable (Fixed APY)"]
        )
    
    with col2:
        st.metric("Variable APY", "5.2%")
        st.metric("Stable APY", "6.8%")
        st.metric("Available to Borrow", "$3,000")
        st.metric("Health Factor", "2.45", help="Above 1.0 is safe")
    
    st.warning(
        "⚠️ Make sure your health factor stays above 1.0 to avoid liquidation. "
        "Provide sufficient collateral before borrowing."
    )
    
    if st.button("💳 " + t("borrow"), use_container_width=True, type="primary"):
        st.success(f"Borrowed {borrow_amount} {borrow_asset} from Aave V3")

# Gas price indicator
st.markdown("---")
col1, col2, col3 = st.columns(3)

with col1:
    st.metric(t("gas_price"), "25 Gwei", "-5 Gwei")

with col2:
    st.metric("Estimated Gas Fee", "$8.50")

with col3:
    st.metric("Network", network, delta_color="off")

# Important warnings
st.markdown("---")
st.error(
    "⚠️ **DeFi RISKS:**\n"
    "- Smart contract risk: Contracts may contain bugs\n"
    "- Impermanent loss: Providing liquidity may result in losses\n"
    "- Liquidation risk: Borrowed positions can be liquidated\n"
    "- Gas fees: Ethereum transactions can be expensive\n"
    "- Market volatility: Crypto prices are highly volatile\n\n"
    "Always do your own research (DYOR) and never invest more than you can afford to lose."
)
