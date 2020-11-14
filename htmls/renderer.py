import glob
from jinja2 import Environment, FileSystemLoader
from lxml import html
import re


class Renderer:

    def __init__(self, output_dir='../docs'):
        self.title = '盆暗の勉強メモ'
        html_dir = './templates'
        self.output_dir = output_dir
        self.env = Environment(
            loader=FileSystemLoader(html_dir),
            trim_blocks=True,
            lstrip_blocks=True
        )
        self._get_html_paths()

    def render_template(self):
        file_name = 'pandoc_template.html'
        template = self.env.get_template(file_name)
        html_ = template.render(
            title=self.title
        )
        self._save_html(html_, file_name)

    def render_index(self):
        file_name = 'index.html'
        template = self.env.get_template(file_name)
        html_ = template.render(
            title=self.title
        )
        self._save_html(html_, file_name)

    def render_category_page(self, file_name='engineering.html'):
        category = file_name.replace('.html', '')
        paths = [f for f in self.html_files
                 if (category in f) and (file_name not in f)]
        path_titles = [self._get_path_titles(f) for f in paths]
        template = self.env.get_template(file_name)
        html_ = template.render(
            title=self.title,
            path_titles=path_titles
        )
        self._save_html(html_, file_name)

    def _get_html_paths(self):
        '''htmlのパスを取得する。output_dirに各記事のhtmlを生成済という前提'''
        files = glob.glob(f'{self.output_dir}/**', recursive=True)
        self.html_files = [f for f in files if f.endswith('.html')]
        # __が入ったものは表示しない
        self.html_files = [f for f in self.html_files if '__' not in f]

    def _save_html(self, html, file_name):
        path = f'{self.output_dir}/{file_name}'
        print('saving', path)
        with open(path, "w") as f:
            f.write(html)
        return self

    def _get_path_titles(self, html_path):
        # get_path
        # ../docs/<article>.htmlから <article>.htmlにする
        dir_name = re.sub(r'(\.{1,2}/)', '', self.output_dir)
        html_name = re.sub(r'(\.{1,2}/|/)', '', html_path)
        path = html_name.replace(dir_name, '')

        # get_title
        with open(html_path, 'r', encoding='utf-8') as f:
            document = f.read()
        tree = html.fromstring(document)
        # タイトルが取れるならそれを使う
        title = tree.xpath('//title/text()')[0] \
            .replace(self.title, '').replace(' – ', '').strip()
        if title == '':
            title = html_path.split('_')[-1].replace('.html', '')
        return [path, title]
