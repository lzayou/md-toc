"""命令行入口的集成测试。"""

import subprocess
import sys
import unittest
from pathlib import Path

# 仓库根目录，保证子进程可以用 python -m 找到 md_toc 包
REPO_ROOT = Path(__file__).resolve().parent.parent


def normalize_newlines(text: str) -> str:
    """统一换行符，避免 Windows 上 CRLF 与 LF 的差异影响断言。"""
    return text.replace("\r\n", "\n")


class CliEncodingTest(unittest.TestCase):
    """命令行工具在管道场景下的字节输出。"""

    def test_output_is_utf8_when_piped(self):
        markdown = "# 标题一\n\n## 标题二\n"
        result = subprocess.run(
            [sys.executable, "-m", "md_toc.cli"],
            input=markdown.encode("utf-8"),
            capture_output=True,
            cwd=str(REPO_ROOT),
        )

        self.assertEqual(result.returncode, 0, result.stderr.decode("utf-8", "replace"))
        # 输出必须是 UTF-8 字节，否则 Windows 中文环境下会出现乱码
        expected = "- [标题一](#标题一)\n  - [标题二](#标题二)\n"
        self.assertEqual(normalize_newlines(result.stdout.decode("utf-8")), expected)

    def test_flat_and_level_filter(self):
        markdown = "# 一级\n\n## 二级\n\n### 三级\n"
        result = subprocess.run(
            [sys.executable, "-m", "md_toc.cli", "--min-level", "2", "--flat"],
            input=markdown.encode("utf-8"),
            capture_output=True,
            cwd=str(REPO_ROOT),
        )

        self.assertEqual(result.returncode, 0, result.stderr.decode("utf-8", "replace"))
        self.assertEqual(
            normalize_newlines(result.stdout.decode("utf-8")),
            "- [二级](#二级)\n- [三级](#三级)\n",
        )

    def test_no_heading_returns_error(self):
        result = subprocess.run(
            [sys.executable, "-m", "md_toc.cli"],
            input="只有正文，没有标题\n".encode("utf-8"),
            capture_output=True,
            cwd=str(REPO_ROOT),
        )

        self.assertEqual(result.returncode, 1)
        self.assertIn("未找到符合条件的标题", result.stderr.decode("utf-8"))


if __name__ == "__main__":
    unittest.main()
