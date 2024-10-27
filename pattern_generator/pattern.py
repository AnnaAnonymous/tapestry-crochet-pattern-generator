"""
https://bidict.readthedocs.io/en/main/ 
"""

from PIL import Image
from bidict import bidict
import math
import csv

PLACE_HOLDER = 0

class Pattern:

    """
    colormap: dict[str, tuple[int, int, int]]
    """
    def __init__(self, filepath: str, colormap: dict[str, tuple[int, int, int]]):
        self.stitch_counts = []
        self.color_blocks = []
        self.color_map = bidict(colormap)
        if ".csv" in filepath:
            self.translate_csv(filepath)
        else:
            self.translate_img(filepath)

    def __str__(self):
        to_print = ""
        for line_index in range(len(self.color_blocks)):
            to_print += str(self.stitch_counts[line_index])
            to_print += "\n"
            to_print += str(self.color_blocks[line_index])
            to_print += "\n"
        return to_print

    def translate_csv(self, filepath: str):
        with open(filepath, mode='r') as file:
            csvFile = csv.reader(file)
            color_line = False
            for line in csvFile:
                if color_line:
                    self.color_blocks.append(line)
                else:
                    self.stitch_counts.append([int(value) for value in line])
                color_line = not color_line

    def translate_img(self, filepath: str):
        image = Image.open(filepath)
        width, height = image.size
        pixels = image.load()
        self.color_blocks.append([PLACE_HOLDER])
        self.stitch_counts.append([PLACE_HOLDER])
        for row in range(height):
            for column in range(width):
                curr_color = self.color_map.inverse[self.find_closest_color(pixels[column, row], list(self.color_map.values()))]
                if self.color_blocks[-1][-1] == curr_color:
                    self.stitch_counts[-1][-1] += 1
                else:
                    self.color_blocks[-1].append(curr_color)
                    self.stitch_counts[-1].append(1)
            self.color_blocks[-1].pop(0)
            self.stitch_counts[-1].pop(0)
            self.color_blocks[-1].reverse()
            self.stitch_counts[-1].reverse()
            self.color_blocks.append([PLACE_HOLDER])
            self.stitch_counts.append([PLACE_HOLDER])
        self.color_blocks.pop(-1)
        self.stitch_counts.pop(-1)
        self.color_blocks.reverse()
        self.stitch_counts.reverse()

    def export_as_csv(self, filepath: str):
        with open(filepath, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            for row in range(len(self.stitch_counts)):
                writer.writerow(self.stitch_counts[row])
                writer.writerow(self.color_blocks[row])

    def export_as_txt(self, filepath: str):
        with open(filepath, mode='w') as file:
            for row in range(len(self.stitch_counts)):
                file.write(f"Row {row + 1}: ")
                for block in range(len(self.color_blocks[row])):
                    file.write(f"{self.color_blocks[row][block]} x{self.stitch_counts[row][block]}")
                    if block != (len(self.color_blocks[row]) - 1):
                        file.write(", ")
                    else:
                        file.write(" ")
                file.write("\n")

    def export_as_img():
        pass
    
    def find_closest_color(self, start_color: tuple[int, int, int], comp_colors: list[tuple[int, int, int]]):
        closest_color = comp_colors[0]
        min_distance = 100
        for curr_color in comp_colors:
            curr_distance = self.compute_color_distance(start_color, curr_color)
            if curr_distance < min_distance:
                closest_color = curr_color
                min_distance = curr_distance
        return closest_color
    
    def compute_color_distance(self, color1: tuple[int, int, int], color2: tuple[int, int, int]):
        rmean = (color1[0] + color2[0]) / 2
        change_r = color1[0] - color2[0]
        change_g = color1[1] - color2[1]
        change_b = color1[2] - color2[2]
        return math.sqrt(((2 + (rmean / 256)) * pow(change_r, 2)) + (4 * pow(change_g, 2)) + (2 + ((255 - rmean)/256)) + pow(change_b, 2))
    