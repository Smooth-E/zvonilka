import winsound


def play(path: str, block_thread: bool = False) -> None:
    flag = winsound.SND_FILENAME
    if not block_thread:
        flag |= winsound.SND_ASYNC

    winsound.PlaySound(path, flag)
