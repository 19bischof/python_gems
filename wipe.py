import os
import shutil

up = '\033[A'
# wipe.cursor(height=None) brings the cursor back to the start so the caller can overwrite the text
# wipe.screen() is normal console clear/cls


class wipe:
    width, height = shutil.get_terminal_size()
    instance = None #instance so __del__ is called at end
    def screen(): return os.system('cls' if os.name == 'nt' else 'clear')

    def cursor(height=None):
        if wipe.instance is None:
            wipe.screen()
            wipe.instance = wipe()
        wipe.instance.to_top_left(height)

    def to_top_left(self, height=None):
        print('\b'*wipe.width, end="")
        if height is None:
            height = wipe.height
        print(up*height, end="")

    def __del__(self):
        wipe.screen()


if __name__ == "__main__":
    import time
    import lorem
    wipe.screen()
    row_count = 5
    for j in range(5):
        for i in range(row_count):
            print(lorem.sentence())
            time.sleep(0.31)
        wipe.cursor(row_count)
    wipe.screen()
