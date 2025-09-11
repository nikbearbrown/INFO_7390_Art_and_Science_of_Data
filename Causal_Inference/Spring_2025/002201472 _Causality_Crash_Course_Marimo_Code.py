import marimo

__generated_with = "0.11.26"
app = marimo.App(
    width="full",
    app_title="Causal Inference",
    auto_download=["ipynb", "html"],
)


@app.cell(hide_code=True)
def _():
    import marimo as mo
    from IPython.display import Image
    mo.as_html(Image(url="https://imgs.xkcd.com/comics/correlation_2x.png")).center()
    return Image, mo


@app.cell(hide_code=True)
def _():
    import numpy as np
    import pandas as pd
    import matplotlib.pyplot as plt
    import seaborn as sns
    from sklearn.linear_model import LinearRegression
    return LinearRegression, np, pd, plt, sns


@app.cell(hide_code=True)
def _(mo):
    mo.md("""# Understanding Causal Inference with IHDP: From Theory to Practice""")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        """
        In predictive modeling, we often focus on finding correlations between variables. However, for decision-making, we need to understand the *causal* relationship between actions and outcomes.

        The fundamental problem of causal inference is that we can never observe both potential outcomes for the same unit - we can't simultaneously observe what happens when a person receives a treatment and doesn't receive a treatment.
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.callout("""
    In causal inference, a confounder is a variable that affects both the treatment (or independent variable) and the outcome (or dependent variable), potentially creating a spurious association if not controlled for. For example, when studying the effect of alcohol consumption on lung cancer risk, smokers tend to drink more and smoking is a direct cause of lung cancer, so smoking acts as a confounder that can distort the observed relationship between alcohol and cancer.
    """, kind="info")
    return


@app.cell(hide_code=True)
def _(LinearRegression, mo, np, pd, plt):
    # Set random seed for reproducibility
    np.random.seed(42)

    # Generate data to illustrate correlation vs causation
    n = 1000

    # Common cause (confounder)
    confounder = np.random.normal(0, 1, n)

    # Treatment influenced by confounder
    treatment = 0.7 * confounder + np.random.normal(0, 0.5, n)

    # Outcome influenced by both treatment and confounder
    outcome = 0.3 * treatment + 0.7 * confounder + np.random.normal(0, 0.5, n)

    # Create a DataFrame
    data = pd.DataFrame({
        'Treatment': treatment,
        'Outcome': outcome,
        'Confounder': confounder
    })

    # Create model for the regression line
    model = LinearRegression()
    model.fit(data[['Treatment']], data['Outcome'])


    fig_1 = plt.figure(figsize=(12, 5))

    # Plot 1: Treatment vs Outcome (shows correlation)
    ax1 = plt.subplot(1, 2, 1)
    ax1.scatter(data['Treatment'], data['Outcome'], alpha=0.5)

    # Add regression line
    x_range = np.linspace(data['Treatment'].min(), data['Treatment'].max(), 100)
    ax1.plot(x_range, model.predict(x_range.reshape(-1, 1)), 'r-', linewidth=2)
    ax1.set_title('Correlation: Treatment vs Outcome\nCorrelation = {:.2f}'.format(
        np.corrcoef(data['Treatment'], data['Outcome'])[0, 1]))
    ax1.set_xlabel('Treatment')
    ax1.set_ylabel('Outcome')

    # Plot 2: Treatment vs Outcome with confounder as color
    ax2 = plt.subplot(1, 2, 2)
    scatter = ax2.scatter(data['Treatment'], data['Outcome'], c=data['Confounder'], cmap='viridis', alpha=0.5)
    plt.colorbar(scatter, label='Confounder')
    ax2.set_title('Causal Structure: Treatment, Outcome, and Confounder')
    ax2.set_xlabel('Treatment')
    ax2.set_ylabel('Outcome')

    plt.tight_layout()

    # Return interactive plot for marimo
    mo.mpl.interactive(fig_1)
    return (
        ax1,
        ax2,
        confounder,
        data,
        fig_1,
        model,
        n,
        outcome,
        scatter,
        treatment,
        x_range,
    )


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        """
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px;">
        <div>
        <h3>Left Plot</h3>
        Shows the correlation between treatment and outcome (0.78), with a regression line indicating a strong positive relationship. This is what you might see in an observational study without accounting for confounders.
        </div>
        <div>
        <h3>Right Plot</h3>
        The same data points, but colored by the confounder value. This reveals the underlying structure - points with similar confounder values cluster together, showing that the apparent treatment-outcome relationship is largely driven by the confounder.
        </div>
        </div>
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.callout("""
    The simulation demonstrates that despite seeing a strong correlation (0.78), the actual causal effect of the treatment on the outcome is weaker (0.3 in the data generation). The rest of the association is due to the confounder creating a spurious correlation - a classic example of "correlation does not imply causation."
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    def _():
        section_header = mo.md("""## 2. Theoretical Foundations of Causal Inference {#foundations}""")
        mo.output.replace(section_header)
    _()
    return


@app.cell(hide_code=True)
def _(mo):
    # Creating application domain columns
    healthcare = mo.md(
    """
    ### Healthcare
    - Evaluating treatment effectiveness
    - Understanding disease progression
    - Personalizing medical decisions
    """
    )

    policy = mo.md(
    """
    ### Policy
    - Program evaluation
    - Social interventions assessment
    - Education policy design
    """
    )

    business = mo.md(
    """
    ### Business
    - Marketing strategy optimization
    - Product feature evaluations
    - Customer retention strategies
    """
    )

    # Real-world applications section with columns
    applications_title = mo.md("### 2.1 Real-World Applications {#applications}\n\nCausal inference is crucial in various domains:")
    applications_columns = mo.hstack([healthcare, policy, business])

    # Key concepts section
    concepts = mo.md(
    """
    ### 2.2 Key Concepts in Causal Inference {#concepts}

    **The Potential Outcomes Framework**

    Developed by Rubin, this framework formalizes causal inference through potential outcomes. For each unit i:
    - Y_i(1): Outcome if unit i receives treatment
    - Y_i(0): Outcome if unit i doesn't receive treatment

    The individual treatment effect is defined as:

    \\[ \\tau_i = Y_i(1) - Y_i(0) \\]

    However, we can only observe one of these outcomes for each unit, which is known as the **fundamental problem of causal inference**.
    """
    )

    # Display all sections
    mo.vstack([applications_title, applications_columns, concepts])
    return (
        applications_columns,
        applications_title,
        business,
        concepts,
        healthcare,
        policy,
    )


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        """
        ### 2.3 Types of Treatment Effects in Causal Inference {#effects}

        ### What are "Treatments" in Causal Inference?

        In causal inference, a **treatment** refers to the intervention or manipulation being studied to determine its causal effect on an outcome of interest. Despite the medical-sounding terminology, treatments extend far beyond healthcare settings:

        - Medical interventions (medications, surgical procedures)
        - Policy changes (minimum wage increases, educational reforms) 
        - Business decisions (pricing strategies, marketing campaigns)
        - Social interventions (training programs, behavioral modifications)

        The **treatment variable** typically represents whether subjects received the intervention, usually coded as a binary variable (1=received treatment, 0=control/placebo), though it can sometimes be categorical for different treatment types or doses.

        ### Why Calculate Treatment Effects?

        Treatment effects measure the causal effect of a treatment on an outcome. We calculate them to:

        1. **Establish causality, not just correlation**: Determine the independent effect of a treatment when other factors are controlled for
        2. **Understand counterfactuals**: Estimate what would have happened to treated units had they not received treatment (and vice versa)
        3. **Quantify impact**: Measure not just whether an intervention worked, but how well it worked and for whom
        4. **Inform decision-making**: Make better decisions about implementing interventions and targeting specific populations

        ### Key Treatment Effect Measures

        **Average Treatment Effect (ATE):**
        The average effect of the treatment across the entire population.

        \\[ ATE = E[Y(1) - Y(0)] \\]

        Where Y(1) represents the potential outcome if treated, and Y(0) represents the potential outcome if not treated. This measures the expected difference in outcomes if everyone in the population received treatment versus if no one did.

        **Conditional Average Treatment Effect (CATE):**
        The average effect of the treatment conditional on specific covariates or characteristics.

        \\[ CATE(X=x) = E[Y(1) - Y(0) | X=x] \\]

        This measures how treatment effects vary across different subgroups defined by characteristics X. CATE helps identify which groups benefit most from treatment, enabling more targeted interventions.

        **Average Treatment Effect on the Treated (ATT/ATET):**
        The average effect among those who actually received the treatment.

        \\[ ATT = E[Y(1) - Y(0) | T=1] \\]

        This answers: "How much did those who received the treatment actually benefit?" It's particularly useful when evaluating programs that were targeted at specific populations or when treatment assignment wasn't random.

        ### Challenges in Estimation

        A fundamental challenge is that we never observe both potential outcomes for the same unit—known as the "fundamental problem of causal inference". Various methods address this challenge, including:

        - Randomized experiments
        - Regression adjustment
        - Matching methods
        - Instrumental variables
        - Inverse probability weighting
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    # Create the header
    header = mo.md("### 2.4 Key Assumptions in Causal Inference {#assumptions}")

    # Create separate elements for each assumption as callouts with fixed height
    assumption1 = mo.callout(
        mo.md(
            """
            ### 1. Unconfoundedness (Ignorability)
            Treatment assignment is independent of potential outcomes given observed covariates.

            \\[ (Y(0), Y(1)) \\perp T | X \\]
            """
        ),
        kind="info"
    )

    assumption2 = mo.callout(
        mo.md(
            """
            ### 2. Positivity (Overlap)
            Every unit has a non-zero probability of receiving either treatment or control.

            \\[ 0 < P(T=1|X=x) < 1 \\text{ for all } x \\]
            """
        ),
        kind="warn"
    )

    assumption3 = mo.callout(
        mo.md(
            """
            ### 3. SUTVA
            **Stable Unit Treatment Value Assumption**

            * No interference: One unit's treatment doesn't affect another unit's outcome
            * No hidden variations of treatment
            """
        ),
        kind="success"
    )

    # Stack the header and the columns of assumptions
    mo.vstack([
        header,
        mo.hstack([assumption1, assumption2, assumption3])
    ])
    return assumption1, assumption2, assumption3, header


@app.cell(hide_code=True)
def _(mo, np, plt):
    def _():
        # Visualize the overlap assumption
        # Use local variables with unique names to avoid conflicts
        sample_size = 1000  # Instead of reusing 'n'

        # Create two features
        X1 = np.random.normal(0, 1, sample_size)
        X2 = np.random.normal(0, 1, sample_size)

        # Scenario 1: Good overlap
        p_good = 1 / (1 + np.exp(-(0.5 * X1)))
        treatment_good = np.random.binomial(1, p_good, sample_size)

        # Scenario 2: Poor overlap
        p_poor = 1 / (1 + np.exp(-(3 * X1 + 2 * X2)))
        treatment_poor = np.random.binomial(1, p_poor, sample_size)

        # Plot - use a different variable name than 'fig'
        overlap_fig, axes = plt.subplots(1, 2, figsize=(10, 5))

        # Good overlap
        axes[0].scatter(X1, X2, c=treatment_good, cmap='coolwarm', alpha=0.6)
        axes[0].set_title('Good Overlap')
        axes[0].set_xlabel('X1')
        axes[0].set_ylabel('X2')

        # Poor overlap
        axes[1].scatter(X1, X2, c=treatment_poor, cmap='coolwarm', alpha=0.6)
        axes[1].set_title('Poor Overlap (Positivity Violation)')
        axes[1].set_xlabel('X1')
        axes[1].set_ylabel('X2')

        plt.tight_layout()

        # Use marimo's display method instead of plt.show()
        return mo.mpl.interactive(overlap_fig)


    _()
    return


@app.cell(hide_code=True)
def _(mo):
    # Create a two-column explanation
    left_column = mo.md("""
    ### Good Overlap (Left Plot)

    In this scenario, treatment assignment is weakly related to feature X1:
    - Blue points (control) and red points (treatment) are well-mixed throughout
    - Units across the entire covariate space have a reasonable probability of being in either treatment or control group
    - Treatment probability is calculated using a mild logistic function: p=11+exp(-(0.5⋅X1))p = 1/(1 + exp(-(0.5 * X1)))
    - This satisfies the positivity assumption because 0<P(T=1∣X=x)<10 < P(T=1|X=x) < 1 for all values of x
    - Makes reliable causal inference possible because counterfactuals exist for all covariate values
    - Allows for unbiased estimation of treatment effects (ATE, CATE, ATT)
    """).callout(kind="success")

    right_column = mo.md("""
    ### Poor Overlap (Right Plot)

    In this scenario, treatment assignment is strongly determined by X1 and X2:
    - Clear separation between blue points (control) and red points (treatment)
    - Left region has almost exclusively control units
    - Right region has almost exclusively treatment units
    - Treatment probability uses a steep logistic function: `p = 1/(1 + exp(-(3 * X1 + 2 * X2)))`
    - Violates the positivity assumption because for some values of x, P(T=1|X=x) ≈ 0 or P(T=1|X=x) ≈ 1
    - Makes causal inference unreliable in regions without overlap
    - Requires strong modeling assumptions or extrapolation to estimate treatment effects
    - May lead to biased estimates, especially in subgroups with poor representation in one treatment condition
    """).callout(kind="danger")

    # Display the two columns side by side
    mo.hstack([left_column, right_column])
    return left_column, right_column


@app.cell(hide_code=True)
def _(mo):
    def _():
        # Create a header for the DAG section
        header = mo.md("### 2.5 Interactive Causal Diagram")

        # Create a mermaid diagram for the IHDP causal structure
        diagram = mo.mermaid("""
        graph TB
            subgraph "Covariates"
                BR["Birth Related\nx_0, x_1, x_2, x_5, x_6"]
                M["Mother's Characteristics\nx_3, x_4, x_8, x_13-x_16"]
                P["Pregnancy Behaviors\nx_9, x_10, x_11, x_18, x_19"]
                S["Socioeconomic\nx_17"]
                L["Location\nx_20-x_24"]
            end

            BR --> T["Treatment\nIHDP Intervention"]
            M --> T
            P --> T
            S --> T
            L --> T

            BR --> Y["Outcome\nCognitive Score"]
            M --> Y
            P --> Y
            S --> Y

            T --> Y

            style T fill:#ff9999
            style Y fill:#99ccff
            style BR fill:#f9f9f9
            style M fill:#f9f9f9
            style P fill:#f9f9f9
            style S fill:#f9f9f9
            style L fill:#f9f9f9
        """)

        explanation = mo.md("""
        This directed acyclic graph (DAG) represents the assumed causal structure in the IHDP dataset:

        - **Covariates** (various characteristics) affect both treatment assignment and outcomes
        - **Treatment** (IHDP intervention) affects the outcome
        - The arrows represent causal relationships

        This structure illustrates why we need causal inference methods - the treatment effect is confounded by covariates that affect both treatment assignment and outcomes.
        """)

        # Replace output with the combined elements
        mo.output.replace(mo.vstack([header, diagram, explanation]))
    _()
    return


@app.cell(hide_code=True)
def _(mo):
    def _():
        # Create a header for the advanced causal inference methods section
        header = mo.md("### Causal Inference Methods")

        # Create a description of propensity score methods
        ps_methods = mo.callout(
            mo.md("""
            #### Propensity Score Methods

            Propensity score methods are statistical techniques for reducing selection bias in observational data. They work by balancing treatment groups on confounding factors to increase the validity of causal inference. The propensity score represents the probability of receiving treatment given a set of observed covariates.

            **Key applications include:**
            - **Matching**: Pairing treated and control units with similar propensity scores
            - **Stratification**: Grouping units into strata based on propensity scores
            - **Inverse Probability Weighting**: Weighting observations by the inverse of their propensity score
            - **Covariate adjustment**: Including propensity scores as covariates in regression models

            While propensity score methods can be powerful, they only adjust for observed confounders and may have limitations when the functional form is misspecified.
            """),
            kind="info"
        )

        # Create a description of difference-in-differences design
        did_methods = mo.callout(
            mo.md("""
            #### Difference-in-Differences (DiD) Design

            The Difference-in-Differences design is a quasi-experimental approach that estimates causal effects by comparing the changes in outcomes over time between a treatment group and a control group.

            **This method is particularly useful when:**
            - Random assignment to treatment is not feasible
            - Pre-treatment data is available for both groups
            - The parallel trends assumption holds (both groups would follow the same trend in the absence of treatment)

            DiD isolates the effect of a treatment by removing biases from permanent differences between groups and from shared time trends.
            """),
            kind="warn"
        )

        # Replace output with the combined elements
        mo.output.replace(mo.vstack([header, ps_methods, did_methods]))
    _()
    return


@app.cell(hide_code=True)
def _(mo):
    def _():
        # Create descriptions of more advanced methods
        rdd_methods = mo.callout(
            mo.md("""
            #### Regression Discontinuity Design (RDD)

            Regression discontinuity design is an important quasi-experimental approach that can be implemented when treatment assignment is determined by whether a continuous variable crosses a specific threshold.

            RDD exploits the fact that units just above and just below the cutoff threshold are similar in all respects except for treatment assignment, creating a situation similar to random assignment around the threshold. This design estimates causal treatment effects by comparing outcomes for units near this threshold.

            **Key elements of RDD:**
            - A continuous **running variable** (or assignment variable)
            - A clear **cutoff threshold** that determines treatment
            - **Sharp RDD**: Treatment is deterministically assigned based on the threshold
            - **Fuzzy RDD**: Threshold increases probability of treatment but doesn't determine it completely
            """),
            kind="info"
        )

        # Create a description of synthetic control methods
        scm_methods = mo.callout(
            mo.md("""
            #### Synthetic Control Methods

            Synthetic control methods allow for causal inference when we have as few as one treated unit and many control units observed over time.

            **The approach:**
            - Creates a weighted combination of control units that resembles the treated unit before intervention
            - Uses this "synthetic control" to estimate what would have happened to the treated unit without treatment
            - Is especially useful for policy interventions affecting entire regions or populations

            This method has been described as "the most important development in program evaluation in the last decade" by some researchers and is particularly valuable for case studies with a small number of treated units.
            """),
            kind="warn"
        )

        # Replace output with the combined elements
        mo.output.replace(mo.vstack([rdd_methods, scm_methods]))
    _()
    return


@app.cell(hide_code=True)
def _(mo):
    def _():
        # Create descriptions of more advanced methods
        sensitivity_methods = mo.callout(
            mo.md("""
            #### Sensitivity Analysis for Unobserved Confounding

            Unobserved confounding is a central barrier to drawing causal inferences from observational data. Sensitivity analysis explores how sensitive causal conclusions are to potential unobserved confounding, helping researchers understand the robustness of their findings.

            **Key approaches include:**
            - **Rosenbaum bounds**: Quantifies how strong an unobserved confounder would need to be to invalidate results
            - **E-values**: Measures the minimum strength of association an unmeasured confounder would need to have with both treatment and outcome to explain away an observed association
            - **Simulation-based methods**: Creating plausible scenarios with simulated confounders to test result stability

            While methods like propensity score matching can adjust for observed confounding, sensitivity analysis helps address the "Achilles heel" of most nonexperimental studies - the potential impact of unmeasured confounding.
            """),
            kind="danger"
        )

        # Create a description of heterogeneous treatment effects
        hte_methods = mo.callout(
            mo.md("""
            #### Heterogeneous Treatment Effects

            Treatment effects often vary across different subpopulations, a phenomenon known as treatment effect heterogeneity. Understanding this heterogeneity is crucial for targeting interventions effectively.

            **Methods for estimating heterogeneous effects include:**
            - **Subgroup analysis**: Estimating treatment effects within predefined subgroups
            - **Interaction terms**: Including treatment-covariate interactions in regression models
            - **Causal trees/forests**: Machine learning approaches that adaptively identify subgroups with different treatment effects
            - **Meta-learners**: Two-stage approaches that separate the estimation of outcome and treatment effect models

            Discovering heterogeneous effects allows for personalized interventions and can reveal important insights about treatment mechanisms that might be masked when looking only at average effects.
            """),
            kind="success"
        )

        # Replace output with the combined elements
        mo.output.replace(mo.vstack([sensitivity_methods, hte_methods]))
    _()
    return


@app.cell(hide_code=True)
def _(mo):
    def _():
        # Create a header for the key terms section
        header = mo.md("### 2.7 Key Terms in Causal Inference {#key-terms}")

        # Create a tabular layout of key causal inference terms
        left_terms = mo.md("""
        | Term | Definition |
        |------|------------|
        | **Potential Outcomes Framework** | The formal mathematical framework for causal inference where each unit has potential outcomes under different treatment conditions |
        | **Average Treatment Effect (ATE)** | The expected difference between potential outcomes if the entire population received treatment versus control |
        | **Average Treatment Effect on the Treated (ATT/ATET)** | The average effect for those who actually received the treatment |
        | **Conditional Average Treatment Effect (CATE)** | Treatment effects for specific subgroups defined by covariates |
        | **Unconfoundedness/Ignorability** | The assumption that treatment assignment is independent of potential outcomes given observed covariates |
        | **Positivity/Overlap** | The assumption that every unit has a non-zero probability of receiving each treatment condition |
        | **Stable Unit Treatment Value Assumption (SUTVA)** | The assumption that one unit's treatment doesn't affect another unit's outcome |
        | **Instrumental Variables** | Variables that affect treatment assignment but not outcomes directly |
        """)

        right_terms = mo.md("""
        | Term | Definition |
        |------|------------|
        | **Mediation Analysis** | The study of how treatments affect outcomes through intermediate variables |
        | **Heterogeneous Treatment Effects** | Variation in treatment effects across different subpopulations |
        | **Doubly Robust Estimation** | Methods that remain consistent if either the outcome model or the treatment assignment model is correctly specified |
        | **Selection Bias** | Bias arising when treatment groups differ systematically in ways that affect outcomes |
        | **Confounding Bias** | Bias due to variables that affect both treatment assignment and outcomes |
        | **Common Support/Overlap Region** | The range of propensity scores where both treated and control units exist |
        | **G-methods** | A class of causal inference methods for time-varying treatments (g-formula, marginal structural models) |
        | **Causal Diagram/DAG** | Directed acyclic graphs that visually represent causal relationships between variables |
        """)

        # Add note about the importance of terminology
        note = mo.callout(
            mo.md("""
            Understanding these terms is crucial for effectively applying causal inference methods and correctly interpreting results. Many of these concepts are interrelated and build upon each other to form the foundation of causal reasoning from observational data.
            """),
            kind="info"
        )

        # Replace output with the combined elements
        mo.output.replace(mo.vstack([header, mo.hstack([left_terms, right_terms]), note]))
    _()
    return


@app.cell(hide_code=True)
def _(mo):
    def _():
        section_header = mo.md("""## 3. The IHDP Dataset {#ihdp-intro}""")
        mo.output.replace(section_header)
    _()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### 3.1 Overview of the IHDP Dataset

        The Infant Health and Development Program (IHDP) was conducted from 1985 to 1988 and was designed to evaluate the effect of educational and family support services along with pediatric follow-up on the development of low birth weight infants.

        The intervention consisted of:
        - Home visits by specialists
        - Child development center attendance
        - Parent group meetings

        For causal inference studies, the dataset has been modified by Jennifer Hill (2011) to create a semi-synthetic version where:
        - Some participants from the treatment group were removed to create selection bias
        - The outcomes were simulated while preserving the relationships with covariates

        This modification allows researchers to know the "ground truth" causal effects, making it an ideal benchmark dataset for causal inference methods.
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.callout("""
    Dataset Context: The Infant Health and Development Program was a randomized controlled intervention designed to evaluate the effect of home visits by specialists on the cognitive development of premature infants.""", kind="info")
    return


@app.cell(hide_code=True)
def _(pd):
    from sklearn.model_selection import train_test_split
    import urllib.request
    import os

    # Function to download and load the IHDP dataset
    def load_ihdp_data():
        """
        Load the IHDP dataset for causal inference

        Returns:
            DataFrame with treatment, outcome, and covariates
        """
        # Create a directory for the data if it doesn't exist    
        if not os.path.exists('data'):
            os.makedirs('data')

        # Download the data if it doesn't exist
        if not os.path.exists('data/ihdp_npci_1.csv'):
            print("Downloading IHDP dataset...")
            url = "https://raw.githubusercontent.com/AMLab-Amsterdam/CEVAE/master/datasets/IHDP/csv/ihdp_npci_1.csv"
            urllib.request.urlretrieve(url, 'data/ihdp_npci_1.csv')

        # Load the data
        data = pd.read_csv('data/ihdp_npci_1.csv')

        # Rename columns for clarity
        column_names = ['treatment']
        column_names.extend([f'y_{i}' for i in range(2)])  # factual and counterfactual outcomes
        column_names.extend([f'mu_{i}' for i in range(2)])  # expected outcomes without noise
        column_names.extend([f'x_{i}' for i in range(25)])  # covariates

        data.columns = column_names

        # Rename for more intuitive understanding
        data.rename(columns={
            'y_0': 'y_factual',
            'y_1': 'y_cfactual',
            'mu_0': 'mu_0',
            'mu_1': 'mu_1'
        }, inplace=True)

        return data

    # Load the IHDP dataset
    ihdp_data = load_ihdp_data()
    return ihdp_data, load_ihdp_data, os, train_test_split, urllib


@app.cell(hide_code=True)
def _(mo):
    def _():
        section_header = mo.md("""## 4. Exploratory Data Analysis {#eda}""")
        mo.output.replace(section_header)
    _()
    return


@app.cell(hide_code=True)
def _(ihdp_data, mo):
    def _():
        m1 = mo.md("### 4.1 IHDP Dataset Preview {#overview}")
        m2 = mo.ui.dataframe(ihdp_data.head())
        mo.output.replace(mo.vstack([m1,m2]))
    _()
    return


@app.cell(hide_code=True)
def _(ihdp_data, mo):
    def _():
        m1 = mo.md("### 4.2 Dataset Information")
        info_md = f"""
        - **Number of samples:** {ihdp_data.shape[0]}
        - **Number of variables:** {ihdp_data.shape[1]}
        - **Treatment assignment rate:** {ihdp_data['treatment'].mean():.2f}
        """
        m3 = mo.md(info_md)
        mo.output.replace(mo.vstack([m1,m3]))

    _()
    return


@app.cell(hide_code=True)
def _(ihdp_data, mo, pd):
    def _():
        m1 = mo.md("### 4.3 Column Types")

        # Create intermediate dataframe
        dtype_df = pd.DataFrame({
            'Column': list(ihdp_data.dtypes.index),
            'Data Type': [str(x) for x in ihdp_data.dtypes.values]
        })

        m2 = mo.ui.dataframe(dtype_df)
        mo.output.replace(mo.vstack([m1,m2]))
    _()
    return


@app.cell(hide_code=True)
def _(ihdp_data, mo, plt, sns):
    def _():
        m1 = mo.md("### 4.4 Treatment Distribution")
        fig, ax = plt.subplots(figsize=(8, 5))
        sns.countplot(x='treatment', data=ihdp_data, ax=ax)
        ax.set_title('Distribution of Treatment Assignment')
        ax.set_xlabel('Treatment (0=Control, 1=Treated)')
        ax.set_ylabel('Count')
        # Use mo.mpl.interactive instead of just passing the figure
        interactive_fig = mo.mpl.interactive(fig)
        mo.output.replace(mo.vstack([m1, interactive_fig]))
    _()
    return


@app.cell(hide_code=True)
def _(ihdp_data, mo, plt, sns):
    # Visualize outcome distributions by treatment
    def _():
        m1 = mo.md("### 4.5 Outcome Distributions by Treatment")
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.boxplot(x='treatment', y='y_factual', data=ihdp_data, ax=ax)
        ax.set_title('Factual Outcome Distribution by Treatment Group')
        ax.set_xlabel('Treatment (0=Control, 1=Treated)')
        ax.set_ylabel('Outcome')
        # Convert to interactive plot
        interactive_fig = mo.mpl.interactive(fig)
        mo.output.replace(mo.vstack([m1, interactive_fig]))
    _()
    return


@app.cell(hide_code=True)
def _(ihdp_data, mo):
    def _():
        m1 = mo.md("### 4.6 Summary Statistics")
        m2 = mo.ui.dataframe(ihdp_data.describe())
        mo.output.replace(mo.vstack([m1, m2]))
    _()
    return


@app.cell
def _(pd):
    # Define covariate descriptions
    covariate_descriptions = {
        'x_0': "Birth weight",
        'x_1': "Birth order",
        'x_2': "Head circumference at birth",
        'x_3': "Mother's age",
        'x_4': "Mother's education level",
        'x_5': "Child is first born",
        'x_6': "Child is male",
        'x_7': "Twin",
        'x_8': "Mother's race/ethnicity",
        'x_9': "Mother smoked during pregnancy",
        'x_10': "Mother drank alcohol during pregnancy",
        'x_11': "Mother had drugs during pregnancy",
        'x_12': "Neonatal health index",
        'x_13': "Mother is married",
        'x_14': "Mother worked during pregnancy",
        'x_15': "Mother had prenatal care",
        'x_16': "Mother's weight gain during pregnancy",
        'x_17': "Family income",
        'x_18': "Preterm birth",
        'x_19': "Birth complications",
        'x_20': "Site 1",
        'x_21': "Site 2",
        'x_22': "Site 3",
        'x_23': "Site 4",
        'x_24': "Site 5"
    }

    # Create a DataFrame for UI display
    covariates_df = pd.DataFrame({
        'Variable': list(covariate_descriptions.keys()),
        'Description': list(covariate_descriptions.values())
    })
    return covariate_descriptions, covariates_df


@app.cell(hide_code=True)
def _(covariates_df, mo):
    def _():
        # Create markdown header for covariate descriptions
        m1 = mo.md("### 4.7 Covariate Descriptions {#covariates}")

        # Display covariate descriptions as an interactive dataframe
        m2 = mo.ui.dataframe(covariates_df)

        # Replace output with vertically stacked components
        mo.output.replace(mo.vstack([m1, m2]))
    _()
    return


@app.cell(hide_code=True)
def _(ihdp_data, mo):
    def _():
        # Define numerical covariates
        numerical_covs = [f'x_{i}' for i in range(5)] + ['x_12']

        # Create markdown header for numerical statistics
        m1 = mo.md("### 4.8 Numerical Covariate Statistics")

        # Display summary statistics as an interactive dataframe
        m2 = mo.ui.dataframe(ihdp_data[numerical_covs].describe())

        # Replace output with vertically stacked components
        mo.output.replace(mo.vstack([m1, m2]))
    _()
    return


@app.cell(hide_code=True)
def _(covariate_descriptions, ihdp_data, mo):
    def _():
        # Define binary covariates
        binary_covs = [f'x_{i}' for i in range(5, 25) if i != 12]

        # Calculate binary rates
        binary_rates = ihdp_data[binary_covs].mean().reset_index()
        binary_rates.columns = ['Variable', 'Rate']
        binary_rates['Description'] = binary_rates['Variable'].map(covariate_descriptions)

        # Create markdown header for binary rates
        m1 = mo.md("### 4.9 Binary Covariate Rates")

        # Display binary rates as an interactive dataframe
        m2 = mo.ui.dataframe(binary_rates)

        # Replace output with vertically stacked components
        mo.output.replace(mo.vstack([m1, m2]))
    _()
    return


@app.cell
def _(mo):
    # Create dropdown for covariate selection
    available_covs = [f'x_{i}' for i in range(5)] + ['x_12']
    covariate_selector = mo.ui.dropdown(
        options=available_covs,
        value='x_0',
        label="Select covariate to visualize"
    )
    return available_covs, covariate_selector


@app.cell(hide_code=True)
def _(covariate_descriptions, covariate_selector, ihdp_data, mo):
    def _():
        # Visualize distribution of selected covariate
        import matplotlib.pyplot as plt
        import seaborn as sns

        def plot_distribution(selected_cov):
            fig, ax = plt.subplots(figsize=(10, 6))
            sns.histplot(ihdp_data[selected_cov], ax=ax, kde=True)
            desc = covariate_descriptions.get(selected_cov, "")
            if len(desc) > 30:
                desc = desc[:30] + "..."
            ax.set_title(f"{selected_cov}: {desc}")
            ax.set_xlabel(selected_cov)
            ax.set_ylabel("Count")
            return fig

        # Create header and layout
        m1 = mo.md("### 4.10 Distribution of Key Numerical Covariates")

        # Get description for the selected covariate
        selected_desc = mo.md(f"**Selected variable**: {covariate_selector.value} - {covariate_descriptions.get(covariate_selector.value, '')}")

        # Create plot based on selected covariate
        plot_fig = plot_distribution(covariate_selector.value)
        interactive_plot = mo.mpl.interactive(plot_fig)

        # Replace output with interactive components
        mo.output.replace(mo.vstack([
            m1,
            mo.hstack([covariate_selector]),
            selected_desc,
            interactive_plot
        ]))
    _()
    return


@app.cell(hide_code=True)
def _(mo):
    def _():
        m1 = mo.md("""
        1. Strong positive correlation (0.85) between x0x_0 (child's birth weight) and x1x_1 (child's birth order). This indicates that higher birth order (later-born children) tends to be associated with higher birth weight.
        2. Strong negative correlation (-0.76 and -0.7) between x2x_2 (head circumference) and both birth weight (x0x_0) and birth order (x1x_1). This is somewhat counterintuitive, as we might expect larger babies to have larger head circumferences. This inverse relationship could suggest measurement issues or certain medical conditions in the dataset.
        3. Most demographic variables (x3x_3 - mother's age, x4x_4 - mother's education) show weak correlations with other variables, suggesting independence.
        4. Child's neonatal health index (x12x_12) has mostly weak correlations with other variables, with the strongest being a mild positive correlation (0.13) with mother's age.
        """)
        m2 = mo.callout("For causal inference, these correlations are important because strongly correlated variables can create confounding issues. For example, if treatment assignment is related to birth weight, birth order might inadvertently become a confounder due to its strong correlation with birth weight.", kind="info")
        mo.output.replace(mo.vstack([m1, m2]))

    _()
    return


@app.cell(hide_code=True)
def _(mo):
    def _():
        section_header = mo.md("""## 5. Setting Up for Causal Analysis {#analysis-setup}""")
        mo.output.replace(section_header)
    _()
    return


@app.cell(hide_code=True)
def _(mo):
    def _():
        subsection_header = mo.md("""### 5.1 Data Preparation {#data-prep}

        > 🔧 **Step 1**: Properly prepare the data for causal analysis

        Before implementing causal inference methods, we need to prepare our data appropriately. This includes:

        1. Splitting the data into training and test sets
        2. Scaling continuous features
        3. Identifying the types of variables (continuous vs. binary)
        4. Handling any missing values (if present)

        This preparation ensures that our causal inference methods will work properly and produce reliable estimates.
        """)
        mo.output.replace(subsection_header)
    _()
    return


@app.cell(hide_code=True)
def _(ihdp_data, mo, pd, plt, sns, train_test_split):
    # Identify continuous and binary variables
    continuous_vars = ['x_0', 'x_1', 'x_2', 'x_3', 'x_4', 'x_12']
    binary_vars = [f'x_{i}' for i in range(5, 25) if i != 12]

    # Check for missing values
    missing_values = ihdp_data.isnull().sum()
    print(f"Missing values in dataset: {missing_values.sum()}")

    # Split the data into features, treatment, and outcomes
    X = ihdp_data[[f'x_{i}' for i in range(25)]]
    T = ihdp_data['treatment']
    Y = ihdp_data['y_factual']

    # Also track true potential outcomes for evaluation (not available in real-world scenarios)
    Y0 = ihdp_data['mu_0']
    Y1 = ihdp_data['mu_1']

    # Split into training and test sets (80/20 split)
    X_train, X_test, T_train, T_test, Y_train, Y_test, Y0_train, Y0_test, Y1_train, Y1_test = train_test_split(
        X, T, Y, Y0, Y1, test_size=0.2, random_state=42
    )
    from sklearn.preprocessing import StandardScaler

    scaler = StandardScaler()
    X_train_scaled = X_train.copy()
    X_test_scaled = X_test.copy()

    for var in continuous_vars:
        X_train_scaled[var] = scaler.fit_transform(X_train[[var]])
        X_test_scaled[var] = scaler.transform(X_test[[var]])

    # Print information about the split
    print(f"Training set: {X_train.shape[0]} samples")
    print(f"Test set: {X_test.shape[0]} samples")
    print(f"Treatment rate in training set: {T_train.mean():.2f}")
    print(f"Treatment rate in test set: {T_test.mean():.2f}")
    print(f"True ATE in training set: {(Y1_train - Y0_train).mean():.4f}")
    print(f"True ATE in test set: {(Y1_test - Y0_test).mean():.4f}")


    # Set plotting style
    def _():
        plt.style.use('seaborn-v0_8-whitegrid')
        sns.set_context("notebook", font_scale=1.2)    

        # Scale continuous features
        # Visualize the data split and scaling effects
        fig, axes = plt.subplots(1, 2, figsize=(10, 5))

        # Plot 1: Training vs Test split by treatment
        train_counts = pd.DataFrame({
            'Set': ['Training'] * 2,
            'Treatment': ['Control', 'Treated'],
            'Count': [(T_train == 0).sum(), (T_train == 1).sum()]
        })

        test_counts = pd.DataFrame({
            'Set': ['Test'] * 2,
            'Treatment': ['Control', 'Treated'],
            'Count': [(T_test == 0).sum(), (T_test == 1).sum()]
        })

        counts_df = pd.concat([train_counts, test_counts])

        sns.barplot(x='Set', y='Count', hue='Treatment', data=counts_df, ax=axes[0])
        axes[0].set_title('Sample Distribution in Training and Test Sets')
        axes[0].set_ylabel('Number of Samples')

        # Plot 2: Effect of scaling on a continuous variable
        sns.histplot(X_train['x_0'], kde=True, label='Before scaling', ax=axes[1], alpha=0.5)
        sns.histplot(X_train_scaled['x_0'], kde=True, label='After scaling', ax=axes[1], alpha=0.5)
        axes[1].set_title('Effect of Scaling on Birth Weight (x_0)')
        axes[1].set_xlabel('Value')
        axes[1].legend()

        plt.tight_layout()

        # Replace plt.show() with mo.mpl.interactive for interactivity
        return mo.mpl.interactive(fig)

    _()
    return (
        StandardScaler,
        T,
        T_test,
        T_train,
        X,
        X_test,
        X_test_scaled,
        X_train,
        X_train_scaled,
        Y,
        Y0,
        Y0_test,
        Y0_train,
        Y1,
        Y1_test,
        Y1_train,
        Y_test,
        Y_train,
        binary_vars,
        continuous_vars,
        missing_values,
        scaler,
        var,
    )


@app.cell(hide_code=True)
def _(mo):
    def _():
        analysis_md = mo.md("""
        **Analysis of Data Preparation:**

        The dataset preparation above accomplishes several important steps for causal inference:

        1. **Splitting the data** into training (80%) and test (20%) sets allows us to evaluate the performance of our causal inference methods on unseen data, which is crucial for assessing their generalizability.

        2. **Standardizing continuous variables** ensures that variables with different scales don't unduly influence our models. This is particularly important for methods that are sensitive to the scale of the input features, such as matching based on distances or regularized regression.

        3. **Preserving the treatment assignment rate** across training and test sets maintains the same level of class imbalance, which is important for methods that are sensitive to treatment prevalence.

        4. **Verifying the absence of missing values** confirms that we don't need to implement imputation strategies, which could introduce additional complexity and potential bias.

        The visualization on the left shows the distribution of treated and control units in both training and test sets, confirming that the treatment assignment rate is similar between the splits. The visualization on the right illustrates the effect of standardization on the birth weight variable, transforming it to have zero mean and unit variance, which makes it more suitable for many statistical and machine learning methods.
        """)

        mo.callout(analysis_md, kind="info")
    _()
    return


@app.cell(hide_code=True)
def _(mo):
    def _():
        subsection_header = mo.md("""### 5.2 Formulating the Causal Question {#causal-question}

        > 📋 **Step 2**: Define what causal effect you want to estimate

        Causal inference begins with a clear formulation of the causal question. For the IHDP dataset, our primary question is:

        **"What is the effect of specialist home visits (treatment) on the cognitive test scores (outcome) of premature infants?"**

        To formalize this question, we need to define:

        1. **Treatment variable (T)**: Binary indicator for receiving home visits
        2. **Outcome variable (Y)**: Cognitive test scores
        3. **Covariates (X)**: Baseline characteristics that may influence treatment assignment or outcomes
        4. **Target population**: Premature infants with low birth weight
        5. **Causal estimand**: The specific causal quantity we want to estimate
        """)
        mo.output.replace(subsection_header)
    _()
    return


@app.cell(hide_code=True)
def _(T_train, Y0_train, Y1_train, Y_train, mo, pd, plt):
    def _():
        # Define the causal question components
        treatment_var = 'Treatment (IHDP intervention)'
        outcome_var = 'Cognitive test scores'
        covariates_var = 'Baseline characteristics (25 variables)'

        # Calculate true causal effects (available in this simulated dataset)
        true_ate = (Y1_train - Y0_train).mean()

        # Calculate naive estimate
        naive_ate = Y_train[T_train == 1].mean() - Y_train[T_train == 0].mean()

        # Calculate true ATT (Average Treatment Effect on the Treated)
        true_att = (Y1_train[T_train == 1] - Y0_train[T_train == 1]).mean()

        # Create a DataFrame for visualization
        estimands_df = pd.DataFrame({
            'Estimand': ['ATE (Average Treatment Effect)', 'ATT (Average Treatment Effect on Treated)', 'Naive Difference in Means'],
            'Value': [true_ate, true_att, naive_ate],
            'Description': [
                'Expected effect if everyone received treatment vs. none',
                'Average effect among those who actually received treatment',
                'Simple difference in mean outcomes (biased estimate)'
            ]
        })

        # Visualize causal estimands
        plt.figure(figsize=(10, 6))
        bars = plt.barh(estimands_df['Estimand'], estimands_df['Value'], color=['skyblue', 'lightgreen', 'salmon'])
        plt.title('Causal Estimands in the IHDP Dataset')
        plt.xlabel('Effect Size')

        # Add value labels to the bars
        for i, bar in enumerate(bars):
            plt.text(bar.get_width() + 0.1, bar.get_y() + bar.get_height()/2, 
                     f'{estimands_df["Value"].iloc[i]:.4f}', 
                     va='center')

        # Add grid lines for readability
        plt.grid(axis='x', alpha=0.3)
        plt.tight_layout()

        # Create a table of key causal components
        causal_components = pd.DataFrame({
            'Component': ['Treatment Variable', 'Outcome Variable', 'Covariates', 'Target Population', 'Primary Causal Estimand'],
            'Definition': [treatment_var, outcome_var, covariates_var, 
                        'Premature infants with low birth weight', 'Average Treatment Effect (ATE)']
        })

        # Create the interactive output
        causal_question_layout = mo.vstack([
            mo.md("#### Causal Components in the IHDP Study"),
            mo.ui.table(causal_components),

            mo.md("#### Comparison of Causal Estimands"),
            mo.mpl.interactive(plt.gcf()),

            mo.md("""**Note:** In real-world causal inference, we typically don't know the true causal effects. 
            The IHDP dataset is semi-synthetic, allowing us to know the ground truth for evaluation.""")
        ])
        mo.output.append(causal_question_layout)
    _()
    return


@app.cell(hide_code=True)
def _(mo):
    def _():
        analysis_md = mo.md("""
        **Analysis of the Causal Question Formulation:**

        The causal question has been clearly formulated, which is a crucial first step in any causal inference analysis. Key observations:

        1. **Treatment-Outcome Relationship**: We're interested in the effect of the IHDP intervention (home visits) on cognitive test scores, a well-defined relationship that aligns with policy and educational interventions.

        2. **Causal Estimands**: We've defined multiple estimands of interest, with the Average Treatment Effect (ATE) as our primary focus. The ATE represents the expected change in cognitive scores if the entire population received the treatment versus if none did.

        3. **ATT vs ATE**: The Average Treatment Effect on the Treated (ATT) is very close to the ATE in this dataset (difference of only 0.0041). This suggests that the treatment effect is relatively homogeneous across the population, or that selection into treatment wasn't strongly related to treatment effect heterogeneity.

        4. **Naive Estimate**: The naive difference in means is similar to the true ATE in this dataset. This is somewhat unexpected, as we would typically expect selection bias to create a difference between the naive estimate and the true causal effect. This similarity could be a characteristic of how the semi-synthetic dataset was generated.

        Formulating these specific causal questions allows us to select appropriate methods for estimation and evaluate their performance against known ground truth values in this unique dataset.
        """)

        mo.output.append(mo.callout(analysis_md, kind="info"))

    _()
    return


@app.cell(hide_code=True)
def _(mo):
    def _():
        subsection_header = mo.md("""### 5.3 Propensity Score Analysis {#propensity-analysis}

        > 🏈 **Step 3**: Analyze propensity scores to check assumptions and prepare for causal methods

        Propensity scores are a key concept in causal inference, representing the probability of receiving treatment given observed covariates. They're useful for:

        1. **Assessing overlap**: Checking the positivity assumption by examining the distribution of propensity scores
        2. **Creating balance**: Helping ensure that treated and control groups are comparable
        3. **Estimation**: Using in various estimation methods like inverse probability weighting, matching, and stratification

        Let's estimate propensity scores for our dataset and analyze their properties.
        """)
        mo.output.replace(subsection_header)
    _()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.callout(mo.md(
        """
        #### What are Propensity Scores?

        Propensity scores represent the probability that a unit receives the treatment, conditional on observed covariates. Mathematically, the propensity score is defined as:

        \[
        e(X) = P(T=1|X)
        \]

        Where \(T\) is the treatment indicator and \(X\) represents the covariates.

        #### Why Are Propensity Scores Important?

        Propensity scores help address the fundamental challenge in causal inference: units are either treated or untreated, never both. By conditioning on the propensity score, we can create balance between treated and control groups, mimicking a randomized experiment.

        Key properties of propensity scores include:

        1. **Balancing score**: Conditioning on the propensity score balances the distribution of covariates between treatment groups
        2. **Dimensionality reduction**: Reduces multiple covariates to a single score
        3. **Identification of areas of common support**: Helps identify regions where causal inference is reliable

        We'll estimate propensity scores using logistic regression and also explore a machine learning approach with random forests.
        """
    ))
    return


@app.cell(hide_code=True)
def _(mo, plt, ps_df, sns):
    def _():
        # Create a figure for propensity score distributions
        fig, axes = plt.subplots(1, 2, figsize=(14, 6))

        # Plot 1: Logistic regression propensity score distributions
        sns.histplot(
            data=ps_df, x='ps_logistic', hue='treatment', 
            bins=30, element="step", common_norm=False,
            ax=axes[0], alpha=0.7
        )
        axes[0].set_title('Propensity Score Distribution (Logistic Regression)')
        axes[0].set_xlabel('Propensity Score')
        axes[0].set_ylabel('Count')

        # Plot 2: Random forest propensity score distributions
        sns.histplot(
            data=ps_df, x='ps_rf', hue='treatment', 
            bins=30, element="step", common_norm=False,
            ax=axes[1], alpha=0.7
        )
        axes[1].set_title('Propensity Score Distribution (Random Forest)')
        axes[1].set_xlabel('Propensity Score')
        axes[1].set_ylabel('Count')

        plt.tight_layout()

        # Return the interactive plot
        plot = mo.mpl.interactive(fig)
        header = mo.md("#### Propensity Score Distributions")
        mo.output.replace(mo.vstack([header, plot]))

    _()
    return


@app.cell(hide_code=True)
def _(T_train, mo, pd, propensity_scores, rf_propensity_scores):
    def _():
        # Check for overlap/positivity assumption
        # Calculate min and max propensity scores for treated and control groups
        ps_stats = pd.DataFrame({
            'Model': ['Logistic Regression', 'Random Forest'],
            'Min (Treated)': [propensity_scores[T_train == 1].min(), rf_propensity_scores[T_train == 1].min()],
            'Max (Treated)': [propensity_scores[T_train == 1].max(), rf_propensity_scores[T_train == 1].max()],
            'Min (Control)': [propensity_scores[T_train == 0].min(), rf_propensity_scores[T_train == 0].min()],
            'Max (Control)': [propensity_scores[T_train == 0].max(), rf_propensity_scores[T_train == 0].max()]
        })

        # Calculate common support region
        ps_stats['Common Support Min'] = ps_stats[['Min (Treated)', 'Min (Control)']].max(axis=1)
        ps_stats['Common Support Max'] = ps_stats[['Max (Treated)', 'Max (Control)']].min(axis=1)

        # Calculate percentage of units in common support
        in_support_logistic = ((propensity_scores >= ps_stats.loc[0, 'Common Support Min']) & 
                              (propensity_scores <= ps_stats.loc[0, 'Common Support Max'])).mean() * 100
        in_support_rf = ((rf_propensity_scores >= ps_stats.loc[1, 'Common Support Min']) & 
                        (rf_propensity_scores <= ps_stats.loc[1, 'Common Support Max'])).mean() * 100

        ps_stats['Units in Common Support (%)'] = [in_support_logistic, in_support_rf]

        # Count extreme propensity scores (< 0.1 or > 0.9)
        extreme_ps_logistic = ((propensity_scores < 0.1) | (propensity_scores > 0.9)).mean() * 100
        extreme_ps_rf = ((rf_propensity_scores < 0.1) | (rf_propensity_scores > 0.9)).mean() * 100

        ps_stats['Extreme PS (%)'] = [extreme_ps_logistic, extreme_ps_rf]

        # Create markdown output
        header = mo.md("#### Overlap and Common Support Analysis")

        explanation = mo.md("""
        To satisfy the positivity assumption for causal inference, we need sufficient overlap in propensity scores between treated and control groups. A good overlap indicates that units with similar characteristics have a chance of being in either treatment group.

        The **common support region** is the range of propensity scores where both treated and control units exist. Ideally, we want most units to fall within this region. Units outside this region may be problematic for causal inference.

        **Extreme propensity scores** (close to 0 or 1) indicate units that are very likely to be in one group only, which can cause issues for some causal inference methods.
        """)

        table = mo.ui.table(ps_stats.round(4))

        # Assessment of positivity assumption
        assessment = mo.callout(
            mo.md("""
            **Assessment of Positivity Assumption:**  

            - For the logistic regression model, {:.1f}% of units are within the common support region.  
            - The random forest model shows {:.1f}% of units in common support.  
            - Extreme propensity scores affect {:.1f}% (logistic) and {:.1f}% (random forest) of units.  

            The {} model provides better overlap. Overall, the positivity assumption appears to be {} satisfied, which {} for reliable causal inference using propensity score methods.
            """.format(
                in_support_logistic, 
                in_support_rf,
                extreme_ps_logistic,
                extreme_ps_rf,
                "logistic regression" if in_support_logistic > in_support_rf else "random forest",
                "reasonably well" if max(in_support_logistic, in_support_rf) > 80 else "partially",
                "is promising" if max(in_support_logistic, in_support_rf) > 80 else "raises some concerns"
            )),
            kind="info"
        )

        mo.output.replace(mo.vstack([header, explanation, table, assessment]))
    _()
    return


@app.cell(hide_code=True)
def _(
    T_train,
    X_train_scaled,
    mo,
    np,
    pd,
    plt,
    propensity_scores,
    rf_propensity_scores,
    roc_auc_score,
    roc_curve,
):
    def _():
        # Create a figure for ROC curves
        fig, ax = plt.subplots(figsize=(10, 6))

        # Calculate ROC curves
        fpr_lr, tpr_lr, _ = roc_curve(T_train, propensity_scores)
        fpr_rf, tpr_rf, _ = roc_curve(T_train, rf_propensity_scores)

        # Calculate AUC scores
        auc_lr = roc_auc_score(T_train, propensity_scores)
        auc_rf = roc_auc_score(T_train, rf_propensity_scores)

        # Plot ROC curves
        ax.plot(fpr_lr, tpr_lr, lw=2, label=f'Logistic Regression (AUC = {auc_lr:.3f})')
        ax.plot(fpr_rf, tpr_rf, lw=2, label=f'Random Forest (AUC = {auc_rf:.3f})')
        ax.plot([0, 1], [0, 1], 'k--', lw=2)

        ax.set_xlim([0.0, 1.0])
        ax.set_ylim([0.0, 1.05])
        ax.set_xlabel('False Positive Rate')
        ax.set_ylabel('True Positive Rate')
        ax.set_title('ROC Curves for Propensity Score Models')
        ax.legend(loc='lower right')

        # Calculate standardized mean differences for covariates
        def calc_smd(var, treatment):
            """Calculate standardized mean difference for a variable"""
            treated_mean = var[treatment == 1].mean()
            control_mean = var[treatment == 0].mean()
            treated_var = var[treatment == 1].var()
            control_var = var[treatment == 0].var()
            pooled_std = np.sqrt((treated_var + control_var) / 2)
            # Handle zero standard deviation
            if pooled_std == 0:
                return 0
            return (treated_mean - control_mean) / pooled_std

        # Calculate SMD for each variable
        smd_values = []
        for col in X_train_scaled.columns:
            smd = calc_smd(X_train_scaled[col], T_train)
            smd_values.append({'Variable': col, 'SMD': smd})

        smd_df = pd.DataFrame(smd_values)

        # Sort by absolute SMD
        smd_df['Abs_SMD'] = smd_df['SMD'].abs()
        smd_df = smd_df.sort_values('Abs_SMD', ascending=False)

        # Create two-part layout
        roc_plot = mo.mpl.interactive(fig)
        roc_header = mo.md("#### Propensity Score Model Evaluation")
        roc_explanation = mo.md("""
        The ROC curves and AUC scores show how well our propensity score models discriminate between treated and control units. Higher AUC indicates better discrimination. 

        The Random Forest model typically achieves higher AUC, but this doesn't necessarily make it better for propensity score estimation. In fact, for propensity score analysis, we often prefer models that achieve good covariate balance rather than maximizing predictive performance.
        """)

        # Show balance table for top 10 most imbalanced covariates
        balance_header = mo.md("#### Covariate Balance Assessment")
        balance_explanation = mo.md("""
        The table below shows the standardized mean differences (SMD) for the most imbalanced covariates. SMD measures the difference in means between treated and control groups in standard deviation units.

        - **SMD > 0.1**: Indicates meaningful imbalance
        - **SMD > 0.25**: Indicates substantial imbalance

        Effective propensity score methods should reduce these imbalances when we condition on the propensity score.
        """)

        balance_table = mo.ui.table(smd_df.head(10).round(4))

        # Combine all elements
        mo.output.replace(mo.vstack([
            roc_header, 
            roc_plot,
            roc_explanation,
            balance_header,
            balance_explanation,
            balance_table
        ]))
    _()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.callout(mo.md("""
    **Summary of Propensity Score Analysis:**

    1. We've estimated propensity scores using both logistic regression and random forest models.
    2. The distributions show some separation between treated and control groups, which is expected in observational data.
    3. The common support analysis confirms that most units fall within regions where causal inference is reliable.
    4. The covariate balance assessment identifies which variables contribute most to selection bias.

    These propensity scores will be used in subsequent sections for implementing various causal inference methods including:
    - Inverse Probability Weighting (IPW)
    - Propensity Score Matching
    - Propensity Score Stratification
    - Doubly Robust methods

    Each method leverages propensity scores differently to estimate causal effects while accounting for confounding.
    """), kind="success")
    return


@app.cell(hide_code=True)
def _(mo):
    def _():
        section_header = mo.md("""## 6. Implementing Causal Inference Methods {#methods}

        In this section, we'll implement and evaluate various causal inference methods on the IHDP dataset. We'll start with simple methods, then move to propensity score-based approaches, and finally explore advanced machine learning methods. For each method, we'll:

        1. Explain the methodology and key assumptions
        2. Implement the method on our training data
        3. Evaluate its performance against the known ground truth
        4. Discuss strengths, weaknesses, and practical considerations
        """)
        mo.output.replace(section_header)
    _()
    return


@app.cell(hide_code=True)
def _(mo):
    def _():
        section_header = mo.md("""### 6.1 Simple Causal Inference Methods {#simple-methods}

        > 🔍 **Step 1**: Start with simple methods before moving to more complex approaches

        We'll begin with straightforward approaches that form the foundation of causal inference. These methods are easy to implement and interpret, making them excellent starting points for causal analysis.
        """)
        mo.output.replace(section_header)
    _()
    return


@app.cell(hide_code=True)
def _(mo):
    # Create a description of naive mean difference approach
    naive_description = mo.callout(
        mo.md(r"""
        #### Naive Mean Difference

        The simplest approach to estimating causal effects is to compare the average outcomes between treated and control groups:

        \[
        \hat{ATE}_{naive} = \frac{1}{n_1}\sum_{i:T_i=1}Y_i - \frac{1}{n_0}\sum_{i:T_i=0}Y_i
        \]

        where \(n_1\) is the number of treated units and \(n_0\) is the number of control units.

        **Key Assumption**: Treatment is randomly assigned (no confounding).

        **Limitations**: In observational studies, this estimate is often biased due to confounding factors that affect both treatment assignment and outcomes.
        """),
        kind="info"
    )

    # Create a description of regression adjustment approach
    regression_description = mo.callout(
        mo.md(r"""
        #### Regression Adjustment

        This method controls for confounding by including covariates in a regression model:

        \[
        Y_i = \alpha + \tau T_i + \beta X_i + \epsilon_i
        \]

        The coefficient \(\tau\) of the treatment variable \(T\) provides an estimate of the ATE.

        **Key Assumption**: The regression model is correctly specified (includes all confounders and captures their relationships with the outcome).

        **Advantages**: Simple to implement, interpretable, can handle continuous and binary covariates.

        **Limitations**: Relies on strong assumptions about the functional form of the relationship between covariates and outcomes.
        """),
        kind="warn"
    )

    # Create a description of stratification approach
    stratification_description = mo.callout(
        mo.md(r"""
        #### Stratification/Subclassification

        This method divides the data into subgroups (strata) based on important covariates, estimates treatment effects within each stratum, and takes a weighted average:

        \[
        \hat{ATE}_{strat} = \sum_{s=1}^{S} w_s (\bar{Y}_{s,1} - \bar{Y}_{s,0})
        \]

        where \(\bar{Y}_{s,1}\) is the average outcome for treated units in stratum \(s\), \(\bar{Y}_{s,0}\) is the average for control units, and \(w_s\) is the proportion of units in stratum \(s\).

        **Key Assumption**: Within each stratum, treatment is effectively randomly assigned.

        **Advantages**: Intuitive, handles non-linear relationships, allows examination of effect heterogeneity.

        **Limitations**: Can only stratify on a few variables before encountering sparsity issues.
        """),
        kind="success"
    )

    # Display all method descriptions together
    mo.vstack([naive_description, regression_description, stratification_description])
    return (
        naive_description,
        regression_description,
        stratification_description,
    )


@app.cell(hide_code=True)
def _(
    LinearRegression,
    T_train,
    X_train_scaled,
    Y0_train,
    Y1_train,
    Y_train,
    mo,
    pd,
    plt,
):
    def _():
        # 1. Naive Mean Difference
        def naive_estimator(T, Y):
            """Calculate naive mean difference between treated and control outcomes"""
            treated_mean = Y[T == 1].mean()
            control_mean = Y[T == 0].mean()
            ate = treated_mean - control_mean
            return ate

        # Calculate naive ATE
        naive_ate = naive_estimator(T_train, Y_train)

        # Get true ATE for comparison
        true_ate = (Y1_train - Y0_train).mean()    

        def regression_adjustment(X, T, Y):
            """Estimate ATE using regression adjustment"""
            # Create a copy of X to avoid modifying the original
            X_with_treatment = X.copy()
            # Add treatment as a feature
            X_with_treatment['treatment'] = T

            # Fit linear regression model
            model = LinearRegression()
            model.fit(X_with_treatment, Y)

            # Extract treatment coefficient
            treatment_idx = X_with_treatment.columns.get_loc('treatment')
            ate = model.coef_[treatment_idx]

            return ate, model

        # Calculate regression-adjusted ATE
        reg_ate, reg_model = regression_adjustment(X_train_scaled, T_train, Y_train)

        # 3. Stratification on an important covariate
        def stratification(X, T, Y, stratify_var, n_strata=5):
            """Estimate ATE by stratifying on a variable"""
            # Create a copy of the data with relevant variables
            data = pd.DataFrame({
                'T': T,
                'Y': Y,
                'strat_var': X[stratify_var]
            })

            # Create equal-sized strata based on the stratification variable
            data['stratum'] = pd.qcut(data['strat_var'], n_strata, labels=False)

            # Calculate treatment effect within each stratum
            strata_effects = []
            strata_sizes = []

            for s in range(n_strata):
                stratum_data = data[data['stratum'] == s]
                # Only calculate if we have both treated and control units
                if (stratum_data['T'] == 1).sum() > 0 and (stratum_data['T'] == 0).sum() > 0:
                    stratum_treated = stratum_data[stratum_data['T'] == 1]['Y'].mean()
                    stratum_control = stratum_data[stratum_data['T'] == 0]['Y'].mean()
                    stratum_effect = stratum_treated - stratum_control
                    stratum_size = len(stratum_data)

                    strata_effects.append(stratum_effect)
                    strata_sizes.append(stratum_size)

            # Calculate weighted average (weighted by stratum size)
            total_size = sum(strata_sizes)
            weights = [size / total_size for size in strata_sizes]
            weighted_ate = sum(effect * weight for effect, weight in zip(strata_effects, weights))

            return weighted_ate, strata_effects, weights

        # Choose birth weight (x_0) as stratification variable
        strat_ate, strat_effects, strat_weights = stratification(X_train_scaled, T_train, Y_train, 'x_0')

        # Compile results
        methods = ['Naive Mean Difference', 'Regression Adjustment', 'Stratification']
        estimates = [naive_ate, reg_ate, strat_ate]
        biases = [est - true_ate for est in estimates]
        abs_biases = [abs(bias) for bias in biases]

        # Print results
        print("Simple Methods Results:")
        print(f"True ATE: {true_ate:.4f}")
        print("-" * 50)
        for method, estimate, bias in zip(methods, estimates, biases):
            print(f"{method}: ATE = {estimate:.4f}, Bias = {bias:.4f}")

        # Return all relevant objects for use in visualization
            # Create figure for comparing estimates from simple methods
        fig, axes = plt.subplots(1, 2, figsize=(14, 6))

        # Plot 1: Bar chart comparing ATE estimates
        bars = axes[0].bar(methods, estimates, color=['skyblue', 'lightgreen', 'salmon'])
        axes[0].axhline(y=true_ate, color='red', linestyle='--', label=f'True ATE = {true_ate:.4f}')
        axes[0].set_title('ATE Estimates from Simple Methods')
        axes[0].set_ylabel('ATE Estimate')
        axes[0].legend()

        # Add value labels to the bars
        for bar in bars:
            height = bar.get_height()
            axes[0].text(
                bar.get_x() + bar.get_width()/2., 
                height + 0.05,
                f'{height:.4f}',
                ha='center', va='bottom', 
                rotation=0
            )

        # Plot 2: Bar chart for bias
        biases_df = pd.DataFrame({
            'Method': methods,
            'Absolute Bias': abs_biases
        }).sort_values('Absolute Bias')

        bars = axes[1].barh(biases_df['Method'], biases_df['Absolute Bias'], color=['lightgreen', 'skyblue', 'salmon'])
        axes[1].set_title('Absolute Bias of Simple Methods')
        axes[1].set_xlabel('Absolute Bias')

        # Add value labels to the bars
        for bar in bars:
            width = bar.get_width()
            axes[1].text(
                width + 0.005, 
                bar.get_y() + bar.get_height()/2.,
                f'{width:.4f}',
                ha='left', va='center'
            )

        plt.tight_layout()

        # Create visualization for stratification results
        fig2, ax2 = plt.subplots(figsize=(10, 6))

        # Plot stratum-specific effects
        strata_indices = list(range(len(strat_effects)))
        ax2.bar(strata_indices, strat_effects, alpha=0.7)
        ax2.axhline(y=true_ate, color='red', linestyle='--', label=f'True ATE = {true_ate:.4f}')

        # Set labels and title
        ax2.set_title('Treatment Effects by Stratum')
        ax2.set_xlabel('Stratum (Birth Weight Quintile)')
        ax2.set_ylabel('Treatment Effect')
        ax2.set_xticks(strata_indices)
        ax2.set_xticklabels([f'Q{i+1}\n({w:.2f})' for i, w in enumerate(strat_weights)])
        ax2.legend()

        # Create layout containing both visualizations
        header = mo.md("#### Simple Methods Comparison")
        methods_comparison = mo.mpl.interactive(fig)

        strat_header = mo.md("#### Heterogeneous Effects by Birth Weight Stratum")
        strat_note = mo.md("*Note: Numbers in parentheses show the weight of each stratum in the overall estimate.*")
        strat_effects_plot = mo.mpl.interactive(fig2)

        methods_analysis = mo.callout(
            mo.md(f"""
            **Analysis of Simple Methods:**

            1. **Naive Mean Difference**: The naive estimate has a bias of {biases[0]:.4f}, which is {abs_biases[0]:.4f} in absolute terms. This is relatively {'small' if abs_biases[0] < 0.1 else 'moderate' if abs_biases[0] < 0.5 else 'large'}, suggesting that selection bias in this dataset may not be very strong.

            2. **Regression Adjustment**: This method has a bias of {biases[1]:.4f} (absolute: {abs_biases[1]:.4f}), {'improving upon' if abs_biases[1] < abs_biases[0] else 'performing worse than'} the naive estimator. This {'improvement' if abs_biases[1] < abs_biases[0] else 'decline'} in performance suggests that the linear model {'adequately' if abs_biases[1] < abs_biases[0] else 'inadequately'} captures the relationship between covariates and outcomes.

            3. **Stratification**: This approach has a bias of {biases[2]:.4f} (absolute: {abs_biases[2]:.4f}), {'outperforming' if abs_biases[2] < min(abs_biases[0], abs_biases[1]) else 'underperforming compared to'} the other methods. Stratification by birth weight reveals some heterogeneity in treatment effects across strata, which is valuable information for targeting interventions.

            Overall, the {'Regression Adjustment' if abs_biases[1] == min(abs_biases) else 'Naive Mean Difference' if abs_biases[0] == min(abs_biases) else 'Stratification'} method performs best in terms of bias reduction for this dataset. However, all methods show relatively small bias, suggesting that the selection mechanism in this semi-synthetic dataset may not induce strong confounding.
            """),
            kind="info"
        )

        # Combine all elements
        mo.output.replace(mo.vstack([
            header,
            methods_comparison,
            methods_analysis,
            strat_header,
            strat_effects_plot,
            strat_note
        ]))

    _()
    return


@app.cell(hide_code=True)
def _(mo):
    def _():
        section_header = mo.md("""### 6.2 Propensity Score Methods {#ps-methods}

        > 🎯 **Step 2**: Apply propensity score-based methods to adjust for confounding

        Building on the propensity scores we estimated earlier, we'll now implement methods that use these scores to create balance between treated and control groups.
        """)
        mo.output.replace(section_header)
    _()
    return


@app.cell(hide_code=True)
def _(mo):
    # Create a description of IPW approach
    ipw_description = mo.callout(
        mo.md(r"""
        #### Inverse Probability Weighting (IPW)

        IPW creates a pseudo-population where the confounding influence is eliminated by weighting each observation by the inverse of its probability of receiving the treatment it actually received:

        \[
        \hat{ATE}_{IPW} = \frac{1}{n} \sum_{i=1}^{n} \left( \frac{T_i Y_i}{e(X_i)} - \frac{(1-T_i) Y_i}{1-e(X_i)} \right)
        \]

        where \(e(X_i)\) is the propensity score for unit \(i\).

        **Key Advantages**:
        - Uses all data points
        - Simple to implement
        - Intuitive connection to survey sampling

        **Limitations**:
        - Sensitive to extreme propensity scores (near 0 or 1)
        - Can have high variance
        - Requires well-specified propensity model
        """),
        kind="info"
    )

    # Create a description of matching approach
    matching_description = mo.callout(
        mo.md(r"""
        #### Propensity Score Matching

        Matching pairs treated units with control units that have similar propensity scores. The average difference in outcomes between matched pairs provides an estimate of the ATE:

        \[
        \hat{ATE}_{match} = \frac{1}{n_1} \sum_{i:T_i=1} (Y_i - Y_{j(i)})
        \]

        where \(j(i)\) is the index of the control unit matched to treated unit \(i\).

        **Key Advantages**:
        - Intuitive and easy to explain
        - Can be combined with exact matching on key variables
        - Preserves the original outcome variable scale

        **Limitations**:
        - Discards units that cannot be matched
        - Choice of matching algorithm and caliper can affect results
        - Matches may not be perfect, leaving some residual confounding
        """),
        kind="warn"
    )

    # Create a description of stratification approach using propensity scores
    ps_stratification_description = mo.callout(
        mo.md(r"""
        #### Propensity Score Stratification

        This method divides the data into strata based on propensity scores, estimates treatment effects within each stratum, and computes a weighted average:

        \[
        \hat{ATE}_{strat} = \sum_{s=1}^{S} w_s (\bar{Y}_{s,1} - \bar{Y}_{s,0})
        \]

        where \(w_s\) is the proportion of units in stratum \(s\), and \(\bar{Y}_{s,1}\) and \(\bar{Y}_{s,0}\) are the average outcomes for treated and control units in that stratum.

        **Key Advantages**:
        - Uses all data points
        - Examines effect heterogeneity across propensity score strata
        - Usually reduces ~90% of confounding bias with just 5 strata

        **Limitations**:
        - Less precise than matching for estimating average effects
        - Choice of strata boundaries can affect results
        - May not fully eliminate confounding within strata
        """),
        kind="success"
    )

    # Display all method descriptions together
    mo.vstack([ipw_description, matching_description, ps_stratification_description])
    return ipw_description, matching_description, ps_stratification_description


@app.cell(hide_code=True)
def _(T_train, X_train_scaled, Y0_train, Y1_train, Y_train, np, pd):
    # Implement propensity score methods
    from sklearn.linear_model import LogisticRegression
    from sklearn.ensemble import RandomForestClassifier
    from sklearn.metrics import roc_auc_score, roc_curve

    # Estimate propensity scores using logistic regression
    propensity_model = LogisticRegression(max_iter=1000, C=1.0)
    propensity_model.fit(X_train_scaled, T_train)

    # Calculate propensity scores (probability of receiving treatment)
    propensity_scores = propensity_model.predict_proba(X_train_scaled)[:, 1]

    # Also estimate propensity scores using a Random Forest for comparison
    rf_propensity_model = RandomForestClassifier(n_estimators=100, min_samples_leaf=10, random_state=42)
    rf_propensity_model.fit(X_train_scaled, T_train)
    rf_propensity_scores = rf_propensity_model.predict_proba(X_train_scaled)[:, 1]

    # Create DataFrame with propensity scores
    ps_df = pd.DataFrame({
        'treatment': T_train,
        'ps_logistic': propensity_scores,
        'ps_rf': rf_propensity_scores
    })

    # Evaluate propensity score models
    logistic_auc = roc_auc_score(T_train, propensity_scores)
    rf_auc = roc_auc_score(T_train, rf_propensity_scores)

    print(f"Logistic Regression AUC: {logistic_auc:.4f}")
    print(f"Random Forest AUC: {rf_auc:.4f}")

    # 1. Implement Inverse Probability Weighting (IPW)
    # Calculate true ATE for comparison
    true_ate = (Y1_train - Y0_train).mean()

    # Function to calculate IPW estimate
    def ipw_estimator(T, Y, ps, stabilized=True, trimming=None):
        """Calculate ATE using inverse probability weighting"""
        # Calculate IPW weights
        if stabilized:
            # Stabilized weights
            p_treatment = T.mean()
            weights = np.where(T == 1, p_treatment / ps, (1 - p_treatment) / (1 - ps))
        else:
            # Unstabilized weights
            weights = np.where(T == 1, 1 / ps, 1 / (1 - ps))

        # Trim weights if requested
        if trimming is not None:
            max_weight = np.percentile(weights, trimming)
            weights = np.minimum(weights, max_weight)

        # Calculate weighted means
        weighted_treated = np.sum(weights[T == 1] * Y[T == 1]) / np.sum(weights[T == 1])
        weighted_control = np.sum(weights[T == 0] * Y[T == 0]) / np.sum(weights[T == 0])

        # Calculate ATE
        ate = weighted_treated - weighted_control

        return ate, weights

    # Calculate IPW estimates using different settings
    ipw_results = []

    for _ps_method, _ps_values in [('Logistic', propensity_scores), ('RF', rf_propensity_scores)]:
        for stabilized in [True, False]:
            for trimming in [None, 95]:
                # Calculate IPW estimate
                ipw_ate, weights = ipw_estimator(T_train, Y_train, _ps_values, 
                                               stabilized=stabilized, trimming=trimming)

                # Save result
                ipw_results.append({
                    'PS Method': _ps_method,
                    'Stabilized': stabilized,
                    'Trimming': trimming,
                    'ATE': ipw_ate,
                    'Bias': ipw_ate - true_ate,
                    'Abs Bias': abs(ipw_ate - true_ate),
                    'Max Weight': np.max(weights),
                    'Weight SD': np.std(weights)
                })

    # Convert to DataFrame for easier visualization
    ipw_results_df = pd.DataFrame(ipw_results)
    print("\nIPW Estimation Results:")
    print(ipw_results_df.sort_values('Abs Bias').head())

    # Find best IPW method
    best_ipw_idx = ipw_results_df['Abs Bias'].idxmin()
    best_ipw = ipw_results_df.loc[best_ipw_idx]
    best_ipw_method = f'IPW ({best_ipw["PS Method"]}, stabilized={best_ipw["Stabilized"]}, trimming={best_ipw["Trimming"]})'    

    # Next cells will implement matching and stratification methods
    return (
        LogisticRegression,
        RandomForestClassifier,
        best_ipw,
        best_ipw_idx,
        best_ipw_method,
        ipw_ate,
        ipw_estimator,
        ipw_results,
        ipw_results_df,
        logistic_auc,
        propensity_model,
        propensity_scores,
        ps_df,
        rf_auc,
        rf_propensity_model,
        rf_propensity_scores,
        roc_auc_score,
        roc_curve,
        stabilized,
        trimming,
        true_ate,
        weights,
    )


@app.cell(hide_code=True)
def _(
    T_train,
    Y_train,
    np,
    pd,
    propensity_scores,
    rf_propensity_scores,
    true_ate,
):
    # 2. Implement Propensity Score Matching
    from sklearn.neighbors import NearestNeighbors

    def ps_matching(T, Y, ps, method='nearest', k=1, caliper=None):
        """Calculate ATE using propensity score matching"""
        # Create a DataFrame with all necessary info
        data = pd.DataFrame({
            'treatment': T.values,
            'outcome': Y.values,
            'ps': ps
        })

        # Separate treated and control
        treated = data[data['treatment'] == 1]
        control = data[data['treatment'] == 0]

        # Reshape propensity scores for NearestNeighbors
        treated_ps = treated['ps'].values.reshape(-1, 1)
        control_ps = control['ps'].values.reshape(-1, 1)

        # Nearest neighbor matching
        nn = NearestNeighbors(n_neighbors=k)
        nn.fit(control_ps)
        distances, indices = nn.kneighbors(treated_ps)

        # For each treated unit, find its matches
        matched_pairs = []

        for i, treated_idx in enumerate(treated.index):
            for j in range(k):
                control_idx = control.index[indices[i, j]]
                dist = distances[i, j]

                # Apply caliper if specified
                if caliper is None or dist < caliper * np.std(data['ps']):
                    matched_pairs.append({
                        'treated_ps': treated.loc[treated_idx, 'ps'],
                        'control_ps': control.loc[control_idx, 'ps'],
                        'treated_outcome': treated.loc[treated_idx, 'outcome'],
                        'control_outcome': control.loc[control_idx, 'outcome'],
                        'ps_diff': abs(treated.loc[treated_idx, 'ps'] - control.loc[control_idx, 'ps'])
                    })

        # Create dataframe of matched pairs
        if len(matched_pairs) > 0:
            matched_df = pd.DataFrame(matched_pairs)

            # Calculate treatment effect
            ate = (matched_df['treated_outcome'] - matched_df['control_outcome']).mean()

            return ate, matched_df
        else:
            print("No matches found with current settings")
            return np.nan, None

    # Apply matching with different settings
    matching_results = []

    for _ps_method, _ps_values in [('Logistic', propensity_scores), ('RF', rf_propensity_scores)]:
        for k in [1, 5]:
            for caliper in [None, 0.2]:
                # Skip multiple neighbors with no caliper
                if k > 1 and caliper is None:
                    continue

                # Calculate matching estimate
                psm_ate, matched_data = ps_matching(T_train, Y_train, _ps_values, 
                                                  method='nearest', k=k, caliper=caliper)

                if not np.isnan(psm_ate) and matched_data is not None:
                    # Save result
                    matching_results.append({
                        'PS Method': _ps_method,
                        'k': k,
                        'Caliper': caliper,
                        'ATE': psm_ate,
                        'Bias': psm_ate - true_ate,
                        'Abs Bias': abs(psm_ate - true_ate),
                        'Matches': len(matched_data),
                        'Matched Data': matched_data
                    })

    # Convert to DataFrame for easier visualization
    matching_results_df = pd.DataFrame([
        {k: v for k, v in result.items() if k != 'Matched Data'} for result in matching_results
    ])

    print("\nPropensity Score Matching Results:")
    print(matching_results_df.sort_values('Abs Bias').head())

    # Find best matching method
    if not matching_results_df.empty:
        best_match_idx = matching_results_df['Abs Bias'].idxmin()
        best_match = matching_results_df.loc[best_match_idx]
        best_match_method = f"Matching ({best_match['PS Method']}, k={best_match['k']}, caliper={best_match['Caliper']})"

        # Get matched data for visualization
        best_matched_data = matching_results[best_match_idx]['Matched Data']
    else:
        best_match = None
        best_match_method = None
        best_matched_data = None
    return (
        NearestNeighbors,
        best_match,
        best_match_idx,
        best_match_method,
        best_matched_data,
        caliper,
        k,
        matched_data,
        matching_results,
        matching_results_df,
        ps_matching,
        psm_ate,
    )


@app.cell(hide_code=True)
def _(
    T_train,
    Y_train,
    best_ipw,
    best_ipw_method,
    best_match,
    best_match_method,
    mo,
    np,
    pd,
    plt,
    propensity_scores,
    rf_propensity_scores,
    true_ate,
):
    # 3. Implement Propensity Score Stratification

    def ps_stratification(T, Y, ps, n_strata=5):
        """Calculate ATE using propensity score stratification"""
        # Create a DataFrame with all necessary variables
        data = pd.DataFrame({
            'treatment': T.values,
            'outcome': Y.values,
            'ps': ps
        })

        # Create strata based on propensity scores
        data['stratum'] = pd.qcut(data['ps'], n_strata, labels=False)

        # Calculate treatment effect within each stratum
        stratum_effects = []
        stratum_sizes = []
        stratum_treated_counts = []
        stratum_control_counts = []

        for stratum in range(n_strata):
            stratum_data = data[data['stratum'] == stratum]

            # Check if both treated and control units exist in this stratum
            treated_count = (stratum_data['treatment'] == 1).sum()
            control_count = (stratum_data['treatment'] == 0).sum()

            if treated_count > 0 and control_count > 0:
                # Calculate treatment effect
                treated_mean = stratum_data.loc[stratum_data['treatment'] == 1, 'outcome'].mean()
                control_mean = stratum_data.loc[stratum_data['treatment'] == 0, 'outcome'].mean()
                effect = treated_mean - control_mean

                # Save effect and size
                stratum_effects.append(effect)
                stratum_sizes.append(len(stratum_data))
                stratum_treated_counts.append(treated_count)
                stratum_control_counts.append(control_count)
            else:
                print(f"Stratum {stratum} does not have both treated and control units.")

        # Calculate weighted average of stratum-specific effects
        if len(stratum_effects) > 0:
            weights = np.array(stratum_sizes) / sum(stratum_sizes)
            ate = sum(weights * np.array(stratum_effects))
            return ate, stratum_effects, stratum_sizes, stratum_treated_counts, stratum_control_counts
        else:
            return np.nan, [], [], [], []

    # Apply stratification with different propensity score models and strata numbers
    strat_results = []

    for _ps_method, _ps_values in [('Logistic', propensity_scores), ('RF', rf_propensity_scores)]:
        for n_strata in [5, 10]:
            # Calculate stratification estimate
            strat_ate, stratum_effects, stratum_sizes, treated_counts, control_counts = \
                ps_stratification(T_train, Y_train, _ps_values, n_strata)

            if not np.isnan(strat_ate):
                # Save result
                strat_results.append({
                    'PS Method': _ps_method,
                    'n_strata': n_strata,
                    'ATE': strat_ate,
                    'Bias': strat_ate - true_ate,
                    'Abs Bias': abs(strat_ate - true_ate),
                    'Stratum Effects': stratum_effects,
                    'Stratum Sizes': stratum_sizes,
                    'Treated Counts': treated_counts,
                    'Control Counts': control_counts
                })

    # Convert to DataFrame for easier visualization
    strat_results_df = pd.DataFrame([
        {k: v for k, v in result.items() if k not in ['Stratum Effects', 'Stratum Sizes', 
                                                   'Treated Counts', 'Control Counts']} 
        for result in strat_results
    ])

    print("\nPropensity Score Stratification Results:")
    print(strat_results_df.sort_values('Abs Bias'))

    # Find best stratification method
    if not strat_results_df.empty:
        best_strat_idx = strat_results_df['Abs Bias'].idxmin()
        best_strat = strat_results_df.loc[best_strat_idx]
        best_strat_method = f"Stratification ({best_strat['PS Method']}, n_strata={best_strat['n_strata']})"

        # Extract details for visualization
        best_strat_effects = strat_results[best_strat_idx]['Stratum Effects']
        best_strat_sizes = strat_results[best_strat_idx]['Stratum Sizes'] 
    else:
        best_strat = None
        best_strat_method = None
        best_strat_effects = None
        best_strat_sizes = None

    # Create strata effects visualization
    if best_strat_effects is not None:
        strat_fig, ax = plt.subplots(figsize=(10, 6))
        strata_indices = list(range(len(best_strat_effects)))
        ax.bar(strata_indices, best_strat_effects, alpha=0.7)
        ax.axhline(y=best_strat['ATE'], color='red', linestyle='--', 
                  label=f'Overall ATE: {best_strat["ATE"]:.4f}')
        ax.axhline(y=true_ate, color='green', linestyle=':', 
                  label=f'True ATE: {true_ate:.4f}')
        ax.set_title('Treatment Effects by Propensity Score Stratum')
        ax.set_xlabel('Propensity Score Stratum (low to high)')
        ax.set_ylabel('Stratum-Specific ATE')
        ax.set_xticks(strata_indices)
        ax.legend()
        strat_plot = mo.mpl.interactive(strat_fig)
    else:
        strat_plot = None

    # Compare all propensity score methods
    ps_methods = []

    # Add best methods from each category
    ps_methods.append({
        'Method': best_ipw_method,
        'ATE': best_ipw['ATE'],
        'Bias': best_ipw['Bias'],
        'Abs Bias': best_ipw['Abs Bias'],
        'Type': 'IPW'
    })

    if best_match is not None:
        ps_methods.append({
            'Method': best_match_method,
            'ATE': best_match['ATE'],
            'Bias': best_match['Bias'],
            'Abs Bias': best_match['Abs Bias'],
            'Type': 'Matching'
        })

    if best_strat is not None:
        ps_methods.append({
            'Method': best_strat_method,
            'ATE': best_strat['ATE'],
            'Bias': best_strat['Bias'],
            'Abs Bias': best_strat['Abs Bias'],
            'Type': 'Stratification'
        })

    # Convert to DataFrame and sort by absolute bias
    ps_methods_df = pd.DataFrame(ps_methods)
    ps_methods_df = ps_methods_df.sort_values('Abs Bias')

    print("\nComparison of Best Propensity Score Methods:")
    print(ps_methods_df)

    # Create comparison visualization
    comp_fig, comp_ax = plt.subplots(figsize=(10, 6))

    # Plot bars
    colors = {'IPW': 'skyblue', 'Matching': 'lightgreen', 'Stratification': 'salmon'}
    for i, (idx, row) in enumerate(ps_methods_df.iterrows()):
        comp_ax.barh(i, row['ATE'], color=colors[row['Type']], label=row['Type'] if i == 0 else "")

    # Add method names and reference line
    comp_ax.set_yticks(range(len(ps_methods_df)))
    comp_ax.set_yticklabels(ps_methods_df['Method'])
    comp_ax.axvline(x=true_ate, color='red', linestyle='--', label=f'True ATE = {true_ate:.4f}')

    # Add legend and labels
    handles, labels = comp_ax.get_legend_handles_labels()
    by_label = dict(zip(labels, handles))
    comp_ax.legend(by_label.values(), by_label.keys(), loc='lower right')

    comp_ax.set_title('Comparison of Best Propensity Score Methods')
    comp_ax.set_xlabel('ATE Estimate')
    comp_ax.grid(True, alpha=0.3)

    # Create interactive plot for marimo
    comparison_plot = mo.mpl.interactive(comp_fig)
    return (
        ax,
        best_strat,
        best_strat_effects,
        best_strat_idx,
        best_strat_method,
        best_strat_sizes,
        by_label,
        colors,
        comp_ax,
        comp_fig,
        comparison_plot,
        control_counts,
        handles,
        i,
        idx,
        labels,
        n_strata,
        ps_methods,
        ps_methods_df,
        ps_stratification,
        row,
        strat_ate,
        strat_fig,
        strat_plot,
        strat_results,
        strat_results_df,
        strata_indices,
        stratum_effects,
        stratum_sizes,
        treated_counts,
    )


@app.cell(hide_code=True)
def _(comparison_plot, mo, ps_methods_df, strat_plot, true_ate):
    # Display results of Propensity Score Methods
    def _():
        # Create header for the section
        header = mo.md("#### Comparison of Propensity Score Methods")

        # Create explanation text
        explanation = mo.md("""
        We've implemented and compared three propensity score-based causal inference methods:

        1. **Inverse Probability Weighting (IPW)**: Weights observations inversely to their probability of receiving the treatment to create balance.
        2. **Propensity Score Matching**: Pairs treated units with similar control units based on propensity scores.
        3. **Propensity Score Stratification**: Divides the sample into strata based on propensity scores and calculates treatment effects within each stratum.

        Each method has different strengths and weaknesses. The comparison below shows their performance in estimating the Average Treatment Effect (ATE).
        """)

        # Create results summary
        best_method_idx = ps_methods_df['Abs Bias'].idxmin()
        best_method = ps_methods_df.loc[best_method_idx]

        summary = mo.callout(
            mo.md(f"""
            **Best Method: {best_method['Method']}**

            - Estimated ATE: {best_method['ATE']:.4f}
            - True ATE: {true_ate:.4f}
            - Absolute Bias: {best_method['Abs Bias']:.4f}

            This analysis shows that propensity score methods can effectively reduce bias in causal estimates from observational data.
            """),
            kind="success"
        )

        # Create table with results
        results_table = mo.ui.table(ps_methods_df.reset_index(drop=True))

        # Display comparison plot
        plot_header = mo.md("#### Visual Comparison of Methods")

        # Display stratification plot if available
        if strat_plot is not None:
            strat_header = mo.md("#### Treatment Effects by Propensity Score Stratum")
            strat_explanation = mo.md("""
            This plot shows how treatment effects vary across different propensity score strata. 
            Heterogeneity in these effects may indicate effect modification by variables related to treatment assignment.
            """)
            strat_section = mo.vstack([strat_header, strat_explanation, strat_plot])
        else:
            strat_section = mo.md("")

        # Combine all components
        components = [header, explanation, summary, results_table, plot_header, comparison_plot]
        if strat_plot is not None:
            components.append(strat_section)

        # Display all components
        mo.output.replace(mo.vstack(components))

    _()
    return


@app.cell(hide_code=True)
def _(mo):
    def _():
        section_header = mo.md("""### 6.3 Advanced Machine Learning Methods {#ml-methods}

        > 🚀 **Step 3**: Leverage machine learning techniques for improved causal inference

        Finally, we'll explore advanced methods that combine machine learning with causal inference principles to estimate treatment effects more accurately. These methods can capture complex non-linear relationships and interactions between variables without requiring strong parametric assumptions.
        """)
        mo.output.replace(section_header)
    _()
    return


@app.cell(hide_code=True)
def _(mo):
    def _():
        subsection_header = mo.md("""#### 6.3.1 Meta-Learners for Causal Inference {#meta-learners}

        Meta-learners are a class of methods that use machine learning algorithms to estimate causal effects by combining multiple prediction models in different ways. Unlike traditional methods, meta-learners can capture complex, non-linear relationships between variables without requiring explicit parametric assumptions.
        """)
        mo.output.replace(subsection_header)
    _()
    return


@app.cell(hide_code=True)
def _(mo):
    s_learner_desc = mo.callout(
        mo.md(r"""
        #### S-Learner (Single Model)

        The S-Learner (Single model) uses a single machine learning model with the treatment indicator included as a regular feature:

        1. **Train a model** to predict outcome using both covariates and treatment: 
           $$\hat{\mu}(x, t) = E[Y | X=x, T=t]$$

        2. **Estimate treatment effects** by taking the difference in predictions for treated vs. untreated:
           $$\hat{\tau}(x) = \hat{\mu}(x, 1) - \hat{\mu}(x, 0)$$

        **Advantages**: Simple to implement, requires only one model

        **Limitations**: May underestimate treatment effects if treatment assignment is highly imbalanced
        """),
        kind="info"
    )

    t_learner_desc = mo.callout(
        mo.md(r"""
        #### T-Learner (Two Models)

        The T-Learner (Two models) fits separate models for the treated and control groups:

        1. **Train two separate models**:
           - Control model: $$\hat{\mu}_0(x) = E[Y | X=x, T=0]$$
           - Treatment model: $$\hat{\mu}_1(x) = E[Y | X=x, T=1]$$

        2. **Estimate treatment effects** by taking the difference in predictions:
           $$\hat{\tau}(x) = \hat{\mu}_1(x) - \hat{\mu}_0(x)$$

        **Advantages**: Can capture heterogeneous response surfaces, doesn't impose shared structure

        **Limitations**: May suffer from high variance in regions with few samples from either group
        """),
        kind="warn"
    )

    x_learner_desc = mo.callout(
        mo.md(r"""
        #### X-Learner

        The X-Learner extends the T-Learner with a more sophisticated approach:

        1. **Train response surface models** (same as T-Learner):
           - Control model: $$\hat{\mu}_0(x) = E[Y | X=x, T=0]$$
           - Treatment model: $$\hat{\mu}_1(x) = E[Y | X=x, T=1]$$

        2. **Impute individual treatment effects** for each unit:
           - For treated units: $$D_i^1 = Y_i(1) - \hat{\mu}_0(X_i)$$
           - For control units: $$D_i^0 = \hat{\mu}_1(X_i) - Y_i(0)$$

        3. **Train two treatment effect models**:
           - Using treated units: $$\hat{\tau}_1(x) = E[D_i^1 | X_i=x]$$
           - Using control units: $$\hat{\tau}_0(x) = E[D_i^0 | X_i=x]$$

        4. **Combine the two estimates** using a weighting function g(x):
           $$\hat{\tau}(x) = g(x)\hat{\tau}_0(x) + (1-g(x))\hat{\tau}_1(x)$$
           where g(x) can be the propensity score.

        **Advantages**: Performs well with heterogeneous treatment effects and imbalanced treatment groups

        **Limitations**: More complex, requires estimating propensity scores
        """),
        kind="success"
    )

    # Stack all descriptions
    mo.vstack([
        mo.md("Meta-learners use machine learning algorithms to estimate causal effects. Here are the three main types:"),
        s_learner_desc,
        t_learner_desc,
        x_learner_desc
    ])
    return s_learner_desc, t_learner_desc, x_learner_desc


@app.cell(hide_code=True)
def _(T_train, X_train_scaled, Y0_train, Y1_train, Y_train, mo, np, pd, plt):
    def _():
        # Import required ML libraries
        from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
        from sklearn.linear_model import LogisticRegression
        from sklearn.metrics import mean_squared_error

        # S-Learner implementation
        def s_learner(X, T, Y, X_test=None, model=None):
            """
            Estimate treatment effects using S-Learner

            Parameters:
            -----------
            X : DataFrame of covariates
            T : Series of treatment assignments
            Y : Series of outcomes
            X_test : DataFrame of test covariates or None
            model : Fitted sklearn model or None

            Returns:
            --------
            ate : Estimated average treatment effect
            cate : Estimated conditional average treatment effects
            model : Fitted model
            """
            # Default model
            if model is None:
                model = RandomForestRegressor(n_estimators=100, min_samples_leaf=5, random_state=42)

            # Create combined dataset
            X_combined = X.copy()
            X_combined['treatment'] = T

            # Fit the model
            model.fit(X_combined, Y)

            # Predict on test set if provided, otherwise on training set
            if X_test is not None:
                X_pred = X_test
            else:
                X_pred = X

            # Create counterfactual datasets
            X_pred_1 = X_pred.copy()
            X_pred_1['treatment'] = 1

            X_pred_0 = X_pred.copy()
            X_pred_0['treatment'] = 0

            # Predict potential outcomes
            y_pred_1 = model.predict(X_pred_1)
            y_pred_0 = model.predict(X_pred_0)

            # Calculate treatment effects
            cate = y_pred_1 - y_pred_0
            ate = cate.mean()

            return ate, cate, model

        # T-Learner implementation
        def t_learner(X, T, Y, X_test=None, model_t=None, model_c=None):
            """
            Estimate treatment effects using T-Learner

            Parameters:
            -----------
            X : DataFrame of covariates
            T : Series of treatment assignments
            Y : Series of outcomes
            X_test : DataFrame of test covariates or None
            model_t : Sklearn model for treated group or None
            model_c : Sklearn model for control group or None

            Returns:
            --------
            ate : Estimated average treatment effect
            cate : Estimated conditional average treatment effects
            models : Tuple of (treatment_model, control_model)
            """
            # Default models
            if model_t is None:
                model_t = RandomForestRegressor(n_estimators=100, min_samples_leaf=5, random_state=42)
            if model_c is None:
                model_c = RandomForestRegressor(n_estimators=100, min_samples_leaf=5, random_state=43)

            # Split data into treated and control groups
            X_t = X[T == 1]
            Y_t = Y[T == 1]
            X_c = X[T == 0]
            Y_c = Y[T == 0]

            # Fit models
            model_t.fit(X_t, Y_t)
            model_c.fit(X_c, Y_c)

            # Predict on test set if provided, otherwise on training set
            if X_test is not None:
                X_pred = X_test
            else:
                X_pred = X

            # Predict potential outcomes
            y_pred_1 = model_t.predict(X_pred)
            y_pred_0 = model_c.predict(X_pred)

            # Calculate treatment effects
            cate = y_pred_1 - y_pred_0
            ate = cate.mean()

            return ate, cate, (model_t, model_c)

        # X-Learner implementation
        def x_learner(X, T, Y, X_test=None, models_t=None, models_c=None, propensity_model=None):
            """
            Estimate treatment effects using X-Learner

            Parameters:
            -----------
            X : DataFrame of covariates
            T : Series of treatment assignments
            Y : Series of outcomes
            X_test : DataFrame of test covariates or None
            models_t : List of two Sklearn models for treated group or None
            models_c : List of two Sklearn models for control group or None
            propensity_model : Sklearn classifier for propensity scores or None

            Returns:
            --------
            ate : Estimated average treatment effect
            cate : Estimated conditional average treatment effects
            models : Tuple of (models_t, models_c, propensity_model)
            """
            # Default models
            if models_t is None:
                models_t = [
                    RandomForestRegressor(n_estimators=100, min_samples_leaf=5, random_state=42),
                    RandomForestRegressor(n_estimators=100, min_samples_leaf=5, random_state=43)
                ]
            if models_c is None:
                models_c = [
                    RandomForestRegressor(n_estimators=100, min_samples_leaf=5, random_state=44),
                    RandomForestRegressor(n_estimators=100, min_samples_leaf=5, random_state=45)
                ]
            if propensity_model is None:
                propensity_model = LogisticRegression(max_iter=1000)

            # Split data into treated and control groups
            X_t = X[T == 1]
            Y_t = Y[T == 1]
            X_c = X[T == 0]
            Y_c = Y[T == 0]

            # Step 1: Estimate the response surfaces
            model_t1, model_c1 = models_t[0], models_c[0]
            model_t1.fit(X_t, Y_t)
            model_c1.fit(X_c, Y_c)

            # Predict responses for all units
            mu_t = model_t1.predict(X)
            mu_c = model_c1.predict(X)

            # Step 2: Compute the imputed treatment effects
            D_t = Y_t.values - model_c1.predict(X_t)  # Imputed effect for treated units
            D_c = model_t1.predict(X_c) - Y_c.values  # Imputed effect for control units

            # Step 3: Estimate the CATE functions
            model_t2, model_c2 = models_t[1], models_c[1]
            model_t2.fit(X_t, D_t)
            model_c2.fit(X_c, D_c)

            # Step 4: Combine the CATE functions using propensity scores
            propensity_model.fit(X, T)
            g = propensity_model.predict_proba(X)[:, 1]  # Propensity scores

            # Predict on test set if provided, otherwise on training set
            if X_test is not None:
                X_pred = X_test
                g_pred = propensity_model.predict_proba(X_pred)[:, 1]
            else:
                X_pred = X
                g_pred = g

            # Predict treatment effects
            tau_t = model_t2.predict(X_pred)
            tau_c = model_c2.predict(X_pred)

            # Weighted average of treatment effects
            cate = g_pred * tau_c + (1 - g_pred) * tau_t
            ate = cate.mean()

            return ate, cate, (models_t, models_c, propensity_model)

        # Compare meta-learners
        np.random.seed(42)  # Set seed for reproducibility

        # Initialize results list
        meta_learner_results = []

        # True ATE for comparison
        true_ate = (Y1_train - Y0_train).mean()

        # S-Learner with different base models
        for model_name, model in [
            ('Random Forest', RandomForestRegressor(n_estimators=100, min_samples_leaf=5, random_state=42)),
            ('Gradient Boosting', GradientBoostingRegressor(n_estimators=100, max_depth=3, random_state=42))
        ]:
            # Train S-Learner
            s_ate, s_cate, _ = s_learner(X_train_scaled, T_train, Y_train, model=model)

            # Save results
            meta_learner_results.append({
                'Method': f'S-Learner ({model_name})',
                'ATE': s_ate,
                'Bias': s_ate - true_ate,
                'Abs Bias': abs(s_ate - true_ate)
            })

        # T-Learner with different base models
        for model_name, model_t, model_c in [
            ('Random Forest', 
             RandomForestRegressor(n_estimators=100, min_samples_leaf=5, random_state=42),
             RandomForestRegressor(n_estimators=100, min_samples_leaf=5, random_state=43)),
            ('Gradient Boosting', 
             GradientBoostingRegressor(n_estimators=100, max_depth=3, random_state=42),
             GradientBoostingRegressor(n_estimators=100, max_depth=3, random_state=43))
        ]:
            # Train T-Learner
            t_ate, t_cate, _ = t_learner(X_train_scaled, T_train, Y_train, model_t=model_t, model_c=model_c)

            # Save results
            meta_learner_results.append({
                'Method': f'T-Learner ({model_name})',
                'ATE': t_ate,
                'Bias': t_ate - true_ate,
                'Abs Bias': abs(t_ate - true_ate)
            })

        # X-Learner with different base models
        for model_name, models_t, models_c, prop_model in [
            ('Random Forest', 
             [RandomForestRegressor(n_estimators=100, min_samples_leaf=5, random_state=42),
              RandomForestRegressor(n_estimators=100, min_samples_leaf=5, random_state=43)],
             [RandomForestRegressor(n_estimators=100, min_samples_leaf=5, random_state=44),
              RandomForestRegressor(n_estimators=100, min_samples_leaf=5, random_state=45)],
             LogisticRegression(max_iter=1000)),
            ('Gradient Boosting', 
             [GradientBoostingRegressor(n_estimators=100, max_depth=3, random_state=42),
              GradientBoostingRegressor(n_estimators=100, max_depth=3, random_state=43)],
             [GradientBoostingRegressor(n_estimators=100, max_depth=3, random_state=44),
              GradientBoostingRegressor(n_estimators=100, max_depth=3, random_state=45)],
             LogisticRegression(max_iter=1000))
        ]:
            # Train X-Learner
            x_ate, x_cate, _ = x_learner(X_train_scaled, T_train, Y_train, 
                                        models_t=models_t, models_c=models_c, 
                                        propensity_model=prop_model)

            # Save results
            meta_learner_results.append({
                'Method': f'X-Learner ({model_name})',
                'ATE': x_ate,
                'Bias': x_ate - true_ate,
                'Abs Bias': abs(x_ate - true_ate)
            })

        # Convert to DataFrame and sort by absolute bias
        meta_learner_df = pd.DataFrame(meta_learner_results)
        meta_learner_df = meta_learner_df.sort_values('Abs Bias')

        # Compare meta-learners - show results
        header = mo.md("#### Meta-Learner Results")
        table = mo.ui.table(meta_learner_df)

        # Visualize comparison
        fig, ax = plt.subplots(figsize=(12, 8))
        ax.barh(y=meta_learner_df['Method'], width=meta_learner_df['ATE'], color='skyblue')
        ax.axvline(x=true_ate, color='red', linestyle='--', label=f'True ATE = {true_ate:.4f}')
        ax.set_title('Comparison of ATE Estimates from Meta-Learners')
        ax.set_xlabel('ATE Estimate')
        ax.set_ylabel('Method')
        ax.grid(True, alpha=0.3)
        ax.legend()
        plt.tight_layout()

        # Create interactive plot
        plot = mo.mpl.interactive(fig)

        # Select the best meta-learner method
        best_ml_idx = meta_learner_df['Abs Bias'].idxmin()
        best_ml = meta_learner_df.loc[best_ml_idx]

        # Create summary of best method
        best_method_summary = mo.callout(
            mo.md(f"""
            **Best Meta-Learner Method:**

            - **Method**: {best_ml['Method']}
            - **ATE Estimate**: {best_ml['ATE']:.4f}
            - **True ATE**: {true_ate:.4f}
            - **Bias**: {best_ml['Bias']:.4f}

            This analysis shows that meta-learners can provide accurate estimates of causal effects by leveraging machine learning algorithms.
            """),
            kind="success"
        )

        # Plot treatment effect heterogeneity
        # Get CATE estimates from X-Learner with Random Forest
        _, x_cate, _ = x_learner(
            X_train_scaled, T_train, Y_train,
            models_t=[RandomForestRegressor(n_estimators=100, min_samples_leaf=5, random_state=42),
                     RandomForestRegressor(n_estimators=100, min_samples_leaf=5, random_state=43)],
            models_c=[RandomForestRegressor(n_estimators=100, min_samples_leaf=5, random_state=44),
                     RandomForestRegressor(n_estimators=100, min_samples_leaf=5, random_state=45)],
            propensity_model=LogisticRegression(max_iter=1000)
        )

        # Plot CATE distribution
        fig2, ax2 = plt.subplots(figsize=(10, 6))
        ax2.hist(x_cate, bins=30, color='skyblue', alpha=0.7)
        ax2.axvline(x=x_cate.mean(), color='red', linestyle='--', 
                   label=f'Mean CATE = {x_cate.mean():.4f}')
        ax2.axvline(x=true_ate, color='green', linestyle=':', 
                   label=f'True ATE = {true_ate:.4f}')
        ax2.set_title('Distribution of Conditional Average Treatment Effects (CATE)')
        ax2.set_xlabel('CATE')
        ax2.set_ylabel('Frequency')
        ax2.legend()
        ax2.grid(True, alpha=0.3)
        plt.tight_layout()

        cate_plot = mo.mpl.interactive(fig2)
        cate_explanation = mo.md("""**Treatment Effect Heterogeneity**: The distribution above shows how treatment effects vary across different individuals. This variation suggests that the intervention may be more effective for some subgroups than others.""")

        # Combine all elements in the output
        mo.output.replace(mo.vstack([
            header,
            table,
            plot,
            best_method_summary,
            mo.md("#### Treatment Effect Heterogeneity"),
            cate_plot,
            cate_explanation
        ]))
    _()
    return


@app.cell(hide_code=True)
def _(mo):
    def _():
        subsection_header = mo.md("""#### 6.3.2 Doubly Robust Methods {#doubly-robust}

        Doubly robust methods combine outcome modeling and propensity score approaches to provide protection against misspecification of either model. This "double robustness" property makes these methods particularly attractive for causal inference in complex settings.
        """)
        mo.output.replace(subsection_header)
    _()
    return


@app.cell(hide_code=True)
def _(mo):
    # Create descriptions of doubly robust methods
    aipw_desc = mo.callout(
        mo.md(r"""
        #### Augmented Inverse Probability Weighting (AIPW)

        AIPW combines outcome regression and IPW by using both models to create a doubly robust estimator:

        The AIPW estimator can be written as:

        \[ \hat{\tau}_{AIPW} = \frac{1}{n} \sum_{i=1}^n \left( \hat{\mu}_1(X_i) - \hat{\mu}_0(X_i) + \frac{T_i(Y_i - \hat{\mu}_1(X_i))}{\hat{e}(X_i)} - \frac{(1-T_i)(Y_i - \hat{\mu}_0(X_i))}{1-\hat{e}(X_i)} \right) \]

        where:
        - \(\hat{\mu}_1(X_i)\) and \(\hat{\mu}_0(X_i)\) are outcome models for treated and control
        - \(\hat{e}(X_i)\) is the propensity score model

        **Key property**: Consistent if *either* the outcome model *or* the propensity score model is correctly specified (not necessarily both)

        **Advantages**: More robust to model misspecification, often lower variance than IPW
        """),
        kind="info"
    )

    dml_desc = mo.callout(
        mo.md(r"""
        #### Double Machine Learning (DML)

        DML addresses issues of regularization bias and overfitting in high-dimensional settings:

        1. **Cross-fitting approach**:
           - Split the data into K folds
           - For each fold, fit models on the other K-1 folds and predict on the held-out fold
           - This reduces the impact of overfitting

        2. **Orthogonalization**:
           - Remove the dependence between treatment and covariates
           - Remove the dependence between outcome and covariates
           - Study the residual relationship

        DML can be implemented as:

        \[ \hat{\tau}_{DML} = \frac{\frac{1}{n}\sum_{i=1}^n (T_i - \hat{e}(X_i))(Y_i - \hat{m}(X_i))}{\frac{1}{n}\sum_{i=1}^n (T_i - \hat{e}(X_i))^2} \]

        where \(\hat{m}(X_i)\) is a model for the outcome and \(\hat{e}(X_i)\) is the propensity score model.

        **Advantages**: Handles high-dimensional settings well, allows complex ML models, reduces regularization bias
        """),
        kind="warn"
    )

    # Stack all descriptions
    mo.vstack([
        mo.md("Doubly robust methods offer protection against model misspecification by combining outcome modeling and propensity score approaches:"),
        aipw_desc,
        dml_desc
    ])
    return aipw_desc, dml_desc


@app.cell(hide_code=True)
def _(T_train, X_train_scaled, Y0_train, Y1_train, Y_train, mo, np, pd, plt):
    def _():
        # Import required libraries
        from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier, GradientBoostingRegressor
        from sklearn.linear_model import LogisticRegression
        from sklearn.model_selection import KFold

        # Implement Augmented Inverse Probability Weighting (AIPW)
        def doubly_robust_aipw(X, T, Y, outcome_model=None, propensity_model=None):
            """
            Estimate ATE using Augmented Inverse Probability Weighting (AIPW)

            Parameters:
            -----------
            X : DataFrame of covariates
            T : Series of treatment assignments
            Y : Series of outcomes
            outcome_model : sklearn regressor or None
            propensity_model : sklearn classifier or None

            Returns:
            --------
            ate : Estimated average treatment effect
            """
            from sklearn.base import clone

            # Default models
            if outcome_model is None:
                outcome_model = RandomForestRegressor(n_estimators=100, min_samples_leaf=5, random_state=42)
            if propensity_model is None:
                propensity_model = LogisticRegression(max_iter=1000)

            # Split data by treatment group
            X_t = X[T == 1]
            Y_t = Y[T == 1]
            X_c = X[T == 0]
            Y_c = Y[T == 0]

            # Fit outcome models for each treatment group
            model_t = clone(outcome_model)
            model_c = clone(outcome_model)
            model_t.fit(X_t, Y_t)
            model_c.fit(X_c, Y_c)

            # Predict potential outcomes for all units
            mu_1 = model_t.predict(X)
            mu_0 = model_c.predict(X)

            # Fit propensity score model
            ps_model = clone(propensity_model)
            ps_model.fit(X, T)
            ps = ps_model.predict_proba(X)[:, 1]

            # Handle extreme propensity scores
            eps = 1e-12
            ps = np.maximum(eps, np.minimum(1 - eps, ps))

            # Calculate AIPW estimator
            aipw_0 = mu_0 + (1 - T) * (Y - mu_0) / (1 - ps)
            aipw_1 = mu_1 + T * (Y - mu_1) / ps

            # Calculate ATE
            ate = (aipw_1 - aipw_0).mean()

            return ate

        # Implement Double Machine Learning (DML)
        def double_machine_learning(X, T, Y, outcome_model=None, propensity_model=None, n_splits=5):
            """
            Estimate ATE using Double Machine Learning with cross-fitting

            Parameters:
            -----------
            X : DataFrame of covariates
            T : Series of treatment assignments
            Y : Series of outcomes
            outcome_model : sklearn regressor or None
            propensity_model : sklearn classifier or None
            n_splits : int, number of folds for cross-fitting

            Returns:
            --------
            ate : Estimated average treatment effect
            """
            from sklearn.base import clone

            # Default models
            if outcome_model is None:
                outcome_model = RandomForestRegressor(n_estimators=100, min_samples_leaf=5, random_state=42)
            if propensity_model is None:
                propensity_model = LogisticRegression(max_iter=1000)

            # Initialize arrays for predictions
            n = len(Y)
            Y_hat = np.zeros(n)
            T_hat = np.zeros(n)

            # Set up cross-fitting
            kf = KFold(n_splits=n_splits, shuffle=True, random_state=42)

            # Perform cross-fitting
            for train_idx, test_idx in kf.split(X):
                # Get train and test data
                X_train = X.iloc[train_idx]
                X_test = X.iloc[test_idx]
                T_train_fold = T.iloc[train_idx]
                T_test = T.iloc[test_idx]
                Y_train_fold = Y.iloc[train_idx]

                # Fit and predict with outcome model
                m_model = clone(outcome_model)
                m_model.fit(X_train, Y_train_fold)
                Y_hat[test_idx] = m_model.predict(X_test)

                # Fit and predict with propensity model
                e_model = clone(propensity_model)
                e_model.fit(X_train, T_train_fold)
                T_hat[test_idx] = e_model.predict_proba(X_test)[:, 1]

            # Calculate residuals
            Y_resid = Y - Y_hat
            T_resid = T - T_hat

            # Estimate treatment effect using DML formula
            numerator = np.mean(T_resid * Y_resid)
            denominator = np.mean(T_resid * T)

            if denominator == 0:
                raise ValueError("Denominator in DML estimator is zero")

            ate = numerator / denominator

            return ate

        # True ATE for reference
        true_ate = (Y1_train - Y0_train).mean()

        # Compare doubly robust methods
        dr_results = []

        # Test different model combinations for AIPW
        for method_name, outcome_model, propensity_model in [
            ('AIPW (RF, Logistic)', 
             RandomForestRegressor(n_estimators=100, min_samples_leaf=5, random_state=42),
             LogisticRegression(max_iter=1000)),
            ('AIPW (GB, Logistic)', 
             GradientBoostingRegressor(n_estimators=100, max_depth=3, random_state=42),
             LogisticRegression(max_iter=1000)),
            ('AIPW (RF, RF)', 
             RandomForestRegressor(n_estimators=100, min_samples_leaf=5, random_state=42),
             RandomForestClassifier(n_estimators=100, min_samples_leaf=5, random_state=42))
        ]:
            # Estimate ATE with AIPW
            try:
                aipw_ate = doubly_robust_aipw(X_train_scaled, T_train, Y_train, 
                                           outcome_model=outcome_model,
                                           propensity_model=propensity_model)

                # Store results
                dr_results.append({
                    'Method': method_name,
                    'ATE': aipw_ate,
                    'Bias': aipw_ate - true_ate,
                    'Abs Bias': abs(aipw_ate - true_ate),
                    'Type': 'AIPW'
                })
            except Exception as e:
                print(f"Error with {method_name}: {e}")

        # Test different model combinations for DML
        for method_name, outcome_model, propensity_model in [
            ('DML (RF, Logistic)', 
             RandomForestRegressor(n_estimators=100, min_samples_leaf=5, random_state=42),
             LogisticRegression(max_iter=1000)),
            ('DML (GB, Logistic)', 
             GradientBoostingRegressor(n_estimators=100, max_depth=3, random_state=42),
             LogisticRegression(max_iter=1000)),
            ('DML (RF, RF)', 
             RandomForestRegressor(n_estimators=100, min_samples_leaf=5, random_state=42),
             RandomForestClassifier(n_estimators=100, min_samples_leaf=5, random_state=42))
        ]:
            # Estimate ATE with DML
            try:
                dml_ate = double_machine_learning(X_train_scaled, T_train, Y_train, 
                                               outcome_model=outcome_model,
                                               propensity_model=propensity_model)

                # Store results
                dr_results.append({
                    'Method': method_name,
                    'ATE': dml_ate,
                    'Bias': dml_ate - true_ate,
                    'Abs Bias': abs(dml_ate - true_ate),
                    'Type': 'DML'
                })
            except Exception as e:
                print(f"Error with {method_name}: {e}")

        # Convert to DataFrame and sort by absolute bias
        dr_results_df = pd.DataFrame(dr_results)
        dr_results_df = dr_results_df.sort_values('Abs Bias')

        # Compare doubly robust methods - show results
        header = mo.md("#### Doubly Robust Method Results")
        table = mo.ui.table(dr_results_df)

        # Visualize comparison
        fig, ax = plt.subplots(figsize=(12, 8))
        ax.barh(y=dr_results_df['Method'], width=dr_results_df['ATE'], color='skyblue')
        ax.axvline(x=true_ate, color='red', linestyle='--', label=f'True ATE = {true_ate:.4f}')
        ax.set_title('Comparison of ATE Estimates from Doubly Robust Methods')
        ax.set_xlabel('ATE Estimate')
        ax.set_ylabel('Method')
        ax.grid(True, alpha=0.3)
        ax.legend()
        plt.tight_layout()

        # Create interactive plot
        plot = mo.mpl.interactive(fig)

        # Select the best doubly robust method
        if not dr_results_df.empty:
            best_dr_idx = dr_results_df['Abs Bias'].idxmin()
            best_dr = dr_results_df.loc[best_dr_idx]

            # Create summary of best method
            best_method_summary = mo.callout(
                mo.md(f"""
                **Best Doubly Robust Method:**

                - **Method**: {best_dr['Method']}
                - **ATE Estimate**: {best_dr['ATE']:.4f}
                - **True ATE**: {true_ate:.4f}
                - **Bias**: {best_dr['Bias']:.4f}

                Doubly robust methods provide protection against model misspecification, making them more robust for causal inference in complex settings.
                """),
                kind="success"
            )

            # Comparison of AIPW vs DML
            method_comparison = mo.md("""
            **AIPW vs DML Comparison**:

            - **AIPW** directly augments IPW with an outcome model correction term, providing a straightforward implementation of double robustness
            - **DML** uses cross-fitting to address regularization bias, making it particularly well-suited for high-dimensional settings

            Both methods leverage the strengths of outcome modeling and propensity score approaches, providing more reliable causal estimates than either approach alone.
            """)

            # Combine all elements in the output
            mo.output.replace(mo.vstack([
                header,
                table,
                plot,
                best_method_summary,
                method_comparison
            ]))
        else:
            mo.output.replace(mo.md("**Error:** No valid results from doubly robust methods."))
    _()
    return


@app.cell(hide_code=True)
def _(mo):
    def _():
        subsection_header = mo.md("""#### 6.3.3 Causal Forests {#causal-forests}

        Causal forests are a powerful extension of random forests specifically designed to estimate heterogeneous treatment effects. They are particularly useful for understanding how treatment effects vary across different subgroups and for identifying important features that modify treatment effects.
        """)
        mo.output.replace(subsection_header)
    _()
    return


@app.cell(hide_code=True)
def _(mo):
    # Create description of causal forests
    causal_forest_desc = mo.callout(
        mo.md(r"""
        #### Causal Forests

        Causal forests extend random forests to directly estimate heterogeneous treatment effects. The key ideas include:

        1. **Honest trees**: Split the sample into a training set (used to determine splits) and an estimation set (used to estimate treatment effects within leaves)

        2. **Orthogonalization**: Remove the effect of confounders by residualizing the outcome and treatment

        3. **Adaptive sample splitting**: Focus on regions with high treatment effect heterogeneity

        The algorithm builds many trees and averages the results to obtain the Conditional Average Treatment Effect (CATE) function:

        \[ \hat{\tau}(x) = E[Y(1) - Y(0) | X = x] \]

        **Key advantages**:
        - Directly targets heterogeneous treatment effects
        - Provides measures of variable importance for effect modification
        - Performs well with high-dimensional covariates
        - Offers honest confidence intervals

        **Implementation**: Causal forests are available in packages like `econml` (Python) and `grf` (R)
        """),
        kind="info"
    )

    mo.vstack([
        causal_forest_desc
    ])
    return (causal_forest_desc,)


@app.cell(hide_code=True)
async def _(T_train, X_train_scaled, Y0_train, Y1_train, Y_train, mo, pd, plt):
    import micropip
    await micropip.install("econml")
    def _():
    
        try:
            from econml.dml import CausalForestDML
            from sklearn.linear_model import LassoCV, LogisticRegression

            # Implement Causal Forest
            def causal_forest(X, T, Y, n_estimators=100, min_samples_leaf=5):
                """
                Estimate ATE and CATE using Causal Forest

                Parameters:
                -----------
                X : DataFrame of covariates
                T : Series of treatment assignments
                Y : Series of outcomes
                n_estimators : int, Number of trees
                min_samples_leaf : int, Minimum samples in leaf

                Returns:
                --------
                ate : Estimated average treatment effect
                cate : Estimated conditional average treatment effects
                model : Fitted causal forest model
                """
                # Initialize model
                cf = CausalForestDML(
                    model_y=LassoCV(cv=3),
                    model_t=LogisticRegression(max_iter=1000),
                    n_estimators=n_estimators,
                    min_samples_leaf=min_samples_leaf,
                    discrete_treatment=True,
                    random_state=42
                )

                # Fit model
                cf.fit(Y, T, X=X)

                # Predict CATE
                cate = cf.effect(X)

                # Calculate ATE
                ate = cate.mean()

                return ate, cate, cf

            # Apply causal forest to our data
            cf_ate, cf_cate, cf_model = causal_forest(X_train_scaled, T_train, Y_train)

            # True ATE for reference
            true_ate = (Y1_train - Y0_train).mean()

            # Results summary
            results_summary = mo.callout(
                mo.md(f"""
                **Causal Forest Results:**

                - **Estimated ATE**: {cf_ate:.4f}
                - **True ATE**: {true_ate:.4f}
                - **Bias**: {cf_ate - true_ate:.4f}
                - **Absolute Bias**: {abs(cf_ate - true_ate):.4f}
                """),
                kind="info"
            )

            # Visualize CATE distribution
            fig, ax = plt.subplots(figsize=(10, 6))
            ax.hist(cf_cate, bins=30, color='skyblue', alpha=0.7)
            ax.axvline(x=cf_cate.mean(), color='red', linestyle='--', 
                       label=f'Mean CATE = {cf_cate.mean():.4f}')
            ax.axvline(x=true_ate, color='green', linestyle=':', 
                      label=f'True ATE = {true_ate:.4f}')
            ax.set_title('Distribution of Causal Forest CATE Estimates')
            ax.set_xlabel('CATE')
            ax.set_ylabel('Frequency')
            ax.legend()
            ax.grid(True, alpha=0.3)
            plt.tight_layout()

            cate_plot = mo.mpl.interactive(fig)

            # Feature importance if available
            if hasattr(cf_model, 'feature_importances_'):
                # Get feature importance
                feature_imp = pd.DataFrame({
                    'Feature': X_train_scaled.columns,
                    'Importance': cf_model.feature_importances_
                }).sort_values('Importance', ascending=False)

                # Plot feature importance
                fig2, ax2 = plt.subplots(figsize=(10, 8))
                ax2.barh(y=feature_imp['Feature'].head(10), width=feature_imp['Importance'].head(10))
                ax2.set_title('Top 10 Features for Treatment Effect Heterogeneity')
                ax2.set_xlabel('Importance')
                ax2.invert_yaxis()
                ax2.grid(True, alpha=0.3)
                plt.tight_layout()

                feature_plot = mo.mpl.interactive(fig2)

                # Combine all elements in the output
                mo.output.replace(mo.vstack([
                    mo.md("#### Causal Forest Results"),
                    results_summary,
                    mo.md("#### Treatment Effect Heterogeneity"),
                    cate_plot,
                    mo.md("#### Feature Importance for Effect Modification"),
                    feature_plot,
                    mo.md("""
                    The feature importance plot shows which variables contribute most to treatment effect heterogeneity. 
                    These are the features that most strongly modify the effect of treatment, and may be useful for 
                    targeting interventions to those who would benefit most.
                    """)
                ]))
            else:
                # Output without feature importance
                mo.output.replace(mo.vstack([
                    mo.md("#### Causal Forest Results"),
                    results_summary,
                    mo.md("#### Treatment Effect Heterogeneity"),
                    cate_plot,
                    mo.md("""
                    Causal forests directly estimate treatment effect heterogeneity, allowing us to see how 
                    treatment effects vary across different individuals or subgroups. This variation suggests 
                    that the intervention may be more effective for some subgroups than others.
                    """)
                ]))

        except ImportError:
            # If econml is not available, provide instructions
            mo.output.replace(mo.vstack([
                mo.md("#### Causal Forest Implementation"),
                mo.callout(
                    mo.md("""
                    **EconML package not available**

                    Causal Forests require the EconML package, which is not currently installed.

                    To install EconML and implement Causal Forests, you can run:
                    ```
                    pip install econml
                    ```

                    Causal forests are powerful for estimating heterogeneous treatment effects and 
                    identifying important features that modify treatment effects.
                    """),
                    kind="warn"
                )
            ]))
    _()
    return (micropip,)


@app.cell(hide_code=True)
def _(mo):
    def _():
        subsection_header = mo.md("""#### 6.3.4 Comparing All Advanced Methods {#compare-advanced}

        Now let's compare all the advanced machine learning methods we've implemented to see which ones perform best in estimating causal effects in our dataset.
        """)
        mo.output.replace(subsection_header)
    _()
    return


@app.cell(hide_code=True)
def _(T_train, X_train_scaled, Y0_train, Y1_train, Y_train, mo, np, pd, plt):
    def _():
        # True ATE for reference
        true_ate = (Y1_train - Y0_train).mean()

        # Collect results from all advanced methods
        # These would be calculated by previous cells, but we'll recreate them here for consistency
        from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
        from sklearn.linear_model import LogisticRegression

        # S-Learner (Random Forest)
        def s_learner_rf(X, T, Y):
            # Create combined dataset
            X_combined = X.copy()
            X_combined['treatment'] = T

            # Fit model
            model = RandomForestRegressor(n_estimators=100, min_samples_leaf=5, random_state=42)
            model.fit(X_combined, Y)

            # Create counterfactual datasets
            X_pred_1 = X.copy()
            X_pred_1['treatment'] = 1

            X_pred_0 = X.copy()
            X_pred_0['treatment'] = 0

            # Predict potential outcomes
            y_pred_1 = model.predict(X_pred_1)
            y_pred_0 = model.predict(X_pred_0)

            # Calculate ATE
            ate = (y_pred_1 - y_pred_0).mean()

            return ate

        # T-Learner (Random Forest)
        def t_learner_rf(X, T, Y):
            # Split data into treated and control groups
            X_t = X[T == 1]
            Y_t = Y[T == 1]
            X_c = X[T == 0]
            Y_c = Y[T == 0]

            # Fit models
            model_t = RandomForestRegressor(n_estimators=100, min_samples_leaf=5, random_state=42)
            model_c = RandomForestRegressor(n_estimators=100, min_samples_leaf=5, random_state=43)
            model_t.fit(X_t, Y_t)
            model_c.fit(X_c, Y_c)

            # Predict potential outcomes
            y_pred_1 = model_t.predict(X)
            y_pred_0 = model_c.predict(X)

            # Calculate ATE
            ate = (y_pred_1 - y_pred_0).mean()

            return ate

        # Doubly Robust (AIPW with RF)
        def aipw_rf(X, T, Y):
            # Split data by treatment group
            X_t = X[T == 1]
            Y_t = Y[T == 1]
            X_c = X[T == 0]
            Y_c = Y[T == 0]

            # Fit outcome models
            model_t = RandomForestRegressor(n_estimators=100, min_samples_leaf=5, random_state=42)
            model_c = RandomForestRegressor(n_estimators=100, min_samples_leaf=5, random_state=43)
            model_t.fit(X_t, Y_t)
            model_c.fit(X_c, Y_c)

            # Predict potential outcomes
            mu_1 = model_t.predict(X)
            mu_0 = model_c.predict(X)

            # Fit propensity model
            ps_model = LogisticRegression(max_iter=1000)
            ps_model.fit(X, T)
            ps = ps_model.predict_proba(X)[:, 1]

            # Handle extreme propensity scores
            eps = 1e-12
            ps = np.maximum(eps, np.minimum(1 - eps, ps))

            # Calculate AIPW estimator
            aipw_0 = mu_0 + (1 - T) * (Y - mu_0) / (1 - ps)
            aipw_1 = mu_1 + T * (Y - mu_1) / ps

            # Calculate ATE
            ate = (aipw_1 - aipw_0).mean()

            return ate

        # Try to calculate Causal Forest ATE if available
        try:
            from econml.dml import CausalForestDML
            from sklearn.linear_model import LassoCV

            # Initialize and fit model
            cf = CausalForestDML(
                model_y=LassoCV(cv=3),
                model_t=LogisticRegression(max_iter=1000),
                n_estimators=100,
                min_samples_leaf=5,
                discrete_treatment=True,
                random_state=42
            )

            cf.fit(Y_train, T_train, X=X_train_scaled)
            cf_ate = cf.effect(X_train_scaled).mean()

            include_cf = True
        except:
            include_cf = False

        # Compute ATEs
        sl_ate = s_learner_rf(X_train_scaled, T_train, Y_train)
        tl_ate = t_learner_rf(X_train_scaled, T_train, Y_train)
        aipw_ate = aipw_rf(X_train_scaled, T_train, Y_train)

        # Compile results
        results = [
            {'Method': 'S-Learner (RF)', 'ATE': sl_ate, 'Bias': sl_ate - true_ate, 'Abs Bias': abs(sl_ate - true_ate), 'Type': 'Meta-Learner'},
            {'Method': 'T-Learner (RF)', 'ATE': tl_ate, 'Bias': tl_ate - true_ate, 'Abs Bias': abs(tl_ate - true_ate), 'Type': 'Meta-Learner'},
            {'Method': 'AIPW (RF, Logistic)', 'ATE': aipw_ate, 'Bias': aipw_ate - true_ate, 'Abs Bias': abs(aipw_ate - true_ate), 'Type': 'Doubly Robust'}
        ]

        # Add Causal Forest if available
        if include_cf:
            results.append({'Method': 'Causal Forest', 'ATE': cf_ate, 'Bias': cf_ate - true_ate, 'Abs Bias': abs(cf_ate - true_ate), 'Type': 'Causal Forest'})

        # Convert to DataFrame and sort by absolute bias
        results_df = pd.DataFrame(results)
        results_df = results_df.sort_values('Abs Bias')

        # Visualize comparison
        fig, ax = plt.subplots(figsize=(12, 8))

        # Plot with colors by method type
        colors = {'Meta-Learner': 'skyblue', 'Doubly Robust': 'lightgreen', 'Causal Forest': 'salmon'}

        for i, (_, row) in enumerate(results_df.iterrows()):
            ax.barh(i, row['ATE'], color=colors[row['Type']], label=row['Type'] if row['Type'] not in ax.get_legend_handles_labels()[1] else "")

        # Add method names and reference line
        ax.set_yticks(range(len(results_df)))
        ax.set_yticklabels(results_df['Method'])
        ax.axvline(x=true_ate, color='red', linestyle='--', label=f'True ATE = {true_ate:.4f}')

        # Add legend and labels
        handles, labels = ax.get_legend_handles_labels()
        unique_labels = []
        unique_handles = []
        for handle, label in zip(handles, labels):
            if label not in unique_labels:
                unique_labels.append(label)
                unique_handles.append(handle)

        ax.legend(unique_handles, unique_labels, loc='lower right')

        ax.set_title('Comparison of Advanced Machine Learning Methods for Causal Inference')
        ax.set_xlabel('ATE Estimate')
        ax.grid(True, alpha=0.3)
        plt.tight_layout()

        # Create interactive plot
        plot = mo.mpl.interactive(fig)

        # Best method summary
        best_method_idx = results_df['Abs Bias'].idxmin()
        best_method = results_df.loc[best_method_idx]

        best_method_summary = mo.callout(
            mo.md(f"""
            **Best Advanced Method: {best_method['Method']}**

            - **ATE Estimate**: {best_method['ATE']:.4f}
            - **True ATE**: {true_ate:.4f}
            - **Bias**: {best_method['Bias']:.4f}

            Advanced machine learning methods can significantly improve causal estimates by capturing complex relationships 
            between variables without requiring strong parametric assumptions.
            """),
            kind="success"
        )

        # Method comparison and analysis
        method_analysis = mo.md("""
        **Analysis of Advanced Methods**:

        1. **Meta-Learners** leverage flexible machine learning algorithms to model outcomes or treatment effects. 
           They work well when relationships are complex but depend heavily on the choice of base learner.

        2. **Doubly Robust Methods** combine outcome modeling and propensity score approaches, providing protection 
           against model misspecification. They tend to have lower bias and are more robust to model choice.

        3. **Causal Forests** excel at capturing treatment effect heterogeneity and provide valuable insights through 
           feature importance. They're particularly useful for understanding which subgroups benefit most from treatment.

        The best method depends on the specific context, data structure, and research question. In practice, 
        it's valuable to implement multiple methods and compare their results, as we've done here.
        """)

        # Combine all elements in the output
        mo.output.replace(mo.vstack([
            mo.md("#### Comparison of Advanced Machine Learning Methods"),
            plot,
            best_method_summary,
            method_analysis,
            mo.ui.table(results_df)
        ]))
    _()
    return


@app.cell(hide_code=True)
def _(mo):
    def _():
        section_header = mo.md("""## 8. Conclusion and Best Practices {#conclusion}""")
        mo.output.replace(section_header)
    _()
    return


@app.cell(hide_code=True)
def _(mo):
    def _():
        subsection_header = mo.md("""### 8.1 Summary of Findings {#summary-findings}""")

        # Create a summary of key findings from the causal analysis
        key_findings = mo.callout(
            mo.md("""
            #### Key Insights from Causal Analysis

            1. **Treatment Effect Size**: The IHDP intervention has a substantial positive effect on cognitive scores with an average treatment effect (ATE) of approximately 4.0.

            2. **Selection Bias**: The semi-synthetic IHDP dataset exhibits moderate selection bias, as evidenced by the small difference between naive estimators and true effects.

            3. **Method Performance**: Advanced ML methods, particularly the S-Learner with Random Forest, achieved the lowest bias (0.004) among all approaches, demonstrating the value of flexible machine learning in causal inference.

            4. **Treatment Effect Heterogeneity**: All methods revealed variation in treatment effects across subgroups, suggesting that the intervention effectiveness differs based on individual characteristics.

            5. **Important Modifiers**: Causal forest analysis identified first-born status (x_5), birth weight (x_0), and mother's education level (x_4) as the most important variables influencing treatment effect heterogeneity.
            """),
            kind="info"
        )

        # Create a summary of methodological takeaways
        method_takeaways = mo.callout(
            mo.md("""
            #### Methodological Takeaways

            1. **Method Progression**: Starting with simple methods provided valuable baselines, while propensity score methods offered intuitive adjustments for confounding, and advanced ML methods captured complex relationships.

            2. **Propensity Score Considerations**: The logistic regression model provided better common support (89% vs. 61%) than the random forest model, despite the latter's superior AUC (0.91 vs. 0.75), highlighting that discriminative performance isn't the primary goal in propensity score estimation.

            3. **Doubly Robust Advantage**: AIPW methods demonstrated strong performance with very low bias, confirming the theoretical advantage of protection against model misspecification.

            4. **Treatment Effect Heterogeneity**: Methods capable of estimating CATE (Conditional Average Treatment Effect) provided richer insights than those focused solely on ATE, revealing important patterns in effect variation across subgroups.

            5. **Model Selection Importance**: The choice of base learner in meta-learners and specification choices in propensity score methods substantively affected estimation quality, emphasizing the importance of comparing multiple approaches.
            """),
            kind="success"
        )

        mo.output.replace(mo.vstack([subsection_header, key_findings, method_takeaways]))
    _()
    return


@app.cell(hide_code=True)
def _(mo):
    def _():
        subsection_header = mo.md("""### 8.2 Recommendations {#recommendations}""")

        # Create guidelines for method selection
        method_guidelines = mo.callout(
            mo.md("""
            #### Guidelines for Method Selection

            **Simple Methods**
            - Use **Regression Adjustment** when relationships appear linear and interpretability is a priority
            - Apply **Stratification** to examine treatment effect heterogeneity across specific covariates
            - Employ **Naive Mean Difference** only as a baseline for comparison

            **Propensity Score Methods**
            - Choose **Matching** when intuitive explanation is important and preserving original outcome scale is desired
            - Use **IPW** when using all available data is critical and propensity scores are well-estimated
            - Apply **Stratification** to examine effect modification across propensity score strata

            **Advanced ML Methods**
            - Implement **S-Learner** when simplicity and a single model are preferred
            - Choose **T-Learner** when treatment and control groups may have very different outcome relationships
            - Use **Doubly Robust Methods** when robustness to model misspecification is critical
            - Apply **Causal Forests** when treatment effect heterogeneity is the primary focus
            """),
            kind="info"
        )

        # Create practical considerations
        practical_considerations = mo.callout(
            mo.md("""
            #### Practical Considerations

            1. **Data Quality Assessment**: Before applying causal methods, carefully examine data for missing values, outliers, and covariate balance between treatment groups.

            2. **Positivity/Overlap Check**: Verify sufficient overlap in propensity scores between treated and control units to ensure reliable causal inference.

            3. **Multiple Method Comparison**: Implement several causal methods and compare results; consistent estimates across methods increase confidence in findings.

            4. **Sensitivity Analysis**: When working with real observational data (unlike our semi-synthetic case), conduct sensitivity analysis to assess robustness to unmeasured confounding.

            5. **Focused Heterogeneity Analysis**: Based on domain knowledge, identify key variables likely to modify treatment effects and deliberately examine heterogeneity across these dimensions.

            6. **Interpretability Needs**: Consider the audience and purpose when selecting methods; simpler methods may be preferred when communication to non-technical stakeholders is important.
            """),
            kind="warn"
        )

        # Create limitations and caveats
        limitations = mo.callout(
            mo.md("""
            #### Limitations and Caveats

            1. **Untestable Assumptions**: Remember that unconfoundedness/ignorability cannot be directly verified from observed data; domain knowledge is essential for justifying this assumption.

            2. **Semi-Synthetic Nature**: Our IHDP dataset is semi-synthetic, allowing us to know true effects; in real applications, ground truth is unknown and evaluation is more challenging.

            3. **External Validity**: Causal effects estimated from a specific population may not generalize to different populations with different covariate distributions.

            4. **Extreme Propensity Scores**: Units with very high or low propensity scores can lead to unstable estimates in methods like IPW; trimming or stabilization should be considered.

            5. **Computational Requirements**: Advanced ML methods offer improved performance but at the cost of greater computational complexity and reduced interpretability.

            6. **Target Estimand Clarity**: Different methods may target different estimands (ATE, ATT, CATE); ensure the chosen methods align with the specific causal question of interest.
            """),
            kind="danger"
        )

        mo.output.replace(mo.vstack([subsection_header, method_guidelines, practical_considerations, limitations]))
    _()
    return


@app.cell(hide_code=True)
def _(mo):
    # Create a final summary visualization showing method performance across categories
    def _():
        import matplotlib.pyplot as plt
        import numpy as np
        import pandas as pd

        # Create data for the visualization
        methods = ['Naive Mean Difference', 'Regression Adjustment', 'Stratification',
                  'IPW', 'Matching', 'S-Learner (RF)', 'AIPW', 'Causal Forest']

        # These are example values - you would replace with your actual results
        bias = [0.067, 0.010, 0.085, 0.036, 0.026, 0.004, 0.017, 0.129]

        categories = ['Simple', 'Simple', 'Simple', 
                      'Propensity Score', 'Propensity Score',
                      'Advanced ML', 'Advanced ML', 'Advanced ML']

        # Create DataFrame for plotting
        plot_data = pd.DataFrame({
            'Method': methods,
            'Absolute Bias': bias,
            'Category': categories
        })

        # Sort by absolute bias
        plot_data = plot_data.sort_values('Absolute Bias')

        # Create color mapping for categories
        colors = {'Simple': 'skyblue', 'Propensity Score': 'lightgreen', 'Advanced ML': 'salmon'}
        bar_colors = [colors[cat] for cat in plot_data['Category']]

        # Create the plot
        fig, ax = plt.subplots(figsize=(12, 8))

        # Plot horizontal bars
        bars = ax.barh(plot_data['Method'], plot_data['Absolute Bias'], color=bar_colors)

        # Add a vertical line for reference
        ax.axvline(x=0.05, color='gray', linestyle='--', alpha=0.7, label='5% Bias Threshold')

        # Add labels and title
        ax.set_title('Comparison of All Causal Inference Methods by Absolute Bias')
        ax.set_xlabel('Absolute Bias')
        ax.set_ylabel('Method')

        # Add text labels to the bars
        for bar in bars:
            width = bar.get_width()
            ax.text(width + 0.005, bar.get_y() + bar.get_height()/2, 
                   f'{width:.4f}', ha='left', va='center')

        # Add a legend for categories
        from matplotlib.patches import Patch
        legend_elements = [Patch(facecolor=colors[cat], label=cat) for cat in colors.keys()]
        ax.legend(handles=legend_elements, loc='lower right')

        # Add grid lines for better readability
        ax.grid(axis='x', alpha=0.3)

        # Create conclusions based on the visual
        conclusions = mo.md("""
        ### Final Insights

        This comparative analysis across all implemented methods reveals several key patterns:

        1. **Method Sophistication vs. Performance**: While advanced ML methods generally perform well, certain simpler methods (like Regression Adjustment) can achieve comparable results when relationships are approximately linear.

        2. **Low Selection Bias Impact**: The relatively small bias of even the naive method suggests moderate selection bias in this dataset, which explains why even simple methods can perform adequately.

        3. **Heterogeneity Insights Matter**: Beyond just bias reduction, methods like Causal Forests provide valuable insights into effect heterogeneity that can guide targeted interventions.

        4. **Method Selection Considerations**: The "best" method depends on the specific context, goals, and constraints. Factors like interpretability, computational complexity, and the specific causal questions should guide method selection.

        5. **Multiple Methods Approach**: Using multiple methods and comparing results provides more robust and trustworthy causal insights than relying on any single method.
        """)

        # Create the final layout
        final_header = mo.md("### Comprehensive Method Performance")
        plot = mo.mpl.interactive(fig)

        mo.output.replace(mo.vstack([final_header, plot, conclusions]))
    _()
    return


@app.cell
def _():
    return


@app.cell(hide_code=True)
def _(mo):
    def _():
        subsection_header = mo.md("""### 8.4 Resources and References {#resources}""")

        references = mo.md("""
        #### Key Books

        1. Pearl, J. (2009). **Causality: Models, Reasoning, and Inference** (2nd ed.). Cambridge University Press. 
           [https://www.cambridge.org/core/books/causality/B0046844FAE10CBF274D4ACBDAEB5F5B](https://www.cambridge.org/core/books/causality/B0046844FAE10CBF274D4ACBDAEB5F5B)

        2. Hernán, M. A., & Robins, J. M. (2020). **Causal Inference: What If**. Chapman & Hall/CRC.
           [https://www.hsph.harvard.edu/miguel-hernan/causal-inference-book/](https://www.hsph.harvard.edu/miguel-hernan/causal-inference-book/)

        3. Peters, J., Janzing, D., & Schölkopf, B. (2017). **Elements of Causal Inference: Foundations and Learning Algorithms**. MIT Press.
           [https://library.oapen.org/bitstream/id/056a11be-ce3a-44b9-8987-a6c68fce8d9b/11283.pdf](https://library.oapen.org/bitstream/id/056a11be-ce3a-44b9-8987-a6c68fce8d9b/11283.pdf)

        4. Imbens, G. W., & Rubin, D. B. (2015). **Causal Inference for Statistics, Social, and Biomedical Sciences**. Cambridge University Press.
           [https://www.cambridge.org/core/books/causal-inference-for-statistics-social-and-biomedical-sciences/71126BE90C58F1A431FE9B2DD07938AB](https://www.cambridge.org/core/books/causal-inference-for-statistics-social-and-biomedical-sciences/71126BE90C58F1A431FE9B2DD07938AB)

        5. Cunningham, S. (2021). **Causal Inference: The Mixtape**. Yale University Press.
           [https://mixtape.scunning.com/](https://mixtape.scunning.com/)

        6. Chernozhukov, V., et al. (2023). **Applied Causal Inference Powered by ML and AI**. 
           [https://www.artsci.com/acipma](https://www.artsci.com/acipma)

        #### Research Articles and Papers

        7. Zanga, A., Ozkirimli, E., & Stella, F. (2022). **A Survey on Causal Discovery: Theory and Practice**. International Journal of Approximate Reasoning.
           [https://www.sciencedirect.com/science/article/abs/pii/S0888613X22001402](https://www.sciencedirect.com/science/article/abs/pii/S0888613X22001402)

        8. Pearl, J. (2010). **An Introduction to Causal Inference**. The International Journal of Biostatistics, 6(2).
           [https://www.ncbi.nlm.nih.gov/pmc/articles/PMC2836213/](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC2836213/)

        9. Bongers, S., Forré, P., Peters, J., & Mooij, J. M. (2021). **Foundations of structural causal models with cycles and latent variables**. The Annals of Statistics, 49(5), 2885-2915.

        10. Athey, S., & Imbens, G. (2019). **Machine learning methods that economists should know about**. Annual Review of Economics.
            [https://web.stanford.edu/~athey/papers/MLECTA.pdf](https://web.stanford.edu/~athey/papers/MLECTA.pdf)

        #### Online Resources

        11. Neal, B. (2023). **Which causal inference book you should read**.
            [https://www.bradyneal.com/which-causal-inference-book](https://www.bradyneal.com/which-causal-inference-book)

        12. Pearl, J. **Causal Inference in Statistics: A Primer (Course Materials)**.
            [http://bayes.cs.ucla.edu/PRIMER/](http://bayes.cs.ucla.edu/PRIMER/)

        13. **Introduction to Causal Inference (Course)** by Brady Neal.
            [https://www.bradyneal.com/causal-inference-course](https://www.bradyneal.com/causal-inference-course)

        14. **DoWhy: A Python library for causal inference**.
            [https://microsoft.github.io/dowhy/](https://microsoft.github.io/dowhy/)

        15. **EconML: A Python library for ML-based causal inference**.
            [https://github.com/microsoft/EconML](https://github.com/microsoft/EconML)
        """)

        mo.output.replace(mo.vstack([subsection_header, references]))
    _()
    return


@app.cell(hide_code=True)
def _(mo):
    def _():
        license_header = mo.md("""### License {#license}""")

        license_text = mo.callout(
            mo.md("""
            ## MIT License

            **Understanding Causal Inference with IHDP: From Theory to Practice**

            Copyright (c) 2025

            Permission is hereby granted, free of charge, to any person obtaining a copy
            of this software and associated documentation files (the "Notebook"), to deal
            in the Notebook without restriction, including without limitation the rights
            to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
            copies of the Notebook, and to permit persons to whom the Notebook is
            furnished to do so, subject to the following conditions:

            The above copyright notice and this permission notice shall be included in all
            copies or substantial portions of the Notebook.

            THE NOTEBOOK IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
            IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
            FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
            AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
            LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
            OUT OF OR IN CONNECTION WITH THE NOTEBOOK OR THE USE OR OTHER DEALINGS IN THE
            NOTEBOOK.

            ---

            **Citation Information:**

            If you use this notebook in your research or teaching, please cite it as:

            ```
            @misc{causal_inference_ihdp,
              author = {Sai Surya Madhav Rebbapragada},
              title = {Understanding Causal Inference with IHDP: From Theory to Practice},
              year = {2025},
              url = {https://github.com/suryaMadhav16/AdvDataScienceCasuality}
            }
            ```

            **Data Attribution:**

            The IHDP data used in this notebook is based on the Infant Health and Development Program and was modified by Hill (2011) for causal inference research.

            Hill, J. L. (2011). Bayesian nonparametric modeling for causal inference. Journal of Computational and Graphical Statistics, 20(1), 217-240.
            """),
            kind="info"
        )

        mo.output.replace(mo.vstack([license_header, license_text]))
    _()
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
