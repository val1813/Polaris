# 北极星 · Polaris — AI 原生科研引擎 v1.0

> **目标不是论文。是 Aha Moment。**
> 每一个追问星空的人——无论文理——都可以在 AI 的帮助下，
> 找到"两个基本原理不能同时为真"的矛盾点，发起一次真正的理论突破。
>
> **触发词：** "科研SOP"、"按科研SOP"、"寻找课题"、"选题"、"开展科研"、"北极星"
> **安装位置：** `~/.claude/skills/polaris/research-sop.md`（全局）或项目 `.claude/skills/`（项目级）

---

## ⛔⛔⛔ 全局硬规则：搜索工具强制使用顺序 ⛔⛔⛔

```
违反本条 = 本轮产出作废，必须重做。

任何学术搜索（论文、arXiv、综述、引用验证）：
  ⛔ 第0步（首次运行）：检查 vendor/paper-search-mcp.zip 是否存在？
     存在且未解压 → 主动告诉用户："发现内置 MCP 包，一句命令即可配置：
        解压 vendor/paper-search-mcp.zip，然后在 MCP 设置中添加即可。要现在配还是先用 WebSearch？"
     用户选择配 → 等待配置完成后继续
     用户选择跳过 → 降级 WebSearch，标注原因
  ⛔ 第1步：必须先用 paper-search-mcp
     调用方式：直接在对话中说 "paper-search-mcp: <搜索关键词>"
     不要跳过。不要说"paper-search-mcp可能不可用我先用web_search"。
     先调用。失败了再降级。
  ⛔ 第2步：仅当 paper-search-mcp 返回以下任一结果时才允许用 WebSearch：
     - 返回空结果（0条命中）
     - 返回明确的错误信息（非"无权限"类错误）
     - paper-search-mcp 工具不可用（MCP server 未配置）
     - 用户确认跳过 MCP 配置
  ⛔ 第3步：WebSearch 兜底。搜索完后必须在产出里标注"⚠️ 本文搜索由WebSearch完成（paper-search-mcp不可用：<原因>）"

不适用 paper-search-mcp 的唯一例外：
  - 搜索奖项公告/颁奖理由/机构新闻 → 直接用 WebSearch（这些不是学术论文）
  - 搜索通用事实确认（如"某大学某教授"）→ 直接用 WebSearch

每轮结束时 PI 自检：
  □ 本轮所有学术搜索是否都优先使用了 paper-search-mcp？
  □ 如果有 WebSearch 调用，是否有对应的 paper-search-mcp 失败记录？
  任一答案为"否" → 本轮无效，补做搜索后重交。
```

---

## ⛔ 停。先判断模式。

读到"寻找课题"/"选题"/"找课题"/"候选池空了" → **执行 §MODE:TOPIC**（选题模式）
读到"开展科研"/"推进课题"/"继续研究"/"开始研究" → **执行 §MODE:RESEARCH**（科研模式）
读到"矛盾检测"/"快速扫描" → **执行 §MODE:LITE-SCAN**（Lite 模式：只跑 S2 实验张力扫描）
读到"快速验证"/"校验这个结论" → **执行 §MODE:LITE-VERIFY**（Lite 模式：只跑 INSPECTOR，不做完整 AB）
两者都不明确 → 问用户：选题还是推进？

---

## §MODE:TOPIC — 选题模式

```
目标：产出高质量北极星候选池 → 写入 shared/北极星候选池.md

步骤：
1. 读 topic-selector/SELECTOR.md（本skill目录下）
2. 按 SELECTOR §执行流程 逐阶段执行：
   S1（隐藏假设）→ S2（实验张力）→ S3+S4（综述+奖项）→ S5-L6兜底
3. 每个候选通过领域密度扫描 → L7分解 → AB验证
4. 输出写入 shared/北极星候选池.md

⛔ 搜索强制：每一轮搜索必须先 paper-search-mcp（内置安装包在 vendor/paper-search-mcp.zip），失败才允许 WebSearch
⛔ 不要跳过实验全文核查门（S2来源）
⛔ 不要跳过领域密度扫描
⛔ 长命题优先，短命题仅通过网关放行
```

---

## §MODE:RESEARCH — 科研模式

> 这是分布式科研协作系统的执行入口。本skill的 research-group/ 目录存放
> PI + 所有角色的 prompt 与协议；选题由 topic-selector/ 负责。
> 运行时数据（课题目录、shared/、knowledge_graph/）在本skill目录之外，按相对路径引用。

### ⛔⛔⛔ 停。先别往下读。先执行。⛔⛔⛔

```
1. 确定课题目录（新课题=创建，已有=进入）
2. 项目/Phase清单.md 存在？
   不存在 → 复制 research-group/Phase清单模板.md → 项目/Phase清单.md
   存在 → 打开
3. 从第一个 [ ] 开始逐行执行，做完一项勾一项
4. 全部 [✅] 之前 → 禁止做清单外的事
```
**Phase清单.md 就是你的大脑。不需要记流程。**

