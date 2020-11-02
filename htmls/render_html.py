import os
from jinja2 import Environment, FileSystemLoader

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
        self.html_dir = './templates'
        self.output_dir = '../docs'
        self.env = Environment(loader=FileSystemLoader(html_dir))

    def main(self):
        pass

    def render_index(self):
        file_name = 'index.html'
        template = self.env.get_template(file_name)
        template.render(
            title=self.title
        )
        self._save_html(html, file_name)

    def render_engineering(self):
        file_name = 'engineering.html'
        prefix = 'engineering_python'
        template = self.env.get_template(file_name)
        template.render(
            title=self.title
        )
        self._save_html(html, file_name)


    def _save_html(self, html, file_name):
        path = f'{self.output_dir}/{file_name}'
        print('saving', path)
        with open(path, "w") as f:
            f.write(html)
        return self



if __name__ == '__main__':
    r = Renderer()
    r.render_index()
    r.render_engineering()
