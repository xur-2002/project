# Step 2 数据表结构设计

本项目使用一张日级业务聚合表，粒度为：
日期 × 内容类目 × 流量来源 × 用户类型 × 实验组别 × 时段。

## 表名
content_platform_daily_fact

## 字段字典

| 字段名 | 字段类型 | 业务含义 | 示例值 | 设计理由 |
|---|---|---|---|---|
| date | date | 统计日期 | 2026-01-15 | 支持日级趋势监控与异常定位 |
| week_day | string | 星期信息 | Monday | 区分工作日与周末季节性波动 |
| hour_bucket | string | 时段分层 | evening | 支持时段归因，定位集中异常时窗 |
| content_category | string | 内容类目 | entertainment | 识别类目结构变化与质量差异 |
| traffic_source | string | 流量来源 | recommendation | 用于定位推荐/搜索/关注等渠道问题 |
| user_type | string | 用户类型 | new_user | 新老用户行为差异归因 |
| city_tier | string | 城市层级 | tier1 | 分析商业化与内容偏好地区差异 |
| experiment_group | string | 实验分组 | B | A/B Test 核心分组字段 |
| content_supply_cnt | int | 当日供给内容量 | 1450 | 用于解释质量波动是否由供给规模变化驱动 |
| exposure | int | 曝光次数 | 125000 | 所有率类指标分母基础 |
| click | int | 点击次数 | 10250 | 计算 CTR，衡量首跳吸引力 |
| view_complete | int | 完播次数 | 5120 | 衡量内容消费质量 |
| like_cnt | int | 点赞次数 | 2310 | 互动质量指标之一 |
| comment_cnt | int | 评论次数 | 580 | 互动深度指标 |
| share_cnt | int | 分享次数 | 220 | 传播意愿指标 |
| report_cnt | int | 举报次数 | 125 | 生态风险护栏指标 |
| conversion_cnt | int | 转化次数 | 760 | 商业化结果指标 |
| avg_watch_seconds | float | 人均观看时长 | 31.6 | 体验质量补充指标 |
| monetization_revenue | float | 当日变现收入 | 28650.5 | 商业结果指标补充 |
| session_uv | int | 访问用户数 | 45200 | 观察流量规模变化 |

## 口径补充
1. interaction_cnt = like_cnt + comment_cnt + share_cnt
2. CTR = click / exposure
3. 完播率 = view_complete / click
4. 互动率 = interaction_cnt / click
5. 举报率 = report_cnt / exposure
6. 转化率 = conversion_cnt / click

## 本步产出
- 完成支持监控、归因、A/B Test 的完整字段设计。
- 定义统一口径，避免后续分析口径漂移。
