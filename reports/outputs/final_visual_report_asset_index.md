# Final Visual Report Asset Index

This index lists the figures and tables used in `reports/final_visual_project_report.md`.

## Figures

| Asset Path | Section | Purpose | One-Line Interpretation |
|---|---|---|---|
| `reports/figures/dashboard_overview.png` | Section 3 | Dashboard overview | Shows the project as a reviewable dashboard workflow rather than raw files. |
| `reports/figures/trend_monitoring.png` | Section 3 | KPI trend monitoring | Shows how KPI movement can be monitored over time. |
| `reports/figures/anomaly_detection.png` | Section 3 | Anomaly alerts | Highlights unusual KPI behavior for follow-up review. |
| `reports/figures/segmented_analysis.png` | Section 3 | Segmented diagnosis | Breaks performance patterns into business-relevant segments. |
| `reports/figures/ab_test_comparison.png` | Section 3 | Simulated A/B evaluation | Compares experiment groups on platform performance metrics. |
| `reports/figures/predictive_model_results.png` | Section 4 | Logistic Regression results | Shows ROC, confusion matrix, and top coefficients for the initial predictive model. |
| `reports/figures/random_forest_model_results.png` | Section 6 | Random Forest results | Summarizes the nonlinear benchmark model and its classification behavior. |
| `reports/figures/model_comparison_results.png` | Section 6 | Initial model comparison | Compares Logistic Regression and Random Forest on the initial split. |
| `reports/figures/nested_cv_model_comparison.png` | Section 7 | Nested CV comparison | Shows the fairer validation comparison across Logistic Regression and Random Forest. |

## Tables

| Asset Path | Section | Purpose | One-Line Interpretation |
|---|---|---|---|
| `reports/outputs/dataset_summary.csv` | Section 2 | Dataset summary | Confirms 97,200 observations, 20 variables, 0 missing values, and 0 duplicate rows. |
| `reports/outputs/variable_categories.csv` | Section 2 | Variable categories | Documents time, categorical, and numeric variables used in the project. |
| `reports/outputs/missing_values.csv` | Section 2 | Missing-value detail | Confirms each variable has 0 missing values. |
| `reports/outputs/kpi_summary.csv` | Section 3 | KPI summary | Summarizes exposure, click, completion, conversion, CTR, and conversion rate. |
| `reports/outputs/ab_test_summary.csv` | Section 3 | Simulated A/B summary | Compares groups A and B on exposure, clicks, conversions, CTR, and conversion rate. |
| `reports/outputs/predictive_model_metrics.csv` | Section 4 | Logistic Regression metrics | Reports the initial split performance for the Logistic Regression prototype. |
| `reports/outputs/model_comparison_metrics.csv` | Section 6 | Initial model comparison metrics | Compares Logistic Regression and Random Forest on the initial split. |
| `reports/outputs/nested_cv_model_comparison_metrics.csv` | Section 7 | Nested CV metrics | Reports fold-level and average nested CV performance for both models. |

## Report Files

| Asset Path | Purpose |
|---|---|
| `reports/final_visual_project_report.md` | Visual-rich final project report with embedded figures and compact tables. |
| `reports/final_visual_presentation_script.md` | About 8-minute speaking script based on the visual report. |
| `reports/outputs/final_visual_report_asset_index.md` | Asset index for figures and tables used in the visual report. |
