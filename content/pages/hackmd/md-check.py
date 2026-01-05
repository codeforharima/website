# Markdownの不正な書式検出スクリプト
import os
import re


def check_markdown_issues(file_path):
    issues = []
    with open(file_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    for i, line in enumerate(lines, 1):
        # 全角スペースの検出
        if "　" in line:
            issues.append(f"行{i}: 全角スペースを含みます")

        # 箇条書きの全角スペース
        if re.match(r"^\s*[*+-]　", line):
            issues.append(f"行{i}: 箇条書きに全角スペースを使用しています: {line.strip()}")

        # 番号付きリストの全角スペース
        if re.match(r"^\s*\d+\.　", line):
            issues.append(f"行{i}: 番号付きリストに全角スペースを使用しています: {line.strip()}")

        # 見出しの全角スペース
        if re.match(r"^#{1,6}　", line):
            issues.append(f"行{i}: 見出しに全角スペースを使用しています: {line.strip()}")

    return issues


def main():
    for root, dirs, files in os.walk("."):
        for file in files:
            if file.endswith(".md"):
                file_path = os.path.join(root, file)
                issues = check_markdown_issues(file_path)
                if issues:
                    print(f"\n=== {file_path} ===")
                    for issue in issues:
                        print(f"  - {issue}")


if __name__ == "__main__":
    main()
