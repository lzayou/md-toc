"""md-toc 核心功能的单元测试。"""

import unittest

from md_toc.core import parse_headings, render_toc, slugify


class SlugifyTest(unittest.TestCase):
    """锚点生成规则。"""

    def test_lowercase_and_hyphenate(self):
        self.assertEqual(slugify("Hello World"), "hello-world")

    def test_drop_punctuation(self):
        self.assertEqual(slugify("C++ / Rust?"), "c-rust")

    def test_keep_chinese_characters(self):
        self.assertEqual(slugify("快速开始"), "快速开始")


class ParseHeadingsTest(unittest.TestCase):
    """标题解析规则。"""

    def test_parse_basic_headings(self):
        headings = parse_headings("# 标题一\n\n## 标题二\n", min_level=1, max_level=3)
        self.assertEqual([h.level for h in headings], [1, 2])
        self.assertEqual([h.title for h in headings], ["标题一", "标题二"])

    def test_skip_fenced_code_block(self):
        markdown = "# 真实标题\n\n```python\n# 这是注释，不是标题\n```\n"
        headings = parse_headings(markdown)
        self.assertEqual([h.title for h in headings], ["真实标题"])

    def test_deduplicate_anchors(self):
        headings = parse_headings("# 重复\n\n# 重复\n\n# 重复\n")
        self.assertEqual([h.anchor for h in headings], ["重复", "重复-1", "重复-2"])

    def test_filter_by_level(self):
        markdown = "# 一级\n\n## 二级\n\n#### 四级\n"
        headings = parse_headings(markdown, min_level=2, max_level=3)
        self.assertEqual([h.title for h in headings], ["二级"])

    def test_strip_inline_markup(self):
        headings = parse_headings("## `code` 与 **粗体** 和 [链接](https://example.com)\n")
        self.assertEqual(headings[0].title, "code 与 粗体 和 链接")


class RenderTocTest(unittest.TestCase):
    """目录渲染规则。"""

    def test_render_indented_toc(self):
        headings = parse_headings("# 一\n\n## 二\n")
        self.assertEqual(render_toc(headings), "- [一](#一)\n  - [二](#二)")

    def test_render_flat_toc(self):
        headings = parse_headings("# 一\n\n## 二\n")
        self.assertEqual(render_toc(headings, indent=False), "- [一](#一)\n- [二](#二)")

    def test_render_empty(self):
        self.assertEqual(render_toc([]), "")


if __name__ == "__main__":
    unittest.main()
