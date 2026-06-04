# 北极星 · Polaris — 演进路线图

> 基于社区反馈的全面诊断。不画大饼，每一期都是能交付的。

---

## 现状评估

**我们有能力做的：**
- Prompt 工程（角色设计、SOP 协议、对抗机制）— 这是我们的核心优势
- 模块化拆分（Lite 模式、按需调用）— 纯 prompt 层面即可实现
- 社区协作基础设施（contrib/、experiments/）— 目录 + 规范即可
- 验证闭环的基础框架（validation/）— 先搭结构，工具慢慢接

**需要外部资源或逐步积累的：**
- 数值验证引擎（Wolfram/COMSOL）— 依赖 API 和预算
- Redis 状态管理 — 需要服务端基础设施
- Agentic Tree Search — 需要 Agent 框架层面的支持
- Polaris-Bench — 需要社区贡献已知矛盾的标准答案

---

## 分期计划

### 🔴 Phase 1：止血（本周可交付）

> **目标：** 让现有流程产出可验证，不再"讲个故事就结束"

| 任务 | 具体动作 | 状态 |
|------|---------|------|
| **validation/ 模块** | 新建 `validation/` 目录 + 验证协议。每个课题收官前强制输出：推导过程 + 数值验证（至少量纲/极限退化）+ 关键结论的独立文献锚点 | ✅ |
| **Adversarial Peer-Review 强化** | 现有的 REVIEWER 每 3 轮触发已是恶意审稿。强化：REVIEWER 报告必须包含"如果我必须挑一个致命错误"条目 | ✅ |
| **INSPECTOR 落地计算自检** | Q6.5 已有但不够强制。改为：无落地 A/B/C 的空白发现 → ⛔ 阻断，禁止进入下一轮 | 🔲 |
| **Polaris Lite 模式** | 新增触发词：`矛盾检测`（只跑 SELECTOR 的 S2 实验张力扫描）、`快速验证`（只跑 INSPECTOR 不做完整 AB） | ✅ |

### 🟡 Phase 2：工程化（2-4 周）

> **目标：** 系统不再"脆弱"，可被非开发者稳定使用

| 任务 | 具体动作 | 状态 |
|------|---------|------|
| **experiments/ A/B 测试框架** | 目录 + 配置规范。不同 Prompt 版本放 experiments/，附 token 消耗 + 结论质量对比 | 🔲 |
| **上下文压缩协议** | 每轮 PI 综合后产出 ≤500 字摘要。下一轮 AB 以摘要为上下文（已有 §6 相位重置，增强为每轮执行） | 🔲 |
| **DeepSeek V4 适配指南** | platforms/ 下新增 deepseek/ 适配文件。确认所有 prompt 在 DeepSeek 上的兼容性 | 🔲 |
| **contrib/ 社区角色** | 目录 + 贡献模板 + 三层架构（SOP宪法/contrib市场/knowledge图书馆）。社区可提交领域专用 Agent | ✅ |
| **Findings Memory** | `knowledge_graph/` 目录 + 标准 JSON schema + 社区提交指南。每个课题收官自动产出，可搜索碰撞 | ✅ |
| **容错重试机制** | SOP 增加：Agent 超时/格式错误 → 自动重试 1 次 → 仍失败 → 降级到 PI 手动处理 + 记录卡点 | ✅ |

### 🟢 Phase 3：生态（1-3 个月）

> **目标：** 从个人项目变成社区项目

| 任务 | 具体动作 | 状态 |
|------|---------|------|
| **Polaris-Bench** | 收集 10-20 个已知科学矛盾（含标准答案），作为基准测试集。社区可提交结果对比 | 🚧 已建 3/8（B01狭义相对论/B02量子/B05超导），持续扩充 |
| **Findings Memory** | 公开的发现记忆库。社区的 Aha Moment 可注册，跨课题碰撞 | 🔲 |
| **Cursor/VSCode 深度适配** | 不是现在 platforms/ 的手动方案，而是一键配置 + 内置工具链对接 | 🔲 |
| **多模型基准报告** | DeepSeek V4 vs Claude vs GPT 在相同 SOP 流程下的对比（耗时/成本/结论质量） | 🔲 |

### 🔵 Phase 4：架构升级（远期）

> **目标：** 从"脚本集合"变成"科研操作系统"

| 任务 | 具体动作 | 状态 |
|------|---------|------|
| **Agentic Tree Search** | 当 AB 结论矛盾且 ARBITRATOR 判 (D) 时，自动分叉多条验证路径并行探索 | 🔲 |
| **Redis 全局状态管理** | ~~Agent 间共享状态~~ → 不需要。Phase清单.md 已是状态管理器，Claude Code 自带重试。实测 13 Agent 无崩溃 | ❌ 不做 |
| **Wolfram/COMSOL 集成** | 假说自动推送到符号计算引擎做数值验证 | 🔲 |
| **插件市场** | 社区可发布、安装、评分 Agent 角色和搜索策略 | 🔲 |

---

## 当前优先级

```
Phase 1（本周）         Phase 2（本月）         Phase 3-4（远期）
████████████            ████████                ████████
validation/              experiments/            Polaris-Bench
Lite 模式               上下文压缩               Findings Memory
REVIEWER 强化           容错重试                 Tree Search
落地计算强制            contrib/                 插件市场
```

**不建议现在做的：** Redis 状态管理、Wolfram 集成、Agentic Tree Search——这些需要 Agent 框架层面的原生支持，纯 prompt 层面做不了。等 Claude Code/Codex 的 Agent 框架成熟后再接。

---

## 如何贡献

每个 Phase 的任务都是独立的——认领一个，做完提 PR。

```
Fork → 在对应目录下实现 → 附测试结果 → PR
```

Phase 1 的四个任务加起来不超过 200 行，一周能交付。
