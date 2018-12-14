from collections import deque
from lib.parsed_page import Page


class Storage:
    def __init__(self):
        self.parsed_page = {}

    def get(self, url: str, pages_amount: int):
        if url not in self.parsed_page:
            return "No {0} in storage".format(url), None
        result = []
        q = deque()
        q.append(url)
        used = set()
        while len(q) > 0:
            current_url = q.popleft()
            if current_url not in self.parsed_page:
                continue
            page = self.parsed_page[current_url]
            result.append(page)
            if len(result) >= pages_amount:
                break
            for next_page in page.get_hyperlinks_iter():
                if next_page in used:
                    continue
                used.add(next_page)
                q.append(next_page)
        return None, result

    def add(self, page: Page):
        self.parsed_page[page.get_url()] = page

