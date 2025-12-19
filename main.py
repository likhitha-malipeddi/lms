import os
import io
import datetime
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from sqlalchemy import create_engine, text
from dotenv import load_dotenv
from ui_helpers import (render_header, render_kpi_row)

# Load environment variables
load_dotenv()

# Basic logging (logs to terminal)
import logging

LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()
logging.basicConfig(level=LOG_LEVEL, format='%(asctime)s %(levelname)s %(message)s')
logger = logging.getLogger('qipp_dashboard')


# Initialize session state for navigation
if 'page' not in st.session_state:
    st.session_state['page'] = 'Home'
if 'selected_material' not in st.session_state:
    st.session_state['selected_material'] = None
if 'selected_plant' not in st.session_state:
    st.session_state['selected_plant'] = None

# Streamlit page config
st.set_page_config(page_title="Demand Forecast Dashboard", layout="wide")

# ==========================================
# PAGE HEADER (ONLY AFTER LOGIN)
# ==========================================
if st.session_state.get('authenticated', False):

    # HOME PAGE
    if st.session_state['page'] == 'Home':
        render_header(
            "Hey Admin",
        )

# ==========================================
# AUTHENTICATION
# ==========================================
if 'authenticated' not in st.session_state:
    st.session_state['authenticated'] = False

