import internetarchive as ia
from io import BytesIO
from threading import Thread
from typing import override


class FileDownload(BytesIO):

    def __init__(self, file_ref : ia.File) -> None:
        super().__init__()
        self.file_ref : ia.File = file_ref
        self.target_size : int = int(file_ref.metadata['size'])
        self.done : bool = False

    @override
    def close(self) -> None:
        self.done = True

    def download(self) -> bool:
        return self.file_ref.download(fileobj=self, verbose=False)

    def download_async(self) -> Thread:
        thread : Thread = Thread(target=self.download)
        thread.start()
        return thread

    def progress(self) -> float:
        return float(len(self.getvalue())) / self.target_size

    def actually_close(self) -> None:
        super().close()


def get_file_ref(group : str) -> ia.File | None:
    if len(group) == 0:
        return None
    root : str = group.split('.', 1)[0]
    item : ia.Item = ia.get_item(identifier='usenet-' + root)
    if not item.item_metadata:
        return None
    file : ia.File = ia.File(item=item, name=group + '.mbox.zip')
    return file if file.metadata else None
