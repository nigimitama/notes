import os
import re
from jinja2 import Environment, FileSystemLoader
import re


def generate_simple():
    title = '盆暗の勉強メモ'
    html_dir = './templates'
    output_dir = '../docs'
    file_names = os.listdir(html_dir)
    for file_name in file_names:
        if ('_' not in file_name) and ('.html' in file_name):
            env = Environment(loader=FileSystemLoader(html_dir))
            template = env.get_template(file_name)
            html = template.render(title=title)
            # save the results
            with open(f'{output_dir}/{file_name}', "w") as f:
                f.write(html)


class Renderer:

    def __init__(self):
        self.title = '盆暗の勉強メモ'
        html_dir = './templates'
        self.output_dir = '../docs'
        self.env = Environment(loader=FileSystemLoader(html_dir))
        md_dir = '../docs_raw'
        files = get_file_paths(md_dir)
        self.md_files = [f for f in files if '.md' in f]

    def main(self):
        pass

    def render_index(self):
        file_name = 'index.html'
        template = self.env.get_template(file_name)
        html = template.render(
            title=self.title
        )
        self._save_html(html, file_name)

    def render_engineering(self):
        file_name = 'engineering.html'
        category = 'engineering'
        paths = [f for f in self.md_files if category in f]
        python_paths = [get_path_titles(f) for f in paths if category in f]
        infra_paths = [get_path_titles(f) for f in paths if category in f]
        template = self.env.get_template(file_name)
        html = template.render(
            title=self.title,
            python_paths=python_paths,
            infra_paths=infra_paths
        )
        self._save_html(html, file_name)

    def _save_html(self, html, file_name):
        path = f'{self.output_dir}/{file_name}'
        print('saving', path)
        with open(path, "w") as f:
            f.write(html)
        return self


def get_file_paths(path):
    paths = []
    for current_dir, dirs, files in os.walk(path):
        if len(dirs) == 0:
            for file in files:
                path = os.path.join(current_dir, file)
                paths.append(path)
        else:
            for dir in dirs:
                for file in files:
                    path = os.path.join(current_dir, dir, file)
                    paths.append(path)
    return paths


def get_path_titles(md_path):
    title = os.path.basename(md_path).replace('.md', '')
    with open(md_path, 'r', encoding='utf-8') as f:
        doc = f.read()
    has_yml = re.match(r'.{0,10}(---)', doc[0:20])
    if has_yml:
        yml = re.match(
            r'.{0,10}(---).{0,100}(---)', doc, re.DOTALL).group()
        title = re.search(
            r'(title)\s?(:)\s?(?P<title>.+)\n', yml).group('title')
    return [md_path, title]
    # return {'path': md_path, 'title': title}


if __name__ == '__main__':
    r = Renderer()
    r.render_index()
    r.render_engineering()
