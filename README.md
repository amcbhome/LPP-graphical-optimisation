# LPP Graphical Optimisation
> **Portfolio Example | Prescriptive Analytics & Operations Research**
> 
> This project demonstrates an **Algebraic Notation** workflow for translating management accounting problems into interactive decision-support tools. Rather than relying on unverified generative AI code, the linear programming model is formulated and validated mathematically first—putting the human first so systemic error remains a consequence, not a cause.

An interactive linear programming web application built with Python and Streamlit to determine the contribution-maximising product mix under resource constraints.

## Live Demo & Repository

* **Streamlit App:** [lpp-graphical-optimisation-c5csmcbg5zwvp4mwqehrhs.streamlit.app](https://lpp-graphical-optimisation-c5csmcbg5zwvp4mwqehrhs.streamlit.app/)
* **GitHub Repository:** [github.com/amcbhome/lpp-graphical-optimisation](https://github.com/amcbhome/lpp-graphical-optimisation)

## Overview

Management accounting and operations research frequently require allocating scarce production resources across competing products to maximise contribution[cite: 1]. This application allows users to adjust unit contributions, resource consumption rates, available capacities, and integer constraints ("Whole units only") to inspect optimal production quantities, maximum contribution, resource utilisation, and slack[cite: 1].

## Design Philosophy: Algebraic Notation First

This project follows an **Algebraic Notation** workflow rather than relying on unverified code generation. The mathematical model—decision variables, objective function, and linear constraints—is specified formally on paper before implementation. Putting human analytical oversight first ensures that computational error remains a measurable consequence rather than an unexamined cause.

## Algebraic Formulation

Let:
* $x_1$ = units of **Product X** to produce[cite: 1]
* $x_2$ = units of **Product Y** to produce[cite: 1]
* $c_1, c_2$ = contribution per unit ($) for Product X and Product Y[cite: 1]
* $a_{m1}, a_{m2}$ = material required per unit (kg) for Product X and Product Y[cite: 1]
* $a_{l1}, a_{l2}$ = labour required per unit (hours) for Product X and Product Y[cite: 1]
* $M$ = total available material (kg)[cite: 1]
* $L$ = total available labour (hours)[cite: 1]

**Objective Function (Maximise Total Contribution):**

$$\text{Maximise } Z = c_1 x_1 + c_2 x_2$$

**Subject to:**

$$\begin{aligned}
a_{m1} x_1 + a_{m2} x_2 &\le M \quad \text{(Material constraint, kg)} \\
a_{l1} x_1 + a_{l2} x_2 &\le L \quad \text{(Labour constraint, hours)} \\
x_1, x_2 &\ge 0 \quad \text{(Non-negativity; or } x_1, x_2 \in \mathbb{Z}_{\ge 0} \text{ when whole units are enforced)}
\end{aligned}$$

## Example Scenario

### Inputs
* **Product X:** $3.00\text{ kg}$ material/unit, $4.00\text{ hours}$ labour/unit, $\$30.00$ contribution/unit[cite: 1]
* **Product Y:** $5.00\text{ kg}$ material/unit, $4.00\text{ hours}$ labour/unit, $\$40.00$ contribution/unit[cite: 1]
* **Available Resources:** $15,000.00\text{ kg}$ material; $16,000.00\text{ hours}$ labour; continuous units[cite: 1]

### Optimised Output
* **Product X:** $2,500.00\text{ units}$[cite: 1]
* **Product Y:** $1,500.00\text{ units}$[cite: 1]
* **Maximum Contribution:** $\$135,000.00$[cite: 1]
* **Resource Utilisation & Slack:**
  * Material: $100.0\%$ used ($0.00\text{ kg}$ slack)[cite: 1]
  * Labour: $100.0\%$ used ($0.00\text{ hours}$ slack)[cite: 1]

## Model Behaviour & Validation

* **Continuous vs. Integer Solutions:** Leaving *Whole units only* unchecked solves a continuous Linear Programming (LP) model[cite: 1]. Checking *Whole units only* switches the formulation to Mixed-Integer Linear Programming (MILP) so fractional units are not recommended when discrete items are required[cite: 1].
* **Binding Constraints & Slack:** Resources at $100.0\%$ utilisation are binding constraints ($0.00$ slack) that limit total contribution[cite: 1]. Non-binding resources display positive slack, indicating unused capacity.
* **Verification:** Solver results are cross-checked against manual simultaneous-equation solutions at the binding intersection ($3x_1 + 5x_2 = 15,000$ and $4x_1 + 4x_2 = 16,000 \implies x_1 = 2,500, x_2 = 1,500$) and spreadsheet solver models[cite: 1].

## Project Structure

* `app.py` — Streamlit user interface, input controls, optimisation solver logic, and results display[cite: 1]
* `requirements.txt` — Python dependencies required to run the application[cite: 1]
* `README.md` — Project documentation and mathematical model specification

## Running Locally

1. Clone the repository:
   ```bash
   git clone [https://github.com/amcbhome/lpp-graphical-optimisation.git](https://github.com/amcbhome/lpp-graphical-optimisation.git)
   cd lpp-graphical-optimisation
