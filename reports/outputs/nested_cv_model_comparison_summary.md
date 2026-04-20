# Nested Cross-Validation Model Comparison Summary

## Why This Update Was Added
The earlier predictive comparison used a single train/test split as an initial baseline. This nested cross-validation workflow provides a more reliable estimate of general predictive performance by tuning hyperparameters and selecting features inside the validation process.

## Nested CV Setup
- Dataset: `data\raw\content_platform_mock_data.csv`
- Task: binary classification of `high_conversion_performance`
- Target threshold: computed separately from the training rows of each outer fold, using the median row-level conversion rate in that outer training set
- Outer CV: 3-fold shuffled KFold, shared by both models
- Inner CV: 3-fold StratifiedKFold inside each outer training fold
- Tuning metric: ROC-AUC in the inner CV
- Feature selection: `SelectKBest(f_classif)` inside each model pipeline
- Leakage control: downstream variables such as click, conversion count, view completion count, report count, monetization revenue, and row-level conversion rate are excluded from the feature matrix

## Average Outer-Fold Metrics
| Model | Accuracy | Precision | Recall | F1-score | ROC-AUC |
|---|---:|---:|---:|---:|---:|
| Logistic Regression | 0.5940 | 0.5767 | 0.7126 | 0.6372 | 0.6383 |
| Random Forest | 0.5939 | 0.5724 | 0.7458 | 0.6477 | 0.6367 |

## Metric Standard Deviations Across Outer Folds
| Model | Accuracy SD | Precision SD | Recall SD | F1-score SD | ROC-AUC SD |
|---|---:|---:|---:|---:|---:|
| Logistic Regression | 0.0027 | 0.0079 | 0.0232 | 0.0046 | 0.0034 |
| Random Forest | 0.0042 | 0.0059 | 0.0011 | 0.0041 | 0.0029 |

## Best Hyperparameters Selected by Inner CV
### Logistic Regression
- Outer fold 1: `{"model__C": 0.1, "model__penalty": "l1", "select__k": 10}`
- Outer fold 2: `{"model__C": 0.1, "model__penalty": "l1", "select__k": 10}`
- Outer fold 3: `{"model__C": 0.1, "model__penalty": "l1", "select__k": 10}`
- Most common selected setting: `{"model__C": 0.1, "model__penalty": "l1", "select__k": 10}`

### Random Forest
- Outer fold 1: `{"model__max_depth": 8, "model__max_features": "sqrt", "model__min_samples_leaf": 20, "model__n_estimators": 80, "select__k": "all"}`
- Outer fold 2: `{"model__max_depth": 8, "model__max_features": "sqrt", "model__min_samples_leaf": 50, "model__n_estimators": 80, "select__k": "all"}`
- Outer fold 3: `{"model__max_depth": 8, "model__max_features": "sqrt", "model__min_samples_leaf": 20, "model__n_estimators": 80, "select__k": "all"}`
- Most common selected setting: `{"model__max_depth": 8, "model__max_features": "sqrt", "model__min_samples_leaf": 20, "model__n_estimators": 80, "select__k": "all"}`

## Model Comparison Conclusion
- Best average ROC-AUC: Logistic Regression
- Best average F1-score: Random Forest
- The models split leadership across metrics, so the comparison should be framed as a tradeoff rather than a single winner.
- Logistic Regression remains the more interpretable model because its coefficients can be explained as directional associations.
- Random Forest remains useful as a flexible benchmark, but stronger performance should still be weighed against lower explainability.
- Results are still based on simulated, aggregated platform data and should not be presented as production deployment evidence.