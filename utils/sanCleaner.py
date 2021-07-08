from pathlib import Path

from bs4 import BeautifulSoup as bs, Doctype


def add_tags(content, has_mathjax):
    # Add html, head tag
    html = bs(str(content), "html5lib")
    doctype = Doctype('html')
    html.insert(0, doctype)
    head = html.head

    # Add style tag
    head.append(html.new_tag('style', type='text/css'))
    # Applying font
    head.style.append('*{font-family: Arial, Helvetica, sans-serif !important;}')

    # For rendering maths equation
    if has_mathjax:
        # Polyfill
        polyfill = html.new_tag('script', src="https://polyfill.io/v3/polyfill.min.js?features=es6")
        head.append(polyfill)

        # MathJax
        mathjax_actions = Path(__file__).parent.joinpath("mathjax-actions.js")
        head.append(html.new_tag('script', src=f'file:///{mathjax_actions.as_posix()}'))
        conf = html.new_tag('script', type="text/x-mathjax-config")
        conf.append("MathJax.Hub.Config({CommonHTML: {scale: 200}});")
        head.append(conf)
        head.append(html.new_tag('script',
                                 id="MathJax-script",
                                 attrs={'async': ''},
                                 src="https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.7/MathJax.js?config=TeX-MML-AM_CHTML"))

    return html.prettify(), has_mathjax


class Cleaner(object):
    def __init__(self):
        self.has_mathjax = False
        self.tags = ['script', 'a', 'noscript']
        self.exclude = ['br', 'img']
        self.ids = [
            'sf-video-ads'
        ]
        self.classes = [
            'mobile-content',
            'desktop-content',
            'sf-nav-bottom',
            'sf-desktop-ads',
            'sf-mobile-ads',
            'sf-video-yt',
            'sf-post-footer',
            'collapseomatic',
        ]
        self.text = lambda x: x and x.startswith((
            'Sanfoundry Global Education',
            'To practice all areas',
            'Participate in the Sanfoundry Certification',
            'advertisment',
        ))

    def clean(self, content):
        self.has_mathjax = False
        if content.select('script[src*="mathjax"]'):
            self.has_mathjax = True

        content = content.find("div", {"class": "entry-content"})

        # Remove attributes of root tag
        content.attrs = {}

        for tag in content.find_all():
            if tag.name in self.exclude:
                continue

            for img in tag.find_all('img'):
                if 'lazyload' in img.get('class', []):
                    img.decompose()
                elif img.parent.name == 'noscript':
                    img.parent.unwrap()
                    img.parent.unwrap()

            # Remove all script and anchor tags
            if tag.name in self.tags:
                tag.decompose()
                continue

            # Remove tags with specified id
            if tag.id and tag.id in self.ids:
                tag.decompose()
                continue

            # Remove tags with specified classes
            if tag.attrs and any(cls in self.classes for cls in tag.attrs.get('class', [])):
                tag.decompose()
                continue

            # Cleaning unwanted text
            if tag.text and self.text(tag.get_text(strip=True)):
                tag.decompose()
                continue

            # Remove empty tags
            if len(tag.get_text(strip=True)) == 0:
                tag.decompose()
                continue

            # Remove all attributes from tag
            tag.attrs = {}

        return add_tags(content, self.has_mathjax)
