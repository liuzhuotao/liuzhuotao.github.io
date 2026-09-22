# 维护论文列表

## 从 BibTeX 导入

1. 在仓库根目录添加或更新 `publications.bib`，放入需要导入的 BibTeX 条目。
2. 推送到 `main` 后，`Import Publications From Bibtex` 工作流会生成一个 PR。
3. 检查 PR 中的 `content/publications/<citation-key>/index.md`，确认作者、日期和链接后合并。

已有论文使用了自定义路径和作者 ID。导入前先搜索标题，避免为已有论文创建重复条目。
组内作者应使用 `content/authors/` 下的目录名，例如 `liuzhuotao`。
需要分类筛选时，在生成的文件中补充 `Subtype`。导入工具不会自动匹配现有的研究分类。
GitHub 仓库需允许 Actions 创建 Pull Request。

## 手动添加

也可以在 `content/publications/<研究方向>/` 下新增一个 Markdown 文件。最小示例：

```yaml
---
title: '论文标题'
date: '2026-01-01'
authors:
  - First Author
  - liuzhuotao
author_notes:
  - null
  - Corresponding Author
publication: '会议或期刊名称'
Subtype: Encrypted Traffic Analysis
links:
  - type: site
    label: Paper
    url: https://www.usenix.org/conference/usenixsecurity25/presentation/yan-jinzhu
---
```

`author_notes` 与 `authors` 按位置对应；没有备注的作者填 `null`。
已有的 `doi` 字段继续支持完整网址和 `10.xxxx/...` 格式的 DOI 编号。
新增普通论文网页推荐使用上面的 `links`；真正的 DOI 也可以写为：

```yaml
hugoblox:
  ids:
    doi: 10.1145/3719027.3744824
```

Code 按钮使用 `links` 中的 `type: code` 和完整仓库 URL。

## 本地验证

```sh
hugo --minify
node scripts/check-publication-links.mjs public
```

部署工作流会执行同样的链接格式检查。它检查重复前缀和格式错误，不检查外部网站的实时可用性。
