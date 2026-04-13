# Predictive Factor Interpretation

## Scope
This note interprets every factor shown in the third panel of the current logistic-regression figure, `Top Logistic Coefficients`.

## Important Modeling Note
The logistic model uses one-hot encoding for all category levels without dropping a single omitted baseline category. That means these coefficients should be read as directional contributions after regularization, not as perfect one-level-versus-baseline causal effects. The supporting summary CSV therefore compares each categorical factor level against the other levels in the same feature family.

Supporting dataset summary: `reports/outputs/predictive_factor_supporting_summary.csv`

## 1. User Type New User

1. Factor name: `user type new user`
2. Association with high conversion performance: negative
3. Statistical meaning: In this logistic model, the coefficient is -0.5508, which means this factor is associated with lower log-odds of `high_conversion_performance`. The corresponding odds ratio is approximately 0.577. Because full one-hot encoding is used, the coefficient is best interpreted as directional support for this level rather than as a strict comparison to one omitted baseline category.
4. Dataset / business context: This factor flags segment-day observations dominated by new users who are still early in their relationship with the platform.
5. Plausible business explanation: New users usually have weaker habit strength, less trust in the platform, and more friction between click and conversion. They may browse because the content is interesting but still fail to complete the monetization step.
6. Signal type: Mostly structural and contextual, with an additional simulated-data component because the generator explicitly lowers conversion tendency for new users.
7. Practical optimization idea: Treat new-user traffic as a separate conversion funnel: simplify landing pages, shorten onboarding friction, and use lighter-weight first-conversion offers instead of assuming the same flow works for established users.
8. Caution: This does not mean new users are unimportant. It means they convert less efficiently in this simulated setup, and the effect is measured on aggregated segment-days rather than on individual users.

### Lightweight supporting evidence
- Support view used: new_user versus all other levels in user_type
- Factor-level average conversion rate: 6.43%
- Comparison average conversion rate: 7.52%
- Factor-level high-conversion positive rate: 36.94%
- Comparison positive rate: 57.48%
- Positive-rate rank within `user_type` levels: 3 of 3
- Interpretation note: Because all category levels are one-hot encoded without dropping a single baseline, this is best read as a directional contribution rather than a strict omitted-category contrast.

## 2. Traffic Source Recommendation

1. Factor name: `traffic source recommendation`
2. Association with high conversion performance: negative
3. Statistical meaning: In this logistic model, the coefficient is -0.2150, which means this factor is associated with lower log-odds of `high_conversion_performance`. The corresponding odds ratio is approximately 0.807. Because full one-hot encoding is used, the coefficient is best interpreted as directional support for this level rather than as a strict comparison to one omitted baseline category.
4. Dataset / business context: This factor represents traffic delivered through the recommendation feed rather than intent-led discovery.
5. Plausible business explanation: Recommendation traffic often carries broader reach but weaker immediate purchase intent. Users may click because content is engaging, not because they have already decided to convert.
6. Signal type: Primarily contextual, but partly simulated-data-specific because search traffic receives an explicit conversion advantage in the data generator, making recommendation look weaker by contrast.
7. Practical optimization idea: Keep recommendation traffic for scale, but improve pre-click relevance and post-click call-to-action design if conversion is the goal. It may be better suited to engagement growth than direct monetization.
8. Caution: A negative coefficient here is not a verdict that recommendation traffic is bad overall. It only says recommendation contexts are less associated with above-median conversion performance than the stronger alternatives in this model.

### Lightweight supporting evidence
- Support view used: recommendation versus all other levels in traffic_source
- Factor-level average conversion rate: 6.92%
- Comparison average conversion rate: 7.24%
- Factor-level high-conversion positive rate: 45.96%
- Comparison positive rate: 52.19%
- Positive-rate rank within `traffic_source` levels: 3 of 4
- Interpretation note: Because all category levels are one-hot encoded without dropping a single baseline, this is best read as a directional contribution rather than a strict omitted-category contrast.

## 3. Traffic Source Follow

