import pandas as pd
import streamlit as st
from sqlalchemy import text

def render_order_optimization_update(engine):


    @st.cache_data
    def get_distinct_values(_engine):
        with _engine.connect() as conn:
            plants = pd.read_sql(
                """
                SELECT DISTINCT plant FROM qtx_demand_final
                """,
                conn
            )
            materials = pd.read_sql(
                """
                SELECT DISTINCT material FROM qtx_demand_final
                """,
                conn
            )
        return (
            plants["plant"].dropna().astype(str).tolist(),
            materials["material"].dropna().astype(str).tolist(),
        )

    plants, materials = get_distinct_values(engine)

    # Fetch distinct materials and plants
    # materials = pd.read_sql("SELECT DISTINCT material FROM qtx_order_optimization", engine)['material'].astype(str).tolist()
    # plants = pd.read_sql("SELECT DISTINCT plant FROM qtx_order_optimization", engine)['plant'].astype(str).tolist()
    #
    # # Selectboxes with unique keys
    col1, col2 = st.columns(2)

    # -------- Material --------
    with col1:
        if materials:
            selected_material = st.selectbox(
                "Select Material",
                materials,
                key="df_material"
            )
        else:
            selected_material = None
            st.info("No materials available")

    # -------- Plant (filtered by material) --------
    plants_for_material = []
    if selected_material:
        @st.cache_data
        def get_plants_for_material(_engine, material):
            with _engine.connect() as conn:
                q = text("""
                    SELECT DISTINCT plant
                    FROM qtx_demand_final
                    WHERE material = :m
                """)
                df = pd.read_sql(q, conn, params={"m": material})
            return df["plant"].dropna().astype(str).tolist()

        plants_for_material = get_plants_for_material(engine, selected_material)

    with col2:
        if plants_for_material:
            selected_plant = st.selectbox(
                "Select Plant",
                plants_for_material,
                key="df_plant"
            )
        else:
            selected_plant = None
            st.info("No plants available for this material")

    # selected_material = st.selectbox("Select Material", options=materials, key="update_material_select")
    # selected_plant = st.selectbox("Select Plant", options=plants, key="update_plant_select")

    if not selected_material or not selected_plant:
        st.info("Select a Plant and a Material to display the pivot table.")
        return

    st.subheader("Plant Data (Tons)")
    query = text("""
            SELECT
                plant,
                warehouse_capacity,
                safety_stock,
                opening_stock AS available_stock
            FROM qtx_stock_calculation
            WHERE plant = :plant
        """)

    df = pd.read_sql(query, engine,params={"plant": selected_plant})

    if df.empty:
        st.warning("No records found")
        return

    st.dataframe(df, use_container_width=True, hide_index=True)

    #st.download_button(
        #"Download Stock Calculation CSV",
        #data=df.to_csv(index=False),
        #file_name=f"stock_calculation_{selected_plant}.csv",
        #mime="text/csv"
    #)

    st.subheader("Order Optimisation")

    # Fetch data
    query = """
        SELECT period, closing_stock, on_route, opening_stock, quantity_predicted,
               safety_stock, warehouse_capacity
        FROM qtx_order_optimization
        WHERE material = :material AND plant = :plant
    """
    df = pd.read_sql(text(query), engine, params={"material": selected_material, "plant": selected_plant})

    if df.empty:
        st.warning("No records found for the selected Plant and Material.")
        return

    # Convert period like '2026_1' → '2026-01'
    df['year_month'] = df['period'].apply(lambda x: f"{int(x.split('_')[0])}-{int(x.split('_')[1]):02d}" if '_' in x else None)
    df = df.dropna(subset=['year_month'])

    # Metrics to pivot
    metrics = ["closing_stock", "on_route", "opening_stock", "quantity_predicted", "safety_stock", "warehouse_capacity"]

    # Build pivot table: metrics as rows, year_month as columns
    pivot_rows = []
    for metric in metrics:
        temp = df.groupby('year_month')[metric].agg('sum' if metric not in ['safety_stock', 'warehouse_capacity'] else 'mean')
        temp = temp.round(2)
        temp.name = metric
        pivot_rows.append(temp)

    pivot = pd.concat(pivot_rows, axis=1).T  # transpose so metrics are rows
    pivot = pivot.reindex(columns=sorted(pivot.columns, key=lambda x: pd.to_datetime(x + '-01')))  # sort columns


    st.dataframe(pivot, use_container_width=True,)

    # Download button
    #st.download_button(
        #"Download Pivot CSV",
        #data=pivot.reset_index().rename(columns={'index': 'Metric'}).to_csv(index=False),
        #file_name=f"order_optimization_pivot_{selected_material}_{selected_plant}.csv",
        #mime="text/csv"
    #)





def render_stock_calculation_table(engine):
    st.subheader("Plant Data (Tons)")

    @st.cache_data
    def get_plants(_engine):
        with _engine.connect() as conn:
            df = pd.read_sql("SELECT DISTINCT plant FROM qtx_stock_calculation", conn)
        return df["plant"].dropna().astype(str).tolist()

    plants = get_plants(engine)

    if not plants:
        st.info("No plants available")
        return

    selected_plant = st.selectbox(
        "Select Plant",
        plants,
        key="stock_plant"
    )

    query = """
        SELECT
            plant,
            warehouse_capacity,
            safety_stock,
            opening_stock AS available_stock
        FROM qtx_stock_calculation
    """


    df = pd.read_sql(query, engine)

    if df.empty:
        st.warning("No records found")
        return

    st.dataframe(df, use_container_width=True, hide_index=True)

    st.download_button(
        "Download Stock Calculation CSV",
        data=df.to_csv(index=False),
        file_name=f"stock_calculation_{selected_plant}.csv",
        mime="text/csv"
    )