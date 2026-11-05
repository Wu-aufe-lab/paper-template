# 这篇论文怎么发 — GitHub 与 DOI 流程

> 本文件随论文仓库一起生成（来自 `paper-template`）。读完这一页，你就知道每个阶段做什么、谁来做。
> 如果你是**组员**：你只需要看 §2 和 §7；建库、发布、DOI 由 owner 做。

## 0. 一页流程图

```
① 建库(owner)      私有 + 本模板
      ↓
② 开发(所有人)     分支 → 提交 → PR
      ↓
③ 投稿前体检(owner) clone 能跑通、CI 绿、数据分层对
      ↓
④ 投稿             Data availability 写清楚
      ↓
⑤ 录用后发布(owner) 转公开 → tag v1.0.0 → Release → Zenodo DOI
      ↓
⑥ 维护             issue、勘误版本（新 version DOI）
```

---

## 1. 建库（owner，5 分钟）

1. 打开 `https://github.com/Wu-aufe-lab/paper-template` → 右上 **Use this template** → **Create a new repository**
2. Owner 选 **`Wu-aufe-lab`**，名字 `paper-<短标题>`（例：`paper-afm-macrophage`）
3. **必须选 Private**
4. 建完改四处占位符：`README.md`、`CITATION.cff`、`.zenodo.json`、`data/MANIFEST.json`
5. 推首版，确认 CI `smoke` 绿

> 仓库一律建在 `Wu-aufe-lab` 组织下，不要建在个人账号。
> 组织设置已锁：成员不能删仓库、不能改可见性；**但 Free 套餐管不住“新建公开仓库”，所以第 3 步靠自觉。**

---

## 2. 开发（所有人）

### 分支与提交

```bash
git clone https://github.com/Wu-aufe-lab/paper-<短标题>.git
cd paper-<短标题>
git checkout -b feat/your-topic      # 不要直接推 main
# ... 改代码 ...
git add -A
git commit -m "feat: 一句话说清改了什么"
git push -u origin feat/your-topic
```

然后在网页上**提 Pull Request**，等 owner merge。

### 三条硬规矩

| 规矩 | 原因 |
|---|---|
| 大文件（>50 MB）不进 git | GitHub 拒收 >100 MB，仓库会永久膨胀 |
| 数据按三层放：`data/demo/` 进库、全量放 Zenodo、`outputs/` 不进库 | 见 `data/README.md` |
| 随机种子写进代码，`--seed` 可配 | 否则结果复现不了 |

### 提交信息

```
feat: 新增什么        fix: 修了什么        data: 数据相关
docs: 文档            exp: 实验脚本        chore: 杂项
```

---

## 3. 投稿前体检（owner，半天）

逐条打勾，缺一条都别投：

- [ ] **新机器能跑通**：`git clone` → `pip install -r requirements.txt` → `python src/train.py` 出结果
- [ ] `requirements.txt` 是 `pip freeze` 出来的**真实版本**，不是手写猜的
- [ ] `README.md` 里每条命令都**实际执行过**
- [ ] GitHub Actions 的 `smoke` 是绿的
- [ ] 没有把 `data/raw/`、`outputs/`、`_external/`、`*.hdf5` 提交进去
- [ ] `LICENSE` 覆盖代码；第三方数据在 `data/MANIFEST.json` 里单独标了 license
- [ ] README 的 Data availability 段落写好了（见 §4）
- [ ] 论文里出现的每个数字，仓库里都能找到对应脚本

> **判据**：一个没见过这个项目的人，只看 README，能不能在半小时内跑出你的主图？不能就别投。

---

## 4. 投稿：Data availability 怎么写

三种写法，按情况选（**能用第一种就别用第三种**）：

| 情形 | 写法 |
|---|---|
| 录用后公开（最常见） | `Code and data will be available at https://github.com/Wu-aufe-lab/<repo> upon publication.` |
| 现在就公开 | `Code and data are available at https://github.com/Wu-aufe-lab/<repo> (v1.0.0).` |
| 数据涉及隐私/专利，只能申请 | `Data are available from the corresponding author upon reasonable request.` |