1. Factor name: `traffic source follow`
2. Association with high conversion performance: negative
3. Statistical meaning: In this logistic model, the coefficient is -0.1933, which means this factor is associated with lower log-odds of `high_conversion_performance`. The corresponding odds ratio is approximately 0.824. Because full one-hot encoding is used, the coefficient is best interpreted as directional support for this level rather than as a strict comparison to one omitted baseline category.
4. Dataset / business context: This factor captures traffic from follow-based content exposure, where users are consuming content from creators or sources they already follow.
5. Plausible business explanation: Follow traffic may reflect loyalty and repeat consumption, but not necessarily immediate transactional intent. In this simulated project it also overlaps with a designed conversion dip for a follow-related anomaly window.
6. Signal type: Contextual, with a meaningful simulated-data component because the generated anomaly includes weaker conversion performance in a follow-related slice.
7. Practical optimization idea: Use follow traffic for retention and upsell design rather than assuming it is the best direct-conversion channel. Conversion-focused experiments on follow traffic should target clearer intent capture.
8. Caution: Part of this negative association may be absorbing the simulated anomaly pattern rather than representing a clean channel effect in a real platform.

### Lightweight supporting evidence
- Support view used: follow versus all other levels in traffic_source
- Factor-level average conversion rate: 6.84%
- Comparison average conversion rate: 7.27%
- Factor-level high-conversion positive rate: 45.27%
- Comparison positive rate: 52.42%
- Positive-rate rank within `traffic_source` levels: 4 of 4
- Interpretation note: Because all category levels are one-hot encoded without dropping a single baseline, this is best read as a directional contribution rather than a strict omitted-category contrast.

## 4. Traffic Source Nearby

1. Factor name: `traffic source nearby`
2. Association with high conversion performance: negative
3. Statistical meaning: In this logistic model, the coefficient is -0.1888, which means this factor is associated with lower log-odds of `high_conversion_performance`. The corresponding odds ratio is approximately 0.828. Because full one-hot encoding is used, the coefficient is best interpreted as directional support for this level rather than as a strict comparison to one omitted baseline category.
4. Dataset / business context: This factor corresponds to location-based or nearby-discovery traffic, which is often exploratory and context-dependent.
5. Plausible business explanation: Nearby traffic may generate useful discovery, but it can include users who are browsing locally relevant options without a strong immediate conversion decision. That can suppress conversion efficiency relative to search.
6. Signal type: Mostly contextual, with some simulated-data influence because only search gets an explicit conversion lift in the data generator.
7. Practical optimization idea: Improve local landing pages, geo-specific offers, and clearer next-step prompts if nearby traffic is expected to convert rather than simply drive discovery.
8. Caution: The effect is modest compared with the strongest factors, so it should be treated as a directional signal rather than a standalone strategy decision.

### Lightweight supporting evidence
- Support view used: nearby versus all other levels in traffic_source
- Factor-level average conversion rate: 6.92%
- Comparison average conversion rate: 7.24%
- Factor-level high-conversion positive rate: 46.12%
- Comparison positive rate: 52.14%
- Positive-rate rank within `traffic_source` levels: 2 of 4
- Interpretation note: Because all category levels are one-hot encoded without dropping a single baseline, this is best read as a directional contribution rather than a strict omitted-category contrast.

## 5. Experiment Group A

1. Factor name: `experiment group A`
2. Association with high conversion performance: negative
3. Statistical meaning: In this logistic model, the coefficient is -0.0282, which means this factor is associated with lower log-odds of `high_conversion_performance`. The corresponding odds ratio is approximately 0.972. Because full one-hot encoding is used, the coefficient is best interpreted as directional support for this level rather than as a strict comparison to one omitted baseline category.
4. Dataset / business context: This factor indicates the control version in the simulated A/B experiment.
5. Plausible business explanation: Its negative sign is mostly the mirror image of the positive B-group signal. Because the data generator directly gives group B a conversion improvement, group A naturally looks slightly less associated with high conversion performance.
6. Signal type: Mostly simulated-data-specific and experimental by design, not a naturally occurring structural business factor.
7. Practical optimization idea: Use it as supporting evidence that the experiment produced lift, but keep the interpretation tied to experiment evaluation and guardrail review rather than turning it into a broad user-segmentation insight.
8. Caution: This coefficient is small and should not be over-read. With full one-hot encoding, A and B appear as small opposing coefficients rather than a single clean treatment-vs-control contrast.

