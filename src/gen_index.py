# トップページ（index.md）を生成する
from pathlib import Path
import yaml


workdir = Path(".")
book_dir = workdir / "book"

with open(book_dir / "_toc.yml", "r", encoding="utf-8") as f:
    toc = yaml.load(f, Loader=yaml.CLoader)


ncols = 2

grid_items = []
for part in toc["parts"]:
    section_title = part["caption"]
    articles = []
    # 第1層までのファイルを取得
    for chapter in part["chapters"]:
        file_path: str = chapter["file"]
        articles.append(f"- []({file_path})")
    articles = "\n".join(articles)
    grid_item = ":::{grid-item-card}\n" + f":columns: {12 // ncols}\n" + f"{section_title}\n" + f"\n{articles}\n" + ":::"
    grid_items.append(grid_item)

grid_items: str = "\n\n".join(grid_items)
grid = """
::::{grid}
:gutter: 2
:padding: 2
:margin: 2
""" + f"\n{grid_items}\n" + "::::"


content = f"""
# データサイエンス関連+αのメモ

統計学・機械学習（+その他の気になった分野）の教科書や論文を読み、自分で理解した範囲の理論と実装をメモしていく場所

{grid}
""".strip()


with open(book_dir / "index.md", "w", encoding="utf-8") as f:
    f.write(content)
