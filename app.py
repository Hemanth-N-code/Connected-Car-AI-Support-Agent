import streamlit as st
import time
from graph.workflow import build_graph
from datetime import datetime
import pandas as pd
import json

# Compile LangGraph
graph = build_graph()

# Configure Streamlit App Layout
st.set_page_config(
    page_title="Connected Car AI Support Console",
    page_icon="🚘",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Utility to strip leading indentation from HTML templates.
# This prevents Streamlit's markdown parser from misinterpreting indented HTML lines as markdown code blocks.
def clean_html(html_str):
    return "\n".join([line.strip() for line in html_str.split("\n")])

# Custom Enterprise Glassmorphism CSS Styling
st.markdown("""
<style>
/* Import Outfit Google Font */
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&display=swap');

/* Global Style Overrides */
html, body, [class*="css"], .stApp {
    font-family: 'Outfit', sans-serif;
    background: linear-gradient(180deg, #070913 0%, #0d1127 100%);
    color: #e2e8f0;
}

/* Custom Header styles */
.app-title-container {
    padding: 10px 0;
    margin-bottom: 25px;
    border-bottom: 1px solid rgba(255, 255, 255, 0.05);
}

.main-title {
    font-size: 36px;
    font-weight: 800;
    background: linear-gradient(90deg, #ffffff 0%, #a5b4fc 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin: 0;
}

.subtitle {
    font-size: 14px;
    color: #818cf8;
    font-weight: 500;
    margin-top: 5px;
    letter-spacing: 0.05em;
    text-transform: uppercase;
}

/* Sidebar Custom Styling */
section[data-testid="stSidebar"] {
    background-color: #050813 !important;
    border-right: 1px solid rgba(255, 255, 255, 0.05) !important;
}

/* Streamlit Button Overrides */
.stButton>button {
    background: linear-gradient(135deg, #4f46e5 0%, #3730a3 100%) !important;
    color: #ffffff !important;
    border: 1px solid rgba(255, 255, 255, 0.1) !important;
    border-radius: 8px !important;
    font-weight: 600 !important;
    padding: 8px 16px !important;
    transition: all 0.25s ease !important;
    box-shadow: 0 4px 12px rgba(79, 70, 229, 0.2) !important;
}

.stButton>button:hover {
    background: linear-gradient(135deg, #6366f1 0%, #4338ca 100%) !important;
    box-shadow: 0 6px 16px rgba(79, 70, 229, 0.3) !important;
    transform: translateY(-1px) !important;
    border-color: rgba(255, 255, 255, 0.2) !important;
}

/* Sidebar Diagnostic Preset Buttons */
div[data-testid="stSidebar"] .stButton>button {
    background: rgba(30, 41, 59, 0.4) !important;
    color: #e2e8f0 !important;
    border: 1px solid rgba(255, 255, 255, 0.05) !important;
    text-align: left !important;
    box-shadow: none !important;
    margin-bottom: 5px !important;
    font-size: 13px !important;
}

div[data-testid="stSidebar"] .stButton>button:hover {
    background: rgba(79, 70, 229, 0.15) !important;
    border-color: rgba(99, 102, 241, 0.3) !important;
    color: #ffffff !important;
    transform: translateX(2px) !important;
}

/* Expanders Styling */
.stElementContainer div[data-testid="stExpander"] {
    background: rgba(15, 23, 42, 0.3);
    border: 1px solid rgba(255, 255, 255, 0.05);
    border-radius: 8px;
}

/* Architecture Flow styles */
.arch-flow {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 15px;
    padding: 10px;
}
.arch-step {
    background: rgba(15, 23, 42, 0.6);
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 10px;
    padding: 12px 20px;
    width: 320px;
    text-align: center;
    font-weight: 600;
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.25);
    transition: all 0.3s ease;
}
.arch-step:hover {
    transform: scale(1.02);
}
.arch-step.mobile { border-color: #3b82f6; color: #60a5fa; }
.arch-step.cloud { border-color: #6366f1; color: #a5b4fc; }
.arch-step.agent { border-color: #10b981; color: #34d399; }
.arch-step.vehicle { border-color: #ef4444; color: #f87171; }
.arch-connector {
    color: rgba(255, 255, 255, 0.2);
    font-size: 18px;
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)

# Helper Functions to Draw High-End UI Cards
def draw_telemetry_card(title, value, status, icon, glow_color):
    html = f"""
    <div style="
        background: rgba(30, 41, 59, 0.25);
        border: 1px solid rgba(255, 255, 255, 0.06);
        border-radius: 12px;
        padding: 18px;
        display: flex;
        align-items: center;
        gap: 15px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
        transition: all 0.3s ease;
    ">
        <div style="
            font-size: 24px;
            background: rgba(255, 255, 255, 0.03);
            padding: 10px;
            border-radius: 8px;
            border: 1px solid rgba(255, 255, 255, 0.08);
            color: {glow_color};
            box-shadow: 0 0 10px {glow_color}1a;
            display: flex;
            align-items: center;
            justify-content: center;
        ">
            {icon}
        </div>
        <div style="flex-grow: 1;">
            <div style="font-size: 11px; color: #9CA3AF; text-transform: uppercase; letter-spacing: 0.05em; font-weight:600;">{title}</div>
            <div style="font-size: 22px; font-weight: 700; color: #FFFFFF; margin-top: 2px;">{value}</div>
            <div style="font-size: 11px; color: {glow_color}; font-weight: 500; margin-top: 4px; display: flex; align-items: center; gap: 4px;">
                <span style="height: 6px; width: 6px; background-color: {glow_color}; border-radius: 50%; display: inline-block;"></span>
                {status}
            </div>
        </div>
    </div>
    """
    return clean_html(html)

def draw_agent_status(name, status, description, icon):
    if status == "COMPLETED":
        badge_color = "#10B981"
        bg_color = "rgba(16, 185, 129, 0.06)"
        border_color = "rgba(16, 185, 129, 0.15)"
    elif status == "SKIPPED":
        badge_color = "#9CA3AF"
        bg_color = "rgba(156, 163, 175, 0.04)"
        border_color = "rgba(156, 163, 175, 0.1)"
    else: # PENDING
        badge_color = "#F59E0B"
        bg_color = "rgba(245, 158, 11, 0.06)"
        border_color = "rgba(245, 158, 11, 0.15)"
        
    html = f"""
    <div style="
        background: {bg_color};
        border: 1px solid {border_color};
        border-radius: 10px;
        padding: 12px 16px;
        margin-bottom: 10px;
        display: flex;
        align-items: center;
        justify-content: space-between;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
    ">
        <div style="display: flex; align-items: center; gap: 12px; max-width: 75%;">
            <span style="font-size: 20px;">{icon}</span>
            <div>
                <div style="font-size: 13px; font-weight: 600; color: #FFFFFF;">{name}</div>
                <div style="font-size: 11px; color: #9CA3AF; margin-top: 1px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap;">{description}</div>
            </div>
        </div>
        <div style="
            background: {badge_color}18;
            color: {badge_color};
            border: 1px solid {badge_color}33;
            padding: 2px 8px;
            border-radius: 12px;
            font-size: 10px;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.05em;
        ">
            {status}
        </div>
    </div>
    """
    return clean_html(html)

def draw_root_cause_card(root_cause, confidence, severity):
    sev = severity.lower()
    if sev == "low":
        color = "#0ea5e9"
        bg = "rgba(14, 165, 233, 0.05)"
        border = "rgba(14, 165, 233, 0.2)"
    elif sev == "medium":
        color = "#f59e0b"
        bg = "rgba(245, 158, 11, 0.05)"
        border = "rgba(245, 158, 11, 0.2)"
    elif sev == "high":
        color = "#f97316"
        bg = "rgba(249, 115, 22, 0.05)"
        border = "rgba(249, 115, 22, 0.2)"
    elif sev == "critical":
        color = "#ef4444"
        bg = "rgba(239, 68, 68, 0.05)"
        border = "rgba(239, 68, 68, 0.2)"
    else:
        color = "#818cf8"
        bg = "rgba(129, 140, 248, 0.05)"
        border = "rgba(129, 140, 248, 0.2)"
        
    html = f"""
    <div style="
        background: {bg};
        border: 1px solid {border};
        border-left: 5px solid {color};
        border-radius: 12px;
        padding: 20px;
        box-shadow: 0 4px 25px rgba(0, 0, 0, 0.2);
        margin-bottom: 20px;
    ">
        <div style="display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid rgba(255, 255, 255, 0.05); padding-bottom: 10px; margin-bottom: 12px;">
            <div style="font-size: 13px; font-weight: 700; color: {color}; text-transform: uppercase; letter-spacing: 0.05em; display: flex; align-items: center; gap: 8px;">
                <span>🚨</span> Root Cause Diagnostic
            </div>
            <div style="
                background: {color}18;
                color: {color};
                border: 1px solid {color}33;
                padding: 2px 8px;
                border-radius: 12px;
                font-size: 10px;
                font-weight: 700;
            ">
                {confidence*100:.0f}% CONFIDENCE
            </div>
        </div>
        <div style="font-size: 16px; font-weight: 600; color: #FFFFFF; line-height: 1.5;">
            {root_cause}
        </div>
    </div>
    """
    return clean_html(html)

def draw_resolution_card(resolution):
    html = f"""
    <div style="
        background: rgba(16, 185, 129, 0.04);
        border: 1px solid rgba(16, 185, 129, 0.15);
        border-left: 5px solid #10B981;
        border-radius: 12px;
        padding: 20px;
        box-shadow: 0 4px 25px rgba(0, 0, 0, 0.2);
        margin-bottom: 20px;
    ">
        <div style="font-size: 13px; font-weight: 700; color: #10B981; text-transform: uppercase; letter-spacing: 0.05em; display: flex; align-items: center; gap: 8px; border-bottom: 1px solid rgba(255, 255, 255, 0.05); padding-bottom: 10px; margin-bottom: 12px;">
            <span>🔧</span> Actionable Remediation
        </div>
        <div style="font-size: 16px; font-weight: 600; color: #FFFFFF; line-height: 1.5;">
            {resolution}
        </div>
    </div>
    """
    return clean_html(html)

def draw_escalation_card(is_escalated, reason):
    if is_escalated:
        color = "#EF4444"
        bg = "rgba(239, 68, 68, 0.05)"
        border = "rgba(239, 68, 68, 0.15)"
        title = "🛡️ Escalated to Tier-3 Automotive Engineering"
        desc = f"Diagnostic flag triggered. Reason: {reason}"
    else:
        color = "#10B981"
        bg = "rgba(16, 185, 129, 0.04)"
        border = "rgba(16, 185, 129, 0.15)"
        title = "⚡ Autonomous Action Active"
        desc = "Confidence is high. System dispatcher cleared for OTA remediation. No manual action required."
        
    html = f"""
    <div style="
        background: {bg};
        border: 1px solid {border};
        border-left: 5px solid {color};
        border-radius: 8px;
        padding: 15px;
        margin-bottom: 20px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
    ">
        <div style="font-size: 12px; font-weight: 700; color: {color}; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 4px;">
            {title}
        </div>
        <div style="font-size: 13px; color: #E2E8F0;">
            {desc}
        </div>
    </div>
    """
    return clean_html(html)

def draw_timeline(steps):
    if not steps:
        return "<p style='color:#9CA3AF;font-style:italic;'>No investigation trace logged.</p>"
    
    html = '<div style="position: relative; padding-left: 20px; border-left: 2px solid rgba(255, 255, 255, 0.08); margin-left: 15px; margin-top: 15px; margin-bottom: 10px;">'
    for i, step in enumerate(steps, start=1):
        if "skip" in step.lower():
            badge_style = "background: #6B7280; box-shadow: none;"
        else:
            badge_style = "background: #4f46e5; box-shadow: 0 0 8px #6366f1;"
            
        step_html = f"""
        <div style="position: relative; margin-bottom: 20px;">
            <div style="
                position: absolute;
                left: -27px;
                top: 4px;
                width: 12px;
                height: 12px;
                border-radius: 50%;
                {badge_style}
                border: 2px solid #070913;
            "></div>
            <div style="
                background: rgba(30, 41, 59, 0.15);
                border: 1px solid rgba(255, 255, 255, 0.04);
                border-radius: 8px;
                padding: 12px 16px;
                box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            ">
                <div style="font-size: 10px; color: #818cf8; font-weight: 700; text-transform: uppercase; letter-spacing: 0.05em;">Step {i}</div>
                <div style="font-size: 13px; color: #E2E8F0; font-weight: 500; margin-top: 2px;">{step}</div>
            </div>
        </div>
        """
        html += clean_html(step_html)
    html += '</div>'
    return html

# Pre-defined Cases for easy diagnostics testing
PRESETS = {
    "📱 Preset 1: App Pairing Disconnect (C001)": {
        "query": "My vehicle mobile app disconnects immediately after login",
        "customer_id": "C001",
        "vehicle_id": "V001"
    },
    "🔑 Preset 2: Door Unlock Failure (C001)": {
        "query": "My phone is showing an error when trying to unlock the vehicle doors",
        "customer_id": "C001",
        "vehicle_id": "V001"
    },
    "💳 Preset 3: Subscription Expired start (C001)": {
        "query": "Can you check my remote start? The dashboard says it is blocked.",
        "customer_id": "C001",
        "vehicle_id": "V001"
    },
    "📶 Preset 4: Navigation offline (C001)": {
        "query": "The screen inside the car says navigation network connection failed",
        "customer_id": "C001",
        "vehicle_id": "V001"
    }
}

# Session State Initialization to maintain diagnostic outputs across renders
if "investigation_result" not in st.session_state:
    st.session_state.investigation_result = None
if "execution_time" not in st.session_state:
    st.session_state.execution_time = 0.0
if "last_run_timestamp" not in st.session_state:
    st.session_state.last_run_timestamp = ""
if "customer_query_input" not in st.session_state:
    st.session_state.customer_query_input = ""
if "customer_id_input" not in st.session_state:
    st.session_state.customer_id_input = "C001"
if "vehicle_id_input" not in st.session_state:
    st.session_state.vehicle_id_input = "V001"

# Sidebar: Vehicle Console Controller
with st.sidebar:
    st.markdown("<h2 style='color:#FFFFFF;margin-bottom:0;'>🚗 Vehicle Control</h2>", unsafe_allow_html=True)
    st.markdown("<p style='color:#818cf8;font-size:12px;margin-bottom:20px;'>AUTONOMOUS DIAGNOSTICS NODE</p>", unsafe_allow_html=True)
    
    st.markdown("<h4>💡 CASE TEMPLATES</h4>", unsafe_allow_html=True)
    st.markdown("<p style='color:#9CA3AF;font-size:12px;margin-bottom:10px;'>Select a pre-configured scenario to populate variables and execute automatically.</p>", unsafe_allow_html=True)
    
    for label, preset_data in PRESETS.items():
        if st.button(label, key=f"p_{label}", use_container_width=True):
            st.session_state.customer_query_input = preset_data["query"]
            st.session_state.customer_id_input = preset_data["customer_id"]
            st.session_state.vehicle_id_input = preset_data["vehicle_id"]
            st.session_state.trigger_run = True
            st.rerun()

    st.divider()
    st.markdown("<h4>📡 NODE INSTANCE</h4>", unsafe_allow_html=True)
    st.success("API Router: Connected")
    st.info("Core Engine: v2.0-Enterprise")
    st.divider()
    st.code(f"active_case: {st.session_state.customer_id_input}\ntarget_node: {st.session_state.vehicle_id_input}\nsync_status: healthy", language="yaml")

# Header section
st.markdown("""
<div class="app-title-container">
    <div class="main-title">🚘 Connected Car Support Console</div>
    <div class="subtitle">Multi-Agent Diagnostics & Orchestration Dashboard • LangGraph Orchestrator</div>
</div>
""", unsafe_allow_html=True)

# Main Navigation Tabs
tabs = st.tabs(["🕹️ Diagnostics Console", "💾 Diagnostic Databases", "🗺️ System Architecture"])

run_diagnostics = False
if st.session_state.pop("trigger_run", False):
    run_diagnostics = True

# Tab 1: Diagnostics Console
with tabs[0]:
    # Form input columns
    col_input, col_telemetry = st.columns([3, 2])
    
    with col_input:
        st.markdown("<h3>🔍 Case Intake Profile</h3>", unsafe_allow_html=True)
        query = st.text_area(
            "Customer Complaint Details",
            value=st.session_state.customer_query_input,
            placeholder="Describe the complaint... e.g. My app is not connecting to the vehicle.",
            height=120,
            key="complaint_area"
        )
        st.session_state.customer_query_input = query
        
        id_col1, id_col2 = st.columns(2)
        with id_col1:
            customer_id = st.text_input("Customer ID", value=st.session_state.customer_id_input, key="c_id")
            st.session_state.customer_id_input = customer_id
        with id_col2:
            vehicle_id = st.text_input("Vehicle ID (VIN)", value=st.session_state.vehicle_id_input, key="v_id")
            st.session_state.vehicle_id_input = vehicle_id
            
        if st.button("🚀 Run Diagnostic Pipeline", use_container_width=True):
            run_diagnostics = True

    # Vehicle Telemetry Grid Column
    with col_telemetry:
        st.markdown("<h3>🚗 Target Vehicle Diagnostics</h3>", unsafe_allow_html=True)
        
        # Load values dynamically from telemetry if executed
        res = st.session_state.investigation_result
        if res and res.get("telematics_data"):
            tele = res.get("telematics_data", {})
            battery_val = f"{tele.get('battery', 78)}%"
            conn_val = "Online" if tele.get('online', True) else "Offline"
            net_val = tele.get('network', 'good').capitalize()
        else:
            battery_val = "87%"
            conn_val = "Online"
            net_val = "Good"
            
        battery_color = "#10B981" if int(battery_val.replace("%", "")) >= 65 else "#F59E0B"
        conn_color = "#10B981" if conn_val == "Online" else "#EF4444"
        net_color = "#0ea5e9" if net_val.lower() == "good" or net_val.lower() == "excellent" else "#F59E0B"
        
        grid_col1, grid_col2 = st.columns(2)
        with grid_col1:
            st.markdown(draw_telemetry_card("State of Charge", battery_val, "Optimal Capacity" if battery_val == "87%" else "Live Feed State", "🔋", battery_color), unsafe_allow_html=True)
            st.markdown(f"<div style='margin-top:12px;'></div>", unsafe_allow_html=True)
            st.markdown(draw_telemetry_card("Cellular Signal", net_val, "eSIM Transceiver", "🌐", net_color), unsafe_allow_html=True)
        with grid_col2:
            st.markdown(draw_telemetry_card("Connectivity", conn_val, "Vehicle Node ping", "📶", conn_color), unsafe_allow_html=True)
            st.markdown(f"<div style='margin-top:12px;'></div>", unsafe_allow_html=True)
            st.markdown(draw_telemetry_card("Cloud Sync", "Healthy", "Diagnostics Node Sync", "🔄", "#10B981"), unsafe_allow_html=True)

    # Trigger diagnostics flow
    if run_diagnostics:
        if not st.session_state.customer_query_input.strip():
            st.warning("Case details cannot be empty. Please input a complaint.")
        else:
            with st.spinner("Initiating LangGraph diagnostic coordinator & polling automotive sub-agents..."):
                start_time = time.time()
                result = graph.invoke({
                    "customer_query": st.session_state.customer_query_input,
                    "customer_id": st.session_state.customer_id_input,
                    "vehicle_id": st.session_state.vehicle_id_input
                })
                end_time = time.time()
                
                st.session_state.investigation_result = result
                st.session_state.execution_time = round(end_time - start_time, 2)
                st.session_state.last_run_timestamp = datetime.now().strftime('%d-%m-%Y %H:%M:%S')
                st.rerun()

    # Display diagnostics report if loaded
    if st.session_state.investigation_result:
        res = st.session_state.investigation_result
        st.divider()
        st.markdown("<h2>⚡ Diagnostics Analysis Report</h2>", unsafe_allow_html=True)
        
        # Summary Header Banner Metrics
        sum_col1, sum_col2, sum_col3, sum_col4, sum_col5 = st.columns(5)
        
        confidence = float(res.get("confidence", 0.0))
        confidence_pct = round(confidence * 100, 1)
        sev = res.get("severity", "Medium").upper()
        
        if sev.lower() == "low":
            sev_badge = f'<span style="background:rgba(14,165,233,0.1);color:#0ea5e9;border:1px solid #0ea5e9;padding:4px 12px;border-radius:12px;font-weight:700;font-size:12px;">{sev}</span>'
        elif sev.lower() == "medium":
            sev_badge = f'<span style="background:rgba(245,158,11,0.1);color:#f59e0b;border:1px solid #f59e0b;padding:4px 12px;border-radius:12px;font-weight:700;font-size:12px;">{sev}</span>'
        elif sev.lower() == "high":
            sev_badge = f'<span style="background:rgba(249,115,22,0.1);color:#f97316;border:1px solid #f97316;padding:4px 12px;border-radius:12px;font-weight:700;font-size:12px;">{sev}</span>'
        else:
            sev_badge = f'<span style="background:rgba(239,68,68,0.1);color:#ef4444;border:1px solid #ef4444;padding:4px 12px;border-radius:12px;font-weight:700;font-size:12px;">{sev}</span>'
            
        with sum_col1:
            st.metric("Issue Vector", res.get("issue_category", "N/A").replace("_", " ").title())
        with sum_col2:
            st.markdown(f"<div style='font-size:12px;color:#9CA3AF;margin-bottom:8px;font-weight:600;'>SEVERITY THREAT</div>{sev_badge}", unsafe_allow_html=True)
        with sum_col3:
            st.metric("AI Classifier Confidence", f"{confidence_pct}%")
        with sum_col4:
            st.metric("Pipeline Runtime", f"{st.session_state.execution_time}s")
        with sum_col5:
            st.metric("Case Stamp", st.session_state.last_run_timestamp.split()[-1] if st.session_state.last_run_timestamp else "N/A")
            
        st.markdown("<div style='margin-top:10px;'></div>", unsafe_allow_html=True)
        st.progress(confidence)
        
        # Split layout details
        out_col1, out_col2 = st.columns([3, 2])
        
        with out_col1:
            # Workflow Visualization Section
            st.markdown("<h3>🛣️ Diagnostic Workflow Flowchart</h3>", unsafe_allow_html=True)
            
            planner_decision = res.get("planner_decision", {})
            investigation_steps = res.get("investigation_steps", [])
            
            crm_executed = planner_decision.get("crm", False) or any("CRM" in s for s in investigation_steps)
            tele_executed = planner_decision.get("telematics", False) or any("Telematics Agent retrieved" in s or "Telematics" in s for s in investigation_steps)
            sub_executed = planner_decision.get("subscription", False) or any("Subscription status" in s or "Subscription" in s for s in investigation_steps)
            
            green_bg = "rgba(16, 185, 129, 0.08)"
            green_border = "#10b981"
            green_shadow = "0 0 10px rgba(16, 185, 129, 0.2)"
            green_text = "#34d399"
            
            gray_bg = "rgba(107, 114, 128, 0.05)"
            gray_border = "#4b5563"
            gray_shadow = "none"
            gray_text = "#9ca3af"

            # CRM
            if crm_executed:
                crm_bg, crm_border_style, crm_shadow_style, crm_color = green_bg, green_border, green_shadow, green_text
                crm_badge = '<span style="color:#10b981;font-weight:700;font-size:9px;">[EXECUTED]</span>'
                crm_desc = f"Profile: {res.get('crm_data', {}).get('name', 'N/A')}"
            else:
                crm_bg, crm_border_style, crm_shadow_style, crm_color = gray_bg, gray_border, gray_shadow, gray_text
                crm_badge = '<span style="color:#6b7280;font-weight:700;font-size:9px;">[SKIPPED]</span>'
                crm_desc = "Skipped by Planner Decision"
                
            # Telematics
            if tele_executed:
                tele_bg, tele_border_style, tele_shadow_style, tele_color = green_bg, green_border, green_shadow, green_text
                tele_badge = '<span style="color:#10b981;font-weight:700;font-size:9px;">[EXECUTED]</span>'
                tele_desc = f"ECU Charge: {res.get('telematics_data', {}).get('battery', 'N/A')}%"
                
                tele_skip_bg, tele_skip_border_style, tele_skip_shadow_style, tele_skip_color = gray_bg, gray_border, gray_shadow, gray_text
                tele_skip_badge = '<span style="color:#6b7280;font-weight:700;font-size:9px;">[SKIPPED]</span>'
                tele_skip_desc = "Path Not Taken"
            else:
                tele_bg, tele_border_style, tele_shadow_style, tele_color = gray_bg, gray_border, gray_shadow, gray_text
                tele_badge = '<span style="color:#6b7280;font-weight:700;font-size:9px;">[SKIPPED]</span>'
                tele_desc = "Skipped by Planner Decision"
                
                tele_skip_bg, tele_skip_border_style, tele_skip_shadow_style, tele_skip_color = green_bg, green_border, green_shadow, green_text
                tele_skip_badge = '<span style="color:#10b981;font-weight:700;font-size:9px;">[EXECUTED]</span>'
                tele_skip_desc = "Bypassed ECU Polling"
                
            # Subscription
            if sub_executed:
                sub_bg, sub_border_style, sub_shadow_style, sub_color = green_bg, green_border, green_shadow, green_text
                sub_badge = '<span style="color:#10b981;font-weight:700;font-size:9px;">[EXECUTED]</span>'
                sub_desc = f"Status: {res.get('subscription_status', 'N/A').upper()}"
                
                sub_skip_bg, sub_skip_border_style, sub_skip_shadow_style, sub_skip_color = gray_bg, gray_border, gray_shadow, gray_text
                sub_skip_badge = '<span style="color:#6b7280;font-weight:700;font-size:9px;">[SKIPPED]</span>'
                sub_skip_desc = "Path Not Taken"
            else:
                sub_bg, sub_border_style, sub_shadow_style, sub_color = gray_bg, gray_border, gray_shadow, gray_text
                sub_badge = '<span style="color:#6b7280;font-weight:700;font-size:9px;">[SKIPPED]</span>'
                sub_desc = "Skipped by Planner Decision"
                
                sub_skip_bg, sub_skip_border_style, sub_skip_shadow_style, sub_skip_color = green_bg, green_border, green_shadow, green_text
                sub_skip_badge = '<span style="color:#10b981;font-weight:700;font-size:9px;">[EXECUTED]</span>'
                sub_skip_desc = "Bypassed Subs Polling"
                
            # Escalation Check
            confidence_val = float(res.get("root_cause_confidence", 0.0))
            escalated = confidence_val < 0.70 or res.get("issue_category") == "unknown"
            if escalated:
                esc_title_color = "#ef4444"
                esc_border = "#ef4444"
                esc_bg = "rgba(239, 68, 68, 0.08)"
                esc_shadow = "0 0 10px rgba(239, 68, 68, 0.15)"
                esc_text = "Escalated: Low Confidence or Unknown Category"
                final_rec_text = "Escalated Support Dispatch"
            else:
                esc_title_color = "#10b981"
                esc_border = "#10b981"
                esc_bg = "rgba(16, 185, 129, 0.08)"
                esc_shadow = "0 0 10px rgba(16, 185, 129, 0.15)"
                esc_text = "Autonomous OTA Remediation Cleared"
                final_rec_text = "Autonomous OTA Remediation Dispatch"
                
            complaint_text = res.get("customer_query", "")
            if len(complaint_text) > 42:
                complaint_text = complaint_text[:39] + "..."
                
            rc_text = res.get("root_cause", "Undetermined")
            if len(rc_text) > 42:
                rc_text = rc_text[:39] + "..."
                
            res_text = res.get("resolution", "No solution mapped")
            if len(res_text) > 42:
                res_text = res_text[:39] + "..."

            flow_html = f"""
            <div style="display: flex; flex-direction: column; align-items: center; width: 100%; gap: 6px; padding: 20px; background: rgba(15, 23, 42, 0.3); border: 1px solid rgba(255, 255, 255, 0.06); border-radius: 12px; margin-bottom: 25px; box-shadow: 0 4px 25px rgba(0, 0, 0, 0.25);">
                
                <!-- Card 1: Customer Complaint -->
                <div style="width: 290px; background: {green_bg}; border: 1.5px solid {green_border}; border-radius: 8px; padding: 8px; text-align: center; color: white; box-shadow: {green_shadow};">
                    <div style="font-size: 11px; color: {green_text}; font-weight: 800; text-transform: uppercase; letter-spacing: 0.05em; display: flex; justify-content: space-between; align-items: center;">
                        <span>💬 Customer Complaint</span>
                        <span style="color:#10b981;font-weight:700;font-size:9px;">[EXECUTED]</span>
                    </div>
                    <div style="font-size: 11px; color: #9ca3af; margin-top: 3px; font-style: italic; overflow: hidden; text-overflow: ellipsis; white-space: nowrap;">"{complaint_text}"</div>
                </div>
                
                <div style="color: {green_border}; font-size: 14px; font-weight: bold; margin: -2px 0;">↓</div>
                
                <!-- Card 2: Intent + Planner Agent -->
                <div style="width: 290px; background: {green_bg}; border: 1.5px solid {green_border}; border-radius: 8px; padding: 8px; text-align: center; color: white; box-shadow: {green_shadow};">
                    <div style="font-size: 11px; color: {green_text}; font-weight: 800; text-transform: uppercase; letter-spacing: 0.05em; display: flex; justify-content: space-between; align-items: center;">
                        <span>🎯 Intent + Planner Agent</span>
                        <span style="color:#10b981;font-weight:700;font-size:9px;">[EXECUTED]</span>
                    </div>
                    <div style="font-size: 11px; color: #e2e8f0; margin-top: 3px; font-weight: 500;">
                        Classified: <span style="color: #818cf8; font-weight: 700;">{res.get('issue_category', 'unknown').upper()}</span>
                    </div>
                </div>
                
                <div style="color: {green_border}; font-size: 14px; font-weight: bold; margin: -2px 0;">↓</div>
                
                <!-- Card 3: CRM Agent -->
                <div style="width: 290px; background: {crm_bg}; border: 1.5px solid {crm_border_style}; border-radius: 8px; padding: 8px; text-align: center; color: white; box-shadow: {crm_shadow_style};">
                    <div style="font-size: 11px; color: {crm_color}; font-weight: 800; text-transform: uppercase; letter-spacing: 0.05em; display: flex; justify-content: space-between; align-items: center;">
                        <span>👤 CRM Agent</span>
                        {crm_badge}
                    </div>
                    <div style="font-size: 11px; color: #9ca3af; margin-top: 3px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap;">{crm_desc}</div>
                </div>
                
                <div style="color: {green_border}; font-size: 14px; font-weight: bold; margin: -2px 0;">↓</div>
                
                <!-- Card 4: Decision: Telematics Branch -->
                <div style="display: flex; flex-direction: column; align-items: center; width: 100%;">
                    <div style="font-size: 9px; color: #818cf8; text-transform: uppercase; font-weight: 800; letter-spacing: 0.05em; margin-bottom: 2px;">Decision: Telematics?</div>
                    <div style="display: flex; gap: 12px; justify-content: center; align-items: stretch; width: 100%;">
                        <!-- Telematics Agent Card -->
                        <div style="width: 145px; background: {tele_bg}; border: 1.5px solid {tele_border_style}; border-radius: 8px; padding: 6px; text-align: center; color: white; box-shadow: {tele_shadow_style}; display: flex; flex-direction: column; justify-content: space-between;">
                            <div style="font-size: 10px; color: {tele_color}; font-weight: 800; text-transform: uppercase; letter-spacing: 0.03em; display: flex; justify-content: space-between; align-items: center;">
                                <span>📡 Telematics</span>
                                {tele_badge}
                            </div>
                            <div style="font-size: 9px; color: #9ca3af; margin-top: 2px; line-height: 1.2; text-overflow: ellipsis; overflow: hidden; white-space: nowrap;">{tele_desc}</div>
                        </div>
                        <!-- Skip Card -->
                        <div style="width: 135px; background: {tele_skip_bg}; border: 1.5px solid {tele_skip_border_style}; border-radius: 8px; padding: 6px; text-align: center; color: white; box-shadow: {tele_skip_shadow_style}; display: flex; flex-direction: column; justify-content: space-between;">
                            <div style="font-size: 10px; color: {tele_skip_color}; font-weight: 800; text-transform: uppercase; letter-spacing: 0.03em; display: flex; justify-content: space-between; align-items: center;">
                                <span>⏭️ Skip</span>
                                {tele_skip_badge}
                            </div>
                            <div style="font-size: 9px; color: #9ca3af; margin-top: 2px; line-height: 1.2; text-overflow: ellipsis; overflow: hidden; white-space: nowrap;">{tele_skip_desc}</div>
                        </div>
                    </div>
                </div>
                
                <div style="color: {green_border}; font-size: 14px; font-weight: bold; margin: 2px 0 -2px 0;">↓</div>
                
                <!-- Card 5: Decision: Subscription Branch -->
                <div style="display: flex; flex-direction: column; align-items: center; width: 100%;">
                    <div style="font-size: 9px; color: #818cf8; text-transform: uppercase; font-weight: 800; letter-spacing: 0.05em; margin-bottom: 2px;">Decision: Subscription?</div>
                    <div style="display: flex; gap: 12px; justify-content: center; align-items: stretch; width: 100%;">
                        <!-- Subscription Agent Card -->
                        <div style="width: 145px; background: {sub_bg}; border: 1.5px solid {sub_border_style}; border-radius: 8px; padding: 6px; text-align: center; color: white; box-shadow: {sub_shadow_style}; display: flex; flex-direction: column; justify-content: space-between;">
                            <div style="font-size: 10px; color: {sub_color}; font-weight: 800; text-transform: uppercase; letter-spacing: 0.03em; display: flex; justify-content: space-between; align-items: center;">
                                <span>💳 Subscription</span>
                                {sub_badge}
                            </div>
                            <div style="font-size: 9px; color: #9ca3af; margin-top: 2px; line-height: 1.2; text-overflow: ellipsis; overflow: hidden; white-space: nowrap;">{sub_desc}</div>
                        </div>
                        <!-- Skip Card -->
                        <div style="width: 135px; background: {sub_skip_bg}; border: 1.5px solid {sub_skip_border_style}; border-radius: 8px; padding: 6px; text-align: center; color: white; box-shadow: {sub_skip_shadow_style}; display: flex; flex-direction: column; justify-content: space-between;">
                            <div style="font-size: 10px; color: {sub_skip_color}; font-weight: 800; text-transform: uppercase; letter-spacing: 0.03em; display: flex; justify-content: space-between; align-items: center;">
                                <span>⏭️ Skip</span>
                                {sub_skip_badge}
                            </div>
                            <div style="font-size: 9px; color: #9ca3af; margin-top: 2px; line-height: 1.2; text-overflow: ellipsis; overflow: hidden; white-space: nowrap;">{sub_skip_desc}</div>
                        </div>
                    </div>
                </div>
                
                <div style="color: {green_border}; font-size: 14px; font-weight: bold; margin: 2px 0 -2px 0;">↓</div>
                
                <!-- Card 6: Knowledge Base (RAG Agent) -->
                <div style="width: 290px; background: {green_bg}; border: 1.5px solid {green_border}; border-radius: 8px; padding: 8px; text-align: center; color: white; box-shadow: {green_shadow};">
                    <div style="font-size: 11px; color: {green_text}; font-weight: 800; text-transform: uppercase; letter-spacing: 0.05em; display: flex; justify-content: space-between; align-items: center;">
                        <span>📚 Knowledge Base (RAG)</span>
                        <span style="color:#10b981;font-weight:700;font-size:9px;">[EXECUTED]</span>
                    </div>
                    <div style="font-size: 11px; color: #9ca3af; margin-top: 3px;">Retrieved technical manuals and bulletins</div>
                </div>
                
                <div style="color: {green_border}; font-size: 14px; font-weight: bold; margin: -2px 0;">↓</div>
                
                <!-- Card 7: Investigation Agent -->
                <div style="width: 290px; background: {green_bg}; border: 1.5px solid {green_border}; border-radius: 8px; padding: 8px; text-align: center; color: white; box-shadow: {green_shadow};">
                    <div style="font-size: 11px; color: {green_text}; font-weight: 800; text-transform: uppercase; letter-spacing: 0.05em; display: flex; justify-content: space-between; align-items: center;">
                        <span>🔍 Investigation Agent</span>
                        <span style="color:#10b981;font-weight:700;font-size:9px;">[EXECUTED]</span>
                    </div>
                    <div style="font-size: 11px; color: #9ca3af; margin-top: 3px;">Synthesized evidence logs and telemetry</div>
                </div>
                
                <div style="color: {green_border}; font-size: 14px; font-weight: bold; margin: -2px 0;">↓</div>
                
                <!-- Card 8: Root Cause Analysis -->
                <div style="width: 290px; background: {green_bg}; border: 1.5px solid {green_border}; border-radius: 8px; padding: 8px; text-align: center; color: white; box-shadow: {green_shadow};">
                    <div style="font-size: 11px; color: {green_text}; font-weight: 800; text-transform: uppercase; letter-spacing: 0.05em; display: flex; justify-content: space-between; align-items: center;">
                        <span>🧠 Root Cause Analysis</span>
                        <span style="color:#10b981;font-weight:700;font-size:9px;">[EXECUTED]</span>
                    </div>
                    <div style="font-size: 11px; color: #e2e8f0; margin-top: 3px; font-weight: 600; text-overflow: ellipsis; overflow: hidden; white-space: nowrap;">{rc_text}</div>
                </div>
                
                <div style="color: {green_border}; font-size: 14px; font-weight: bold; margin: -2px 0;">↓</div>
                
                <!-- Card 9: Resolution Generation -->
                <div style="width: 290px; background: {green_bg}; border: 1.5px solid {green_border}; border-radius: 8px; padding: 8px; text-align: center; color: white; box-shadow: {green_shadow};">
                    <div style="font-size: 11px; color: {green_text}; font-weight: 800; text-transform: uppercase; letter-spacing: 0.05em; display: flex; justify-content: space-between; align-items: center;">
                        <span>🔧 Resolution Generation</span>
                        <span style="color:#10b981;font-weight:700;font-size:9px;">[EXECUTED]</span>
                    </div>
                    <div style="font-size: 11px; color: #e2e8f0; margin-top: 3px; font-weight: 500; text-overflow: ellipsis; overflow: hidden; white-space: nowrap;">{res_text}</div>
                </div>
                
                <div style="color: {green_border}; font-size: 14px; font-weight: bold; margin: -2px 0;">↓</div>
                
                <!-- Card 10: Escalation Check -->
                <div style="width: 290px; background: {esc_bg}; border: 1.5px solid {esc_border}; border-radius: 8px; padding: 8px; text-align: center; color: white; box-shadow: {esc_shadow};">
                    <div style="font-size: 11px; color: {esc_title_color}; font-weight: 800; text-transform: uppercase; letter-spacing: 0.05em; display: flex; justify-content: space-between; align-items: center;">
                        <span>🛡️ Escalation Check</span>
                        <span style="color:#10b981;font-weight:700;font-size:9px;">[EXECUTED]</span>
                    </div>
                    <div style="font-size: 11px; color: #9ca3af; margin-top: 3px; text-overflow: ellipsis; overflow: hidden; white-space: nowrap;">{esc_text}</div>
                </div>
                
                <div style="color: {green_border}; font-size: 14px; font-weight: bold; margin: -2px 0;">↓</div>
                
                <!-- Card 11: Final Support Recommendation -->
                <div style="width: 290px; background: {green_bg}; border: 1.5px solid {green_border}; border-radius: 8px; padding: 8px; text-align: center; color: white; box-shadow: {green_shadow};">
                    <div style="font-size: 11px; color: {green_text}; font-weight: 800; text-transform: uppercase; letter-spacing: 0.05em; display: flex; justify-content: space-between; align-items: center;">
                        <span>📋 Final Recommendation</span>
                        <span style="color:#10b981;font-weight:700;font-size:9px;">[EXECUTED]</span>
                    </div>
                    <div style="font-size: 11px; color: #818cf8; margin-top: 3px; font-weight: 700; text-overflow: ellipsis; overflow: hidden; white-space: nowrap;">{final_rec_text}</div>
                </div>
                
            </div>
            """
            st.markdown(clean_html(flow_html), unsafe_allow_html=True)

            st.markdown(draw_root_cause_card(res.get("root_cause", "Undetermined"), res.get("root_cause_confidence", 0.0), sev), unsafe_allow_html=True)
            st.markdown(draw_resolution_card(res.get("resolution", "No solution mapped")), unsafe_allow_html=True)
            
            # Evidence catalog
            st.markdown("<h3>📋 System Evidence Trace</h3>", unsafe_allow_html=True)
            evidence = res.get("evidence_used", [])
            if evidence:
                evidence_html = "<div style='background:rgba(30, 41, 59, 0.15);border:1px solid rgba(255,255,255,0.04);border-radius:10px;padding:18px;margin-bottom:20px;'>"
                for item in evidence:
                    item_html = f"""
                    <div style='display:flex;align-items:flex-start;gap:10px;margin-bottom:10px;'>
                        <span style='color:#10B981;font-weight:bold;font-size:16px;'>✓</span>
                        <span style='font-size:13px;color:#E2E8F0;line-height:1.4;'>{item}</span>
                    </div>
                    """
                    evidence_html += clean_html(item_html)
                evidence_html += "</div>"
                st.markdown(evidence_html, unsafe_allow_html=True)
            else:
                st.info("No primary evidence elements captured during this execution cycle.")
                
            # Governance Escalation Section
            st.markdown("<h3>🛡️ Governance & Safety Dispatch</h3>", unsafe_allow_html=True)
            escalate_flag = False
            escalate_reason = ""
            if res.get("root_cause_confidence", 0) < 0.70:
                escalate_flag = True
                escalate_reason = "System classification confidence score fell below acceptable threshold (< 70%)"
            elif res.get("issue_category") == "unknown":
                escalate_flag = True
                escalate_reason = "Target category classified as 'unknown'"
                
            st.markdown(draw_escalation_card(escalate_flag, escalate_reason), unsafe_allow_html=True)
            
            # Sub-agent state viewer metrics
            st.markdown("<h3>🧠 Active Sub-Agent Database Inspector</h3>", unsafe_allow_html=True)
            sub1, sub2, sub3, sub4 = st.columns(4)
            with sub1:
                with st.expander("👤 CRM Registry", expanded=False):
                    st.json(res.get("crm_data", {}))
            with sub2:
                with st.expander("📡 Telematics ECU", expanded=False):
                    st.json(res.get("telematics_data", {}))
            with sub3:
                with st.expander("💳 Subscriptions", expanded=False):
                    if res.get("subscription_status"):
                        st.info(f"Status: {res.get('subscription_status')}")
                    else:
                        st.warning("Not queried")
            with sub4:
                with st.expander("📚 Knowledge KB", expanded=False):
                    st.text_area("RAG Reference", value=res.get("kb_context", ""), height=150, disabled=True, key="kb_area_view")
                    
        with out_col2:
            st.markdown("<h3>🤖 Diagnostic Agent Pipeline</h3>", unsafe_allow_html=True)
            
            # Draw status details for each Agent
            st.markdown(draw_agent_status("Intent & Planner Classifier", "COMPLETED", f"Intent: {res.get('issue_category', 'unknown').upper()}", "🎯"), unsafe_allow_html=True)
            
            crm_s = "COMPLETED" if res.get("crm_data") else "SKIPPED"
            crm_d = f"Retrieved record for {res.get('crm_data', {}).get('name', 'N/A')}" if res.get("crm_data") else "Bypassed by coordinator decision"
            st.markdown(draw_agent_status("CRM History Profiler", crm_s, crm_d, "👤"), unsafe_allow_html=True)
            
            tele_s = "COMPLETED" if res.get("telematics_data") else "SKIPPED"
            tele_d = "Parsed live telematics frame" if res.get("telematics_data") else "Telemetry validation bypassed"
            st.markdown(draw_agent_status("Telematics Diagnostics", tele_s, tele_d, "📡"), unsafe_allow_html=True)
            
            sub_s = "COMPLETED" if res.get("subscription_status") else "SKIPPED"
            sub_d = f"Status validation: {res.get('subscription_status')}" if res.get("subscription_status") else "Subscription validation bypassed"
            st.markdown(draw_agent_status("Subscription Verification", sub_s, sub_d, "💳"), unsafe_allow_html=True)
            
            kb_s = "COMPLETED" if res.get("kb_context") else "SKIPPED"
            kb_d = "Retrieved RAG resolution blueprints" if res.get("kb_context") else "RAG system bypassed"
            st.markdown(draw_agent_status("Knowledge Base RAG Searcher", kb_s, kb_d, "📚"), unsafe_allow_html=True)
            
            rc_s = "COMPLETED" if res.get("root_cause") else "SKIPPED"
            rc_d = "Compiled root failure point"
            st.markdown(draw_agent_status("Root Cause Analyst Node", rc_s, rc_d, "🧠"), unsafe_allow_html=True)
            
            resol_s = "COMPLETED" if res.get("resolution") else "SKIPPED"
            resol_d = "Composed final repair procedure"
            st.markdown(draw_agent_status("Actionable Resolution Node", resol_s, resol_d, "🔧"), unsafe_allow_html=True)
            
            # Stepper Timeline View
            st.markdown("<h3>🕒 Diagnostics Flow Trace</h3>", unsafe_allow_html=True)
            st.markdown(draw_timeline(res.get("investigation_steps", [])), unsafe_allow_html=True)
            
            with st.expander("🛠 View Orchestrator Log Frame"):
                st.json(res)
    else:
        st.divider()
        st.markdown("""
        <div style="text-align: center; padding: 60px 40px; border: 2px dashed rgba(255, 255, 255, 0.05); border-radius: 16px; background: rgba(30, 41, 59, 0.1); box-shadow: inset 0 4px 20px rgba(0,0,0,0.15);">
            <div style="font-size: 50px; margin-bottom: 20px; color: #4f46e5; filter: drop-shadow(0 0 10px rgba(79, 70, 229, 0.3));">🛸</div>
            <h3 style="color: #FFFFFF; font-weight:600; font-size:22px; margin-bottom: 10px;">Diagnostic Console Standby</h3>
            <p style="color: #9CA3AF; font-size: 14px; max-width: 480px; margin: 0 auto 24px auto; line-height:1.6;">
                The Agentic AI Support node is online. Choose a preset template case from the sidebar or enter a custom customer log to execute diagnostics.
            </p>
        </div>
        """, unsafe_allow_html=True)

# Tab 2: Live Diagnostic Databases
with tabs[1]:
    st.markdown("<h2>💾 Diagnostic Registry Databases</h2>", unsafe_allow_html=True)
    st.markdown("<p style='color:#9CA3AF;margin-bottom:30px;'>Support technician portal. Displays live diagnostic registers, subscriptions, and telemetry databases.</p>", unsafe_allow_html=True)
    
    db_col1, db_col2 = st.columns(2)
    
    with db_col1:
        st.markdown("<h3>👤 Customer Profile Database (CRM)</h3>", unsafe_allow_html=True)
        try:
            with open("data/crm.json") as f:
                crm_db = json.load(f)
            crm_list = []
            for cid, details in crm_db.items():
                crm_list.append({
                    "Customer ID": cid,
                    "Full Name": details.get("name", "N/A"),
                    "Linked Vehicle (VIN)": details.get("vehicle_id", "N/A"),
                    "Prior Cases count": details.get("previous_tickets", 0)
                })
            st.dataframe(pd.DataFrame(crm_list), use_container_width=True)
        except Exception as e:
            st.error(f"Failed to read CRM Database: {e}")
            
        st.markdown("<div style='margin-top:24px;'></div>", unsafe_allow_html=True)
        st.markdown("<h3>💳 Service Entitlement Subscriptions</h3>", unsafe_allow_html=True)
        try:
            with open("data/subscriptions.json") as f:
                sub_db = json.load(f)
            sub_list = []
            for cid, details in sub_db.items():
                sub_list.append({
                    "Customer ID": cid,
                    "Subscription Status": details.get("status", "N/A").upper()
                })
            st.dataframe(pd.DataFrame(sub_list), use_container_width=True)
        except Exception as e:
            st.error(f"Failed to load Subscription Database: {e}")
            
    with db_col2:
        st.markdown("<h3>🛰️ ECU Telematics Diagnostic Registers</h3>", unsafe_allow_html=True)
        try:
            with open("data/telematics.json") as f:
                tele_db = json.load(f)
            tele_list = []
            for vid, details in tele_db.items():
                tele_list.append({
                    "Vehicle ID (VIN)": vid,
                    "eSIM Network register": "ONLINE" if details.get("online") else "OFFLINE",
                    "ECU Charge SOC": f"{details.get('battery', 0)}%",
                    "RSSI Signal Strength": details.get("network", "N/A").upper()
                })
            st.dataframe(pd.DataFrame(tele_list), use_container_width=True)
        except Exception as e:
            st.error(f"Failed to load Telematics database: {e}")

# Tab 3: System Architecture
with tabs[2]:
    st.markdown("<h2>🗺️ Workflow Architecture Specification</h2>", unsafe_allow_html=True)
    st.markdown("<p style='color:#9CA3AF;margin-bottom:25px;'>Technical blueprint demonstrating multi-agent orchestrations, vehicle transceiver systems, and workflow loops.</p>", unsafe_allow_html=True)
    
    arch_html = """
    <div style="padding: 30px 15px; display: flex; flex-direction: column; align-items: center; gap: 15px; background: rgba(30, 41, 59, 0.15); border: 1px solid rgba(255, 255, 255, 0.05); border-radius: 16px; margin-bottom: 25px; box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.25);">
        <h4 style="color:#FFFFFF; margin-bottom: 20px; text-align:center; letter-spacing:0.05em; font-weight:700;">WORKFLOW ARCHITECTURE</h4>
        
        <!-- Layer 1: Mobile Client -->
        <div class="arch-step mobile" style="border-radius: 20px; border-width: 2px; border-color: #3b82f6; width: 265px; padding: 15px; background: rgba(59, 130, 246, 0.06); box-shadow: 0 4px 15px rgba(59, 130, 246, 0.1); margin-bottom: 2px;">
            <div style="font-size: 26px; margin-bottom: 4px;">📱</div>
            <div style="font-size: 15px; font-weight: 800;">Mobile Intake Client</div>
            <div style="color: #9ca3af; font-size: 11px; margin-top: 2px; font-weight: normal;">Submits customer complaint log</div>
        </div>
        
        <div style="color: #818cf8; font-size: 18px; font-weight: bold; margin: 2px 0;">⬇️</div>
        
        <!-- Layer 2: Coordinator Router -->
        <div class="arch-step cloud" style="border-radius: 10px; border-width: 2px; border-color: #6366f1; width: 280px; padding: 12px; background: rgba(99, 102, 241, 0.06); border-style: double; box-shadow: 0 4px 15px rgba(99, 102, 241, 0.1); margin-bottom: 2px;">
            <div style="font-size: 26px; margin-bottom: 4px;">🔀</div>
            <div style="font-size: 15px; font-weight: 800;">LangGraph Router</div>
            <div style="color: #9ca3af; font-size: 11px; margin-top: 2px; font-weight: normal;">Evaluates intent & selects nodes</div>
        </div>
        
        <div style="color: #818cf8; font-size: 18px; font-weight: bold; margin: 2px 0;">⬇️</div>
        
        <!-- Layer 3: Parallel Sub-Agents -->
        <div style="display: flex; gap: 15px; flex-wrap: wrap; justify-content: center; width: 100%; max-width: 850px; margin: 10px 0;">
            <!-- CRM Node -->
            <div class="arch-step agent" style="border-radius: 12px; border-width: 1px; border-color: #10b981; width: 180px; padding: 15px 10px; background: rgba(16, 185, 129, 0.04); text-align: center;">
                <div style="font-size: 24px; margin-bottom: 4px;">👤</div>
                <div style="font-weight: 700; font-size: 13px; color: #34d399;">CRM Profiler</div>
                <div style="color: #9ca3af; font-size: 10px; margin-top: 2px; font-weight: normal;">Retrieves profile records</div>
            </div>
            
            <!-- Telematics Node -->
            <div class="arch-step agent" style="border-radius: 12px; border-width: 1px; border-color: #10b981; width: 180px; padding: 15px 10px; background: rgba(16, 185, 129, 0.04); text-align: center;">
                <div style="font-size: 24px; margin-bottom: 4px;">📡</div>
                <div style="font-weight: 700; font-size: 13px; color: #34d399;">Telematics ECU</div>
                <div style="color: #9ca3af; font-size: 10px; margin-top: 2px; font-weight: normal;">Checks vehicle signal</div>
            </div>
            
            <!-- Subscription Node -->
            <div class="arch-step agent" style="border-radius: 12px; border-width: 1px; border-color: #10b981; width: 180px; padding: 15px 10px; background: rgba(16, 185, 129, 0.04); text-align: center;">
                <div style="font-size: 24px; margin-bottom: 4px;">💳</div>
                <div style="font-weight: 700; font-size: 13px; color: #34d399;">Subscription Check</div>
                <div style="color: #9ca3af; font-size: 10px; margin-top: 2px; font-weight: normal;">Validates account state</div>
            </div>
            
            <!-- RAG Node -->
            <div class="arch-step agent" style="border-radius: 12px; border-width: 1px; border-color: #10b981; width: 180px; padding: 15px 10px; background: rgba(16, 185, 129, 0.04); text-align: center;">
                <div style="font-size: 24px; margin-bottom: 4px;">📚</div>
                <div style="font-weight: 700; font-size: 13px; color: #34d399;">Knowledge RAG</div>
                <div style="color: #9ca3af; font-size: 10px; margin-top: 2px; font-weight: normal;">Finds manual steps</div>
            </div>
        </div>
        
        <div style="color: #10b981; font-size: 18px; font-weight: bold; margin: 2px 0;">⬇️</div>
        
        <!-- Layer 4: Synthesis Node -->
        <div class="arch-step cloud" style="border-radius: 14px; border-width: 2px; border-color: #10b981; width: 280px; padding: 15px; background: rgba(16, 185, 129, 0.06); box-shadow: 0 4px 15px rgba(16, 185, 129, 0.1); margin-bottom: 2px;">
            <div style="font-size: 26px; margin-bottom: 4px;">🧠</div>
            <div style="font-size: 15px; font-weight: 800; color: #34d399;">Root Cause Synthesis</div>
            <div style="color: #e2e8f0; font-size: 11px; margin-top: 2px; font-weight: normal;">Formulates diagnostic repair plans</div>
        </div>
        
        <div style="color: #ef4444; font-size: 18px; font-weight: bold; margin: 2px 0;">⬇️</div>
        
        <!-- Layer 5: Vehicle Target -->
        <div class="arch-step vehicle" style="border-radius: 18px; border-width: 2px; border-color: #ef4444; width: 265px; padding: 15px; background: rgba(239, 68, 68, 0.06); box-shadow: 0 4px 15px rgba(239, 68, 68, 0.1);">
            <div style="font-size: 30px; margin-bottom: 4px;">🚗</div>
            <div style="font-size: 16px; font-weight: 800; color: #f87171;">Target Connected Vehicle</div>
            <div style="color: #9ca3af; font-size: 11px; margin-top: 2px; font-weight: normal;">Receives OTA lock/unlock execution</div>
        </div>
    </div>
    """
    st.markdown(clean_html(arch_html), unsafe_allow_html=True)
    
    st.markdown("### 🧬 Orchestration Logic Blueprint")
    st.markdown("""
    The dashboard diagnostic backbone is orchestrated using a LangGraph DAG (Directed Acyclic Graph):
    1. **Intake & Classification**: The customer's text query is parsed by the **Intent Agent** to establish the primary category (`app_pairing`, `connectivity_issue`, etc.) and severity profile.
    2. **Orchestrator Planner**: Evaluates the classification results and decides which system queries are required. 
       - e.g. A door lock issue skips cellular checks and triggers CRM validation.
    3. **Parallel Agents Polling**: LangGraph executes sub-agents which connect to real-world resources (CRM Databases, eSIM Status transceivers, Subscription registries).
    4. **Knowledge Retrieval (RAG)**: Connects with a vector database holding product manuals, technical bulletins, and FAQs to supply resolving documentation context.
    5. **Synthesis Node**: The **Root Cause Agent** and **Resolution Agent** compile all evidence logs and produce a cohesive analysis output, determining whether the problem can be addressed autonomously or requires human escalations.
    """)