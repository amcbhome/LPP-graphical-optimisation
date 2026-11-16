
import streamlit as st
import pulp
import math

st.set_page_config(
    page_title="Production Optimisation",
    page_icon="📊",
    layout="wide"
)

# -------------------------------
# SESSION STATE
# -------------------------------

if "show_calculator" not in st.session_state:
    st.session_state.show_calculator = False

# -------------------------------
# HEADER
# -------------------------------

st.title("Production Optimisation")
st.caption("PRESCRIPTIVE ANALYTICS  |  LINEAR PROGRAMMING")

st.markdown("""
A manufacturing business produces two products, X and Y.

Each product consumes material and production labour.
Both resources are limited.

The objective is to determine the optimal production
combination that maximises total contribution.
""")

st.divider()

# -------------------------------
# BUSINESS DATA
# -------------------------------

st.subheader("Business data")

col1, col2 = st.columns(2)

with col1:
    st.markdown("**Product requirements**")

    st.table({
        "Input": [
            "Material (kg/unit)",
            "Labour (hours/unit)",
            "Contribution ($/unit)"
        ],
        "Product X": [3, 4, 30],
        "Product Y": [5, 4, 40]
    })

with col2:
    st.markdown("**Available resources**")

    st.table({
        "Resource": ["Material", "Labour"],
        "Available": ["15,000 kg", "16,000 hours"]
    })

st.info(
    "The figures above are the default ACCA example. "
    "You can change them using the calculator."
)

# -------------------------------
# OPEN CALCULATOR
# -------------------------------

st.divider()

col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    if st.button(
        "🧮 Open Optimisation Calculator",
        type="primary",
        use_container_width=True
    ):
        st.session_state.show_calculator = True

# -------------------------------
# CALCULATOR
# -------------------------------

