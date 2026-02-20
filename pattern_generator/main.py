"""
https://www.compuphase.com/cmetric.htm 
https://stackoverflow.com/questions/35113979/calculate-distance-between-colors-in-hsv-space 
https://patorjk.com/software/taag 
    small or small script
https://www.yarnspirations.com/blogs/how-to/anchor-color-chart?srsltid=AfmBOopyDgUrBgC9h3dNykhVivkUuSClMWgISAJPE0s8B4vWcoxArQcu#color-black 
https://threadcolors.com/ 

convert between different data types
classes

"""

from PIL import Image
import math
import csv
import constants as c
from pattern import Pattern

def print_banner(banner: list[str]):
    print()
    for line in banner:
        print(line)
    print()

def extract_colors_from_map(color_map: dict[int, tuple[int, int, int]]):
    print("By default, the color number code will be used as pattern color labels. Would you prefer to enter custom labels? (y/n): ", end="")
    user_input = input()
    custom_labels = False
    if user_input == 'y':
        custom_labels = True
    color_map = {}
    print("Please enter the number code for your first color: ", end="")
    color_code = int(input())
    color_label = color_code
    if custom_labels:
        print("What is the label for this color?: ", end="")
        color_label = input()
    color_map[color_label] = color_map[color_code]
    print("Select another color? (y/n): ", end="")
    more_colors = input()
    while more_colors == 'y':
        print("Please enter the number code: ", end="")
        color_code = int(input())
        color_label = color_code
        if custom_labels:
            print("What is the label for this color?: ", end="")
            color_label = input()
        color_map[color_label] = color_map[color_code]
        print("Select another color? (y/n): ", end="")
        more_colors = input()
    return color_map

def select_manual_RGB_colors():
    print("Please enter the red value for your first color: ", end="")
    red = int(input())
    print("green: ", end="")
    green = int(input())
    print("blue: ", end="")
    blue = int(input())
    print("what is the name of your color (must be unique): ", end="")
    name = input()
    color_map = {(red, green, blue) : name}
    print("Add another color? (y/n): ", end="")
    more_colors = input()
    while more_colors == "y":
        print("red: ", end="")
        red = int(input())
        print("green: ", end="")
        green = int(input())
        print("blue: ", end="")
        blue = int(input())
        print("what is the name of your color (must be unique): ", end="")
        name = input()
        color_map[(red, green, blue)] = name
        print("Add another color? (y/n): ", end="")
        more_colors = input()
    return color_map

def main():
    print_banner(c.NAME_BANNER)
    print_banner(c.DESCRIPTION)
    print_banner(c.START_MENU)
    menu_option = input()
    while menu_option != "1":
        if menu_option == "2":
            pass
        elif menu_option == "3":
            pass
        elif menu_option == "4":
            pass 
        else:
            print(c.INPUT_ERROR)
        print_banner(c.START_MENU)
    print(c.PICTURE_PROMPT)
    file_path = input()
    color_map = {
        "w" : (235, 212, 187),
        "b" : (67, 69, 80),
        "g" : (108, 112, 92)
    }
    user_pattern = Pattern(file_path, color_map)
    print(c.FILE_PROMPT)
    file_path = input()
    user_pattern.export_as_txt(file_path)

if __name__ == "__main__":
    main()