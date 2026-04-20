# Data-Driven Decision Support for Evaluating AI-Generated Advertising Content in a Simulated Content Platform

## Authors and Team
Rui Xu

## 1. Executive Summary
This project supports a content-platform decision about how to evaluate and optimize AI-generated advertising content while monitoring growth, quality, and risk. The core business question is whether platform operators can identify strong-performing content and traffic contexts, detect abnormal KPI movements, diagnose possible drivers, and compare experiment outcomes before making broader rollout decisions.

The business value is a reusable decision-support workflow rather than a single production recommendation. The workflow combines KPI monitoring, anomaly alerts, segmented root-cause analysis, simulated A/B evaluation, dashboard reporting, and a lightweight predictive modeling extension. The data used in this project is simulated platform data, so the results should be interpreted as prototype evidence for an analytics process, not as proof of real deployed business impact.

Since the midterm, the project has moved beyond descriptive packaging. Major additions include a cleaner English progress report, dashboard and appendix outputs, an initial Logistic Regression predictive prototype, factor-level interpretation of the coefficient chart, a Random Forest benchmark, and a nested cross-validation workflow that responds directly to feedback about more rigorous training and test logic.

## 2. Data Description and Preprocessing
The dataset is stored at `data/raw/content_platform_mock_data.csv`. It represents simulated content-platform observations across content categories, traffic sources, user types, city tiers, experiment groups, time buckets, and business performance metrics. The project uses this dataset as the source of truth for the descriptive, diagnostic, experimental, and predictive components.

Key dataset summary:

| Item | Value |
|---|---:|
| Observations | 97,200 |
| Variables | 20 |
| Numeric variables | 12 |
| Categorical variables | 8 |
| Time variables | 1 |
| Missing values | 0 |
| Duplicate rows | 0 |

Important categorical variables include content category, traffic source, user type, city tier, experiment group, hour bucket, and weekday. Important numeric variables include exposure, click, conversion, completion, report, revenue, content supply, and session-level measures. The timestamp field supports trend monitoring and time-aware evaluation.

The preprocessing workflow checks missing values, duplicate rows, KPI validity, and funnel consistency. KPI ratios such as click-through rate, conversion rate, completion rate, interaction rate, report rate, and revenue per exposure are derived from the simulated count fields. Funnel consistency checks are important because downstream metrics such as conversions should not exceed upstream actions in a coherent analytics table.

Anomaly and outlier detection is handled as a monitoring layer rather than a production alerting system. The project uses moving baselines, threshold-style comparisons, and segmented follow-up summaries to flag unusual KPI movements. These alerts then feed root-cause analysis by content category, traffic source, user type, and time segment.

## 3. Descriptive Analytics and Dashboard Workflow
The descriptive workflow starts with KPI monitoring. It summarizes high-level platform performance and tracks core metrics across time. Trend monitoring helps identify whether metric changes are isolated spikes or sustained movements.

The anomaly workflow flags unusual KPI behavior, and the segmented diagnosis workflow provides possible root-cause context by comparing segment contributions. This does not prove causality, but it gives operators a structured way to ask which segment combinations may deserve follow-up review.

The simulated A/B evaluation module compares experiment groups on business and guardrail metrics. It is useful for showing how an experiment review could balance conversion gains with quality or risk indicators. Because the data is simulated, the A/B module should be presented as an evaluation prototype rather than evidence from a real deployed experiment.

The dashboard prototype organizes the workflow into presentation-friendly views. Existing artifacts include KPI summaries, anomaly summaries, root-cause summaries, A/B summaries, dashboard screenshots, appendix outputs, and generated report tables. Key output areas include `reports/outputs/`, `reports/figures/`, and `reports/tables/`.

## 4. Predictive Modeling Prototype
Predictive modeling was added after the midterm to extend the project from monitoring and diagnosis toward prediction. The task is binary classification of high conversion performance at the row level.

The target is `high_conversion_performance`. In the initial split model, a row is labeled positive if its conversion rate is at or above the training-set median conversion rate. In the nested cross-validation workflow, the target threshold is recomputed within each outer training fold to avoid leakage from the held-out fold.

The initial model uses a compact business-relevant feature set:

| Feature Type | Features |
|---|---|
| Categorical | content_category, traffic_source, user_type, city_tier, experiment_group, hour_bucket, week_day |
| Numeric | content_supply_cnt, session_uv, is_weekend |

Downstream leakage variables are excluded from the predictive feature matrix. These include click, conversion count, view completion count, report count, monetization revenue, and direct outcome-rate variables. This keeps the prototype closer to a realistic prediction setting where the model should not use the answer as an input.

Initial Logistic Regression split metrics:

| Metric | Value |
|---|---:|
| Accuracy | 0.6219 |
| Precision | 0.6082 |
| Recall | 0.7879 |
| F1-score | 0.6865 |
| ROC-AUC | 0.6606 |

The ROC curve shows how well the model separates high-conversion and lower-conversion rows across classification thresholds. The confusion matrix shows correct and incorrect classifications at one selected threshold. The coefficient plot shows which encoded features have positive or negative associations with the probability of high conversion performance in the Logistic Regression model.