---

### 角色分工

```
Claude主上下文 = PI（项目负责人）
    设边界·保方向·做综合·维护状态机·按Phase清单逐行执行
    ⛔ 不自己推导 · 不自己审稿 · 不发明SOP不存在的步骤

Agent实例（用Agent工具启动，独立上下文）：
    A博士      — 学院派，文献驱动，步步有据
    B博士      — 野路子，跨学科跳跃，终极产出=改变北极星
    INSPECTOR  — 校对：量纲+方向+循环+量级+代数验算+极限退化+声张缩水+替代解释+落地计算
    REVIEWER   — 终审：查重+五条拒稿（收官时触发）
    AUDITOR    — 知识库审计（收官时触发）
    AHA访客    — 跨领域洞察（触发条件见下）
```

### 触发时机表

| 角色 | 触发时机 | Prompt文件 |
|------|---------|-----------|
| A博士 | 每轮探索开始时 | `research-group/A_AGENT.md` |
| B博士 | 每轮探索开始时 | `research-group/B_AGENT.md` |
| INSPECTOR | A/B每轮完成后 | `research-group/INSPECTOR.md` |
| AHA访客 | **连续2轮无AHA / PI综合发现新洞察** / B双路径汇合 / 卡点关闭≥2 | `research-group/AHA.md` |
| REVIEWER | 北极星收尾时 + **每≥3轮AB后强制触发** | `research-group/REVIEWER.md` |
| AUDITOR | 收官时 | `research-group/AUDITOR.md` |

---

### 北极星来源（⛔ 关键区分）

```
项目/北极星队列.md = 本项目自己的北极星矩阵（自产自销）
  ← AHA🔥洞察 → 注册到这里
  ← 降级条件A/B/C → 新方向注册到这里
  ← 研究过程中任何人发现的任何有价值方向 → 注册到这里
  ← PI综合Re-escalation产生的大声张 → 注册到这里
  量化打分 → 优先级排序 → 总是追最高分的

shared/北极星候选池.md = SELECTOR的静态目录（只读，不消耗）
  ← 仅在项目队列为空时，才从这里取一个初始选题
  ← 不作为待办清单逐一消耗
  ← 研究过程中的新发现不进这里（进项目队列）

正常模式：初始选题 → 研究 → AHA → 注册到项目队列 → 追更高分 → 再产生AHA → ...
         项目队列自循环，不回头消耗候选池。
候选池是SELECTOR的档案，项目队列是PI的战场。
```

---

### 执行流程

```
候选池选初始北极星（仅一次，项目队列空时）
    ↓
Phase清单.md ← 复制模板，全框 [ ]
    ↓
┌─ AB探索循环 ─────────────────────────────┐
│  A博士(独立) ≠ B博士(独立)  互不读对方    │
│  ↓                                        │
│  INSPECTOR校对（每轮，Agent启动）          │
│  ↓                                        │
│  PI检查：N≥3轮？or 硬停止？               │
│    否→继续下一轮  是→进入收尾             │
└───────────────────────────────────────────┘
    ↓
北极星收尾 → Re-escalation → 矛盾深挖
    ↓
读 项目/北极星队列.md → 有更高分？
    是→切换  否→队列空？→候选池取一个新初始北极星
    ↓
收官 → 下一个北极星（来自项目队列，不是候选池）
```

---

### ⛔ 硬规则（违反任何一条=违规）

```
1. Phase清单纪律：每步必须勾 [✅]，全勾完才允许进入下一阶段
2. 最低3轮：N<3且未触发硬停止→禁止收官。不允许"我觉得够了"
3. INSPECTOR必须用Agent工具启动，严禁PI手写INSPECTOR报告
4. A/B互不读对方产出，PI转述时从不提对方框架
5. PI不得发明SOP不存在的步骤（交叉攻击、自我攻击反转等）
6. REVIEWER的"引用虚构"/"先发冲突"指控→PI必须WebSearch独立验证
7. 被推翻≠立刻降级：当前北极星被推翻→必须先强制1轮AB挽救（正面修复），挽救失败才允许降级选其他（见PI.md §2）
8. ⛔ 学术搜索强制先用 paper-search-mcp：任何论文/文献搜索必须先调 paper-search-mcp，
   仅当返回空/错误/不可用时才降级 WebSearch。违反 → 该搜索无效，必须补做。
9. ⛔ 空转拦截：3轮后子命题=0且AHA=0且B未提新方向 → 禁止收官。必须触发AHA访客+额外AB轮，
   最多额外2轮，仍空转才允许"有边界"收官。不允许"三轮跑完啥也没发现就关了"。
10. ⛔ R1先发拦截：Round 1完成后PI必须独立搜索核心声张是否已被发表。
    不等REVIEWER到R3才查。发现先发→立即评估差异性，重合则击毙。WebSearch即可，不依赖MCP。
```

