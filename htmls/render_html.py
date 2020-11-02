import os
import re
import glob
from jinja2 import Environment, FileSystemLoader
from lxml import html


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
        self._get_html_paths()

    def main(self):
        pass

    def render_index(self):
        file_name = 'index.html'
        template = self.env.get_template(file_name)
        html_ = template.render(
            title=self.title
        )
        self._save_html(html_, file_name)

    def _get_html_paths(self):
        '''htmlのパスを取得する。output_dirに各記事のhtmlを生成済という前提'''
        # files = get_file_paths(self.output_dir)
        files = glob.glob(f'{self.output_dir}/**', recursive=True)
        self.html_files = [f for f in files if f.endswith('.html')]

    def render_engineering(self):
        file_name = 'engineering.html'
        category = 'engineering'
        paths = [f for f in self.html_files
                 if (category in f) and (file_name not in f)]
        python_paths = [self._get_path_titles(f) for f in paths
                        if 'python' in f]
        infra_paths = [self._get_path_titles(f) for f in paths
                       if 'infrastructure' in f]
        template = self.env.get_template(file_name)
        html_ = template.render(
            title=self.title,
            python_paths=python_paths,
            infra_paths=infra_paths
        )
        self._save_html(html_, file_name)

    def _save_html(self, html, file_name):
        path = f'{self.output_dir}/{file_name}'
        print('saving', path)
        with open(path, "w") as f:
            f.write(html)
        return self

    def _get_path_titles(self, html_path):
        with open(html_path, 'r', encoding='utf-8') as f:
            document = f.read()
        tree = html.fromstring(document)
        # タイトルが取れるならそれを使う
        title = tree.xpath('//title/text()')[0] \
            .replace(self.title, '').replace(' – ', '').strip()
        if title == '':
            title = html_path.split('_')[-1].replace('.html', '')
        return [html_path, title]


def get_file_paths(path):
    paths = []
    for dirpath, _, filenames in os.walk(path):
        for filename in filenames:
            path = os.path.join(dirpath, filename)
            paths.append(path)
    return paths


if __name__ == '__main__':
    r = Renderer()
    r.render_index()
    r.render_engineering()
