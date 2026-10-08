"""md-toc：零依赖的 Markdown 目录（TOC）生成器。"""

from .core import Heading, parse_headings, render_toc, slugify

__version__ = "0.1.0"

__all__ = ["Heading", "parse_headings", "render_toc", "slugify", "__version__"]
