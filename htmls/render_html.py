'''
render htmls
'''
from renderer import Renderer


if __name__ == '__main__':
    r = Renderer()
    r.render_index()
    r.render_category_page('data_science.html')
    r.render_category_page('engineering.html')
    r.render_category_page('mathematics.html')
