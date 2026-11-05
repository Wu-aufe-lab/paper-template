# 模板使用说明（新仓库建好后可直接删除本文件）

这是一个「论文代码 + 数据」仓库模板。用 **Use this template** 建新仓库后，按下面四步改。

## 1. 建仓库后必改的 4 处

| 文件 | 改什么 |
|---|---|
| `README.md` | 第 1 行标题、引用块（作者/年份/刊名/DOI）、末尾 DOI badge |
| `CITATION.cff` | `title` / `authors` / `preferred-citation` / `repository-code` / `url` |
| `.zenodo.json` | `title` / `creators` / `related_identifiers`（论文 DOI） |
| `data/MANIFEST.json` | 真实数据文件的 url / sha256 / 字段说明 |

## 2. 代码放哪

- 每个阶段一个入口：`src/train.py`、`src/evaluate.py`、`src/plot.py`
- **不要**硬编码路径：一律 `argparse` 传 `--data` / `--out`
- **必须**固定随机种子：`--seed`，论文里写清楚用的是哪个值
- 输出只写进 `--out`，产出 `metrics.json` 这类机器可读文件，不要只 print

## 3. 数据分三层

| 层 | 位置 | 进 git 吗 |
|---|---|---|
| demo 小样本（几百行，够跑通） | `data/demo/` | 进 |
| 全量数据 | Zenodo / Figshare / 机构库 | 不进，写进 `MANIFEST.json` |
| 运行产物 | `outputs/` | 不进（已在 .gitignore） |

大文件进 git 的三个后果：GitHub 拒收 >100 MB、仓库体积永久膨胀、数据没有独立 DOI。

## 4. 发布流程

1. 确认 CI 绿：GitHub 仓库页 → Actions → `smoke` 全绿
2. Zenodo → Settings → GitHub → 打开本仓库开关
3. GitHub → Releases → Draft a new release → tag `v1.0.0` → Publish
4. Zenodo 自动归档并发 DOI
5. 回填 README badge + `CITATION.cff` 的 `url`
6. 论文 Data availability 写：`https://doi.org/10.5281/zenodo.XXXXXXX`（v1.0.0, commit `abcdef1`）

## 5. 组内协作

- 仓库转到 Organization，组员进 Team，权限给 **Write**（删不了库）
- `main` 开 branch ruleset：禁删除、禁 force push、必须 PR + 1 人 review
- 组员只能「建分支 → 提 PR」，你在 PR 里点 merge —— 这就是「能上传、不能删」

## 6. 自检清单

- [ ] 新机器 `git clone` 后 `pip install -r requirements.txt && python src/train.py` 能跑通
- [ ] `requirements.txt` 是 `pip freeze` 出来的真实版本，不是手写的
- [ ] README 里每条命令都实际执行过
- [ ] 没有把 `_external/`、`data/raw/`、`outputs/` 提交进去
- [ ] LICENSE 覆盖代码；第三方数据在 `MANIFEST.json` 里单独标了 license
