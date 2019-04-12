from html.parser import HTMLParser


class Parser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.index = 0
        self.data = {1: "", 2: "", 3: ""}
        self.links = []

    def handle_starttag(self, tag, attrs):
        if tag in ['p', 'a', 'meta']:
            self.index = 1
        if tag in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']:
            self.index = 2
        if tag in ['title']:
            self.index = 3
        for attr in attrs:
            if attr[0] == 'alt':
                self.data[self.index] += attr[1] + " "
            elif attr[0] == 'href':
                link = attr[1]
                if link.startswith('#'):
                    continue
                if link.startswith('/'):
                    link = url[:url.index('/', 8)] + link
                self.links.append(link)

    def handle_endtag(self, tag):
        self.index = 0

    def handle_data(self, data):
        data = data.strip()
        if self.index and data:
            self.data[self.index] += data + " "