### Lightweight supporting evidence
- Support view used: A versus all other levels in experiment_group
- Factor-level average conversion rate: 7.08%
- Comparison average conversion rate: 7.23%
- Factor-level high-conversion positive rate: 49.20%
- Comparison positive rate: 52.07%
- Positive-rate rank within `experiment_group` levels: 2 of 2
- Interpretation note: Because all category levels are one-hot encoded without dropping a single baseline, this is best read as a directional contribution rather than a strict omitted-category contrast.

## 6. Traffic Source Search

1. Factor name: `traffic source search`
2. Association with high conversion performance: positive
3. Statistical meaning: In this logistic model, the coefficient is 0.5985, which means this factor is associated with higher log-odds of `high_conversion_performance`. The corresponding odds ratio is approximately 1.819. Because full one-hot encoding is used, the coefficient is best interpreted as directional support for this level rather than as a strict comparison to one omitted baseline category.
4. Dataset / business context: This factor captures users arriving from search, where demand and intent are usually clearer than in recommendation-led discovery.
5. Plausible business explanation: Search traffic often has the strongest purchase or action intent because users are actively looking for something. In the simulated generator, search also gets an explicit conversion advantage, which reinforces this pattern.
6. Signal type: Both structural/contextual and simulated-data-specific. The business logic is plausible, but the effect is also intentionally built into the synthetic data design.
7. Practical optimization idea: Prioritize high-quality landing experiences, keyword-to-content relevance, and monetization placement for search traffic because it is the most conversion-oriented segment in this prototype.
8. Caution: Search may convert better than other channels while still contributing less total volume. A strong coefficient does not automatically mean search should replace the rest of the traffic mix.

### Lightweight supporting evidence
- Support view used: search versus all other levels in traffic_source
- Factor-level average conversion rate: 7.95%
- Comparison average conversion rate: 6.89%
- Factor-level high-conversion positive rate: 65.19%
- Comparison positive rate: 45.78%
- Positive-rate rank within `traffic_source` levels: 1 of 4
- Interpretation note: Because all category levels are one-hot encoded without dropping a single baseline, this is best read as a directional contribution rather than a strict omitted-category contrast.

## 7. User Type Active User

1. Factor name: `user type active user`
2. Association with high conversion performance: positive
3. Statistical meaning: In this logistic model, the coefficient is 0.3186, which means this factor is associated with higher log-odds of `high_conversion_performance`. The corresponding odds ratio is approximately 1.375. Because full one-hot encoding is used, the coefficient is best interpreted as directional support for this level rather than as a strict comparison to one omitted baseline category.
4. Dataset / business context: This factor represents users with ongoing platform engagement rather than first-time or sporadic usage.
5. Plausible business explanation: Active users usually understand the product better, trust the experience more, and are less likely to drop off between click and monetization. They often respond better to optimized flows.
6. Signal type: Mostly structural and contextual. It fits the broader business logic that established users tend to convert more reliably than new users.
7. Practical optimization idea: Use active users as the most promising audience for monetization experiments, premium offers, and higher-friction conversion flows because they are more resilient in the funnel.
8. Caution: This is still an association, not proof that making someone more active will automatically cause the same conversion lift.

### Lightweight supporting evidence
- Support view used: active_user versus all other levels in user_type
- Factor-level average conversion rate: 7.53%
- Comparison average conversion rate: 6.97%
- Factor-level high-conversion positive rate: 58.49%
- Comparison positive rate: 46.70%
- Positive-rate rank within `user_type` levels: 1 of 3
- Interpretation note: Because all category levels are one-hot encoded without dropping a single baseline, this is best read as a directional contribution rather than a strict omitted-category contrast.

## 8. User Type Returning User

1. Factor name: `user type returning user`
2. Association with high conversion performance: positive
3. Statistical meaning: In this logistic model, the coefficient is 0.2335, which means this factor is associated with higher log-odds of `high_conversion_performance`. The corresponding odds ratio is approximately 1.263. Because full one-hot encoding is used, the coefficient is best interpreted as directional support for this level rather than as a strict comparison to one omitted baseline category.
4. Dataset / business context: This factor covers users who are not brand new, but are also not as consistently engaged as the active-user group.
5. Plausible business explanation: Returning users retain some familiarity and trust, so they tend to convert better than new users, even if they are not as reliable as highly active users.
6. Signal type: Mostly structural and contextual, with a reasonable business interpretation inside the simulated platform setting.
7. Practical optimization idea: Use returning users for reactivation or remarketing flows. They may be a practical middle segment for conversion optimization without the high acquisition friction of new users.
8. Caution: This signal is weaker than the active-user effect, so the model suggests a spectrum of user familiarity rather than a simple active-vs-not-active split.

