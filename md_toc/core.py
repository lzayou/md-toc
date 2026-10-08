"""Markdown 目录（TOC）生成的核心逻辑。

本模块只依赖标准库，负责三件事：

1. 从 Markdown 文本中解析 ATX 标题（``# 标题`` 这类写法）；
2. 生成与 GitHub 章节链接一致的锚点；
3. 把标题渲染成 Markdown 列表形式的目录。
"""

from __future__ import annotations

import re
from dataclasses import dataclass

# 匹配 ATX 标题，允许结尾出现跟随的 # 符号
_HEADING_RE = re.compile(r"^(#{1,6})\s+(.*?)\s*#*\s*$")
# 匹配围栏代码块的开头或结尾
_FENCE_RE = re.compile(r"^\s*(`{3,}|~{3,})")
# 标题中的行内代码
_INLINE_CODE_RE = re.compile(r"`([^`]*)`")
# 标题中的链接与图片，保留可见文字
_LINK_RE = re.compile(r"!?\[([^\]]*)\]\([^)]*\)")
# 标题中的强调标记
_EMPHASIS_RE = re.compile(r"(\*{1,2}|_{1,2}|~~)(.*?)\1")
# 标题中的 HTML 标签
_HTML_TAG_RE = re.compile(r"<[^>]+>")


@dataclass(frozen=True)
class Heading:
    """一个解析后的 Markdown 标题。"""

    level: int
    """标题层级，1 表示一级标题。"""

    text: str
    """标题的原始文本。"""

    title: str
    """去除行内标记后用于展示的文本。"""

    anchor: str
    """GitHub 风格的锚点，可直接用于 ``#锚点`` 链接。"""


def strip_inline_markup(text: str) -> str:
    """去掉标题里的行内标记，保留可读文字。"""
    text = _INLINE_CODE_RE.sub(r"\1", text)
    text = _LINK_RE.sub(r"\1", text)
    text = _EMPHASIS_RE.sub(r"\2", text)
    text = _HTML_TAG_RE.sub("", text)
    return text.strip()


def slugify(title: str) -> str:
    """把标题文本转换成 GitHub 风格的锚点（不含重名后缀）。"""
    text = title.strip().lower()
    # 保留字母、数字、下划线、连字符、空格以及中日韩等文字，其余标点全部丢弃
    text = re.sub(r"[^\w\s-]", "", text)
    text = re.sub(r"\s+", "-", text)
    return text


def parse_headings(
    markdown: str,
    min_level: int = 1,
    max_level: int = 3,
) -> list[Heading]:
    """解析 Markdown 文本中的标题。

    围栏代码块（``` 与 ~~~）内的 ``#`` 不会被当作标题。
    重名标题会按照 GitHub 的规则追加 ``-1``、``-2`` 等后缀。
    """
    headings: list[Heading] = []
    seen: dict[str, int] = {}
    fence_char = ""
    fence_len = 0

    for line in markdown.splitlines():
        fence = _FENCE_RE.match(line)
        if fence:
            marker = fence.group(1)
            char, length = marker[0], len(marker)
            if not fence_char:
                fence_char, fence_len = char, length
            elif char == fence_char and length >= fence_len:
                fence_char, fence_len = "", 0
            continue

        if fence_char:
            # 位于代码块内部，跳过
            continue

        match = _HEADING_RE.match(line)
        if not match:
            continue

        level = len(match.group(1))
        if level < min_level or level > max_level:
            continue

        raw = match.group(2).strip()
        title = strip_inline_markup(raw)
        if not title:
            continue

        base = slugify(title)
        count = seen.get(base, 0)
        seen[base] = count + 1
        anchor = base if count == 0 else f"{base}-{count}"

        headings.append(Heading(level=level, text=raw, title=title, anchor=anchor))

    return headings


def render_toc(headings: list[Heading], indent: bool = True) -> str:
    """把标题列表渲染成 Markdown 目录。"""
    if not headings:
        return ""

    base_level = min(heading.level for heading in headings)
    lines = []
    for heading in headings:
        prefix = "  " * (heading.level - base_level) if indent else ""
        lines.append(f"{prefix}- [{heading.title}](#{heading.anchor})")
    return "\n".join(lines)
