'''
render pandoc template
'''
from renderer import Renderer


if __name__ == '__main__':
    r = Renderer(output_dir='../pandoc/modules')
    r.render_template()
