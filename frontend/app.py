"""
TradeForge AaaS - Streamlit Dashboard
Author: Ary HH
Email: cateryatechnology@proton.me
GitHub: https://github.com/cateryatechnology
© 2026

Main Streamlit application entry point with bilingual support.
"""

import streamlit as st
import requests
from components.translation import get_translator, LANGUAGES
import logging

# Configure page
st.set_page_config(
    page_title="TradeForge AaaS",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Backend API URL
API_BASE_URL = "http://backend:8000"  # Docker service name
# API_BASE_URL = "http://localhost:8000"  # Local development


def init_session_state():
    """Initialize session state variables."""
    if "language" not in st.session_state:
        st.session_state.language = "en"
    
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False
    
    if "user" not in st.session_state:
        st.session_state.user = None
    
    if "access_token" not in st.session_state:
        st.session_state.access_token = None


def main():
    """Main application entry point."""
    init_session_state()
    
    # Get translator
    t = get_translator(st.session_state.language)
    
    # ============================================
    # SIDEBAR
    # ============================================
    with st.sidebar:
        st.image("https://via.placeholder.com/200x60?text=TradeForge+AaaS", width=200)
        st.markdown("---")
        
        # Language selector
        st.subheader("🌍 " + t("language"))
        language = st.selectbox(
            label="Select Language / Pilih Bahasa",
            options=list(LANGUAGES.keys()),
            format_func=lambda x: LANGUAGES[x],
            key="language_selector",
            label_visibility="collapsed"
        )
        
        if language != st.session_state.language:
            st.session_state.language = language
            st.rerun()
        
        st.markdown("---")
        
        # User info
        if st.session_state.authenticated:
            st.success(t("login_success"))
            st.write(f"👤 {st.session_state.user.get('email', 'User')}")
            
            if st.button(t("logout"), use_container_width=True):
                st.session_state.authenticated = False
                st.session_state.user = None
                st.session_state.access_token = None
                st.rerun()
        else:
            st.info(t("login"))
        
        st.markdown("---")
        
        # Info
        st.caption("**Author:** Ary HH")
        st.caption("**Email:** cateryatechnology@proton.me")
        st.caption("**GitHub:** [cateryatechnology](https://github.com/cateryatechnology)")
        st.caption("© 2026")
    
    # ============================================
    # MAIN CONTENT
    # ============================================
    
    # Welcome header
    st.title(t("welcome"))
    
    if not st.session_state.authenticated:
        # Login/Register page
        show_login_page(t)
    else:
        # Dashboard
        show_dashboard(t)


def show_login_page(t):
    """Show login/register page."""
    st.info(t("login") + " / " + t("register"))
    
    tab1, tab2 = st.tabs([t("login"), t("register")])
    
    # Login tab
    with tab1:
        st.subheader(t("login"))
        
        email = st.text_input(t("email"), key="login_email")
        password = st.text_input(t("password"), type="password", key="login_password")
        
        if st.button(t("login"), key="login_button", use_container_width=True):
            if email and password:
                # TODO: Implement actual login API call
                # For now, simulate successful login
                st.session_state.authenticated = True
                st.session_state.user = {"email": email}
                st.session_state.access_token = "demo_token"
                st.success(t("login_success"))
                st.rerun()
            else:
                st.error(t("login_failed"))
    
    # Register tab
    with tab2:
        st.subheader(t("register"))
        
        reg_email = st.text_input(t("email"), key="register_email")
        reg_username = st.text_input(t("username"), key="register_username")
        reg_password = st.text_input(t("password"), type="password", key="register_password")
        reg_password_confirm = st.text_input(
            "Confirm " + t("password"),
            type="password",
            key="register_password_confirm"
        )
        
        if st.button(t("register"), key="register_button", use_container_width=True):
            if reg_email and reg_username and reg_password:
                if reg_password == reg_password_confirm:
                    # TODO: Implement actual register API call
                    st.success(t("register_success"))
                else:
                    st.error("Passwords do not match / Kata sandi tidak cocok")
            else:
                st.error("Please fill all fields / Silakan isi semua kolom")


def show_dashboard(t):
    """Show main dashboard."""
    st.subheader(t("dashboard"))
    
    # Quick stats
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label=t("balance"),
            value="$10,000.00",
            delta="+$250.00"
        )
    
    with col2:
        st.metric(
            label=t("today_pnl"),
            value="+$125.50",
            delta="+1.25%"
        )
    
    with col3:
        st.metric(
            label=t("total_trades"),
            value="24",
            delta="+3"
        )
    
    with col4:
        st.metric(
            label=t("win_rate"),
            value="62.5%",
            delta="+2.5%"
        )
    
    st.markdown("---")
    
    # Recent activity
    st.subheader(t("overview"))
    
    st.info(
        "📊 " + t("backtest") + " • "
        "🤖 " + t("live_trading") + " • "
        "🌐 " + t("defi_operations") + " • "
        "⚙️ " + t("settings")
    )
    
    # Portfolio chart placeholder
    st.line_chart(
        data={
            "Portfolio Value": [10000, 10050, 10025, 10100, 10075, 10150, 10125],
        },
        height=300
    )
    
    # Quick actions
    st.subheader("Quick Actions")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📊 " + t("run_backtest"), use_container_width=True):
            st.switch_page("pages/1_Backtest.py")
    
    with col2:
        if st.button("🤖 " + t("live_trading"), use_container_width=True):
            st.switch_page("pages/2_Live_Trading.py")
    
    with col3:
        if st.button("🌐 " + t("defi_operations"), use_container_width=True):
            st.switch_page("pages/3_DeFi_Operations.py")
    
    # Risk warning
    st.markdown("---")
    st.warning(
        "⚠️ **RISK WARNING / PERINGATAN RISIKO**\n\n"
        "Trading and DeFi operations carry substantial risk of financial loss. "
        "Never invest more than you can afford to lose.\n\n"
        "Trading dan operasi DeFi membawa risiko kerugian finansial yang substansial. "
        "Jangan investasi lebih dari yang mampu Anda rugikan."
    )


# Test backend connection
def test_backend_connection():
    """Test connection to backend API."""
    try:
        response = requests.get(f"{API_BASE_URL}/health", timeout=5)
        if response.status_code == 200:
            st.sidebar.success("✅ Backend connected")
        else:
            st.sidebar.error("❌ Backend error")
    except Exception as e:
        st.sidebar.error(f"❌ Backend offline")
        logger.error(f"Backend connection failed: {str(e)}")


if __name__ == "__main__":
    # test_backend_connection()  # Uncomment to test backend
    main()