if not st.session_state['authenticated']:
    # Custom CSS for blue-themed login page
    st.markdown("""
<style>
    /* Hide default Streamlit elements on login page */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* Blue gradient background */
    .stApp {
        background: linear-gradient(135deg, #020617 0%, #0f172a 50%, #1e3a8a 100%);
        overflow: hidden; /* Prevent scrolling on body if possible */
    }

    /* Login container styling */
    .login-container {
        display: flex;
        height: 90vh; /* Fixed height to viewport */
        align-items: center;
        justify-content: center;
        padding: 1rem;
    }

    /* Card styling - Dark Glassmorphism */
    .login-card {
        background: rgba(15, 23, 42, 0.6);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 24px;
        box-shadow: 0 30px 60px -12px rgba(0, 0, 0, 0.6);
        overflow: hidden;
        display: flex;
        width: 100%;
        max-width: 1100px; /* Constrain width */
    }

    /* typography */
    .platform-name {
        font-size: 32px; /* Slightly smaller */
        font-weight: 800;
        color: #ffffff !important;
        margin-bottom: 0.2rem;
        line-height: 1.1;
        text-shadow: 0 2px 4px rgba(0,0,0,0.5);
    }

    .platform-tagline {
        color: #94a3b8;
        font-size: 14px;
        margin-bottom: 1.5rem;
    }

    /* Input styling - Dark Theme */
    .stTextInput > div > div > input {
        background: rgba(30, 41, 59, 0.5) !important; /* Dark semi-transparent */
        color: #ffffff !important; /* White Text */
        border: 1px solid rgba(148, 163, 184, 0.2) !important;
        border-radius: 12px !important;
        padding: 12px 14px !important; /* Reduced padding */
        font-size: 15px !important;
    }

    /* Input Label styling */
    .stTextInput > label {
        color: #e2e8f0 !important;
        font-size: 13px !important;
        font-weight: 500 !important;
    }

    .stButton > button {
        background: linear-gradient(135deg, #3b82f6, #2563eb) !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 12px 24px !important; /* Reduced padding */
        font-size: 16px !important;
        font-weight: 600 !important;
        width: 100% !important;
        box-shadow: 0 4px 15px rgba(59, 130, 246, 0.4) !important;
        margin-top: 5px;
    }

    .stButton > button:hover {
        background: linear-gradient(135deg, #2563eb, #1d4ed8) !important;
        transform: translateY(-1px);
        box-shadow: 0 6px 20px rgba(59, 130, 246, 0.5) !important;
    }

    /* Compact layout adjustments */
    .block-container {
        padding-top: 2rem !important;
        padding-bottom: 1rem !important;
        max-width: 1200px;
    }

</style>
""", unsafe_allow_html=True)

    # Layout: 1.2 : 1 ratio
    left_col, right_col = st.columns([1.2, 1], gap="large")

    # --- LEFT COLUMN: Hero Section ---
    with left_col:

        # Load the image
        import base64
        from pathlib import Path

        image_path = Path(__file__).parent / "assets" / "ai_procurement_hero_v2.jpg"

        img_html = ""
        if image_path.exists():
            with open(image_path, "rb") as f:
                img_data = base64.b64encode(f.read()).decode()
            # Reduced max-width to 380px to save space
            img_html = f'<img src="data:image/png;base64,{img_data}" style="width: 100%; max-width: 380px; height: auto; border-radius: 16px; box-shadow: 0 10px 30px rgba(0,0,0,0.5); margin-bottom: 15px;">'

        # Use a container with a dark distinct background for the visual side
        # Compacted padding and height
        st.markdown(f"""
<div style="background: linear-gradient(180deg, rgba(30, 41, 59, 0.3) 0%, rgba(15, 23, 42, 0.3) 100%); border-right: 1px solid rgba(255,255,255,0.05); border-radius: 24px 0 0 24px; padding: 2rem; display: flex; flex-direction: column; justify-content: center; align-items: center; min-height: 500px; text-align: center;">
<div class="platform-name">
Quadratyx Intelligent
Procurement Platform
</div>
<div class="platform-tagline">
AI-Powered Supply Chain Intelligence
</div>
{img_html}
<div style="font-size: 11px; color: #64748b; letter-spacing: 1.5px; text-transform: uppercase; margin-top: 0.5rem; font-weight: 500;">
Powered by Advanced AI Models
</div>
</div>
""", unsafe_allow_html=True)

    # --- RIGHT COLUMN: Login Form ---
    with right_col:
        # Reduced spacer
        st.markdown("<div style='height: 40px;'></div>", unsafe_allow_html=True)

        # Simple Login Header - White Text
        st.markdown("""
<div style="padding: 0 1rem; margin-bottom: 1.5rem; text-align: left;">
<div style="font-size: 28px; font-weight: 700; color: #ffffff; letter-spacing: -0.5px;">
Login
</div>
<div style="color: #94a3b8; font-size: 13px; margin-top: 4px;">
Enter your credentials to access the platform.
</div>
</div>
""", unsafe_allow_html=True)

        # Streamlit form container
        with st.container():
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")

            st.markdown("<div style='height: 15px'></div>", unsafe_allow_html=True)

            if st.button("Login", use_container_width=True):
                # SECURE: Get credentials from env ONLY.
                valid_user = os.getenv("APP_USERNAME")
                valid_pass = os.getenv("APP_PASSWORD")

                if not valid_user or not valid_pass:
                    st.error("⚠️ Authentication system is not configured. Please contact the administrator.")
                elif username == valid_user and password == valid_pass:
                    st.session_state['authenticated'] = True
                    st.rerun()
                else:
                    st.error("❌ Invalid credentials")

        st.markdown("""
<div style="text-align: center; margin-top: 3rem; color: #475569; font-size: 12px;">
&copy; 2024 Quadratyx. All rights reserved.
</div>
""", unsafe_allow_html=True)

    # Stop execution here if not authenticated
    st.stop()

# ===============================
# TOP RIGHT LOGOUT BUTTON
# ===============================
#if st.sidebar.button("Logout"):
    #st.session_state['authenticated'] = False
    #st.session_state['page'] = 'Home'
    #st.rerun()

# --- Sidebar Logo ---
from pathlib import Path
logo_path = Path(__file__).parent / "assets" / "quadratyx_logo.jpg"
if logo_path.exists():
    st.sidebar.image(str(logo_path), use_container_width=True)
    st.sidebar.markdown('<div style="margin-bottom: 20px;"></div>', unsafe_allow_html=True)
# Attractive header via helper

# Streamlit page config
#st.set_page_config(page_title="Demand Forecast Dashboard", layout="wide")