if st.session_state.show_calculator:

    st.divider()
    st.header("Optimisation Calculator")

    st.write(
        "Enter the business assumptions and calculate "
        "the optimal production quantities."
    )

    with st.form("optimisation_form"):

        st.subheader("1. Product inputs")

        x_col, y_col = st.columns(2)

        with x_col:
            st.markdown("**Product X**")

            mx = st.number_input(
                "Material per unit (kg)",
                min_value=0.01,
                value=3.0
            )

            lx = st.number_input(
                "Labour per unit (hours)",
                min_value=0.01,
                value=4.0
            )

            cx = st.number_input(
                "Contribution per unit ($)",
                min_value=0.0,
                value=30.0
            )

        with y_col:
            st.markdown("**Product Y**")

            my = st.number_input(
                "Material per unit (kg)",
                min_value=0.01,
                value=5.0
            )

            ly = st.number_input(
                "Labour per unit (hours)",
                min_value=0.01,
                value=4.0
            )

            cy = st.number_input(
                "Contribution per unit ($)",
                min_value=0.0,
                value=40.0
            )

        st.divider()
        st.subheader("2. Available resources")

        r1, r2 = st.columns(2)

        with r1:
            material_capacity = st.number_input(
                "Material available (kg)",
                min_value=0.01,
                value=15000.0,
                step=500.0
            )

        with r2:
            labour_capacity = st.number_input(
                "Labour available (hours)",
                min_value=0.01,
                value=16000.0,
                step=500.0
            )

        st.divider()

        integer_production = st.checkbox(
            "Require whole production units",
            value=False
        )

        calculate = st.form_submit_button(
            "Calculate Optimal Solution",
            type="primary",
            use_container_width=True
        )

    # ---------------------------
    # VALIDATION AND SOLUTION
    # ---------------------------

    if calculate:

        values = [
            mx, my, lx, ly, cx, cy,
            material_capacity, labour_capacity
        ]

        errors = []

        if not all(math.isfinite(v) for v in values):
            errors.append("Inputs must be finite numbers.")

        if mx <= 0 or my <= 0:
            errors.append("Material requirements must be positive.")

        if lx <= 0 or ly <= 0:
            errors.append("Labour requirements must be positive.")

        if material_capacity <= 0 or labour_capacity <= 0:
            errors.append("Resource availability must be positive.")

        if cx < 0 or cy < 0:
            errors.append("Contribution cannot be negative.")

        if cx == 0 and cy == 0:
            errors.append("At least one product needs positive contribution.")

        if errors:

            st.error("The model cannot be calculated.")

            for error in errors:
                st.write(f"❌ {error}")

        else:

            try:

                model = pulp.LpProblem(
                    "Production_Optimisation",
                    pulp.LpMaximize
                )

                variable_type = (
                    pulp.LpInteger
                    if integer_production
                    else pulp.LpContinuous
                )

                x = pulp.LpVariable(
                    "Product_X",
                    lowBound=0,
                    cat=variable_type
                )

                y = pulp.LpVariable(
                    "Product_Y",
                    lowBound=0,
                    cat=variable_type
                )

                # Objective function
                model += cx*x + cy*y

                # Resource constraints
                model += mx*x + my*y <= material_capacity
                model += lx*x + ly*y <= labour_capacity

                # Solve
                model.solve(
                    pulp.PULP_CBC_CMD(msg=False)
                )

                if pulp.LpStatus[model.status] != "Optimal":

                    st.error(
                        "No optimal solution found: "
                        + pulp.LpStatus[model.status]
                    )

                else:

                    xv = x.varValue
                    yv = y.varValue
                    result = pulp.value(model.objective)

                    if not all(
                        math.isfinite(v)
                        for v in [xv, yv, result]
                    ):
                        st.error("Invalid solver results.")
                        st.stop()

                    material_used = mx*xv + my*yv
                    labour_used = lx*xv + ly*yv

                    material_slack = material_capacity - material_used
                    labour_slack = labour_capacity - labour_used

                    st.divider()
                    st.header("Optimised solution")

                    st.success("Optimal solution found")

                    # MAIN RESULT CARDS

                    a, b, c = st.columns(3)

                    a.metric(
                        "Product X",
                        f"{xv:,.2f} units"
                    )

                    b.metric(
                        "Product Y",
                        f"{yv:,.2f} units"
                    )

                    c.metric(
                        "Maximum contribution",
                        f"${result:,.2f}"
                    )

                    st.caption(
                        "Contribution is not necessarily net accounting profit."
                    )

                    st.divider()
                    st.subheader("Resource utilisation")

                    left, right = st.columns(2)

                    with left:
                        st.markdown("**Material**")

                        st.progress(
                            min(material_used/material_capacity, 1.0)
                        )

                        st.write(
                            f"Used: {material_used:,.2f} kg"
                        )

                        st.write(
                            f"Unused: {material_slack:,.2f} kg"
                        )

                    with right:
                        st.markdown("**Labour**")

                        st.progress(
                            min(labour_used/labour_capacity, 1.0)
                        )

                        st.write(
                            f"Used: {labour_used:,.2f} hours"
                        )

                        st.write(
                            f"Unused: {labour_slack:,.2f} hours"
                        )

                    with st.expander("View mathematical model"):

                        st.latex(
                            rf"\text{{Maximise }} Z = "
                            rf"{cx:g}x + {cy:g}y"
                        )

                        st.latex(
                            rf"{mx:g}x + {my:g}y "
                            rf"\leq {material_capacity:g}"
                        )

                        st.latex(
                            rf"{lx:g}x + {ly:g}y "
                            rf"\leq {labour_capacity:g}"
                        )

                        st.latex(
                            r"x,y\geq0"
                        )

                        if integer_production:
                            st.latex(
                                r"x,y\in\mathbb{Z}_{\geq0}"
                            )

                    st.caption(
                        "Solver: PuLP / CBC | "
                        "Status: Optimal"
                    )

            except Exception as e:

                st.error("An error occurred during optimisation.")
                st.exception(e)

    # CLOSE CALCULATOR

    if st.button("Close calculator"):
        st.session_state.show_calculator = False
        st.rerun()

# -------------------------------
# FOOTER
# -------------------------------

st.divider()

st.caption(
    "Production Optimisation | "
    "Python · Streamlit · PuLP"
)
