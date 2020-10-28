import os
import sys
from py_modules import get_files, is_image, rename_files, remove_empty_subdirs

if __name__ == "__main__":
    # print("enter type of images (e.g. '2D_static'):")
    # _type = input()
    _type = sys.argv[1]
    work_dir = sys.argv[2]
    os.chdir(work_dir)

    dir_name = f"image_{_type}"
    if not os.path.exists(dir_name):
        raise ValueError("Directory Not Found")
    files = get_files(dir_name)
    image_paths = [f for f in files if is_image(f)]
    image_paths = rename_files(image_paths)
    print(image_paths)
    remove_empty_subdirs(dir_name)

    from jinja2 import Environment, FileSystemLoader
    html_dir = "../template"
    env = Environment(loader=FileSystemLoader(html_dir))
    template = env.get_template("base.html")
    html = template.render(
        title=_type,
        image_paths=image_paths
    )
    # to save the results
    with open(f"{_type}.html", "w") as f:
        f.write(html)
