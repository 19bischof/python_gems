import os
import shutil

up = '\033[A'
# wipe.cursor(height=None) brings the cursor back to the start so the caller can overwrite the text
# wipe.screen() is normal console clear/cls


class wipe:
    """
    utility that cleans the console screen efficiently
    Call with wipe.cursor()
    """
    width, height = shutil.get_terminal_size()
    instance = None #instance so __del__ is called at end
    def screen(): return os.system('cls' if os.name == 'nt' else 'clear')

    def cursor(height=None,no_traces=False):
        """entry point to use as a module"""
        if wipe.instance is None:
            wipe.screen()
            wipe.instance = wipe()
        if height is None: height = wipe.height
        wipe.instance.to_top_left(height,no_traces)

    def to_top_left(self, height,no_traces):
        """cleans the console through overwriting with spaces"""
        for _ in range(height):
            print('\b'*wipe.width, end="")
            if no_traces:
                print(" "*(wipe.width),end="")
            print(up, end="")
        print('\b'*wipe.width,flush=True,end="")

    def __del__(self):
        wipe.screen()


if __name__ == "__main__":
    import time
    import lorem #install with pip if not already
    row_count = 5
    for j in range(5):
        for i in range(row_count):
            print(lorem.sentence())
            time.sleep(0.31)
        wipe.cursor(row_count,no_traces=True)
