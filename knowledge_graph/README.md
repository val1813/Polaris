# Knowledge Graph — 发现记忆库

> 每个课题收官后的结构化遗产 = 一份 JSON。**这是 Polaris 的论文格式。**
> 完整 Schema → `validation/schema.md`

## 提交什么

跑完课题后，GATE 7 自动产出 JSON。提 PR 放到这个目录。

文件名：`[课题ID]_v[版本]_[日期].json`  例：`LP27_v1.0_20260604.json`

## 格式速查

```json
{
  "project": {
    "id": "LP27", "title": "...", "domain": "...",
    "contributor": {
      "orcid": "0000-0002-1825-0097",   // 学术身份证（免费：orcid.org）
      "github": "your-username",         // 必须
      "name": "可选真名或笔名"
    }
  },
  "contradiction": {"proposition_A": {...}, "proposition_B": {...}},
  "derivation_chain": [{"step": 1, "formulas": [...], "validation": {...}}],
  "claims": [{"id": "C1", "confidence": 0.75, "status": "survived"}],
  "predictions": [{"observable": "...", "expected_values": {...}}],
  "ab_contributions": {"agent_A": {...}, "agent_B": {...}},
  "validation": {"dimension_checks": {...}, "prior_art_search": {...}},
  "reviewer_report": {"verdict": "...", "fatal_issues": 2},
  "lessons": [{"category": "...", "lesson": "..."}],
  "references": [{"doi": "...", "role": "foundation"}]
}
```

## 能做什么

| 用途 | 怎么用 |
|------|--------|
| **SELECTOR 跨课题碰撞** | `math_objects` 字段 → 自动发现共享数学结构的课题 |
| **社区复现** | 下载 JSON → `validation` 字段描述的环境跑一遍 → 对比 |
| **元分析** | 搜 `lessons[].category="prior_art"` → 所有先发漏检的教训汇总 |
| **知识累积** | 每个课题的推导链可被后续课题直接引用——不从头推导 |