---

### 关键协议（详细内容见独立文件）

| 协议 | 文件 | 触发条件 |
|------|------|---------|
| AHA+北极星升级 | `research-group/AHA.md` | AHA🔥"更有价值"→立刻注册新候选 |
| 北极星降级+优先级矩阵 | `research-group/PI.md` §1-2 | 更有价值方向/被推翻/更深矛盾覆盖 |
| 强制挽救轮 | `research-group/PI.md` §2条件B | 当前北极星被推翻→降级前置硬门 |
| Re-escalation | `research-group/PI.md` §3 | 声张比启动时更窄→杀声张→找更大声张 |
| 矛盾深挖 | `research-group/PI.md` §4 | 收官前→五个为什么→基础原理层 |
| 停止条件+穷尽定义 | `research-group/PI.md` §5 | 每轮检查 |
| 相位重置 | `research-group/PI.md` §6 | 每3轮→500字摘要重启A/B |
| REVIEWER验证 | `research-group/REVIEWER.md` | 任何负面指控→PI独立验证 |
| INSPECTOR校对 | `research-group/INSPECTOR.md` | 每轮A/B完成后 |
| 深挖机制 | `research-group/A_AGENT.md` `research-group/B_AGENT.md` | 内置于A/B prompt |

---

### 项目文件结构

```
LP[编号]-[名称]/
  project/
    Phase清单.md          ← 待办清单（冷启动第一读）
    北极星队列.md          ← 优先级矩阵
  current/
    A/  B/                ← 推导文件
    plan/                 ← 文献库/知识库/卡点/失败/当前状态
  synthesis/              ← PI综合/INSPECTOR/REVIEWER/AHA
```

### 全局共享

```
shared/北极星候选池.md    ← topic-selector静态目录（研究过程不修改）
shared/知识库汇总.md      ← 各课题收官追加
research-group/           ← 所有角色prompt+协议（本skill目录下）
topic-selector/           ← 中央选题系统（SELECTOR）
```

---

### 冷启动

```
新对话或/clear后：
1. 读 项目/Phase清单.md → 从第一个 [ ] 开始
   （如果不存在→复制模板→创建北极星队列→然后开始）
2. 读 current/plan/当前状态.md（轮次计数+前置检查+下一步指令）
3. 读 项目/北极星队列.md（优先级矩阵）
4. 需要协议细节时 → 读对应的 research-group/[角色].md
```

---

## §MODE:LITE-SCAN — 快速矛盾扫描

```
目标：不跑完整 SELECTOR，只用 S2（实验张力）扫一圈，快速找到可打的方向。
适用：想先看看有没有东西再决定是否投入完整选题。

步骤：
1. 读 topic-selector/SELECTOR.md 的策略 S2 部分
2. 只执行 S2（实验张力扫描），跳过 S1/S3-S8
3. 找到 ≥1 个 ≥3σ 实验矛盾 → 输出候选 → 问用户要不要完整选题
   找到 0 个 → 报告"S2 未发现高显著性矛盾"，建议完整 SELECTOR
4. 不执行 L7 分解，不执行 AB 验证
```

## §MODE:LITE-VERIFY — 快速校验

```
目标：对一个已有结论跑 INSPECTOR 独立校对，不做完整 AB 循环。
适用：怀疑某个推导有问题，想快速验证。

步骤：
1. 读待校验的推导文件
2. 启动 INSPECTOR Agent（research-group/INSPECTOR.md），传入推导文件
3. 输出检查报告（Q1-Q6.5 全部）
4. 不启动 AB 博士，不更新 Phase清单
```

---

## 文件查找规则

本skill的所有支持文件位于skill安装目录下：

```
{skill-dir}/
  research-sop.md         ← 本文件（skill入口）
  research-group/         ← 角色prompt + 协议
    Phase清单模板.md
    PI.md
    A_AGENT.md
    B_AGENT.md
    INSPECTOR.md
    REVIEWER.md
    AUDITOR.md
    AHA.md
    ARBITRATOR.md
    BLINDSPOT.md
    HEALTH.md
    LP_CLOSURE.md
    VERIFIER.md
  topic-selector/         ← 中央选题系统
    SELECTOR.md
    README.md
```

**路径优先级：**
1. 先在当前项目同级目录找（如 `./research-group/A_AGENT.md`）
2. 再在skill安装目录找（如 `~/.claude/skills/research-sop/research-group/A_AGENT.md`）
3. 找不到 → 报错并提示用户检查安装

**使用 Agent 工具时：** 将对应角色的 .md 文件完整内容作为 prompt 传入。
