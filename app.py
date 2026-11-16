
import streamlit as st
import pulp

st.set_page_config(
    page_title="Production Optimisation",
    page_icon="📊",
    layout="wide"
)

# Compact page styling
st.markdown("""
<style>
.block-container {
    padding-top: 1.5rem;
    padding-bottom: 1rem;
    max-width: 1200px;
}
h1 { padding-bottom: 0; }
div[data-testid="stVerticalBlock"] {
    gap: 0.6rem;
}
div[data-testid="stNumberInput"] {
    margin-bottom: -8px;
}
</style>
""", unsafe_allow_html=True)

st.title("Production Optimisation")
st.caption(
    "Determine the optimal production quantities "
    "to maximise contribution using limited resources."
)

# Product inputs
st.subheader("1. Product inputs")

x_col, y_col = st.columns(2)

with x_col:
    st.markdown("**Product X**")
    mx = st.number_input(
        "Material per unit (kg)", min_value=0.01,
        value=3.0, step=0.5, key="material_x"
    )
    lx = st.number_input(
        "Labour per unit (hours)", min_value=0.01,
        value=4.0, step=0.5, key="labour_x"
    )
    cx = st.number_input(
        "Contribution per unit ($)", min_value=0.0,
        value=30.0, step=1.0, key="contribution_x"
    )

with y_col:
    st.markdown("**Product Y**")
    my = st.number_input(
        "Material per unit (kg)", min_value=0.01,
        value=5.0, step=0.5, key="material_y"
    )
    ly = st.number_input(
        "Labour per unit (hours)", min_value=0.01,
        value=4.0, step=0.5, key="labour_y"
    )
    cy = st.number_input(
        "Contribution per unit ($)", min_value=0.0,
        value=40.0, step=1.0, key="contribution_y"
    )

st.divider()

# Resource availability
st.subheader("2. Available resources")

material_col, labour_col, option_col = st.columns(3)

with material_col:
    material_available = st.number_input(
        "Material available (kg)",
        min_value=0.01, value=15000.0,
        step=500.0, key="material_available"
    )

with labour_col:
    labour_available = st.number_input(
        "Labour available (hours)",
        min_value=0.01, value=16000.0,
        step=500.0, key="labour_available"
    )

with option_col:
    integer_units = st.checkbox(
        "Whole units only", value=False
    )

# Calculate
if st.button("Calculate optimal solution", type="primary",
             use_container_width=True):

    model = pulp.LpProblem(
        "Production_Optimisation",
        pulp.LpMaximize
    )

    category = (
        pulp.LpInteger if integer_units
        else pulp.LpContinuous
    )

    x = pulp.LpVariable("Product_X", lowBound=0,
                        cat=category)
    y = pulp.LpVariable("Product_Y", lowBound=0,
                        cat=category)

    model += cx * x + cy * y

    model += mx * x + my * y <= material_available
    model += lx * x + ly * y <= labour_available

    model.solve(pulp.PULP_CBC_CMD(msg=False))

    if pulp.LpStatus[model.status] == "Optimal":

        xv = pulp.value(x)
        yv = pulp.value(y)
        contribution = pulp.value(model.objective)

        st.divider()
        st.subheader("3. Optimised solution")

        a, b, c = st.columns(3)

        a.metric("Product X", f"{xv:,.2f} units")
        b.metric("Product Y", f"{yv:,.2f} units")
        c.metric("Maximum contribution", f"${contribution:,.2f}")

        # Resource utilisation
        material_used = mx * xv + my * yv
        labour_used = lx * xv + ly * yv

        st.markdown("**Resource utilisation**")

        r1, r2 = st.columns(2)

        with r1:
            st.caption("Material")
            st.progress(min(material_used / material_available, 1.0))
            st.write(
                f"{material_used:,.2f} / "
                f"{material_available:,.2f} kg"
            )

        with r2:
            st.caption("Labour")
            st.progress(min(labour_used / labour_available, 1.0))
            st.write(
                f"{labour_used:,.2f} / "
                f"{labour_available:,.2f} hours"
            )

    else:
        st.error(
            f"No optimal solution found. "
            f"Solver status: {pulp.LpStatus[model.status]}"
        )

st.divider()
st.caption("Linear Programming | PuLP optimisation solver")
