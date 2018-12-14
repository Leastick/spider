import pickle
from lib.storage import Storage
from lib.spider_robot import Spider


def save(storage):
    with open('data/storage.pkl', 'wb') as f:
        pickle.dump(storage, f, 2)


def load():
    try:
        with open('data/storage.pkl', 'rb') as f:
            return pickle.load(f)
    except FileNotFoundError:
        return Storage()


def start(load_request: bool,
          get_request: bool,
          url: str,
          sites_amount: int,
          max_depth: int,
          ):
    storage = load()
    if load_request:
        spider = Spider(url, storage, max_depth)
        for page in spider.traverse():
            storage.add(page)
        save(storage)
        return None, None
    if get_request:
        return storage.get(url, sites_amount)
