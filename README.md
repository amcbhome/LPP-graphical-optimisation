# Production Optimisation

An interactive linear programming web application built with Python and Streamlit to determine the contribution-maximising product mix under resource constraints.

## Live Demo & Repository

* **Streamlit App:** [appuction-optimisation-9s8d2bz8ywcbmkxnyhk843.streamlit.app](https://appuction-optimisation-9s8d2bz8ywcbmkxnyhk843.streamlit.app/)
* **GitHub Repository:** [github.com/amcbhome/production-optimisation](https://github.com/amcbhome/production-optimisation)

## Overview

Management accounting and operations research frequently require allocating scarce production resources across competing products to maximise contribution. This tool lets users adjust unit contributions, resource requirements, resource availability, and integer-only ("Whole units only") constraints to inspect optimal production quantities, maximum contribution, resource utilisation, and slack.

## Algebraic Formulation

Let:
* $x_1$ = units of **Product X** to produce
* $x_2$ = units of **Product Y** to produce
* $c_1, c_2$ = contribution per unit ($) for Product X and Product Y
* $a_{m1}, a_{m2}$ = material required per unit (kg) for Product X and Product Y
* $a_{l1}, a_{l2}$ = labour required per unit (hours) for Product X and Product Y
* $M$ = total available material (kg)
* $L$ = total available labour (hours)

**Objective Function (Maximise Total Contribution):**

$$\text{Maximise } Z = c_1 x_1 + c_2 x_2$$

**Subject to:**

$$\begin{aligned}
a_{m1} x_1 + a_{m2} x_2 &\le M \quad \text{(Material constraint, kg)} \\
a_{l1} x_1 + a_{l2} x_2 &\le L \quad \text{(Labour constraint, hours)} \\
x_1, x_2 &\ge 0 \quad \text{(Non-negativity; or } x_1, x_2 \in \mathbb{Z}_{\ge 0} \text{ when whole units are enforced)}
\end{aligned}$$

## Example Scenario (Screenshot Parameters)

### Inputs
* **Product X:** $3.00\text{ kg}$ material/unit, $4.00\text{ hours}$ labour/unit, $\$30.00$ contribution/unit
* **Product Y:** $5.00\text{ kg}$ material/unit, $4.00\text{ hours}$ labour/unit, $\$40.00$ contribution/unit
* **Available Resources:** $15,000.00\text{ kg}$ material; $16,000.00\text{ hours}$ labour; continuous (non-integer) units

### Optimised Output
* **Product X:** $2,500.00\text{ units}$
* **Product Y:** $1,500.00\text{ units}$
* **Maximum Contribution:** $\$135,000.00$
* **Resource Utilisation & Slack:**
  * Material: $100.0\%$ used ($0.00\text{ kg}$ slack)
  * Labour: $100.0\%$ used ($0.00\text{ hours}$ slack)

## Project Structure

* `app.py` — Streamlit user interface, input controls, optimisation solver logic, and results display
* `requirements.txt` — Python dependencies required to run the application
* `README.md` — Project documentation and mathematical model specification

## Running Locally

1. Clone the repository:
   ```bash
   git clone [https://github.com/amcbhome/production-optimisation.git](https://github.com/amcbhome/production-optimisation.git)
   cd production-optimisation
