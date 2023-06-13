import requests
from bs4 import BeautifulSoup
import unicodedata
import re
import uuid


class Article():

    url: str

    def __init__(self, url: str):
        self.id = uuid.uuid4().hex
        self.url = url
        self.data = self.get_data_from_url()

    def clean_document_content(self, content: str):
        content = content.replace('\n', ' ')
        document_cleaned = []
        # Parametro criado para auxiliar a remover referencias do texto #
        ref = False
        for ch in content:
            if ch == "[":
                ref = True
            elif ch == "]":
                ref = False
            elif ref:
                pass
            else:
                nfkd = unicodedata.normalize('NFKD', ch)
                filter = re.sub('[^A-z 0-9 , . ( ) / - -\\\]', '', nfkd)
                char = u"".join(
                    [c for c in filter if not unicodedata.combining(c)])
                document_cleaned.append(char)
        return ''.join(document_cleaned)

    def get_data_from_url(self):
        response = requests.get(self.url)
        soup = BeautifulSoup(response.content, 'html.parser')
        bodydiv = soup.body.find("div", {"itemprop": "articleBody"})
        bodycontent = bodydiv.find_all(
            lambda tag: tag.name == 'p' and not tag.attrs)
        bodycontentfinal = ""
        for p in bodycontent[1:]:
            bodycontentfinal += p.get_text() + " "
        document = self.clean_document_content(content=bodycontentfinal)
        self.document = document
