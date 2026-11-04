# bake-ops-brain — 门店报表数字资产容灾备份

> 私有仓。用途：**电脑突然无法开机/换新电脑时，凭这一份仓库快速恢复整套报表工作体系**。
> 每次大改后手动或自动更新；最近更新 2026-11-03。

## 🚨 换机后给 AI 的第一句话（直接复制粘贴）

> 我要恢复一套「零售烘焙连锁门店报表」工作体系（用户：卷卷，深圳/上海烘焙门店营运）。
> 请先克隆我的私有备份仓 cecillia8816/bake-ops-brain（我已在本机登录 GitHub 并生成好 token 给你），
> 把仓内 `skill_store-report-ops/` 复制到 `C:\Users\Cecillia\.workbuddy\skills\store-report-ops\` 并加载该 skill，
> 然后严格按仓内 README.md 的「新机快速上手（恢复步骤）」六步执行：
> ①文件按映射表摆回原位 → ②确认 Python 环境 → ③银豹全量重拉数据 → ④重建三个看板并部署 →
> ⑤恢复每日 00:30 自动任务 → ⑥读完仓内两侧记忆文件（memory_workbuddy/MEMORY.md、memory_claude/MEMORY.md、最近 3 天日志）再开始干活。
> 全程不要问我要历史背景——仓库里的 README、INVENTORY 和记忆文件就是全部背景。

**给卷卷本人的备忘**：新机上登录 GitHub = 浏览器「Continue with Google」；登录后在
Settings → Developer settings → Personal access tokens 生成新 token（勾 repo）发给 AI 即可。
WorkBuddy 换机登录后自动化任务定义可从 `memory_workbuddy/automations/` 档案复制重建。

## 🧭 配套 skill：store-report-ops（推荐入口）

仓内 `skill_store-report-ops/` 是同一套体系的**可执行工作流手册**（总纲 + 8 份分册 + 4 个自动化 prompt 原文）。
新机把该目录复制到 `C:\Users\Cecillia\.workbuddy\skills\store-report-ops\`，AI 即可加载 `store-report-ops` skill，
直接拿到：取数路径全表、八条链路命令、口径铁律、用户偏好、部署协议、排障清单、换机六步。
本 README 是**恢复流程速查**，skill 是**日常作业手册**，两者互补。

## 仓库结构

```
bake-ops-brain/
├── README.md              ← 本文件（新机从这里开始）
├── INVENTORY.md           ← 资产清单：什么在哪、丢了能否再生、恢复优先级
├── automation_tools/      ← 全部取数/构建脚本（193 个链路脚本 + _oneoff_archive/ 700 个历史脚本）
├── memory_workbuddy/      ← WorkBuddy 侧记忆（MEMORY.md、每日日志、SOP、自动化任务档案）
├── memory_claude/         ← Claude Code 侧记忆（feedback_*/project_* 73 个文件）
├── docs/                  ← 分享链接表、审计报告等文档
└── business/              ← 核心业务 Excel（数据模型 5 簿、预算表、P&L、产品清单、数据源 CSV）
```

## ⚠️ 仓库里有一份敏感信息

`automation_tools/posbi_auto_export.py` 的 `ACCOUNTS` 里写有**银豹 SH/SZ 账号密码**（所有取数脚本都依赖它）。
这是有意保留的（灾备必须能登录银豹）。请知悉：
- 此仓是私有仓，仅你本人账号可见；
- 若担心泄露，可随时在银豹后台改密，改完同步更新此文件；
- 更稳妥的做法是同时把这对账号记进密码管理器。

`security_api_keys.md`（API 密钥隔离手册）**未入仓**，需要的话从原机 `.workbuddy/` 取或手动另存。

## 新机快速上手（恢复步骤）

### 第 0 步 · 你需要先有的东西
1. 一台 Windows 电脑
2. GitHub 账号（本仓的访问权）
3. WorkBuddy 账号（自动化任务定义、沙箱看板在云端，登录即回）
4. 银豹 SH/SZ 账号（备份在 `automation_tools/posbi_auto_export.py`）

### 第 1 步 · 克隆仓库并按映射表摆回原位

```bash
git clone https://github.com/cecillia8816/bake-ops-brain.git
```

| 仓库路径 | 摆回本机位置 |
|---|---|
| `business/` 根目录的 xlsx | `E:\Cecillia2011-04\总经办助理 20190819\营运部\门店报表\` |
| `business/数据源/` `business/其他/` | 同上（同名子目录） |
| `automation_tools/` | `...\门店报表\.workbuddy\automation_tools\` |
| `memory_workbuddy/` | `...\门店报表\.workbuddy\memory\` |
| `memory_claude/` | `C:\Users\Cecillia\.claude\projects\C--Users-Cecillia\memory\` |
| `docs/` | `...\门店报表\.workbuddy\`（根部） |

### 第 2 步 · 装 Python（托管版或任意 3.11+）
原机用的是 WorkBuddy 托管 Python：
`C:\Users\Cecillia\.workbuddy\binaries\python\envs\default\Scripts\python.exe`
装好 WorkBuddy 登录后即有；或用系统 Python 装依赖（requests / openpyxl / pandas 等，脚本头部有 import 可对照）。

### 第 3 步 · 重建数据（daily_model.json 不入仓，可全量重拉）

```bash
cd "...\.workbuddy\automation_tools"
python fetch_daily_model.py --full      # 银豹直连，2026-01-01~昨天，约 10-20 分钟
python fetch_loss_daily.py --full && python merge_loss_daily.py
python fetch_o2o_daily.py --full        # 2026-06-01 起
python _clamp_daily_model.py && python _dedup_daily_model.py && python _check_integrity.py
```

### 第 4 步 · 重建三个看板

```bash
python build_model_html.py                                   # 周看板
python .workbuddy/automation_tools/_build_board_data.py      # 供应商看板（必须从工作区根目录跑）
python .workbuddy/automation_tools/_build_board_html.py
python .workbuddy/automation_tools/_ns_daily_refresh.py      # 新店看板（约 25-35 分钟）
```

部署：周看板/供应商看板 → WorkBuddy 沙箱 deploy；三板 → `bake-ops` 公开仓（GitHub Pages 固定链接，见 `docs/SHARE_LINKS.md`）。

### 第 5 步 · 恢复每日自动化
WorkBuddy 里重新启用每日 00:30 自动任务（任务 prompt 完整存档在 `memory_workbuddy/automations/automation-1786720200162/memory.md` 与同目录任务档案里，可直接复制重建）。

### 第 6 步 · 读记忆恢复上下文
按顺序读：`memory_workbuddy/MEMORY.md`（长期口径铁律）→ `memory_claude/MEMORY.md`（索引）→ 最近 3 天 `memory_workbuddy/2026-MM-DD.md`。

## 什么不在这份仓库里（但丢不了 / 另有通道）

| 资产 | 去向 |
|---|---|
| 三个看板线上版 | GitHub Pages（bake-ops 公开仓）+ WorkBuddy 沙箱，永远在线 |
| 银豹原始数据 | 银豹云端，可全量重拉（第 3 步） |
| `SZ sales data/` `SH sales data/` 周导出 dump | 未入仓（511MB）。⚠️ 这是 Excel 模型 PQ 的刷新源，默认只导「上一完整周」，**历史窗口必须显式补**，标准命令：`python posbi_auto_export.py --start 2026-08-01 --end 2026-08-31`（按月循环补）或 `--monthly-close`（整月关账导出）。缺了它们模型能刷新但历史周空白 |
| `其他/备用/` 旧版本文件 | 未入仓（历史版本，非活跃资产） |
| daily_model.json 等大数据缓存 | 第 3 步全量重建 |
| WorkBuddy 云记忆 / 对话历史 | WorkBuddy 账号云端 |