These metrics indicate that the model captures some signal in the simulated data, but it is not a production-ready predictor. The model is best framed as a lightweight predictive prototype that makes the decision-support workflow more complete.

## 5. Factor-Level Interpretation
The Logistic Regression coefficient analysis was expanded into a factor-level interpretation so the model can be explained in presentation and Q&A settings. Positive coefficients indicate higher predicted odds of high conversion performance relative to the encoded baseline or numeric scale. Negative coefficients indicate lower predicted odds. These are associations in simulated data, not causal effects.

| Factor | Direction | Business Interpretation | Optimization Idea | Caution |
|---|---|---|---|---|
| user type new user | Suppresses high conversion performance | New users may be less familiar with the platform, less trusting of ad content, or earlier in the intent funnel. | Improve onboarding, simplify ad landing paths, and use lighter calls to action for new-user traffic. | The signal may reflect simulated user-behavior assumptions rather than a true real-world barrier. |
| traffic source recommendation | Suppresses high conversion performance | Recommendation traffic may prioritize engagement or discovery rather than immediate purchase intent. | Separate engagement-oriented recommendation traffic from conversion-oriented ad objectives. | The coefficient is relative to the encoded baseline and should not be treated as proof that recommendations are low quality. |
| traffic source follow | Suppresses high conversion performance | Follow-feed users may already have relationship-based browsing habits and may respond less to inserted advertising. | Test more native ad formats or creator-aligned messaging in follow-feed placements. | This may be contextual to the simulated feed design. |
| traffic source nearby | Suppresses high conversion performance | Nearby traffic may reflect casual local browsing where conversion intent is uneven. | Use location-relevant offers and tighter category matching for nearby traffic. | Local context can vary widely in real data, so this should be validated before action. |
| experiment group A | Slightly suppresses high conversion performance | Group A appears slightly below the baseline or alternative group in the predictive model. | Treat Group A as the comparison condition and investigate what differs from Group B. | The magnitude is small, so it should not drive decisions alone. |
| traffic source search | Promotes high conversion performance | Search traffic usually reflects explicit intent, so users may be closer to conversion. | Prioritize high-intent ad matching and landing-page quality for search-origin sessions. | This is plausible structurally, but still based on simulated data. |
| user type active user | Promotes high conversion performance | Active users may have stronger habits, better platform familiarity, and more stable response behavior. | Use active-user segments for controlled optimization tests and high-confidence message matching. | Active-user performance may not generalize to new-user acquisition goals. |
| user type returning user | Promotes high conversion performance | Returning users may have enough familiarity to convert more readily than new users. | Use retargeting-style creative and continuity messaging for returning users. | Returning-user lift is associative and may overlap with unobserved loyalty or intent factors. |
| experiment group B | Slightly promotes high conversion performance | Group B is associated with a small positive conversion signal in the model. | Use Group B as a candidate for further review in the simulated experiment workflow. | The effect is small and should be considered alongside A/B summaries and guardrail metrics. |
| session uv | Slightly promotes high conversion performance | Higher session volume may indicate stronger segment demand or a healthier traffic context. | Prioritize monitoring of high-volume segments where small improvements can matter operationally. | As a numeric aggregate, session volume may also proxy for other unmodeled factors. |

The main takeaway is that the coefficient chart is useful for explaining directional associations. Search traffic and more established user types look more favorable in the simulated model, while new users and some discovery-feed sources look less favorable. The practical value is not to declare winners, but to generate hypotheses for targeting, creative design, and experiment follow-up.

## 6. Model Comparison: Logistic Regression vs Random Forest
Random Forest was added as a benchmark because it can capture nonlinear patterns and interactions that Logistic Regression may miss. The comparison uses the same predictive task and a comparable feature setup so the two models can be discussed fairly.

Initial split comparison:

| Model | Accuracy | Precision | Recall | F1-score | ROC-AUC |
|---|---:|---:|---:|---:|---:|
| Logistic Regression | 0.6219 | 0.6082 | 0.7879 | 0.6865 | 0.6606 |
| Random Forest | 0.6133 | 0.6090 | 0.7371 | 0.6670 | 0.6536 |

In the initial comparison, Logistic Regression is slightly stronger overall on ROC-AUC and F1-score. It is also easier to explain because coefficients show directional associations. Random Forest remains useful as a flexible benchmark, but it is not clearly better here. For a simulated classroom project focused on decision support and presentation clarity, Logistic Regression remains the more interpretable model, while Random Forest provides a helpful robustness check.

## 7. Improved Validation: Nested Cross-Validation
This section responds directly to the professor feedback about more proper training and test logic. The earlier train/test split was useful as an initial baseline, but a single split can be sensitive to the chosen partition. The nested cross-validation workflow provides a more reliable estimate of general predictive performance because model selection happens inside the validation process.

Nested CV setup:

