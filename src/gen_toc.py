# generate _toc.yml
# tocに入れ忘れている記事を探す
from pathlib import Path
import yaml
import os

book_dir = Path("./book")
os.chdir(book_dir)
book_dir = Path(".")

def is_valid(path: Path):
    """パスの検索から除外したいディレクトリはfalseで返す"""
    return (".ipynb_checkpoints" not in str(path)) \
        and ("__pycache__" not in str(path)) \
        and ("_build" not in str(path))\
        and ("_static" not in str(path))

def trim_suffix(path: Path) -> str:
    return str(path).replace(".ipynb", "")

def get_notebooks(dir: Path) -> list[Path]:
    return [path for path in dir.glob("*.ipynb") if is_valid(path)]

def get_dirs(dir: Path) -> list[Path]:
    return [path for path in dir.glob("*") if path.is_dir() and is_valid(path)]


data = {"root": "index", "parts": []}
# mathematicsなどの第1レイヤー
part_dirs = get_dirs(book_dir)
part_dirs = [part_dir for part_dir in part_dirs if part_dir.stem == "mathematics"]
for part_dir in part_dirs:
    # get caption name: _config.ymlに name: 数学 など名前を入れてる想定
    config_path = part_dir / "_config.yml"
    if not config_path.exists():
        continue

    with open(config_path, "r") as f:
        conf: dict = yaml.load(f, Loader=yaml.CLoader)
    caption_name = conf["name"]

    # get chapter files
    chapter_files = [{"file": trim_suffix(path)} for path in get_notebooks(part_dir)]
    section_dirs = get_dirs(part_dir)

    if section_dirs != []:
        print(section_dirs)

    for section_dir in section_dirs:
        section_files = [{"file": trim_suffix(path)} for path in get_notebooks(section_dir)]

        index_files = [f for f in section_files if f["file"].endswith("index")]
        if index_files != []:
            chapter_files.append({
                "file": index_files[0]["file"],
                "sections": [f for f in section_files if not f["file"].endswith("index")]
            })

    data["parts"].append({
        "caption": caption_name,
        "chapters": chapter_files
    })

with open(book_dir / "_toc_gen.yml", "w", encoding="utf-8") as f:
    yaml.dump(data, f, encoding="utf-8")




part_dirs = get_dirs(book_dir)
for part_dir in part_dirs:
    section_dirs = get_dirs(part_dir)
    nb_paths = list(part_dir.glob("*.ipynb"))


