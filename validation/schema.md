# Unified JSON Schema — 中间过程全用 JSON

> **A博士、B博士、INSPECTOR、PI综合 → 全部 JSON。只有收官才写 md。**
> 节约 token，提高效率，机器直读。
>
> **最终遗产 = knowledge_graph JSON。这是 Polaris 的"论文格式"。**
> 标准化的矛盾+推导链+验证数据，机器原生，人类可读。
> 愿景：这份 JSON 替代学术论文。

## 完整 Schema

```json
{
  "project": "LP27",
  "round": 1,
  "agent": "A",
  "polaris": "T-linear不逻辑蕴含准粒子破坏",
  "claims": [
    {
      "id": "C1",
      "statement": "一句话声张",
      "confidence": 0.75,
      "equations": [
        {
          "label": "F1",
          "expression": "m/(n*e**2*tau)",
          "description": "Drude电导率",
          "variables": {
            "m": "electron_mass",
            "n": "density",
            "e": "elementary_charge",
            "tau": "scattering_time"
          },
          "units": "ohm*meter",
          "limits": [
            {"variable": "tau", "to": "oo", "expected": "0", "desc": "完美导体极限"}
          ],
          "numerical_test": {
            "substitutions": {"m": 9.11e-31, "n": 1e28, "e": 1.6e-19, "tau": 1e-14},
            "expected_range": [1e-8, 1e-5]
          }
        }
      ],
      "references": [{"doi": "10.1103/PhysRevLett.75.1260", "label": "Jacobson 1995"}],
      "assumptions": ["各向同性散射", "自由电子气"],
      "new_insight": false
    }
  ]
}
```

## 字段说明

| 字段 | 必须 | 类型 | 说明 |
|------|------|------|------|
| `project` | ✅ | string | 课题编号，如 "LP27" |
| `round` | ✅ | int | 第几轮 1/2/3 |
| `agent` | ✅ | "A"\|"B" | 哪个博士 |
| `polaris` | ✅ | string | 当前北极星一句话 |
| `claims[].id` | ✅ | string | 声张编号 C1/C2/... |
| `claims[].statement` | ✅ | string | 一句话声张 |
| `claims[].confidence` | ✅ | 0.0~1.0 | 确信度（0=瞎猜，1=得证） |
| `claims[].equations[].expression` | ✅ | string | **SymPy 兼容的表达式**（用 `**` 不要 `^`） |
| `claims[].equations[].variables` | ⚠️ | object | 变量名→物理含义映射 |
| `claims[].equations[].units` | ⚠️ | string | SI 单位，如 "ohm*meter" |
| `claims[].equations[].limits` | ⚠️ | array | 极限退化测试用例 |
| `claims[].equations[].numerical_test` | ⚠️ | object | 数值代入+预期范围 |
| `claims[].references` | ⚠️ | array | 支撑文献 |
| `claims[].assumptions` | ⚠️ | array | 依赖的前提假设 |
| `claims[].new_insight` | ✅ | bool | **本轮是否新发现？**（true→触发AHA检查） |

## SymPy 表达式规范

```
✅ 正确：m/(n*e**2*tau)          exp(-t/tau)           sin(theta)
❌ 错误：m/(n*e^2*τ)             e^{-t/τ}               \sin(\theta)
          ^ 用 ** 不要 ^          ^ 用 exp() 不要 e^     ^ 去掉 LaTeX 命令
```

## 验证流程

```
A博士/B博士产出 roundN_claims.json
        │
        ▼
python validation/validate.py roundN_claims.json
        │
        ├─ PASS → 进 INSPECTOR（只做语义检查）
        └─ FAIL → 打回修正（标注阻断公式）
                  └─ 修正后重跑 validate.py
                  └─ 通过后进 INSPECTOR
```

## `new_insight` 字段说明

每轮 AB 博士必须诚实标注每个声张是否是"本轮新发现"：
- `true` → PI 在综合时会检查是否应触发 AHA 访客
- `false` → 已知结论的深化/修正/验证

