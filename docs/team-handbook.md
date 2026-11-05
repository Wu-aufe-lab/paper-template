# Wu-aufe-lab 组员手册

> **两种读法**
> - **人**：§1 照做一遍，§3 存书签，§4 红线背下来。
> - **智能体（大模型）**：整份投喂，然后**严格执行 §6 的协议**；§0–§5 是约束上下文，不是建议。
>
> 有冲突时：本文件 > 你自己的默认习惯 > 网上教程。

---

## 0. 一分钟版

```
收邀请 → 装 git → 配身份 → clone
    → git checkout -b feat/xxx
    → 改 → commit → push
    → 网页提 PR → owner merge
```

**永远不要直接推 `main`。** 其他都是细节。

---

## 1. 加入课题组（一次性，约 10 分钟）

### 1.1 准备

| 需要 | 说明 |
|---|---|
| GitHub 账号 | 没有就注册；**用户名发给 owner** |
| 电脑 | Windows / macOS / Linux 都行 |
| 学校邮箱 | 用于 git 身份配置，**要和论文署名对得上** |

### 1.2 接受邀请

owner 发邀请后，你的**邮箱**会收到一封来自 GitHub 的邮件，点 **Join @Wu-aufe-lab**。

找不到邮件时，直接打开 <https://github.com/Wu-aufe-lab>，页面顶部会有 **Join** 按钮。

### 1.3 装 git 并配置身份

