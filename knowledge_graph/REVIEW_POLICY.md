# Knowledge Graph 入库审核标准

> 不是所有 JSON 都能进。三级审核，自动+人工。

## 质量等级

| 等级 | 标签 | 标准 | 自动检查 | 人工审核 |
|------|------|------|---------|---------|
| 🥇 **验证** | `verified` | 被另一个独立用户复现 | 无 | 需要 ≥1 个独立复现报告 |
| 🥈 **通过** | `accepted` | 自动检查全过 + 人工过 | metrics.py ≥ 70% + schema 校验 | 审查者抽查 1-2 条引用 |
| 🥉 **提交** | `submitted` | PR 已开，格式完整 | schema 校验通过 | 无（等审查） |
| ❌ **退回** | `rejected` | schema 不通过 或 数据明显伪造 | schema 校验失败 | — |

## 自动检查（PR 触发，GitHub Actions 可跑）

```
1. JSON schema 校验         → validation/validate_schema.py
2. 结构质量评分              → benchmarks/metrics.py ≥ 70%
3. 引用真实性抽查（DOI解析）  → 随机抽 2 个 DOI，验证格式有效
4. contributor 字段存在      → github 字段必须有（PR 来源）
```

全部通过 → 自动标 `accepted`，等人工抽查后合入。
任一失败 → 标 `submitted`，PR comment 里写原因。

## 人工审核清单（3 分钟/份）

```
[ ] nodes 里有没有 ≥1 个 confidence ≥ 0.6 的条目？（不是纯 speculation）
[ ] surviving_claims 和 killed_claims 都不为空？（诚实记录失败）
[ ] lessons 里有没有 ≥1 条？（不是"跑完了，一切顺利"）
[ ] 抽查 1 个 DOI 是否真实存在？
[ ] 如果没有 ORCID → 提醒用户注册
```

## 不接受的

- 没有 derivation_chain（纯 LLM 幻觉，没有经过 AB 推导）
- surviving_claims 为空且 killed_claims 为空（什么都没发现，但没记录）
- 所有 confidence ≥ 0.95（不诚实——科学没有 100%）
- 引用全是"众所周知"没有具体 DOI
