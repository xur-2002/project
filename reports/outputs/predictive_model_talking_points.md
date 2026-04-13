# Predictive Model Talking Points

## How to explain the logistic coefficient chart
- Positive bars mean the model associates that factor with a higher probability of above-median conversion performance.
- Negative bars mean the model associates that factor with a lower probability of above-median conversion performance.
- Because all category levels were one-hot encoded instead of dropping one clean baseline, the coefficients should be explained as directional associations, not as strict causal effects against a single omitted category.

## How to explain why some factors promote or suppress conversion
- The strongest positive signal is `traffic source search`, which fits the project story that higher-intent contexts tend to produce better conversion outcomes.
- The strongest negative signal is `user type new user`, which fits the idea that lower-familiarity or lower-intent contexts convert less efficiently.
- The A/B group coefficients should be explained carefully: they are small and mainly confirm the simulated treatment effect already seen in the A/B evaluation module.
- `session_uv` is best explained as a weak context variable, not as a direct causal business lever.

## How to explain Random Forest vs Logistic Regression
- Logistic Regression metrics: accuracy 0.6219, F1 0.6865, ROC-AUC 0.6606.
- Random Forest metrics: accuracy 0.6133, F1 0.6670, ROC-AUC 0.6536.
- Logistic Regression is easier to explain because each coefficient has a direction and a concrete business narrative.
- Random Forest can capture more complicated patterns, so it is useful as a benchmark even if it is harder to explain.
- For presentation, the best framing is: Random Forest was tested as a benchmark, but Logistic Regression remained the stronger model overall because it stayed more interpretable and slightly outperformed the benchmark.