### Lightweight supporting evidence
- Support view used: returning_user versus all other levels in user_type
- Factor-level average conversion rate: 7.52%
- Comparison average conversion rate: 6.98%
- Factor-level high-conversion positive rate: 56.46%
- Comparison positive rate: 47.72%
- Positive-rate rank within `user_type` levels: 2 of 3
- Interpretation note: Because all category levels are one-hot encoded without dropping a single baseline, this is best read as a directional contribution rather than a strict omitted-category contrast.

## 9. Experiment Group B

1. Factor name: `experiment group B`
2. Association with high conversion performance: positive
3. Statistical meaning: In this logistic model, the coefficient is 0.0296, which means this factor is associated with higher log-odds of `high_conversion_performance`. The corresponding odds ratio is approximately 1.030. Because full one-hot encoding is used, the coefficient is best interpreted as directional support for this level rather than as a strict comparison to one omitted baseline category.
4. Dataset / business context: This factor indicates the treatment version in the simulated A/B experiment.
5. Plausible business explanation: Its small positive sign is consistent with the experiment design: version B was simulated to improve conversion performance, so it slightly increases the probability of above-median conversion outcomes.
6. Signal type: Mostly simulated-data-specific and experimental by design rather than a naturally persistent business segment.
7. Practical optimization idea: Use this as one more consistency check between the predictive model and the separate A/B evaluation module. It helps show that the predictive prototype is directionally aligned with the experiment results.
8. Caution: Because this is a designed experiment effect, it should not be generalized as a universal causal truth. The standalone coefficient is small and should always be interpreted alongside guardrail metrics.

### Lightweight supporting evidence
- Support view used: B versus all other levels in experiment_group
- Factor-level average conversion rate: 7.23%
- Comparison average conversion rate: 7.08%
- Factor-level high-conversion positive rate: 52.07%
- Comparison positive rate: 49.20%
- Positive-rate rank within `experiment_group` levels: 1 of 2
- Interpretation note: Because all category levels are one-hot encoded without dropping a single baseline, this is best read as a directional contribution rather than a strict omitted-category contrast.

## 10. Session Uv

1. Factor name: `session uv`
2. Association with high conversion performance: positive
3. Statistical meaning: In this logistic model, the coefficient is 0.0259, which means this factor is associated with higher log-odds of `high_conversion_performance`. The corresponding odds ratio is approximately 1.026. Because `session_uv` is standardized before modeling, this effect should be read as the approximate direction of the odds change for a higher-value context, not as a direct raw-unit business lever.
4. Dataset / business context: This factor is the session-level user-volume measure included as a numeric context variable.
5. Plausible business explanation: Higher session UV may be associated with healthier or more active platform contexts, which can slightly improve the likelihood of above-median conversion performance. It can also proxy for demand concentration or stronger daily traffic conditions.
6. Signal type: Mostly contextual and relatively weak. It is plausible as a broad environment signal, but it is also the least cleanly interpretable factor among the top coefficients.
7. Practical optimization idea: Use session UV as a context variable for forecasting or scenario analysis, not as a direct optimization lever. It is more useful for explaining environment conditions than prescribing a single product change.
8. Caution: This is the weakest and most confounded factor in the chart. Higher session UV does not cause higher conversion on its own, and the effect is small after standardization.

### Lightweight supporting evidence
- Support view used: top quartile (651.00+) versus bottom quartile (397.00 and below)
- Factor-level average conversion rate: 7.27%
- Comparison average conversion rate: 7.03%
- Factor-level high-conversion positive rate: 53.49%
- Comparison positive rate: 48.05%
- Mean session UV for positive class vs negative class: 552.53 vs 536.34
- Interpretation note: This numeric coefficient is applied after standardization, so it represents the direction of the log-odds change for higher session UV rather than a binary category jump.
