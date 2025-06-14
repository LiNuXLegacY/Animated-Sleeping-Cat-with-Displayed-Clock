import tkinter as tk
from PIL import Image, ImageTk
import datetime

class TransparentGifCanvas:
    def __init__(self, master, bg_gif_path, cat_gif_path, cat_scale=0.6, bg_slowdown=3):
        self.master = master
        self.canvas = tk.Canvas(master)
        self.canvas.pack(fill="both", expand=True)

        self.bg_gif = Image.open(bg_gif_path)
        self.bg_frames = self.extract_frames(self.bg_gif)

        self.cat_gif = Image.open(cat_gif_path)
        self.cat_scale = cat_scale
        self.cat_frames = self.extract_and_resize_cat_frames(self.cat_gif, self.cat_scale)

        self.frame_index = 0
        original_delay = self.bg_gif.info.get('duration', 100)
        self.delay = original_delay * bg_slowdown
        self.canvas.config(width=self.bg_gif.width, height=self.bg_gif.height)
        self.animate()

    def extract_frames(self, gif):
        frames = []
        try:
            while True:
                frames.append(gif.copy().convert('RGBA'))
                gif.seek(len(frames))
        except EOFError:
            pass
        return frames

    def extract_and_resize_cat_frames(self, gif, scale):
        frames = []
        try:
            while True:
                frame = gif.copy().convert('RGBA')
                new_size = (int(frame.width * scale), int(frame.height * scale))
                resized_frame = frame.resize(new_size, Image.Resampling.LANCZOS)
                frames.append(resized_frame)
                gif.seek(len(frames))
        except EOFError:
            pass
        return frames

    def animate(self):
        bg_frame = self.bg_frames[self.frame_index % len(self.bg_frames)]
        cat_frame = self.cat_frames[self.frame_index % len(self.cat_frames)]

        composite = bg_frame.copy()

        cat_x = int(composite.width * 0.35)
        cat_y = int(composite.height * 0.65)

        composite.paste(cat_frame, (cat_x, cat_y), cat_frame)

        self.photo = ImageTk.PhotoImage(composite)
        self.canvas.delete("all")
        self.canvas.create_image(0, 0, anchor="nw", image=self.photo)

        self.frame_index += 1
        self.master.after(self.delay, self.animate)


class PixelClock(tk.Label):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.current_time = datetime.datetime.combine(datetime.date.today(), datetime.time(22, 0, 0))
        self.update_clock()

    def update_clock(self):
        time_str = self.current_time.strftime("%I:%M %p")
        self.config(text=time_str)
        self.current_time += datetime.timedelta(seconds=1)
        self.after(1000, self.update_clock)


def main():
    root = tk.Tk()
    root.title("Pixel Cat Animation Near Bike with Clock")

    gif_canvas = TransparentGifCanvas(root,
                                      "original-6a159483a08f9d79930f9632e4a97e86.gif",
                                      "GuSHJB.gif",
                                      cat_scale=0.6,
                                      bg_slowdown=3)

    clock = PixelClock(root, font=("Courier", 16, "bold"), fg="green", bg="#000000")
    clock.place(relx=0.95, rely=0.05, anchor="ne")

    root.geometry(f"{gif_canvas.bg_gif.width}x{gif_canvas.bg_gif.height}")

    root.mainloop()


if __name__ == "__main__":
    main()

