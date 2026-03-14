# Step 5 异常监控分析

## 方法说明
1. 按日聚合核心指标并计算 CTR、完播率、互动率、举报率、转化率。
2. 使用前 7 日移动均值作为基线，结合标准差阈值与偏离比例识别异常。
3. 全局规则：|当日值-基线| > 2.5*std 且偏离比例 > 12%。
4. 分层规则：|当日值-基线| > 2.0*std 且偏离比例 > 8%。

## 异常识别结果
共识别异常点 24 个。

| 日期 | 作用域 | 维度 | 分层 | 指标 | 当日值 | 基线 | 变动% | 业务判断 |
|---|---|---|---|---:|---:|---:|---:|---|
| 2025-12-23 | segment | content_category | food | report_rate | 0.0020 | 0.0018 | 10.48% | 生态风险抬升，建议联动审核策略和问题类目治理。 |
| 2026-01-20 | segment | content_category | entertainment | ctr | 0.0944 | 0.1081 | -12.64% | 点击吸引力下降，需优先排查推荐内容供给质量。 |
| 2026-01-20 | segment | traffic_source | recommendation | ctr | 0.0995 | 0.1085 | -8.30% | 点击吸引力下降，需优先排查推荐内容供给质量。 |
| 2026-01-21 | segment | content_category | entertainment | ctr | 0.0949 | 0.1061 | -10.59% | 点击吸引力下降，需优先排查推荐内容供给质量。 |
| 2026-01-29 | segment | content_category | entertainment | ctr | 0.1080 | 0.0948 | 13.91% | 指标偏离基线，建议进入分层归因排查。 |
| 2026-01-29 | segment | traffic_source | recommendation | ctr | 0.1085 | 0.0992 | 9.38% | 指标偏离基线，建议进入分层归因排查。 |
| 2026-01-30 | segment | content_category | entertainment | ctr | 0.1076 | 0.0967 | 11.29% | 指标偏离基线，建议进入分层归因排查。 |
| 2026-02-01 | segment | content_category | food | report_rate | 0.0020 | 0.0018 | 12.59% | 生态风险抬升，建议联动审核策略和问题类目治理。 |
| 2026-02-01 | segment | traffic_source | recommendation | ctr | 0.1126 | 0.1032 | 9.11% | 指标偏离基线，建议进入分层归因排查。 |
| 2026-02-01 | segment | traffic_source | search | report_rate | 0.0021 | 0.0019 | 10.10% | 生态风险抬升，建议联动审核策略和问题类目治理。 |
| 2026-02-05 | overall | all | all | report_rate | 0.0023 | 0.0020 | 15.56% | 生态风险抬升，建议联动审核策略和问题类目治理。 |
| 2026-02-05 | segment | content_category | food | report_rate | 0.0028 | 0.0019 | 53.37% | 生态风险抬升，建议联动审核策略和问题类目治理。 |
| 2026-02-05 | segment | traffic_source | search | report_rate | 0.0028 | 0.0020 | 40.70% | 生态风险抬升，建议联动审核策略和问题类目治理。 |
| 2026-02-13 | segment | content_category | food | report_rate | 0.0018 | 0.0028 | -38.02% | 指标偏离基线，建议进入分层归因排查。 |
| 2026-02-13 | segment | traffic_source | search | report_rate | 0.0020 | 0.0027 | -25.53% | 指标偏离基线，建议进入分层归因排查。 |
| 2026-02-14 | segment | traffic_source | search | report_rate | 0.0020 | 0.0026 | -22.57% | 指标偏离基线，建议进入分层归因排查。 |
| 2026-02-15 | segment | traffic_source | follow | conversion_rate | 0.0620 | 0.0710 | -12.65% | 商业转化效率下滑，需检查链路与人群匹配。 |
| 2026-02-16 | segment | traffic_source | follow | conversion_rate | 0.0613 | 0.0694 | -11.62% | 商业转化效率下滑，需检查链路与人群匹配。 |
| 2026-02-17 | segment | user_type | new_user | conversion_rate | 0.0589 | 0.0647 | -9.02% | 商业转化效率下滑，需检查链路与人群匹配。 |
| 2026-02-23 | segment | traffic_source | follow | conversion_rate | 0.0717 | 0.0622 | 15.21% | 指标偏离基线，建议进入分层归因排查。 |

## 下一步
基于异常时间窗进入内容类目、流量来源、用户类型分层归因分析。