# Database config (source)
DB_NAME = os.getenv("SOURCE_DATABASE_NAME")
DB_USER = os.getenv("SOURCE_DATABASE_USER")
DB_PASS = os.getenv("SOURCE_DATABASE_PASSWORD")
DB_HOST = os.getenv("SOURCE_DATABASE_HOST")
DB_PORT = os.getenv("SOURCE_DATABASE_PORT", "3306")

# Database config (output)
OUTPUT_DB_NAME = os.getenv("OUTPUT_DATABASE_NAME")
OUTPUT_DB_USER = os.getenv("OUTPUT_DATABASE_USER")
OUTPUT_DB_PASS = os.getenv("OUTPUT_DATABASE_PASSWORD")
OUTPUT_DB_HOST = os.getenv("OUTPUT_DATABASE_HOST")
OUTPUT_DB_PORT = os.getenv("OUTPUT_DATABASE_PORT", "3306")


@st.cache_resource
def get_engine(name=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST, port=DB_PORT):
    return create_engine(
        f"mysql+pymysql://{user}:{password}@{host}:{port}/{name}",
        pool_pre_ping=True
    )


@st.cache_resource
def get_output_engine():
    if not all([OUTPUT_DB_NAME, OUTPUT_DB_USER, OUTPUT_DB_PASS, OUTPUT_DB_HOST]):
        return None
    return get_engine(name=OUTPUT_DB_NAME, user=OUTPUT_DB_USER, password=OUTPUT_DB_PASS, host=OUTPUT_DB_HOST,
                      port=OUTPUT_DB_PORT)


# Try to connect to both databases (output is optional)
source_engine = None
output_engine = None
try:
    source_engine = get_engine()
    logger.info("Connected to source MySQL database")
except Exception as e:
    st.error(f"❌ Source DB connection failed: {e}")
    logger.exception("Source DB connection failed")

try:
    output_engine = get_output_engine()
    if output_engine is None:
        logger.info("Output DB variables not set — output DB unavailable")
    else:
        # Test connection
        with output_engine.connect() as _:
            logger.info("Connected to output MySQL database")
except Exception as e:
    st.error(f"❌ Output DB connection failed: {e}")
    logger.exception("Output DB connection failed")

# Use the output database exclusively for this dashboard
engine = output_engine
if engine is None:
    st.error(
        "No output database configured or connection failed. Please set OUTPUT_* env vars and ensure connectivity.")
    st.stop()

# Get table list
with engine.connect() as conn:
    tables = conn.execute(text("SHOW TABLES")).fetchall()
    logger.info(f"Found tables: {[t[0] for t in tables]}")

table_names = [t[0] for t in tables]

def \
        render_cell(col, text, font_size="12px"):
    col.markdown(
        f"""
        <div style="
            font-size: {font_size};
            line-height: 1.3;
            word-wrap: break-word;
            white-space: normal;
            overflow-wrap: anywhere;
            min-height: 38px;
        ">
            {text}
        </div>
        """,
        unsafe_allow_html=True
    )

