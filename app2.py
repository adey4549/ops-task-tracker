from datetime import datetime
import os
import pandas as pd
import streamlit as st
import getpass

st.set_page_config(page_title="Ops Task Logger", layout="centered")

st.title("⚡ Operational Task Logger")
st.caption("Quick Log: Submit completed task metadata under 5 seconds.")

CURRENT_USER = getpass.getuser().upper()


def clear_form_state():
  """Resets widget keys in session state to default values."""
  st.session_state["input_txn"] = ""
  st.session_state["input_req"] = "Security Master Setup"
  st.session_state["input_role"] = "Maker"
  st.session_state["input_err"] = 0
  st.session_state["input_vol"] = 1


# Ensure session state is initialized on first load
if "input_txn" not in st.session_state:
  clear_form_state()


def handle_submit():
  """Saves record and clears the form before rerun."""
  txn_val = st.session_state.get("input_txn", "").strip()

  if not txn_val:
    st.session_state["toast_info"] = (
        "Transaction ID is mandatory! Enter an ID or type 'N/A'.", "⚠️"
    )
    return
    
  new_record = {
      "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
      "user_id": CURRENT_USER,
      "transaction_id": txn_val,
      "request_type": st.session_state.get(
          "input_req", "Security Master Setup"
      ),
      "role": st.session_state.get("input_role", "Maker"),
      "error_count": st.session_state.get("input_err", 0),
      "volume_count": st.session_state.get("input_vol", 1),
  }

  df_new = pd.DataFrame([new_record])
  file_exists = os.path.isfile("ops_task_logs.csv")
  df_new.to_csv(
      "ops_task_logs.csv", mode="a", header=not file_exists, index=False
  )

  clear_form_state()
  st.session_state["toast_info"] = ("Task saved successfully!", "✅")


def handle_clear():
  """Clears form fields before rerun."""
  clear_form_state()
  st.session_state["toast_info"] = ("Form cleared.", "🧹")


# Header fields
col1, col2 = st.columns(2)
with col1:
  st.text_input("User ID", value=CURRENT_USER, disabled=True)
with col2:
  st.text_input(
      "Timestamp",
      value=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
      disabled=True,
  )

# --- Standard inputs ---
st.text_input(
    "Transaction / Ticket ID *",
    placeholder="e.g., TXN-98421 (If none, enter N/A)",
    key="input_txn",
)

st.selectbox(
    "Request Type",
    options=[
        "Security Master Setup",
        "Daily NAV Pricing Discrepancy",
        "Corporate Action Event Scrubbing",
        "Cash & Trade Break Recon",
        "Static Reference Data Update",
    ],
    key="input_req",
)

st.radio(
    "Function Role",
    options=["Maker", "Checker"],
    horizontal=True,
    key="input_role",
)

st.number_input(
    "Error Count", min_value=0, max_value=50, step=1, key="input_err"
)

st.number_input(
    "Volume Count (Items Processed)",
    min_value=1,
    max_value=500,
    step=1,
    key="input_vol",
)

# Action Buttons with callbacks
btn_col1, btn_col2 = st.columns(2)
with btn_col1:
  st.button(
      "Submit Task (1-Click)", on_click=handle_submit, use_container_width=True
  )
with btn_col2:
  st.button("Clear / Reset", on_click=handle_clear, use_container_width=True)

# Display toast notification if set during callback
if "toast_info" in st.session_state:
  msg, icon = st.session_state.pop("toast_info")
  st.toast(msg, icon=icon)