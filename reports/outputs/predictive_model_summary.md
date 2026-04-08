# Lightweight Predictive Model Summary

## Modeling Task
- Task type: binary classification
- Target: `high_conversion_performance`
- Label definition: 1 if row-level `conversion_rate` >= training median (0.070312); otherwise 0
- Model: logistic regression
- Split: time-based train/test split using the earlier 78% of dates for training and the latest 22% for testing

## Feature Set
- Categorical features: content_category, traffic_source, user_type, city_tier, experiment_group, hour_bucket, week_day
- Numeric features: content_supply_cnt, session_uv, is_weekend
- Excluded downstream fields: click, conversion_cnt, view_complete, report_cnt, monetization_revenue, and other direct outcome columns

## Data Split
- Training rows: 75,600
- Test rows: 21,600
- Training positive rate: 0.501
- Test positive rate: 0.525

## Evaluation
- Accuracy: 0.6219
- Precision: 0.6082
- Recall: 0.7879
- F1-score: 0.6865
- ROC-AUC: 0.6606

## Interpretation
- This model predicts whether a segment-day observation is likely to have relatively strong conversion performance, not absolute business value or causal impact.
- Positive coefficients indicate segment contexts associated with a higher probability of above-median conversion performance in the simulated data.
- Negative coefficients indicate contexts associated with lower predicted conversion performance.

## Top Positive Coefficients
- traffic source search: 0.5985
- user type active user: 0.3186
- user type returning user: 0.2335
- experiment group B: 0.0296
- session uv: 0.0259

## Top Negative Coefficients
- user type new user: -0.5508
- traffic source recommendation: -0.2150
- traffic source follow: -0.1933
- traffic source nearby: -0.1888
- experiment group A: -0.0282

## Limitations
- The data is simulated and the target is threshold-based, so this is a lightweight predictive prototype rather than a production-ready model.
- The model should be interpreted as a presentation-friendly extension beyond descriptive analytics, not as a validated deployment decision engine.
- Because the source data is aggregated at the segment-day level, the model predicts segment performance patterns rather than individual content outcomes.