def render_action(col, key):
    col.markdown(
        f"""
        <style>
        div[data-testid="stButton"] > button#{key} {{
            background: none;
            border: none;
            padding: 0;
            color: #2563eb;
            font-size: 12px;
            font-weight: normal;
            text-decoration: underline;
            cursor: pointer;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

    return col.button("👁️", key=key)



# ==========================================
# HOME PAGE
# ==========================================
if st.session_state['page'] == 'Home':
    st.subheader("Consolidated View")

    df_alerts = pd.read_sql("SELECT * FROM qtx_inventory_alerts", engine)

    columns = df_alerts.columns.tolist()
    display_columns = columns + ["Action"]

    col_widths = [2] * len(columns) + [1]

    # -------- Header row --------
    header_cols = st.columns(col_widths)
    for col, name in zip(header_cols, display_columns):
        col.markdown(
            f"""
            <div style="
                border: 0.5px #d1d5db;
                font-weight: 200;
                font-size: 10px;
                background-color: #f9fafb;
            ">
                {name}
            </div>
            """,
            unsafe_allow_html=True
        )

    # -------- Data rows --------
    for i, row in df_alerts.iterrows():
        row_cols = st.columns(col_widths)

        # Normal data cells
        for idx, col_name in enumerate(columns):
            render_cell(row_cols[idx], str(row[col_name]), font_size="12px")

        # Action cell (NORMAL text look, clickable)
        if render_action(row_cols[-1], key=f"view_{i}"):
            st.session_state['selected_material'] = str(row['material'])
            st.session_state['selected_plant'] = str(row['plant'])
            st.session_state['page'] = 'Dashboard'
            st.rerun()



# ==========================================
# DASHBOARD PAGE (Existing Logic)
# ==========================================
else:  # page == 'Dashboard' or 'Order Optimisation'
    if st.sidebar.button("Home"):
        st.session_state['page'] = 'Home'
        st.session_state['selected_material'] = None
        st.session_state['selected_plant'] = None
        st.rerun()


    # (Table selector removed — dashboard focuses on the Output DB demand/historical tables)

    # Special UI for output DB: demand vs historical plotting
    if set(["qtx_historical_consumption", "qtx_demand_final"]).issubset(set(table_names)):
        #st.subheader("Demand vs Historical (Output DB)")


        # @st.cache_data
        # def get_distinct_values(_engine):
        #     with _engine.connect() as conn:
        #         plants = pd.read_sql(
        #             "SELECT DISTINCT plant FROM qtx_historical_consumption UNION SELECT DISTINCT plant FROM qtx_demand_final",
        #             conn)
        #         materials = pd.read_sql(
        #             "SELECT DISTINCT material FROM qtx_historical_consumption UNION SELECT DISTINCT material FROM qtx_demand_final",
        #             conn)
        #     return plants['plant'].dropna().astype(str).tolist(), materials['material'].dropna().astype(str).tolist()
        #
        #
        # plants, materials = get_distinct_values(engine)
        #
        # # Controls: select Material first, then show only Plants that have that Material; date picker in the third column
        # c1, c2, c3 = st.columns([2, 2, 3])
        #
        # if materials:
        #     # Set index based on session state selection if available
        #     mat_index = 0
        #     if st.session_state['selected_material'] in materials:
        #         mat_index = materials.index(st.session_state['selected_material'])
        #
        #     selected_material = c1.selectbox("Select Material", options=materials, index=mat_index)
        #     # Update session state if changed manually
        #     st.session_state['selected_material'] = selected_material
        # else:
        #     selected_material = None
        #     c1.info("No materials available")
        #
        # # Get plants that have the selected material
        # plants_for_material = []
        # if selected_material:
        #     @st.cache_data
        #     def get_plants_for_material(_engine, material):
        #         with _engine.connect() as conn:
        #             q = text(
        #                 "SELECT DISTINCT plant FROM qtx_historical_consumption WHERE material = :m UNION SELECT DISTINCT plant FROM qtx_demand_final WHERE material = :m")
        #             df = pd.read_sql(q, conn, params={"m": material})
        #         return df['plant'].dropna().astype(str).tolist()
        #
        #
        #     plants_for_material = get_plants_for_material(engine, selected_material)
        #
        # if plants_for_material:
        #     # Set index based on session state selection if available
        #     plant_index = 0
        #     if st.session_state['selected_plant'] in plants_for_material:
        #         plant_index = plants_for_material.index(st.session_state['selected_plant'])
        #
        #     selected_plant = c2.selectbox("Select Plant", options=plants_for_material, index=plant_index)
        #     # Update session state if changed
        #     st.session_state['selected_plant'] = selected_plant
        # else:
        #     selected_plant = None
        #     c2.info("No plants available for the selected Material")
        #
        # # Date range picker (defaults: last 24 months to next 6 months)
        # today = datetime.date.today()
        # default_start = today - datetime.timedelta(days=365 * 2)
        # default_end = today + datetime.timedelta(days=365 // 2)
        # start_date, end_date = c3.date_input('Select date range', value=(default_start, default_end))
        # start_dt = pd.to_datetime(start_date)
        # end_dt = pd.to_datetime(end_date)

        if st.sidebar.button("Demand Forecast"):
            st.session_state['page_select'] = "Demand Forecast"

        if st.sidebar.button("Order Optimisation"):
            st.session_state['page_select'] = "Order Optimisation"

        page_select = st.session_state.get("page_select", "Demand Forecast")

        # Logout at the bottom of sidebar
        st.sidebar.markdown("<div style='height: 35vh'></div>", unsafe_allow_html=True) # Vertical spacer
        st.sidebar.divider()
        if st.sidebar.button("🚪 Logout"):
            st.session_state['authenticated'] = False
            st.session_state['page'] = 'Home'
            st.rerun()



        if page_select == 'Demand Forecast':
            render_header("Demand Forecast")


            @st.cache_data
            def get_distinct_values(_engine):
                with _engine.connect() as conn:
                    plants = pd.read_sql(
                        "SELECT DISTINCT plant FROM qtx_historical_consumption UNION SELECT DISTINCT plant FROM qtx_demand_final",
                        conn)
                    materials = pd.read_sql(
                        "SELECT DISTINCT material FROM qtx_historical_consumption UNION SELECT DISTINCT material FROM qtx_demand_final",
                        conn)
                return plants['plant'].dropna().astype(str).tolist(), materials['material'].dropna().astype(
                    str).tolist()


            plants, materials = get_distinct_values(engine)

            # Controls: select Material first, then show only Plants that have that Material; date picker in the third column
            c1, c2, c3 = st.columns([2, 2, 3])

            if materials:
                # Set index based on session state selection if available
                mat_index = 0
                if st.session_state['selected_material'] in materials:
                    mat_index = materials.index(st.session_state['selected_material'])

                selected_material = c1.selectbox("Select Material", options=materials, index=mat_index)
                # Update session state if changed manually
                st.session_state['selected_material'] = selected_material
            else:
                selected_material = None
                c1.info("No materials available")

            # Get plants that have the selected material
            plants_for_material = []
            if selected_material:
                @st.cache_data
                def get_plants_for_material(_engine, material):
                    with _engine.connect() as conn:
                        q = text(
                            "SELECT DISTINCT plant FROM qtx_historical_consumption WHERE material = :m UNION SELECT DISTINCT plant FROM qtx_demand_final WHERE material = :m")
                        df = pd.read_sql(q, conn, params={"m": material})
                    return df['plant'].dropna().astype(str).tolist()


                plants_for_material = get_plants_for_material(engine, selected_material)

            if plants_for_material:
                # Set index based on session state selection if available
                plant_index = 0
                if st.session_state['selected_plant'] in plants_for_material:
                    plant_index = plants_for_material.index(st.session_state['selected_plant'])

                selected_plant = c2.selectbox("Select Plant", options=plants_for_material, index=plant_index)
                # Update session state if changed
                st.session_state['selected_plant'] = selected_plant
            else:
                selected_plant = None
                c2.info("No plants available for the selected Material")

            # Date range picker (defaults: last 24 months to next 6 months)
            today = datetime.date.today()
            default_start = today - datetime.timedelta(days=365 * 2)
            default_end = today + datetime.timedelta(days=365 // 2)
            start_date, end_date = c3.date_input('Select date range', value=(default_start, default_end))
            start_dt = pd.to_datetime(start_date)
            end_dt = pd.to_datetime(end_date)

            if not selected_plant or not selected_material:
                st.info("Select a Plant and a Material to generate the chart.")
                st.info(f"Current selection: Material={selected_material}, Plant={selected_plant}")
            else:
                plant_param = "'" + selected_plant.replace("'", "''") + "'"
                mat_param = "'" + selected_material.replace("'", "''") + "'"

                hist_q = f"SELECT period, quantity FROM qtx_historical_consumption WHERE plant = {plant_param} AND material = {mat_param}"
                dem_q = f"SELECT * FROM qtx_demand_final WHERE plant = {plant_param} AND material = {mat_param}"

                try:
                    hist_df = pd.read_sql(hist_q, engine)
                except Exception as e:
                    st.error(f"Failed to query historical data: {e}")
                    hist_df = pd.DataFrame(columns=['period', 'quantity'])

                try:
                    dem_df = pd.read_sql(dem_q, engine)
                except Exception as e:
                    st.error(f"Failed to query demand data: {e}")
                    dem_df = pd.DataFrame(columns=['period', 'predicted_qty'])

                # Normalize and parse periods
                for df_ in (hist_df, dem_df):
                    if 'period' in df_.columns:
                        df_['period'] = pd.to_datetime(df_['period'], errors='coerce')

                hist_df = hist_df.dropna(subset=['period'])
                dem_df = dem_df.dropna(subset=['period'])

                # Aggregate by period in case multiples exist
                if 'quantity' in hist_df.columns:
                    hist_ag = hist_df.groupby('period', as_index=False)['quantity'].sum()
                else:
                    hist_ag = pd.DataFrame(columns=['period', 'quantity'])

                if 'predicted_qty' in dem_df.columns:
                    dem_ag = dem_df.groupby('period', as_index=False)['predicted_qty'].sum()
                else:
                    dem_ag = pd.DataFrame(columns=['period', 'predicted_qty'])

                # Combine into a single continuous series: historical 'quantity' then demand 'predicted_qty'.
                # Prefer predicted values when periods overlap so the series continues into the forecast.
                hist_series = hist_ag.rename(
                    columns={'quantity': 'value'}) if 'quantity' in hist_ag.columns else pd.DataFrame(
                    columns=['period', 'value'])
                dem_series = dem_ag.rename(
                    columns={'predicted_qty': 'value'}) if 'predicted_qty' in dem_ag.columns else pd.DataFrame(
                    columns=['period', 'value'])

                # Prepare for plotting: keep historical and predicted series as separate traces so colors differ
                hist_series = hist_ag.rename(
                    columns={'quantity': 'value'}) if 'quantity' in hist_ag.columns else pd.DataFrame(
                    columns=['period', 'value'])
                dem_series = dem_ag.rename(
                    columns={'predicted_qty': 'value'}) if 'predicted_qty' in dem_ag.columns else pd.DataFrame(
                    columns=['period', 'value'])

                # Drop NA periods and sort
                hist_series = hist_series.dropna(subset=['period']).sort_values('period').reset_index(drop=True)
                dem_series = dem_series.dropna(subset=['period']).sort_values('period').reset_index(drop=True)

                # Filter the series by selected date range
                hist_series = hist_series[(hist_series['period'] >= start_dt) & (hist_series['period'] <= end_dt)]
                dem_series = dem_series[(dem_series['period'] >= start_dt) & (dem_series['period'] <= end_dt)]

                if hist_series.empty and dem_series.empty:
                    st.warning('No data available for the selected Plant(s) / Material(s) and date range.')
                else:
                    # Recompute aggregated frames used for KPIs
                    hist_ag2 = hist_series.groupby('period', as_index=False).agg(
                        {'value': 'sum'}) if not hist_series.empty else pd.DataFrame(columns=['period', 'value'])
                    dem_ag2 = dem_series.groupby('period', as_index=False).agg(
                        {'value': 'sum'}) if not dem_series.empty else pd.DataFrame(columns=['period', 'value'])

                    # Build combined series (predicted overrides historical) — used for continuity & plotting
                    combined = pd.concat(
                        [hist_series.assign(source='historical'), dem_series.assign(source='predicted')],
                        ignore_index=True)
                    combined = combined.sort_values('period').reset_index(drop=True)
                    combined_agg = combined.groupby('period', as_index=False).agg({'value': 'last'}).sort_values(
                        'period').reset_index(drop=True)

                    # Ensure the two traces join seamlessly by adding a connection point to predicted series if needed
                    if not hist_series.empty and not dem_series.empty:
                        last_hist_period = hist_series['period'].max()
                        last_hist_value = hist_series.loc[hist_series['period'] == last_hist_period, 'value'].iloc[-1]
                        first_dem_period = dem_series['period'].min()

                        # If predicted starts after historical, prepend a connecting point so the connecting segment uses predicted color
                        if first_dem_period > last_hist_period:
                            conn_row = pd.DataFrame({'period': [last_hist_period], 'value': [last_hist_value]})
                            dem_series = pd.concat([conn_row, dem_series], ignore_index=True).sort_values(
                                'period').reset_index(drop=True)

                        # Trim historical series so it does NOT draw over the predicted segment (ensures predicted color shows on the join and overlapping periods)
                        hist_series = hist_series[hist_series['period'] < dem_series['period'].min()].reset_index(
                            drop=True)

                    # Demand forecast pivot table (monthly) — shows months as columns and predicted_qty sums
                    if not dem_df.empty and 'predicted_qty' in dem_df.columns:
                        df_pivot = dem_df.copy()
                        df_pivot = df_pivot[(df_pivot['period'] >= start_dt) & (df_pivot['period'] <= end_dt)]
                        if not df_pivot.empty:
                            df_pivot['month'] = df_pivot['period'].dt.to_period('M').astype(str)
                            pivot = df_pivot.pivot_table(index=['material'], columns='month', values='predicted_qty',
                                                         aggfunc='sum', fill_value=0)
                            # Sort month columns chronologically
                            try:
                                month_cols = sorted(pivot.columns, key=lambda x: pd.to_datetime(x + '-01'))
                                pivot = pivot.reindex(columns=month_cols)
                            except Exception:
                                pass
                            pivot = pivot.reset_index()
                            pivot['Total'] = pivot.loc[:, pivot.columns.difference(['material'])].sum(axis=1)

                            # Display as a compact table above the chart
                            st.subheader('Demand Forecast (Tons)')
                            st.dataframe(pivot, use_container_width=True, hide_index=True)
                            #st.download_button('Download forecast pivot CSV', data=pivot.to_csv(index=False),
                                               #
                            #file_name=f'forecast_pivot_{start_date}_{end_date}.csv', mime='text/csv')

                    # Plotting: ensure continuous combined line then overlay colored segments
                    # Combined aggregated series (predict overrides historical for overlaps)
                    combined_full = combined_agg.copy()

                    fig = go.Figure()
                    # Base combined line (use predicted color so continuity is visually indistinguishable)
                    if not combined_full.empty:
                        fig.add_trace(go.Scatter(
                            x=combined_full['period'],
                            y=combined_full['value'],
                            mode='lines',
                            name='Combined',
                            line=dict(color='#ff7f0e', width=4),
                            hoverinfo='skip',
                            showlegend=False
                        ))

                    # Overlay historical and predicted with same width so the join looks continuous
                    if not hist_series.empty:
                        fig.add_trace(go.Scatter(
                            x=hist_series['period'],
                            y=hist_series['value'],
                            mode='lines',
                            name='Historical',
                            line=dict(color='#1f77b4', width=4),
                            connectgaps=True
                        ))
                    if not dem_series.empty:
                        fig.add_trace(go.Scatter(
                            x=dem_series['period'],
                            y=dem_series['value'],
                            mode='lines',
                            name='Predicted',
                            line=dict(color='#ff7f0e', width=4),
                            connectgaps=True
                        ))

                    fig.update_layout(xaxis_title='Period', yaxis_title='Quantity', legend_title_text='Series')
                    st.plotly_chart(fig, use_container_width=True)



        elif page_select == 'Order Optimisation':

            render_header(

                "Order Optimisation",


            )


            from order_optimisation import (

                render_order_optimization_update,

                render_stock_calculation_table

            )

            # render_stock_calculation_table(engine)

            render_order_optimization_update(engine)

