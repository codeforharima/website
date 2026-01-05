# Markdownの不正な書式修正スクリプト
import re
from pathlib import Path


def fix_markdown_spaces_safely(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    # 修正前の状態を保存
    original = content

    # 修正パターン
    patterns = [
        (r"^(\s*[*+-])　", r"\1 ", re.MULTILINE),  # 箇条書き
        (r"^(\s*\d+\.)　", r"\1 ", re.MULTILINE),  # 番号付きリスト
        (r"^(#{1,6})　", r"\1 ", re.MULTILINE),  # 見出し
        (r"([*_`\[])\u3000", r"\1 ", re.MULTILINE),  # Markdown記号の後
        (r"\u3000([*_`\]])", r" \1", re.MULTILINE),  # Markdown記号の前
    ]

    fixes_made = []
    for pattern, replacement, flags in patterns:
        matches = list(re.finditer(pattern, content, flags))
        if matches:
            fixes_made.append({"pattern": pattern, "count": len(matches), "matches": [m.group() for m in matches[:3]]})  # 最初の3つだけ表示
            content = re.sub(pattern, replacement, content, flags=flags)

    if content != original:
        # バックアップ作成（任意）
        backup_path = file_path.with_suffix(".md.bak")
        if not backup_path.exists():
            import shutil

            shutil.copy2(file_path, backup_path)

        # 修正を適用
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)

        return True, fixes_made
    return False, []


def main():
    import sys

    if len(sys.argv) > 1:
        root_dir = sys.argv[1]
    else:
        root_dir = "."

    for md_file in Path(root_dir).rglob("*.md"):
        print(f"処理中: {md_file}")
        changed, fixes = fix_markdown_spaces_safely(md_file)
        if changed:
            print(f"  ✓ 修正しました")
            for fix in fixes:
                print(f"    - {fix['pattern']}: {fix['count']}箇所")
                if fix["matches"]:
                    print(f"      例: {fix['matches']}")
        else:
            print(f"  ○ 問題なし")


if __name__ == "__main__":
    main()
