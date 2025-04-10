#!/usr/bin/python
# -*- coding:utf-8 -*-
import os
import sys
import time
from threading import Thread
from PIL import Image, ImageDraw, ImageFont
import logging

libdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'lib')
if os.path.exists(libdir):
    sys.path.append(libdir)

from waveshare_epd import epd7in5_V2

class Display:
    DISPLAY_WIDTH = 480
    DISPLAY_HEIGHT = 800

    def __init__(self, epd):
        self.image = Image.new('1', (self.DISPLAY_WIDTH, self.DISPLAY_HEIGHT), 255)
        self.draw = ImageDraw.Draw(self.image)
        self.tasks = []
        self.threads = []  # Store threads
        self.epd = epd
        self.epd.init()
        self.epd.Clear()

    def add_task(self, task):
        self.tasks.append(task)

    def start_tasks(self):
        for task in self.tasks:
            thread = Thread(target=task.update, args=(self.draw, self.image))
            thread.daemon = True
            thread.start()
            self.threads.append(thread)

    def join_tasks(self):
        for thread in self.threads:
            thread.join()

    def show_image(self, image):
        image = image.rotate(90, expand=True)
        self.epd.display(self.epd.getbuffer(image))
        time.sleep(3)

class Task:
    def __init__(self, display, area, update_interval):
        self.display = display
        self.area = area
        self.update_interval = update_interval

    def update(self, draw, image):
        raise NotImplementedError("Must override update method")

    def clear(self, draw):
        raise NotImplementedError("Must override clear method")

class ImageTask(Task):
    def __init__(self, display, image_dir, update_interval=3):
        super().__init__(display, (0, 30, display.DISPLAY_WIDTH, display.DISPLAY_HEIGHT), update_interval)
        self.image_files = self.find_image_files(image_dir)
        print(self.image_files)

    def find_image_files(self, root_dir):
        extensions = ('.jpg', '.jpeg', '.png')
        if not os.path.exists(root_dir):
            return []

        image_files = []
        for dirpath, dirnames, filenames in os.walk(root_dir):
            for filename in filenames:
                if filename.lower().endswith(extensions):
                    # Create absolute path
                    full_path = os.path.abspath(os.path.join(dirpath, filename))
                    # Normalize path separators for consistency across OS
                    normalized_path = full_path.replace(os.sep, '/')
                    image_files.append(normalized_path)

        # Sort the list of image files by their full normalized absolute paths
        return sorted(image_files)

    def clear(self, draw):
        draw.rectangle(self.area, fill=255)

    def update(self, draw, image):
        current_index = 0
        while True:
            if self.image_files:
                img_path = self.image_files[current_index]
                img = Image.open(img_path)
                w, h = img.size
                new_h = int(self.display.DISPLAY_HEIGHT * 0.9)
                new_w = int(new_h * w / h)
                img = img.resize((new_w, new_h), Image.BILINEAR)
                self.clear(draw)
                image.paste(img, (self.area[0], self.area[1]))
                self.display.show_image(image)
                current_index = (current_index + 1) % len(self.image_files)
            time.sleep(self.update_interval)

def main():
    logging.basicConfig(level=logging.DEBUG)
    font_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'pic')
    zen_img_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'zen_img')

    epd = epd7in5_V2.EPD()
    display = Display(epd)
    display.add_task(ImageTask(display, zen_img_dir))
    display.start_tasks()
    display.join_tasks()

if __name__ == '__main__':
    main()