第三种越来越不被接受——审稿人现在会直接问“为什么不能公开”。用之前先想清楚：能不能只公开**处理后的**数据？

**发表后**换成正式 DOI 写法：

```
Code and data are available at https://doi.org/10.5281/zenodo.XXXXXXX (v1.0.0, commit abc1234).
```

---

## 5. 录用后发布（owner，1 小时）

### 第 1 步：转公开
仓库 **Settings → General → Danger Zone → Change visibility → Public**
（组织设置禁止成员改可见性，**owner 不受限**）

### 第 2 步：补分支保护
转公开后立刻加 ruleset：`main` 禁删除、禁 force push、必须 PR。
（私有库在 Free 套餐下加不了，公开库可以。）

### 第 3 步：打 tag
```bash
git checkout main && git pull
git tag -a v1.0.0 -m "release for <期刊> submission"
git push origin v1.0.0
```

### 第 4 步：发 Release
仓库 **Releases → Draft a new release** → 选 `v1.0.0` → 标题写论文短名 → **Publish release**

### 第 5 步：Zenodo 出 DOI（只做一次授权）
1. 登录 [zenodo.org](https://zenodo.org)（用 GitHub 账号）
2. **Settings → GitHub** → 找到本仓库 → 打开开关
3. 回到 Release 页面，确认 Zenodo 已归档（会显示 DOI badge）
4. 记下两个 DOI：
   - **Concept DOI**（`10.5281/zenodo.XXXXXXX`）→ 永远指向最新版，**论文里写这个**
   - **Version DOI** → 指这一版，复现时引用

### 第 6 步：回填
- README 顶部的 badge
- `CITATION.cff` 的 `url`
- 论文的 Data availability
- 组会/汇报里同步这个链接

---

## 6. 维护

| 情况 | 怎么做 |
|---|---|
| 有人提 issue | 一周内回，哪怕只说“看到了，会处理” |
| 发现错误要勘误 | 修完发 `v1.0.1` → Zenodo 出新 **version DOI**，**concept DOI 不变** |
| 有人复现失败 | 优先修 `README` 和 `requirements.txt`——八成是环境问题 |
| **已发布的 tag 不能改** | 不能 force push、不能删；要改就发新版本 |

---

## 7. 常见错误

| 错误 | 后果 | 正确做法 |
|---|---|---|
| 仓库建在个人账号下 | 组员没权限、换人时麻烦 | 建在 `Wu-aufe-lab` 组织下 |
| 建库时没细看选了 Public | 未发表数据提前泄漏 | 一律 Private；要公开等录用 |
| 把数据 push 进 git | 仓库几十 G、clone 不下来 | 大文件走 Zenodo + MANIFEST |
| `requirements.txt` 写 `tensorflow` 不写版本 | 半年后别人装出来跑不通 | `pip freeze` 出真实版本 |
| 论文里写“代码可向作者索取” | 审稿人认为不可复现，直接质疑 | 尽量公开；不能公开就说明原因 |
| 直接推 main | 覆盖别人的改动 | 建分支 + PR |
| Release 之后又改了代码 | DOI 指向的版本和仓库对不上 | 改动发新版本 `v1.0.1` |

---

## 8. 命令速查

```bash
# 克隆
git clone https://github.com/Wu-aufe-lab/paper-<短标题>.git

# 开分支干活
git checkout -b feat/xxx
git add -A && git commit -m "feat: xxx"
git push -u origin feat/xxx

# 同步主分支
git checkout main && git pull

# 打标签发布
git tag -a v1.0.0 -m "release"
git push origin v1.0.0

# 看当前提交（写进论文用）
git rev-parse --short HEAD
```

---

## 9. 谁做什么

| 阶段 | Owner | 组员 |
|---|---|---|
| 建库 | ✅ | — |
| 开发 | ✅ | ✅（走 PR） |
| 投稿前体检 | ✅ | 配合补材料 |
| 投稿 | ✅（或通讯作者） | — |
| 转公开 / Release / DOI | ✅ | — |
| 维护 | ✅ | 提 issue |

有问题先看本文件，再问 owner。**不要直接推 main。**