| Component | Setup |
|---|---|
| Outer CV | 3 shuffled KFold folds |
| Inner CV | 3 StratifiedKFold folds |
| Models compared | Logistic Regression and Random Forest |
| Shared outer folds | Yes |
| Inner tuning metric | ROC-AUC |
| Feature selection | SelectKBest inside the pipeline |
| Target threshold | Computed only from each outer training fold |
| Leakage control | Downstream outcome variables excluded |

The outer CV estimates generalization performance. The inner CV tunes hyperparameters and chooses the feature-selection setting. SelectKBest is inside the scikit-learn pipeline, so feature selection is refit within each training fold rather than being computed on the full dataset. This avoids leaking information from validation rows into preprocessing.

Best hyperparameters selected by inner CV:

| Model | Selected Setting |
|---|---|
| Logistic Regression | C=0.1, penalty=l1, SelectKBest k=10 |
| Random Forest | n_estimators=80, max_depth=8, min_samples_leaf=20, max_features=sqrt, SelectKBest k=all |

Nested CV average metrics:

| Model | Accuracy | Precision | Recall | F1-score | ROC-AUC |
|---|---:|---:|---:|---:|---:|
| Logistic Regression | 0.5940 | 0.5767 | 0.7126 | 0.6372 | 0.6383 |
| Random Forest | 0.5939 | 0.5724 | 0.7458 | 0.6477 | 0.6367 |

The nested CV result is a tradeoff rather than a single definitive winner. Logistic Regression has slightly better ROC-AUC, while Random Forest has slightly better recall and F1-score. The overall difference is small. The main improvement is not a dramatic performance gain; it is the stronger validation logic and fairer comparison framework.

## 8. Source Code and Repository Structure
GitHub repository: https://github.com/xur-2002/project

Main source code components:

| Path | Purpose |
|---|---|
| `src/generate_data.py` | Simulated content-platform dataset generation |
| `src/anomaly_detection.py` | KPI monitoring and anomaly detection logic |
| `src/root_cause_analysis.py` | Segmented diagnosis and root-cause style summaries |
| `src/ab_test_analysis.py` | Simulated A/B evaluation workflow |
| `src/lightweight_predictive_model.py` | Initial Logistic Regression predictive prototype |
| `src/predictive_factor_analysis.py` | Factor-level interpretation and supporting summaries |
| `src/random_forest_predictive_model.py` | Random Forest benchmark model |
| `src/nested_cv_model_comparison.py` | Nested cross-validation comparison workflow |
| `dashboard/app.py` | Streamlit dashboard prototype |

Main output locations:

| Path | Contents |
|---|---|
| `reports/outputs/` | Summary markdown files, metrics CSVs, supporting tables, and generated report outputs |
| `reports/figures/` | KPI, anomaly, dashboard, predictive model, model comparison, and nested CV figures |
| `reports/tables/` | Earlier analysis tables such as anomaly, root-cause, and A/B summaries |
| `reports/final_integrated_project_report.md` | Final integrated project report |
| `reports/final_integrated_presentation_notes.md` | Short presentation-oriented notes |

## 9. Limitations
The data is simulated, so the project does not prove real-world business impact. It demonstrates an analytics workflow that could be adapted to real platform data.

The A/B module is a simulated evaluation, not a real deployed experiment. Its results are useful for showing how decision criteria could be structured, but they should not be presented as actual experimental evidence.

The predictive models are prototypes. Logistic Regression coefficients show association, not causation. Random Forest importance and performance metrics are also based on simulated patterns and may not generalize.

Nested cross-validation improves the validation design by reducing leakage and making model comparison fairer, but it cannot solve the limitations of simulated data. Future work would need real operational data, external validation, and stronger business guardrail review before any production use.

## 10. Next Steps
The immediate next step is to finalize the April 24 presentation story around a clear analytics progression: descriptive monitoring, diagnostic analysis, simulated experiment evaluation, and predictive validation.

Recommended preparation steps:

1. Select final figures and tables for slides, especially the KPI overview, anomaly summary, predictive model results, model comparison, and nested CV comparison.
2. Refine the speaking narrative so the nested CV update is presented as a methodological improvement rather than a dramatic performance breakthrough.
3. Keep the predictive task focused on high conversion performance unless there is time to validate a better target with real or more detailed data.
4. Improve documentation consistency across the dashboard, report outputs, and source scripts.
5. Prepare concise answers about simulated data, leakage prevention, coefficient interpretation, and why Random Forest is a benchmark rather than an automatic deployment choice.

## 11. Conclusion
The project now covers descriptive, diagnostic, experimental, and initial predictive analytics in one decision-support workflow. The dashboard and report outputs make the descriptive and diagnostic results easier to communicate, while the predictive modeling work adds a more advanced post-midterm component.

The nested cross-validation workflow is the most important modeling-method improvement. It tunes hyperparameters and selects features inside the validation process, computes target thresholds within each outer training fold, and compares Logistic Regression and Random Forest under the same framework.

Overall, the project has moved from dashboard-only monitoring toward a more complete simulated decision-support prototype for evaluating AI-generated advertising content.
