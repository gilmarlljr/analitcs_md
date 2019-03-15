import HTMLParser
import pycontractions

class TextCleaner:
    def __init__(self, text: str):
        self.original_text = text
        self.cleaned_text = ''

    def clean(self):
        self.cleaned_text = TextCleaner.html_parser(self.original_text)
        self.cleaned_text = TextCleaner.utf8_decode(self.cleaned_text)
        self.cleaned_text = TextCleaner.
        self.cleaned_text = TextCleaner.
        self.cleaned_text = TextCleaner.
        self.cleaned_text = TextCleaner.
        self.cleaned_text = TextCleaner.
        return self.cleaned_text;

    @staticmethod
    def html_parser(text):
        html_parser = HTMLParser.HTMLParser()
        return html_parser.unescape(text)

    @staticmethod
    def utf8_decode(text):
        return text.decode("utf8").encode('ascii','ignore')
