from io import BytesIO
import json
from threading import Thread
from typing import override
from urllib import request

CHUNK_SIZE = 1_000_000


def get_size(newsgroup : str):
    root : str = newsgroup.split('.')[0]
    meta_url : str = 'https://archive.org/metadata/usenet-%s/files/%s.mbox.zip' % (root, newsgroup)
    with request.urlopen(meta_url) as resp:
        body = json.loads(resp.read())
    if body and 'result' in body:
        return int(body['result']['size'])
    else:
        return -1


class FileDownload(BytesIO):

    def __init__(self, url : str, target_size : int, chunk_size : int = 1_000_000) -> None:
        super().__init__()
        self.url : str = url
        self.target_size : int = target_size
        self.chunk_size : int = chunk_size
        self.current_size : int = 0
        self.done : bool = False

    def download(self, into : BytesIO) -> bool:
        if self.target_size == -1:
            self.done = True
            return False

        with request.urlopen(self.url) as resp:
            while True:
                buffer = resp.read(self.chunk_size)
                if not buffer:
                    break
                into.write(buffer)
                self.current_size += len(buffer)
            self.done = True
            return True

    def download_async(self, into : BytesIO) -> Thread:
        thread : Thread = Thread(target=lambda: self.download(into))
        thread.start()
        return thread

    def progress(self) -> float:
        if self.done:
            return 1.0
        elif self.current_size == 0:
            return 0.0
        else:
            return float(self.current_size) / float(self.target_size)



NEWSGROUP = 'rec.arts.anime'
size = get_size(NEWSGROUP)
if size == -1:
    print('ERROR: file not found')

root = NEWSGROUP.split('.')[0]
dl_url = 'https://archive.org/download/usenet-%s/%s.mbox.zip' % (root, NEWSGROUP)
with FileDownload(url=dl_url, target_size=size) as fdl:
    output = BytesIO()
    thrd = fdl.download_async(output)
    while not fdl.done:
        print(fdl.progress())

    thrd.join()