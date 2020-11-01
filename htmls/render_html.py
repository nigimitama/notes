import os
from jinja2 import Environment, FileSystemLoader


if __name__ == '__main__':
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
