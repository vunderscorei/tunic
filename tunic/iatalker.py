from io import BytesIO
import json
from threading import Thread
from urllib import request


def get_size(newsgroup : str) -> int:
    root : str = newsgroup.split('.')[0]
    meta_url : str = 'https://archive.org/metadata/usenet-%s/files/%s.mbox.zip' % (root, newsgroup)
    with request.urlopen(meta_url) as resp:
        body : dict = json.loads(resp.read())
    if body and 'result' in body:
        return int(body['result']['size'])
    else:
        return -1


def get_url(newsgroup : str) -> str:
    root : str = newsgroup.split('.')[0]
    return 'https://archive.org/download/usenet-%s/%s.mbox.zip' % (root, newsgroup)


class FileDownload(BytesIO):

    def __init__(self, url : str, target_size : int, chunk_size : int = 1_000_000) -> None:
        super().__init__()
        self.url : str = url
        self.target_size : int = target_size
        self.chunk_size : int = chunk_size
        self.current_size : int = 0
        self.done : bool = False
        self.stop_requested : bool = False


    def download(self) -> bool:
        if self.target_size == -1:
            self.done = True
            return False

        with request.urlopen(self.url) as resp:
            while True:
                if self.stop_requested:
                    self.flush()
                    self.done = False
                    self.stop_requested = False
                    self.chunk_size = 0
                    return False

                buffer = resp.read(self.chunk_size)
                if not buffer:
                    break
                self.write(buffer)
                self.current_size += len(buffer)
            self.done = True
            return True


    def download_async(self) -> Thread:
        thread : Thread = Thread(target=self.download)
        thread.start()
        return thread


    def progress(self) -> float:
        if self.done:
            return 1.0
        elif self.current_size == 0:
            return 0.0
        else:
            return float(self.current_size) / float(self.target_size)