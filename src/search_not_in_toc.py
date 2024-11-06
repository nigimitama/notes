# tocに入れ忘れている記事を探す
from pathlib import Path
import yaml
import os


book_dir = Path("./book")
os.chdir(book_dir)
book_dir = Path(".")

with open(book_dir / "_toc.yml", "r") as f:
    toc = yaml.load(f, Loader=yaml.CLoader)


for part in toc["parts"]:

    files = []
    for chapter in part["chapters"]:
        files.append(chapter["file"])
        if "sections" in chapter:
            for section in chapter["sections"]:
                files.append(section["file"])
                if "sections" in section:
                    for section_ in section["sections"]:
                        files.append(section_["file"])

    def valid_path(path: Path):
        return (".ipynb_checkpoints" not in str(path)) \
            and ("__pycache__" not in str(path)) \
            and ("_build" not in str(path))

    parent_dir = Path(part["chapters"][0]["file"]).parent
    notebooks = list(parent_dir.glob("*.ipynb")) + list(parent_dir.glob("*/*.ipynb"))
    detected_files = [str(path).replace(".ipynb", "") for path in notebooks if valid_path(path)]

    files_not_in = set(detected_files) - set(files)
    if len(files_not_in) != 0:
        print(part["caption"], "-"*10)
        print(f"{len(files_not_in)} files are detected")
        for file in files_not_in:
            print(file)