Windows 下载 [Git for Windows](https://git-scm.com/download/win)，一路默认即可。

然后打开终端（Git Bash / PowerShell / 命令行都行）：

```bash
git config --global user.name "张三"
git config --global user.email "zhangsan@aufe.edu.cn"
```

**这两行必须做。** 不配的话，提交记录显示的是别人的名字或一串乱码，以后论文里对不上人。

### 1.4 第一次登录（只需一次）

第一次 `clone` 私有仓库时，会弹出一个 **Git Credential Manager** 窗口：

1. 点 **Sign in with your browser**
2. 浏览器里用你的 GitHub 账号登录
3. 点绿色的 **Authorize** 按钮
4. 回到弹窗，它会自动关闭

之后这台机器上所有 GitHub 操作都免密。**不需要**自己生成 token。

### 1.5 验证成功

```bash
git clone https://github.com/Wu-aufe-lab/<任意一个仓库>.git
```

能下来就是成功了。报 `Repository not found` 说明邀请还没接受，或者 owner 还没给你仓库权限。

---

## 2. 你能做什么、不能做什么

| 你能做 | 你不能做 | 为什么 |
|---|---|---|
| clone / pull 所有你有权限的仓库 | 删除仓库 | 组织设置已锁，只有 owner 能删 |
| 建分支、推分支 | 把私有仓库改成公开 | 组织设置已锁，防止未发表数据泄漏 |
| 提 PR、提 issue | 直接推 `main` | 分支保护（仓库转公开后生效） |
| 在 PR 里讨论、改代码 | 改别人已发布的 tag | 论文引用的版本必须永久有效 |
| 上传代码和小样本数据 | 上传 >50 MB 的文件 | GitHub 会拒收，仓库会永久膨胀 |

**你的基础权限是 `read`**（只读）。owner 会把你加进 `lab` 团队并给 **Write**，那时才能推代码。如果推不上去先问 owner，不要反复试。

---

## 3. 日常怎么用

### 3.1 第一次拿到代码

```bash
git clone https://github.com/Wu-aufe-lab/paper-<短标题>.git
cd paper-<短标题>
```

### 3.2 一天的标准循环

```bash
# ① 先同步最新代码（每天开工第一件事）
git checkout main
git pull

# ② 开一个分支干活（分支名见下）
git checkout -b feat/your-topic

# ③ 改代码……

# ④ 提交
git add -A
git commit -m "feat: 新增 XXX 特征提取"

# ⑤ 推上去
git push -u origin feat/your-topic

# ⑥ 去网页提 PR，等 owner merge
```

**分支命名**：

| 前缀 | 用途 | 例 |
|---|---|---|
| `feat/` | 新功能 | `feat/force-curve-filter` |
| `fix/` | 修 bug | `fix/nan-in-normalization` |
| `data/` | 数据处理 | `data/m1-m2-split` |
| `docs/` | 文档 | `docs/readme-reproduce` |
| `exp/` | 实验脚本 | `exp/seed-sweep` |

**提交信息格式**：`<类型>: <一句话说清改了什么>`

```
feat: 新增 AFM 力曲线平滑滤波
fix: 修正归一化除零
data: 补充 M2 组 200 个样本
docs: README 补复现步骤
```

不要写 `update`、`修改`、`111`、`final`、`真的最终版`。三个月后你自己也看不懂。

### 3.3 上传代码

就是正常 `commit` + `push`。注意三条：

1. 先 `git status` 看一眼，别把临时文件带上去
2. 不要提交 `data/raw/`、`outputs/`、`__pycache__/`（`.gitignore` 已经挡了，但别自己加例外）
3. 大文件先看 §3.4

### 3.4 上传数据（最容易出错的地方）

**数据分三层，只有第一层进 git：**

| 层 | 放哪 | 进 git 吗 |
|---|---|---|
| 小样本 / demo（几百行） | `data/demo/` | ✅ 进 |
| 全量数据（几十 MB 到几 GB） | Zenodo / Figshare / 组内网盘 | ❌ 不进，写进 `data/MANIFEST.json` |
| 运行产物（图、模型、中间结果） | `outputs/` | ❌ 不进（已在 .gitignore） |

**判断标准很简单：单文件超过 50 MB，就不要进 git。**

要公开全量数据时，按 `data/README.md` 的清单填 `MANIFEST.json`：

```json
{
  "name": "data_point_pd.pkl",
  "url": "https://zenodo.org/records/XXXXX/files/data_point_pd.pkl",
  "sha256": "<64 位十六进制>",
  "size_bytes": 12345678,
  "description": "一行一个像素点；列 feature_1..6 + label(M0/M1/M2)",
  "license": "CC-BY-4.0"
}
```

算 sha256：

```bash
python -c "import hashlib,sys;print(hashlib.sha256(open(sys.argv[1],'rb').read()).hexdigest())" 文件名
```

### 3.5 下载

| 我要什么 | 怎么做 |
|---|---|
| 整个仓库 | `git clone <url>` |
| 最新代码 | `git pull` |
| 只要一个文件 | 网页打开文件 → 右上 **Raw** → 另存 |
| 全量数据 | 按 `data/MANIFEST.json` 的 url 下载，**必须校验 sha256** |
| 别人的开源代码 | 不要 `git clone` 到本仓库里，放 `_external/`（已在 .gitignore） |

校验 sha256：

```bash
python -c "import hashlib,sys;print(hashlib.sha256(open(sys.argv[1],'rb').read()).hexdigest())" 下载的文件
# 和 MANIFEST.json 里的 sha256 逐字比对，不一致就是文件坏了或被换过
```

### 3.6 提 PR 的规矩

- **一个 PR 只做一件事**。顺手改了五处，owner 没法审。
- 标题写成一句话，和提交信息同风格：`feat: 新增力曲线平滑滤波`
- 描述里写三行：**改了什么 / 为什么改 / 怎么验证的**
- 如果结果有变化，把新旧数字贴出来

```markdown
## 改了什么
新增 Savitzky-Golay 平滑，替换原来的滑动平均

## 为什么
滑动平均把峰位压平了，M1/M2 的 F1 掉了 3 个点

## 怎么验证
在 demo 数据上跑 `python src/train.py --seed 0`，accuracy 0.883 → 0.897
```

---

## 4. 红线（做了会出事）

| 别做 | 后果 | 正确做法 |
|---|---|---|
| 直接推 `main` | 覆盖别人的改动，无法追溯 | 建分支 → PR |
| `git push --force` | 抹掉别人的提交历史 | 用 `git revert` 或新提交修正 |
| 提交数据 / 模型权重 | 仓库几十 G，别人 clone 不下来 | 三层规则，见 §3.4 |
| 提交 `.env` / token / 密钥 | **一旦推上去就等于泄漏**，GitHub 上删掉也能被扒出来 | 用环境变量；发现推了立刻告诉 owner |
| 把私有仓库改成公开 | 未发表数据提前暴露，可能影响投稿 | 由 owner 决定，见 `docs/publishing.md` |
| 改或删已发布的 tag | 论文里引用的版本对不上 | 发新版本 `v1.0.1` |
| 一个 PR 塞五件事 | owner 没法审，拖慢进度 | 拆开 |

---

## 5. 出了事怎么办

| 情况 | 处理 |
|---|---|
| **推到了 main（还没人拉）** | 立刻告诉 owner，别自己 `reset --hard` 硬来 |
| **提交了不该提交的数据** | `git rm --cached 文件` → 加进 `.gitignore` → 新提交。**不要改历史**（rebase/force 会毁掉别人的工作） |
| **推了密钥/token** | **第一件事：去 GitHub 页面把这个 token 作废**。然后告诉 owner。历史清理是第二步 |
| **push 被拒：`protected branch`** | 说明你在推 main，改推分支 |
| **push 被拒：`non-fast-forward`** | 先 `git pull --rebase`，有冲突就解决；搞不定找 owner |
| **push 报 `Could not connect to server`** | 这是本机到 github.com 的间歇性断连（不是你的问题）。等 2–3 分钟重试；连试 3 次不行就找 owner |
| **clone 私有库报 `Repository not found`** | ① 邀请没接受 ② owner 没给 Write 权限 ③ 登录的账号不对 |
| **忘了开分支，改已经在 main 上** | `git stash` → `git checkout -b feat/xxx` → `git stash pop` |

---

## 6. 智能体执行协议（喂给大模型时用这一节）

> 把这份文档整份贴给智能体，并附一句：
> **「严格按 §6 执行，其余章节是约束上下文。」**

### 6.1 开工前（缺一不可）

1. 确认在仓库内：`git rev-parse --show-toplevel`；不在就停下来问用户仓库路径。
2. `git checkout main && git pull` —— 任何写操作之前。
3. 检查身份：`git config user.name` 和 `user.email`。**为空就问用户，不要自己编一个。**

### 6.2 分支

- **绝不允许直接提交或推送到 `main`。** 无论用户怎么说"就改一下"，也先建分支。
- 分支名：`feat/<kebab>`、`fix/<kebab>`、`data/<kebab>`、`docs/<kebab>`、`exp/<kebab>`。
- 一个分支只做一件事。

### 6.3 提交前自检（三条，缺一条就不许提交）

1. `git status --porcelain` 的清单里**不得出现**：
   - `data/raw/`、`outputs/`、`_external/`
   - `*.hdf5`、`*.h5`、`*.pkl`、`*.npy`、`*.zip`、`*.tar.gz`
   - `.env`、`token.txt`、`*.key`、`*.pem`、`id_rsa*`
   出现了就先 `git rm --cached` 并追加 `.gitignore`，再提交。
2. 任何**单文件 >50 MB** → 停下来报告用户，不要提交。
3. 提交信息格式 `<type>: <一句话>`，`type` ∈ `feat|fix|data|docs|exp|chore`。

### 6.4 推送与失败分支

```bash
git push -u origin <分支名>
```

| 报错 | 处理 |
|---|---|
| `Could not connect to server` / `Connection was reset` / `Failed to connect ... 443` | 本机到 github.com 间歇性断连。**最多重试 3 次**，仍失败则改用 API 通道：<br>`python C:\Users\Administrator\.dsh\tools\ghget\api-commit.py --repo <owner/repo> --message "<提交信息>" --file <路径>` |
| `protected branch` | 目标分支受保护，改推分支 |
| `non-fast-forward` | `git pull --rebase origin <分支>`，冲突无法解决就停下问人 |

**该 API 通道在同一台机器上可用**；其他机器上不要用，直接重试并报告。

### 6.5 数据相关

- **不自行决定公开任何数据。** 涉及数据公开、改仓库可见性，一律停下问用户。
- 下载外部数据：按 `data/MANIFEST.json` 取，**必须校验 sha256**，不一致就报错停下。
- 引用别人的代码：记 `owner/repo@<commit sha>` + license；license 为 `unknown` 时只能读，不能复制进本仓库。

### 6.6 不得擅自修改

除非用户明确要求，**不要**改：

- `LICENSE`
- `.github/workflows/**`
- `.gitignore` 里已有的规则（只能追加）
- 已存在的 tag、已合并的 PR 描述

### 6.7 汇报格式（做完必须给）

```
分支   feat/force-curve-filter
commit 4a9f2c1
改动   src/preprocess.py (+42/-8)
检查   大文件 0；敏感文件 0；>50MB 0
待办   PR 未提（需要用户在网页操作），或：PR 已提 #12
```

### 6.8 停机条件（遇到就停，不要硬想办法）

- 需要公开数据 / 改仓库可见性
- 需要删除仓库、删除分支、改写历史
- 需要操作别人的 PR 或 issue
- 需要用户提供 token、密码、验证码
- 以上任何一条，**停下来把情况说清楚**，不要"先做了再说"。

---

## 7. 常用命令速查

```bash
# 身份（一次性）
git config --global user.name "张三"
git config --global user.email "zhangsan@aufe.edu.cn"

# 拿到代码 / 同步
git clone https://github.com/Wu-aufe-lab/paper-<短标题>.git
git checkout main && git pull

# 干活
git checkout -b feat/xxx
git status                      # 看清楚再 add
git add -A
git commit -m "feat: xxx"
git push -u origin feat/xxx

# 出错时
git log --oneline -5            # 最近 5 次提交
git diff                        # 还没 add 的改动
git diff --cached               # 已 add 未提交的改动
git checkout -- 文件            # 丢弃某个文件的改动
git stash                       # 临时收起改动
git stash pop                   # 恢复

# 看当前版本（写论文要用）
git rev-parse --short HEAD
```

---

## 8. 找人

| 问题 | 找谁 |
|---|---|
| 邀请、权限、仓库建在哪 | owner（WuHao，GitHub `120200004`） |
| 怎么发这篇论文、DOI | 看 `docs/publishing.md` |
| 数据该放哪、能不能公开 | 先问 owner，**不要自己决定** |
| 代码跑不通 | 先看 README，再在 issue 里写清楚：命令 + 完整报错 + 环境 |

---

**最后一句**：这个仓库的目的是让论文可复现。你现在多写一句 README、多锁一个版本号，将来就少一个审稿人问"你的代码能跑吗"。
