# Random Forest Predictive Model Summary

## Modeling Task
- Task type: binary classification
- Target: `high_conversion_performance`
- Label definition: 1 if row-level `conversion_rate` >= training median (0.070312); otherwise 0
- Model: Random Forest classifier
- Split: same time-based train/test split used in the Logistic Regression prototype

## Feature Set
- Categorical features: content_category, traffic_source, user_type, city_tier, experiment_group, hour_bucket, week_day
- Numeric features: content_supply_cnt, session_uv, is_weekend
- Same target definition and same train/test logic as the Logistic Regression model

## Data Split
- Training rows: 75,600
- Test rows: 21,600
- Training positive rate: 0.501
- Test positive rate: 0.525

## Evaluation
- Accuracy: 0.6133
- Precision: 0.6090
- Recall: 0.7371
- F1-score: 0.6670
- ROC-AUC: 0.6536

## Top Feature Importances
- user type new user: 0.2513
- traffic source search: 0.1991
- session uv: 0.0862
- content supply cnt: 0.0840
- user type active user: 0.0785
- user type returning user: 0.0678
- traffic source recommendation: 0.0384
- traffic source follow: 0.0303
- traffic source nearby: 0.0299
- hour bucket morning: 0.0080

## Interpretation
- Random Forest can absorb nonlinear patterns and interactions that Logistic Regression cannot express directly.
- Its feature importance values are useful for ranking signals, but they are less transparent than logistic coefficients when explaining direction and business meaning.

## Limitations
- This remains a lightweight predictive prototype trained on simulated, aggregated segment-day data.
- Better predictive performance does not automatically make the model the best business explanation tool.
- Feature importance does not imply causality and should not be presented as proof of intervention effect.