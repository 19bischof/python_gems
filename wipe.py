import os
import shutil

up = '\033[A'
# wipe.cursor(height=None) brings the cursor back to the start so the caller can overwrite the text
# wipe.screen() is normal console clear/cls


class wipe:
    width, height = shutil.get_terminal_size()
    print("height:", height, "width:", width)
    def screen(): return os.system('cls' if os.name == 'nt' else 'clear')

    def cursor(height=None):
        print('\b'*wipe.width, end="")
        if height is None:
            height = wipe.height
        print(up*height, end="")


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
