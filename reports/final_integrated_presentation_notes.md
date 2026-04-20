# Final Integrated Presentation Notes

## 6 to 8 Minute Speaking Outline

### 1. Project Purpose: 45 seconds
This project builds a simulated decision-support workflow for evaluating AI-generated advertising content on a content platform. The decision being supported is how platform teams can monitor performance, detect problems, diagnose possible drivers, evaluate experiment groups, and begin predicting high conversion performance.

Key framing: this is a simulated analytics prototype, not proof of a deployed production strategy.

### 2. Data and Preprocessing: 60 seconds
The project uses `data/raw/content_platform_mock_data.csv` with 97,200 observations and 20 variables. The dataset includes 12 numeric variables, 8 categorical variables, and 1 time variable. The checks found 0 missing values and 0 duplicate rows.

The preprocessing workflow checks KPI validity, funnel consistency, and whether the dataset is clean enough for monitoring, dashboarding, and modeling.

### 3. Descriptive and Diagnostic Workflow: 90 seconds
The first part of the project is descriptive analytics:

- KPI monitoring tracks conversion, click, completion, report, interaction, and revenue-related metrics.
- Trend monitoring shows how performance changes over time.
- Anomaly alerts flag unusual metric movements.
- Segmented diagnosis breaks issues down by content category, traffic source, user type, and time segment.
- The simulated A/B module compares experiment groups while balancing performance and guardrail metrics.
- The dashboard prototype makes these outputs easier to review.

### 4. What Was Added After the Midterm: 90 seconds
After the midterm, the project added a predictive modeling layer. The task is binary classification of high conversion performance.

The initial Logistic Regression model predicts whether a row is likely to have conversion performance at or above the training-set median. It uses interpretable features such as content category, traffic source, user type, city tier, experiment group, time variables, content supply, session UV, and weekend indicator.

The initial Logistic Regression metrics were:

- Accuracy: 0.6219
- Precision: 0.6082
- Recall: 0.7879
- F1-score: 0.6865
- ROC-AUC: 0.6606

How to explain the figure:

- The ROC curve shows separation ability across thresholds.
- The confusion matrix shows correct and incorrect high-performance classifications.
- The coefficient chart shows which factors are positively or negatively associated with high conversion performance.

### 5. Factor Interpretation: 75 seconds
The coefficient interpretation turns the model into business language.

Positive factors include search traffic, active users, returning users, experiment group B, and session UV. These factors likely reflect stronger intent, greater familiarity, or healthier demand contexts in the simulated data.

Negative factors include new users, recommendation traffic, follow traffic, nearby traffic, and experiment group A. These may reflect lower intent, discovery-oriented browsing, or less conversion-ready user contexts.

Important caution: these are associations in simulated data, not causal proof.

### 6. Logistic Regression vs Random Forest: 75 seconds
Random Forest was added as a benchmark because it can capture nonlinear relationships. In the initial split comparison, Logistic Regression was slightly stronger overall:

- Logistic Regression ROC-AUC: 0.6606
- Random Forest ROC-AUC: 0.6536
- Logistic Regression F1-score: 0.6865
- Random Forest F1-score: 0.6670

The interpretation is that Logistic Regression is easier to explain and slightly better in the initial comparison. Random Forest is still useful as a benchmark, but it is not clearly better here.

### 7. Nested Cross-Validation Update: 90 seconds
This is the most important methodological improvement. The earlier train/test split was only an initial baseline. Nested CV gives a more reliable estimate of general predictive performance.

Setup:

- 3 outer shuffled KFold folds estimate generalization performance.
- 3 inner StratifiedKFold folds tune hyperparameters.
- SelectKBest feature selection is inside the pipeline to avoid leakage.
- The high-conversion target threshold is computed only from the outer training fold.
- Logistic Regression and Random Forest use the same outer folds.

Nested CV average metrics:

| Model | Accuracy | Precision | Recall | F1-score | ROC-AUC |
|---|---:|---:|---:|---:|---:|
| Logistic Regression | 0.5940 | 0.5767 | 0.7126 | 0.6372 | 0.6383 |
| Random Forest | 0.5939 | 0.5724 | 0.7458 | 0.6477 | 0.6367 |

Conclusion: Logistic Regression has slightly better ROC-AUC, Random Forest has slightly better recall and F1-score, and the difference is small. The main value is the improved validation logic.

### 8. Limitations and Final Takeaway: 45 seconds
The key limitation is that the data is simulated. The A/B module is simulated, the predictive model is a prototype, and coefficients show association rather than causation.

Final takeaway: the project now covers descriptive, diagnostic, experimental, and initial predictive analytics. The nested CV update makes the model comparison more rigorous and moves the project toward a more complete decision-support workflow.

## Short Q&A Talking Points

- If asked why Logistic Regression matters: it is interpretable and gives factor-level explanations.
- If asked why Random Forest was included: it provides a nonlinear benchmark.
- If asked why nested CV was added: it prevents model selection from being evaluated on the same data used to tune the model.
- If asked whether this is production-ready: no, it is a simulated prototype and would need real data validation.
- If asked what changed after the midterm: predictive modeling, factor interpretation, Random Forest comparison, and nested CV validation were added.
