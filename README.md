# LPP Graphical Optimisation

> **Portfolio Example | Prescriptive Analytics & Operations Research**
> 
> This project demonstrates an **Algebraic Notation** workflow for translating management accounting problems into interactive decision-support tools. Rather than relying on unverified generative AI code, the linear programming model is formulated and validated mathematically first. By anchoring the project to an ACCA example, the output can be assessed for accuracy.

## Live Demo & Repository

* **Streamlit App:** [lpp-graphical-optimisation-c5csmcbg5zwvp4mwqehrhs.streamlit.app](https://lpp-graphical-optimisation-c5csmcbg5zwvp4mwqehrhs.streamlit.app/)
* **GitHub Repository:** [github.com/amcbhome/LPP-graphical-optimisation](https://github.com/amcbhome/LPP-graphical-optimisation)
* **Reference Methodology:** [ACCA — Linear Programming (Performance Management / F5 Technical Article)](https://www.accaglobal.com/uk/en/student/exam-support-resources/fundamentals-exams-study-resources/f5/technical-articles/linear-programming.html)

## Overview

Management accounting and operations research frequently require allocating scarce production resources across competing products to maximise contribution. This application allows users to adjust unit contributions, resource consumption rates, available capacities, and integer constraints ("Whole units only") to inspect optimal production quantities, maximum contribution, resource utilisation, and slack.

## Dynamic Data Model & "What If" Scenario Analysis

The underlying data model is **not static**. While the default inputs provide a baseline scenario anchored to an ACCA linear programming example so outputs can be verified directly against established workings, all input parameters are interactive:

* **Adjustable Model Inputs:** Users can modify unit contribution values, per-unit material and labour requirements, total available resource capacities, and the whole-units integer toggle.
* **Scenario Testing:** Changing any parameter re-solves the model dynamically, making it straightforward to explore "what if" scenarios—such as resource bottlenecks, shifts in contribution margins, capacity expansions, or discrete batch constraints—and observe how the optimal product mix, maximum contribution, resource utilisation, and slack respond.

## Design Philosophy: Algebraic Notation First

This project follows an **Algebraic Notation** workflow rather than relying on unverified code generation. The mathematical model—decision variables, objective function, and linear constraints—is specified formally on paper before implementation. Putting human analytical oversight first ensures that computational error remains a measurable consequence rather than an unexamined cause.

## Algebraic Formulation

Let:
* $X$ = units of **Product X** to produce
* $Y$ = units of **Product Y** to produce
* Contribution per unit: $30 for Product X and $40 for Product Y

**Objective Function (Maximise Total Contribution):**

$$\text{Maximise } Z = 30X + 40Y$$

**Subject to:**

$$\begin{aligned}
3X + 5Y &\le 15,000 \quad \text{(Material constraint, kg)} \\
4X + 4Y &\le 16,000 \quad \text{(Labour constraint, hours)} \\
X, Y &\ge 0 \quad \text{(Non-negativity; or } X, Y \in \mathbb{Z}_{\ge 0} \text{ when whole units are enforced)}
\end{aligned}$$

## From Algebra to Prompt Engineering & PuLP

Those few lines of algebra act directly as the specification for both **prompt engineering** and the **`PuLP`** model translation—keeping AI code generation anchored to explicit mathematical constraints rather than guesswork:

* **Prompt Engineering Specification:** Rather than asking an AI assistant for a generic "production app," the prompt supplies the exact objective ($\text{Maximise } Z = 30X + 40Y$), constraints ($3X + 5Y \le 15,000$ and $4X + 4Y \le 16,000$), non-negativity/integer option, and required outputs (optimal $X$, $Y$, contribution, and resource slack).
* **Translation into `PuLP`:** Each algebraic element maps one-to-one into `PuLP`:
  * **Problem & Sense:** `LpProblem("Production_Optimisation", pulp.LpMaximize)`
  * **Decision Variables:** `LpVariable("X", lowBound=0, cat="Continuous")` (or `"Integer"` when *Whole units only* is selected) and `LpVariable("Y", lowBound=0, cat=...)`
  * **Objective Function:** `prob += 30 * X + 40 * Y, "Total_Contribution"`
  * **Constraints:** `prob += 3 * X + 5 * Y <= 15000, "Material_Limit"` and `prob += 4 * X + 4 * Y <= 16000, "Labour_Limit"`

## Example Scenario & Workings

### Inputs
* **Product X:** $3.00\text{ kg}$ material/unit, $4.00\text{ hours}$ labour/unit, $30.00 contribution/unit
* **Product Y:** $5.00\text{ kg}$ material/unit, $4.00\text{ hours}$ labour/unit, $40.00 contribution/unit
* **Available Resources:** $15,000.00\text{ kg}$ material; $16,000.00\text{ hours}$ labour; continuous units

### Working 1

The optimal point is at point B, which is at the intersection of:

$$3X + 5Y = 15,000$$

$$4X + 4Y = 16,000$$

Multiplying the first equation by four and the second by three we get:

$$12X + 20Y = 60,000$$

$$12X + 12Y = 48,000$$

The difference in the two equations is:

$$8Y = 12,000, \quad \text{or} \quad Y = 1,500$$

Substituting $Y = 1,500$ in any of the above equations will give us the $X$ value:

$$3X + 5(1,500) = 15,000$$

$$3X = 7,500$$

$$X = 2,500$$

The contribution gained is:

$$(2,500 \times 30) + (1,500 \times 40) = 135,000$$

### Optimised Output
* **Product X:** $2,500.00\text{ units}$
* **Product Y:** $1,500.00\text{ units}$
* **Maximum Contribution:** $135,000.00
* **Resource Utilisation & Slack:**
  * Material: $100.0\%$ used ($0.00\text{ kg}$ slack)
  * Labour: $100.0\%$ used ($0.00\text{ hours}$ slack)

## Model Behaviour & Validation

* **Continuous vs. Integer Solutions:** Leaving *Whole units only* unchecked solves a continuous Linear Programming (LP) model. Checking *Whole units only* switches the formulation to Mixed-Integer Linear Programming (MILP) when discrete items are required.
* **Binding Constraints & Slack:** Resources at $100.0\%$ utilisation are binding constraints ($0.00$ slack) that limit total contribution. Non-binding resources display positive slack, indicating unused capacity.
* **Verification:** By anchoring the baseline scenario to an ACCA linear programming example, solver outputs can be assessed for accuracy against Working 1 and spreadsheet solver models.

## Project Structure

* `app.py` — Streamlit user interface, input controls, optimisation solver logic, and results display
* `requirements.txt` — Python dependencies required to run the application
* `README.md` — Project documentation and mathematical model specification

## Running Locally

1. Clone the repository:
   ```bash
   git clone [https://github.com/amcbhome/LPP-graphical-optimisation.git](https://github.com/amcbhome/LPP-graphical-optimisation.git)
   cd lpp-graphical-optimisation
