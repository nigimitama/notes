# トップページ（index.md）を生成する
from pathlib import Path
import yaml


workdir = Path(".")
book_dir = workdir / "book"

with open(book_dir / "myst.yml", "r", encoding="utf-8") as f:
    config = yaml.load(f, Loader=yaml.CLoader)

toc = config["project"]["toc"]


ncols = 2

def make_card(section: dict) -> str:
    """セクション（title + children）から grid-item-card を作る"""
    articles = []
    # 第1層までのファイルを取得
    for chapter in section["children"]:
        if "file" not in chapter:
            continue
        file_path: str = chapter["file"]
        articles.append(f"- []({file_path})")
    articles = "\n".join(articles)
    return ":::{grid-item-card}\n" + f"{section['title']}\n" + f"\n{articles}\n" + ":::"


def make_grid(cards: list[str]) -> str:
    cards = "\n\n".join(cards)
    return (
        f"::::{{grid}} 1 1 {ncols} {ncols}\n"
        ":gutter: 2\n"
        ":padding: 2\n"
        ":margin: 2\n"
    ) + f"\n{cards}\n" + "::::"


# toc は「カテゴリ（title + children）> セクション（title + children）> ファイル」の構造
parts = []
for category in toc:
    # index.md などカテゴリ（title + children）でないエントリはスキップ
    if "title" not in category or "children" not in category:
        continue
    cards = [
        make_card(section)
        for section in category["children"]
        if "title" in section and "children" in section
    ]
    if not cards:
        continue
    parts.append(f"## {category['title']}\n\n" + make_grid(cards))

grid = "\n\n".join(parts)

content = f"""
# データサイエンス関連+αのメモ

統計学・機械学習（+その他の気になった分野）の教科書や論文を読み、自分で理解した範囲の理論と実装をメモしていく場所

{grid}
""".strip()


with open(book_dir / "index.md", "w", encoding="utf-8") as f:
    f.write(content)
