def add_style(content):
    from bs4 import BeautifulSoup as bs

    # Add html, head tag
    html = bs(str(content), "html5lib")
    head = html.head

    # Add style tag
    head.append(html.new_tag('style', type='text/css'))

    # Applying font
    head.style.append('*{font-family: Arial, Helvetica, sans-serif !important;}')

    return html.prettify()


class Cleaner(object):
    def __init__(self):
        self.tags = ['script', 'a']
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
        # Remove attributes of root div
        content.attrs = {}

        for tag in content.find_all():
            # Remove all script and style tags
            if tag.name in self.tags:
                tag.decompose()

            # Remove tags with specified id
            if tag.id and tag.id in self.ids:
                tag.decompose()

            # Remove tags with specified classes
            if tag.attrs and any(cls in self.classes for cls in tag.attrs.get('class', [])):
                tag.decompose()

            # Remove all attributes from tag
            tag.attrs = {}

            # Cleaning unwanted text
            if tag.text and self.text(tag.text.strip()):
                tag.decompose()

        return add_style(content)