如果一轮中 ≥1 个声张 `new_insight=true`，PI 必须触发 AHA 检查。

---

## Knowledge Graph JSON — 课题最终遗产（Polaris 论文格式）

> 这是一份自包含的科学记录。没有 LaTeX，没有"Dear Editor"。
> 机器可碰撞，人类可读，社区可复现。

### 完整 Schema

```json
{
  "polaris_version": "1.0",
  "project": {
    "id": "LP27",
    "title": "T-linear电阻率不逻辑蕴含非费米液体",
    "domain": "cond-mat.str-el",
    "contradiction_type": "hidden-assumption",
    "tags": ["information-theoretic", "renormalization-group"],
    "selector_strategy": "S1",
    "hidden_assumption": "T-linear电阻率是准粒子破坏的充分必要条件",
    "date_start": "2026-06-04",
    "date_closure": "2026-06-04",
    "contributor": {
      "orcid": "0000-0002-1825-0097",
      "github": "val1813",
      "name": "可选真名或笔名",
      "email": "可选（不会公开显示）"
    },
    "rounds": 3,
    "status": "有边界完成",
    "verdict": "T-linear不逻辑蕴含准粒子破坏(75%)"
  },

  "contradiction": {
    "proposition_A": {
      "statement": "T-linear电阻率意味着准粒子被破坏",
      "evidence": ["ARPES无准粒子峰", "比热异常", "光导反常"],
      "confidence_before": 0.9
    },
    "proposition_B": {
      "statement": "存在保持准粒子的T-linear机制",
      "evidence": ["Lee 2024 umklapp FL", "Levitov 2024流体动力学"],
      "confidence_before": 0.6
    },
    "why_not_both": "A声称T-linear universal→准粒子消失。B声称∃T-linear with intact准粒子。B为真则A的普遍性声明被打破。",
    "resolution_after": "T-linear是各向同性散射率的充要条件，不逻辑蕴含准粒子破坏。B的构造有效，A的普遍性声明被打破(75%确信度)。"
  },

  "derivation_chain": [
    {
      "step": 1,
      "agent": "A",
      "round": 1,
      "description": "Hlubina-Rice逆定理：T-linear充要条件是各向同性散射率",
      "formulas": [
        {
          "label": "F1",
          "expression": "1/tau = g**2 * N(0) * pi * T",
          "latex": "\\frac{1}{\\tau} = g^2 N(0) \\pi T",
          "variables": {"g": "coupling", "N(0)": "DOS_at_Fermi", "T": "temperature"},
          "units": "s^{-1}",
          "derived_from": "Fermi黄金规则 + 各向同性假设"
        }
      ],
      "assumptions": ["各向同性散射", "费米液体基态存在"],
      "validation": {"dimensions": "PASS", "limits": "PASS", "magnitude": "PASS"}
    }
  ],

  "claims": [
    {
      "id": "C1",
      "statement": "T-linear电阻率不逻辑蕴含准粒子破坏",
      "confidence": 0.75,
      "status": "survived",
      "evidence_for": [
        "Lee 2024: umklapp FL模型产生T-linear",
        "Levitov 2024: 流体动力学产生T-linear",
        "Z(T)∈[0.19,0.53]在Caprara温区保持正 → 准粒子权重未消失"
      ],
      "evidence_against": [
        "Tulipman&Berg 2023先发 — 部分预占C1",
        "Section 3.4方向错误 — 被REVIEWER致命指控"
      ],
      "inspector_verdict": "PASS (R2修正后无阻断)",
      "reviewer_verdict": "大修 — 先发部分预占，需明确差异化",
      "math_objects": ["各向同性散射率充要条件", "Eliashberg Z(T)"]
    },
    {
      "id": "C4",
      "statement": "SOC 1/f噪声纳米增强是排他性预测",
      "confidence": 0.40,
      "status": "killed",
      "killed_by": "REVIEWER — SOC基础缺失，核心文献未引用",
      "lesson": "跨学科跳跃需要先建立学科基础再预测"
    }
  ],

  "predictions": [
    {
      "id": "P1",
      "statement": "Fano因子可区分FL/NFL/SYK",
      "type": "experimentally_testable",
      "observable": "散粒噪声Fano因子 F",
      "expected_values": {
        "FL": {"value": 0.433, "uncertainty": 0.05, "unit": "dimensionless"},
        "SYK_NFL": {"value": 0.167, "uncertainty": 0.03, "unit": "dimensionless"},
        "MFL": {"value": "→0", "uncertainty": null, "unit": "dimensionless"}
      },
      "measurement_conditions": "T < 100K, 直流极限, 弹道输运区",
      "existing_data": "Wang PRR 2024 (FL), Nikolaenko PRR 2023 (SYK)",
      "new_experiment_needed": false
    }
  ],

  "ab_contributions": {
    "agent_A": {
      "framework": "凝聚态/费米液体理论",
      "key_findings": ["Hlubina-Rice逆定理", "I/II/III型奇异金属三分类", "Z(T)∈[0.19,0.53]"],
      "rounds_summary": {
        "R1": "402行 — 发现充要条件, 3阻断",
        "R2": "583行 — 修正全部阻断, Z(T)定量",
        "R3": "445行 — 三分类收敛, 交叉诊断矩阵"
      }
    },
    "agent_B": {
      "framework": "信息论/MaxCal/统计推断",
      "key_findings": ["MaxCal吸引子", "分形输运网络维度依赖", "接触几何统一结构"],
      "rounds_summary": {
        "R1": "413行 — 3跨学科跳跃, 3阻断(评分4.6/10)",
        "R2": "830行 — 6定量预测, 修正全部阻断",
        "R3": "520行 — SOC跳跃, 6.3/10, 诚实收敛报告"
      }
    },
    "convergence": "互补 — A提供机制(是什么), B提供原理(为什么)"
  },

  "validation": {
    "dimension_checks": {"total": 12, "passed": 12, "failed": 0},
    "limit_degeneration": {"total": 8, "passed": 7, "failed": 1, "failed_detail": "tau→∞极限化简未完成"},
    "magnitude_sanity": {"total": 5, "passed": 5, "failed": 0},
    "algebraic_identity": {"total": 3, "passed": 3, "failed": 0},
    "prior_art_search": {
      "performed": true,
      "tool": "WebSearch (paper-search-mcp unavailable)",
      "found": ["Tulipman&Berg 2023"],
      "missed_by_selector": true,
      "caught_by": "REVIEWER Round 3"
    },
    "reproducible_predictions": ["P1_Fano因子"]
  },

  "reviewer_report": {
    "verdict": "大修 (Major Revision)",
    "fatal_issues": 2,
    "serious_issues": 2,
    "moderate_issues": 1,
    "fatal_detail": [
      "Section 3.4方向错误",
      "Tulipman&Berg 2023先发 — 核心声张被部分预占"
    ],
    "must_fix": "如果必须挑一个致命错误：Section 3.4的Z(T)符号方向反了。修正后整体框架仍成立。"
  },

  "lessons": [
    {
      "category": "prior_art",
      "lesson": "Tulipman&Berg 2023先发漏检 → R1先发拦截必须强制执行",
      "action_taken": "已在Phase清单添加R1先发拦截gate"
    },
    {
      "category": "tooling",
      "lesson": "paper-search-mcp不可用 → SELECTOR AB验证精度不足 → 先发漏检",
      "action_taken": "vendor/内置MCP包, 安装指南强化"
    },
    {
      "category": "method",
      "lesson": "B博士跨学科跳跃R1评分4.6/10, 3轮才收敛到6.3 → B博士需要更多轮次或更强引导",
      "action_taken": "AHA触发频率从5轮降至2轮"
    }
  ],

  "references": [
    {"doi": "10.1038/s42005-021-00779-5", "label": "Caprara et al. 2022", "role": "foundation"},
    {"doi": "10.1103/PhysRevB.108.235157", "label": "Tulipman & Berg 2023", "role": "prior_art"},
    {"doi": "10.1103/PhysRevB.110.155136", "label": "Skrlec 2024", "role": "support"},
    {"doi": "10.1103/PhysRevResearch.6.L042045", "label": "Wang et al. 2024", "role": "support"}
  ],

  "cross_project_connections": [
    {"target": "LP24", "connection": "共享各向同性散射率数学结构", "strength": "weak"}
  ]
}
```

