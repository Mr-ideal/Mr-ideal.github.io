import os
import sys
import tkinter as tk
from tkinter import ttk

try:
    from PIL import Image, ImageTk
    PIL_AVAILABLE = True
except Exception:
    PIL_AVAILABLE = False

IMAGE_EXTS = (
    '.png', '.jpg', '.jpeg', '.gif', '.bmp', '.tiff'
)

class ImageWindow:
    def __init__(self, root, directory):
        self.directory = directory
        self.window = tk.Toplevel(root)
        self.window.title(directory)
        self.label = ttk.Label(self.window)
        self.label.pack()
        self.current_path = None
        self.photo = None
        self.update_image()

    def latest_image_path(self):
        try:
            files = [
                os.path.join(self.directory, f)
                for f in os.listdir(self.directory)
                if f.lower().endswith(IMAGE_EXTS)
            ]
        except FileNotFoundError:
            return None
        if not files:
            return None
        return max(files, key=os.path.getmtime)

    def update_image(self):
        path = self.latest_image_path()
        if path and path != self.current_path:
            try:
                if PIL_AVAILABLE:
                    img = Image.open(path)
                    img = img.copy()
                    self.photo = ImageTk.PhotoImage(img)
                else:
                    self.photo = tk.PhotoImage(file=path)
                self.label.configure(image=self.photo)
                self.current_path = path
            except Exception as exc:
                print(f"Failed to load {path}: {exc}")
        self.window.after(1000, self.update_image)


def main(directories):
    root = tk.Tk()
    root.withdraw()
    windows = [ImageWindow(root, d) for d in directories]
    root.mainloop()


if __name__ == '__main__':
    if len(sys.argv) != 7:
        prog = os.path.basename(sys.argv[0])
        print(f"Usage: {prog} dir1 dir2 dir3 dir4 dir5 dir6")
        sys.exit(1)
    main(sys.argv[1:])
