# Model Comparison Summary

## Metric Table
| Model | Accuracy | Precision | Recall | F1-score | ROC-AUC |
|---|---:|---:|---:|---:|---:|
| Logistic Regression | 0.6219 | 0.6082 | 0.7879 | 0.6865 | 0.6606 |
| Random Forest | 0.6133 | 0.6090 | 0.7371 | 0.6670 | 0.6536 |

## Comparison Interpretation
Logistic Regression is the stronger predictive model on both ROC-AUC and F1-score in this comparison.
- Logistic Regression remains the more interpretable model because its coefficients show directional associations for specific factor levels.
- Random Forest is better suited to capturing nonlinear interactions, but its importance scores are less straightforward for business explanation.
- For this simulated project, Logistic Regression is still the easiest model to present and defend in a classroom or business-facing setting.
- In this run, Random Forest did not outperform Logistic Regression on the key metrics, so the simpler and more interpretable model remains the stronger choice for this project.