### 字段全表

| 层级 | 字段 | 必须 | 记录什么 |
|------|------|------|---------|
| 📋 元信息 | `project.*` | ✅ | 课题ID、**领域(arXiv分类)**、**矛盾类型**、**方法标签**、策略、起止日期、轮次、状态、**贡献者身份** |
| 🏷️ 分类 | `project.domain` `contradiction_type` `tags` | ✅ | 见 `knowledge_graph/TAXONOMY.md`——三类标签，可从已有选也可自创 |
| 🪪 贡献者 | `project.contributor` | ✅ | **ORCID iD（学术身份证）+ GitHub + 可选姓名** |
| ⚡ 矛盾 | `contradiction.*` | ✅ | 命题A/B原文+证据、为何不共存、解决后结论 |
| 🔗 推导链 | `derivation_chain[]` | ⛔ 必填 | 每步：谁做的、公式(SymPy+LaTeX)、变量/单位、假设、验证结果。**没有推导链 = 不可验证 = 退回** |
| 📢 声张 | `claims[]` | ✅ | 声张原文、确信度、存活/被证伪、正反证据、INSPECTOR+REVIEWER判定 |
| 🔮 预言 | `predictions[]` | ⚠️ | 可检验预言：可观测量+数值+单位+误差+测量条件 |
| 👥 AB贡献 | `ab_contributions` | ✅ | A/B各自框架、关键发现、每轮摘要、收敛判断 |
| 🔍 验证 | `validation` | ✅ | 量纲/极限/量级/代数 确定性检查结果 + 先发检索记录 |
| 📝 审稿 | `reviewer_report` | ✅ | REVIEWER判决、致命/严重/中等问题数、致命一击 |
| 📖 教训 | `lessons[]` | ✅ | 分类(category)、教训原文、已采取的行动 |
| 📚 引用 | `references[]` | ✅ | DOI、标签、角色(foundation/prior_art/support/contradiction) |
| 🌐 跨课题 | `cross_project_connections[]` | ⚠️ | 与其他课题的连接+强度 |

