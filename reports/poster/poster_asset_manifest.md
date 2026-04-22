# Poster Asset Manifest

## Main Report Source Used
- Primary: `reports/final_visual_project_report.md`
- Cross-check: `reports/final_integrated_project_report.md`

## Figures Included
- `reports/figures/predictive_model_results.png` - chosen as the main predictive figure because it combines ROC curve, confusion matrix, and top Logistic Regression coefficients in one panel.
- `reports/figures/model_comparison_results.png` - chosen to summarize the initial Logistic Regression vs Random Forest comparison visually.
- `reports/figures/nested_cv_model_comparison.png` - chosen as the strongest validation figure because it reflects nested cross-validation rather than a single split.
- `reports/figures/dashboard_overview.png` - chosen to show the descriptive decision-support dashboard layer.
- `reports/figures/anomaly_detection.png` - chosen to show KPI alerting/monitoring behavior.
- `reports/figures/segmented_analysis.png` - chosen to show diagnostic segmentation.
- `reports/figures/ab_test_comparison.png` - chosen to show the simulated experiment comparison layer.

Similar assets not selected for main emphasis:
- `reports/figures/random_forest_model_results.png` was not emphasized because the poster prioritizes the more interpretable Logistic Regression figure and compact comparison tables.
- `reports/figures/trend_monitoring.png` was not included because the descriptive section already contains dashboard, anomaly, segmentation, and A/B visuals; the poster needed space for predictive validation.

## Tables Used
- Dataset summary table from `reports/outputs/dataset_summary.csv`.
- Simulated A/B summary from `reports/outputs/ab_test_summary.csv`.
- Initial model comparison metrics from `reports/outputs/model_comparison_metrics.csv`.
- Nested CV mean metrics from `reports/outputs/nested_cv_model_comparison_metrics.csv`.
- Logistic Regression metric badges from `reports/outputs/predictive_model_metrics.csv`.

## Final Key Conclusions Included
- The workflow integrates descriptive, diagnostic, experimental, and predictive analytics.
- Search traffic and established user types are more associated with high conversion performance in the simulated model.
- Logistic Regression remains the most interpretable predictive baseline.
- Random Forest is a useful benchmark but is not clearly better overall.
- Nested CV improves validation rigor and reduces the risk of over-optimistic evaluation.
- The data and A/B module are simulated, so results are prototype evidence rather than real-world causal proof.

## Quality Checks Intended
- Poster language: English only.
- Poster page size: 24 inches by 36 inches, portrait, set through CSS `@page` and fixed poster dimensions.
- Bottom-right note included: "Created with assistance from ChatGPT".
- GitHub reference included: https://github.com/xur-2002/project
