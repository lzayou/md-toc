"""md-toc 的命令行入口。"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from .core import parse_headings, render_toc


def _configure_stdio() -> None:
    """把标准输入输出固定为 UTF-8。

    Windows 中文环境的控制台默认使用 GBK，输出通过管道时中文会变成乱码，
    因此这里显式统一编码。
    """
    for stream in (sys.stdin, sys.stdout, sys.stderr):
        reconfigure = getattr(stream, "reconfigure", None)
        if reconfigure is None:
            continue
        try:
            reconfigure(encoding="utf-8")
        except (ValueError, OSError):
            # 流已经被重定向为不支持修改编码的对象时忽略即可
            pass


def build_parser() -> argparse.ArgumentParser:
    """构造命令行参数解析器。"""
    parser = argparse.ArgumentParser(
        prog="md-toc",
        description="从 Markdown 文件生成目录（TOC）。",
    )
    parser.add_argument("path", nargs="?", help="Markdown 文件路径，缺省时从标准输入读取。")
    parser.add_argument("--min-level", type=int, default=1, help="最小标题层级，默认为 1。")
    parser.add_argument("--max-level", type=int, default=3, help="最大标题层级，默认为 3。")
    parser.add_argument("--flat", action="store_true", help="输出不使用缩进的扁平列表。")
    parser.add_argument("--heading", default="", help="在目录前附加的标题，例如“## 目录”。")
    return parser


def main(argv: list[str] | None = None) -> int:
    """执行命令行逻辑，返回进程退出码。"""
    _configure_stdio()
    args = build_parser().parse_args(argv)

    if args.path:
        text = Path(args.path).read_text(encoding="utf-8")
    else:
        text = sys.stdin.read()

    headings = parse_headings(text, min_level=args.min_level, max_level=args.max_level)
    toc = render_toc(headings, indent=not args.flat)

    if not toc:
        print("未找到符合条件的标题。", file=sys.stderr)
        return 1

    if args.heading:
        print(args.heading)
        print()

    print(toc)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