### 贡献者身份 — 你的学术指纹

| 字段 | 必须 | 说明 |
|------|------|------|
| `orcid` | ⚠️ 强烈建议 | **ORCID iD**（如 `0000-0002-1825-0097`）。免费注册 [orcid.org](https://orcid.org)。学术界公认的永久身份标识。即使换了机构、换了邮箱，ORCID 不变。 |
| `github` | ✅ 必须 | GitHub 用户名。提交 PR 用的就是它。 |
| `name` | 自由 | 真名、笔名、"布衣科学家"——你自己决定。 |
| `email` | 可选 | 不会公开显示，仅用于私下联系。 |

> **ORCID 是最好的选择。** DOI 标识论文，ORCID 标识人。一份 JSON 上同时有 DOI（引用）和 ORCID（作者），就和传统论文没有区别——甚至更好，因为 DOI 可能烂掉，ORCID 永远指向你。

**匿名贡献？可以。** `orcid` 留空，`name` 写 "Anonymous"，`github` 必须有（PR 来源可追溯）。

### 为什么 JSON 能替代论文

- **完整**：假设→推导→公式→计算→声张→预言→验证→审稿→教训，全链路
- **机器可碰撞**：`math_objects` 字段让 SELECTOR 直接检索跨课题数学结构
- **可验证**：`validation` 是确定性检查结果，`reviewer_report` 是 AI 审稿——两层验证
- **可复现**：`derivation_chain` 的每步都有 SymPy 表达式，机器可直接验算
- **诚实**：`killed_claims` + `lessons` 记录失败，不是只写成功
- **可累积**：`cross_project_connections` 让知识网络生长，不孤立
