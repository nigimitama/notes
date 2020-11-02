import glob
from jinja2 import Environment, FileSystemLoader
from lxml import html


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
        files = glob.glob(f'{self.output_dir}/**', recursive=True)
        self.html_files = [f for f in files if f.endswith('.html')]

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


if __name__ == '__main__':
    r = Renderer()
    r.render_index()
    r.render_category_page('data_science.html')
    r.render_category_page('engineering.html')
    r.render_category_page('mathematics.html')
