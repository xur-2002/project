# Final Visual Presentation Script

## Opening: Project Motivation
Good morning. My project is about building a data-driven decision-support workflow for evaluating AI-generated advertising content on a simulated content platform.

The business problem is that a platform team needs to monitor performance, detect abnormal KPI movement, understand possible drivers, evaluate experiment variants, and eventually estimate which content or traffic contexts are more likely to produce high conversion performance.

The important framing is that this is a simulated analytics prototype. I am not claiming that the results prove a real business strategy. The goal is to show a complete and realistic analytics workflow.

## Data and Preprocessing
The dataset is `data/raw/content_platform_mock_data.csv`. It contains 97,200 observations and 20 variables. There are 12 numeric variables, 8 categorical variables, and 1 time variable.

The preprocessing checks found 0 missing values and 0 duplicate rows. I also checked KPI validity and funnel consistency, because the rest of the project depends on rates such as click-through rate, conversion rate, completion rate, and report rate.

So before any modeling, the project establishes that the simulated dataset is clean enough for monitoring, dashboarding, and prototype predictive analysis.

Transition: After the data checks, the first part of the project is descriptive analytics.

## Dashboard and Descriptive Analytics
In the visual report, Figure 1 shows the dashboard overview. This is the operating layer of the project. Instead of looking at raw rows, the dashboard organizes the KPIs, trends, anomaly alerts, segmented diagnosis, and experiment evaluation.

Figure 2 shows KPI trend monitoring. This helps answer whether performance movement is temporary or sustained over time.

Figure 3 shows anomaly detection. The purpose is not to automatically prove a root cause. The purpose is to flag unusual KPI movement so that the analyst knows where to investigate.

Figure 4 shows segmented analysis. This is the diagnostic layer. It breaks performance patterns down by business dimensions like traffic source, user type, content category, and time bucket.

Figure 5 shows the simulated A/B comparison. This part of the project demonstrates how an experiment review could compare performance metrics while still considering tradeoffs. Because this is simulated data, I frame it as an evaluation prototype rather than a real deployed experiment.

Transition: After building this monitoring and diagnostic foundation, I added predictive modeling after the midterm.

## Predictive Modeling Prototype
The predictive task is binary classification of high conversion performance. A row is labeled as high conversion performance if its conversion rate is at or above the training-set median.

The initial model is Logistic Regression. I chose Logistic Regression because it is lightweight, interpretable, and easy to explain in a business setting.

The model uses features such as content category, traffic source, user type, city tier, experiment group, time variables, content supply, session UV, and weekend indicator. I excluded downstream leakage variables like click count, conversion count, report count, view completion count, monetization revenue, and direct outcome-rate variables.

Figure 6 shows the initial Logistic Regression results. The ROC curve shows the model's ability to separate high-conversion and lower-conversion rows across thresholds. The confusion matrix shows correct and incorrect classifications. The coefficient chart shows which factors have positive or negative associations with high conversion performance.

The initial Logistic Regression metrics were accuracy 0.6219, precision 0.6082, recall 0.7879, F1-score 0.6865, and ROC-AUC 0.6606.

These results suggest that the model captures some useful signal in the simulated data, but it is still only a lightweight prototype.

Transition: The most presentation-friendly part of Logistic Regression is the coefficient interpretation.

## Factor Interpretation
The coefficient chart helps translate the model into business language.

Positive factors include search traffic, active users, returning users, experiment group B, and session UV. A practical interpretation is that search traffic may reflect stronger user intent, and active or returning users may be more familiar with the platform.

Negative factors include new users, recommendation traffic, follow traffic, nearby traffic, and experiment group A. These factors may represent less conversion-ready contexts, discovery-oriented browsing, or segments where ad content needs better matching.

The business action is not to blindly optimize based on coefficients. Instead, the coefficients create hypotheses. For example, search traffic may deserve high-intent landing page optimization, while new-user traffic may need simpler onboarding or lighter calls to action.

The key caution is that coefficients are associations in simulated data. They are not causal proof.

Transition: To check whether a more flexible model performs better, I added a Random Forest benchmark.

## Logistic Regression vs Random Forest
Figure 7 shows the Random Forest results. Random Forest can capture nonlinear patterns and interactions, so it is useful as a benchmark.

Figure 8 compares Logistic Regression and Random Forest on the initial split. Logistic Regression had ROC-AUC 0.6606 and F1-score 0.6865. Random Forest had ROC-AUC 0.6536 and F1-score 0.6670.

So in the initial comparison, Logistic Regression was slightly stronger overall and easier to explain. Random Forest was useful as a benchmark, but it was not clearly better.

Transition: My professor's feedback was that the project needed more proper training and test logic. That led to the nested cross-validation update.

## Nested Cross-Validation Validation
Figure 9 is the most important model validation figure in the final report.

The earlier train/test split was only an initial baseline. Nested cross-validation is stronger because it separates model evaluation from model tuning.

The outer loop estimates generalization performance. The inner loop tunes hyperparameters and performs feature selection. I used 3 outer shuffled KFold folds and 3 inner StratifiedKFold folds. Both Logistic Regression and Random Forest use the same outer folds.

Feature selection uses SelectKBest inside the pipeline, so feature selection is learned only from training folds. Also, the high-conversion threshold is computed only from each outer training fold. This avoids leakage from the validation fold.

In nested CV, Logistic Regression had average ROC-AUC 0.6383 and F1-score 0.6372. Random Forest had average ROC-AUC 0.6367 and F1-score 0.6477.

The interpretation is a tradeoff. Logistic Regression has slightly better ROC-AUC. Random Forest has slightly better recall and F1-score. The difference is small, so there is no single definitive winner.

The main improvement is not a dramatic increase in metrics. The main improvement is that the validation logic is more rigorous and fair.

Transition: I will close with limitations and next steps.

## Limitations and Next Steps
The biggest limitation is that the data is simulated. The A/B evaluation is simulated, the predictive models are prototypes, and the coefficients show association rather than causation.

Nested cross-validation improves the model comparison, but it does not solve the limitation that this is not real operational data.

The next steps are to finalize the presentation figures, keep the predictive task focused and leakage-safe, improve documentation consistency, and prepare a clear final story.

## Final Takeaway
The project started as a monitoring and diagnosis workflow. It now includes descriptive analytics, diagnostic analytics, simulated experimental evaluation, and initial predictive modeling.

The latest update adds nested cross-validation, which makes the model comparison more rigorous. So the project has moved from monitoring-only toward a more complete decision-support workflow for evaluating AI-generated advertising content.

## Short Q&A Backup Points
- Why simulated data? The project is designed to demonstrate an end-to-end analytics workflow when real platform data is not available.
- Why Logistic Regression? It is lightweight, interpretable, and gives coefficients that can be explained in business language.
- Why add Random Forest? It provides a nonlinear benchmark to test whether a more flexible model clearly improves performance.
- What does nested CV add? It separates model tuning from model evaluation and gives a more reliable estimate of general performance.
- What do the coefficients mean? They show associations with high conversion performance, not causal effects.
- Is the model production-ready? No. It is a simulated predictive prototype and would need real data validation.
- What limitations remain? Simulated data, no real deployed experiment, and no external validation.
- What is the main final improvement? The project now has more rigorous validation logic through nested cross-validation.
