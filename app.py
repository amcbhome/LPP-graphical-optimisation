
import streamlit as st
import pulp

st.set_page_config(
    page_title="Production Optimisation",
    page_icon="📊",
    layout="wide"
)

# Calculator-style appearance
st.markdown("""
<style>
.block-container {
    max-width: 1600px;
    padding-top: 1.2rem;
    padding-bottom: 0.5rem;
}

h1 {
    font-size: 2.5rem !important;
    margin-bottom: 0.2rem;
}

h2, h3 {
    font-size: 1.5rem !important;
}

p, label, .stMarkdown {
    font-size: 1.05rem;
}

div[data-testid="stNumberInput"] input {
    font-size: 1.35rem !important;
    font-weight: 600;
    min-height: 3rem;
}

div[data-testid="stMetricValue"] {
    font-size: 2.7rem !important;
    font-weight: 700;
}

div[data-testid="stMetricLabel"] {
    font-size: 1.1rem !important;
}

div[data-testid="stButton"] button {
    min-height: 3.5rem;
    font-size: 1.25rem;
    font-weight: 700;
}

div[data-testid="stCheckbox"] label {
    font-size: 1.1rem;
}

</style>
""", unsafe_allow_html=True)

st.title("Production Optimisation")
st.caption(
    "Linear programming calculator | "
    "Maximise contribution from limited resources"
)

# Two main panels
left, right = st.columns([1.15, 1], gap="large")

with left:

    st.subheader("1. Product inputs")

    x_col, y_col = st.columns(2)

    with x_col:
        st.markdown("**PRODUCT X**")

        mx = st.number_input(
            "Material per unit (kg)",
            min_value=0.01, value=3.0,
            key="mx"
        )

        lx = st.number_input(
            "Labour per unit (hours)",
            min_value=0.01, value=4.0,
            key="lx"
        )

        cx = st.number_input(
            "Contribution per unit ($)",
            min_value=0.0, value=30.0,
            key="cx"
        )

    with y_col:
        st.markdown("**PRODUCT Y**")

        my = st.number_input(
            "Material per unit (kg)",
            min_value=0.01, value=5.0,
            key="my"
        )

        ly = st.number_input(
            "Labour per unit (hours)",
            min_value=0.01, value=4.0,
            key="ly"
        )

        cy = st.number_input(
            "Contribution per unit ($)",
            min_value=0.0, value=40.0,
            key="cy"
        )

    st.divider()

    st.subheader("2. Available resources")

    material_available = st.number_input(
        "Material available (kg)",
        min_value=0.01,
        value=15000.0,
        step=500.0,
        key="material_available"
    )

    labour_available = st.number_input(
        "Labour available (hours)",
        min_value=0.01,
        value=16000.0,
        step=500.0,
        key="labour_available"
    )

    integer_units = st.checkbox("Whole units only")

    calculate = st.button(
        "CALCULATE OPTIMAL SOLUTION",
        type="primary",
        use_container_width=True
    )

with right:

    st.subheader("3. Optimised solution")

    if calculate:

        model = pulp.LpProblem(
            "Production_Optimisation",
            pulp.LpMaximize
        )

        category = (
            pulp.LpInteger if integer_units
            else pulp.LpContinuous
        )

        x = pulp.LpVariable(
            "Product_X", lowBound=0, cat=category
        )

        y = pulp.LpVariable(
            "Product_Y", lowBound=0, cat=category
        )

        model += cx * x + cy * y

        model += (
            mx * x + my * y <= material_available
        )

        model += (
            lx * x + ly * y <= labour_available
        )

        model.solve(pulp.PULP_CBC_CMD(msg=False))

        if pulp.LpStatus[model.status] == "Optimal":

            xv = pulp.value(x)
            yv = pulp.value(y)
            contribution = pulp.value(model.objective)

            st.markdown("**PRODUCT X**")
            st.metric(
                label="Units to produce",
                value=f"{xv:,.2f}"
            )

            st.markdown("**PRODUCT Y**")
            st.metric(
                label="Units to produce",
                value=f"{yv:,.2f}"
            )

            st.divider()

            st.markdown("**MAXIMUM CONTRIBUTION**")
            st.metric(
                label="Optimised value",
                value=f"${contribution:,.2f}"
            )

            # Resource utilisation
            material_used = mx * xv + my * yv
            labour_used = lx * xv + ly * yv

            st.divider()
            st.markdown("**RESOURCE UTILISATION**")

            m_pct = material_used / material_available
            l_pct = labour_used / labour_available

            st.caption(
                f"Material: {m_pct:.1%} used | "
                f"Slack: {material_available - material_used:,.2f} kg"
            )
            st.progress(min(m_pct, 1.0))

            st.caption(
                f"Labour: {l_pct:.1%} used | "
                f"Slack: {labour_available - labour_used:,.2f} hours"
            )
            st.progress(min(l_pct, 1.0))

        else:
            st.error(
                f"Solver status: {pulp.LpStatus[model.status]}"
            )

    else:
        st.info(
            "Enter your assumptions on the left "
            "and select Calculate Optimal Solution."
        )

        st.markdown("### Ready to calculate")
        st.caption(
            "The optimal production quantities and "
            "maximum contribution will appear here."
        )

st.divider()
st.caption("Production Optimisation | Powered by Python and PuLP")
