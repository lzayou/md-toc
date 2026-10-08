# md-toc

[![CI](https://github.com/lzayou/md-toc/actions/workflows/ci.yml/badge.svg)](https://github.com/lzayou/md-toc/actions/workflows/ci.yml)

零依赖的 Markdown 目录（TOC）生成器。

`md-toc` 从 Markdown 文档中提取标题，生成与 GitHub 章节链接一致的目录，全程只使用 Python 标准库。

## 特性

- 零第三方依赖，Python 3.9 及以上可用
- 支持 ATX 标题，即 `#` 到 `######`
- 自动跳过围栏代码块中的 `#`
- 锚点规则与 GitHub 保持一致，重名标题自动追加 `-1`、`-2` 后缀
- 支持中文标题、标题层级过滤、缩进与扁平两种输出

## 安装

```bash
pip install .
```

## 使用

从文件生成目录：

```bash
md-toc README.md
```

从标准输入读取：

```bash
cat README.md | md-toc
```

只保留二级和三级标题，并附加一个目录标题：

```bash
md-toc README.md --min-level 2 --max-level 3 --heading "## 目录"
```

输出扁平列表：

```bash
md-toc README.md --flat
```

### 输出示例

输入：

```markdown
# 项目说明

## 快速开始

## 快速开始
```

输出：

```markdown
- [项目说明](#项目说明)
  - [快速开始](#快速开始)
  - [快速开始](#快速开始-1)
```

## 命令行参数

| 参数 | 说明 | 默认值 |
| --- | --- | --- |
| `path` | Markdown 文件路径，缺省时从标准输入读取 | 无 |
| `--min-level` | 最小标题层级 | `1` |
| `--max-level` | 最大标题层级 | `3` |
| `--flat` | 输出扁平列表，不使用缩进 | 关闭 |
| `--heading` | 在目录前附加的标题文本 | 空 |

## 开发

运行单元测试：

```bash
python -m unittest discover -s tests -v
```

## 许可证

本项目基于 [MIT](LICENSE) 许可证开源。
