
import streamlit as st
import pulp

st.set_page_config(page_title="Production Optimisation")

st.title("Production Optimisation")
st.write("Linear Programming – Product Mix")

# Business data
material_x, material_y = 3, 5
labour_x, labour_y = 4, 4
contribution_x, contribution_y = 30, 40

material_available = 14500
labour_available = 16000

# Optimisation model
model = pulp.LpProblem(
    "Production_Optimisation",
    pulp.LpMaximize
)

# Decision variables
x = pulp.LpVariable("Product_X", lowBound=0)
y = pulp.LpVariable("Product_Y", lowBound=0)

# Objective function
model += 30*x + 40*y

# Constraints
model += 3*x + 5*y <= material_available
model += 4*x + 4*y <= labour_available

# Solve
solver = pulp.PULP_CBC_CMD(msg=False)
model.solve(solver)

if model.status == pulp.LpStatusOptimal:

    st.success("Optimal solution found")

    col1, col2, col3 = st.columns(3)

    col1.metric("Product X", f"{x.varValue:,.0f}")
    col2.metric("Product Y", f"{y.varValue:,.0f}")
    col3.metric(
        "Maximum contribution",
        f"£{pulp.value(model.objective):,.2f}"
    )

    st.subheader("Resource utilisation")

    st.write(f"Material used: {3*x.varValue + 5*y.varValue:,.0f} kg")
    st.write(f"Labour used: {4*x.varValue + 4*y.varValue:,.0f} hours")

else:
    st.error(f"Solver status: {pulp.LpStatus[model.status]}")
