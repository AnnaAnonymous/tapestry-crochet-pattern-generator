"""
https://www.compuphase.com/cmetric.htm 
https://stackoverflow.com/questions/35113979/calculate-distance-between-colors-in-hsv-space 
https://patorjk.com/software/taag 
    small or small script
https://www.yarnspirations.com/blogs/how-to/anchor-color-chart?srsltid=AfmBOopyDgUrBgC9h3dNykhVivkUuSClMWgISAJPE0s8B4vWcoxArQcu#color-black 
https://threadcolors.com/ 

"""

from PIL import Image
import math
import csv

name_banner = [
    "  _____                                __                                ",
    " () | _,       _  , _|_  ,_           / ()  ,_   _   _  |)    __|_       ",
    "    |/ |  |/\\_|/ / \\_|  /  | |  |    |     /  | / \\_/   |/\\  |/ |        ",
    "  (/ \\/|_/|_/ |_/ \\/ |_/   |/ \\/|/    \\___/   |/\\_/ \\__/|  |/|_/|_/      ",
    "  , _    (|                    (|                                        ",
    " /|/ \\ _, _|__|_  _  ,_            () | _        _  ,_   _, _|_  _   ,_  ",
    "  |__// |  |  |  |/ /  | /|/|      /\\/||/ /|/|  |/ /  | / |  |  / \\_/  | ",
    "  |   \\/|_/|_/|_/|_/   |/ | |_/   /(_/ |_/ | |_/|_/   |/\\/|_/|_/\\_/    |/"
]

alt_name_banner = [
    "  _____                  _               ___             _        _      ",
    " |_   _|_ _ _ __  ___ __| |_ _ _ _  _   / __|_ _ ___  __| |_  ___| |_    ",
    "   | |/ _` | '_ \\/ -_|_-<  _| '_| || | | (__| '_/ _ \\/ _| ' \\/ -_)  _|   ",
    "   |_|\\__,_| .__/\\___/__/\\__|_|  \\_, |  \\___|_| \\___/\\__|_||_\\___|\\__|   ",
    "  ___      |_| _                 |__/_                       _           ",
    " | _ \\__ _| |_| |_ ___ _ _ _ _    / __|___ _ _  ___ _ _ __ _| |_ ___ _ _ ",
    " |  _/ _` |  _|  _/ -_) '_| ' \\  | (_ / -_) ' \\/ -_) '_/ _` |  _/ _ \\ '_|",
    " |_| \\__,_|\\__|\\__\\___|_| |_||_|  \\___\\___|_||_\\___|_| \\__,_|\\__\\___/_|  "
]

color_options_menu = [
    " 1) From specified Anchor Colors",
    " 2) From specified DMC Colors",
    " 3) From all Anchor Colors",
    " 4) From all DMC Colors",
    " 5) Manual RGB Input"
]

def translate_image(file_path: str, colors: list[tuple[int, int, int]], colormap: dict[tuple[int, int, int], str]):
    image = Image.open(file_path)
    width, height = image.size
    pixels = image.load()
    pattern_colors = [["blank"]]
    pattern_count = [[0]]
    for row in range(height):
        for column in range(width):
            curr_color = colormap[find_closest_color(pixels[column, row], colors)]
            if pattern_colors[-1][-1] == curr_color:
                pattern_count[-1][-1] += 1
            else:
                pattern_colors[-1].append(curr_color)
                pattern_count[-1].append(1)
        pattern_colors[-1].pop(0)
        pattern_count[-1].pop(0)
        pattern_colors[-1].reverse()
        pattern_count[-1].reverse()
        pattern_colors.append(["blank"])
        pattern_count.append([0])
    pattern_colors.pop(-1)
    pattern_count.pop(-1)
    pattern_colors.reverse()
    pattern_count.reverse()
    return pattern_colors, pattern_count

def write_pattern_to_file(pattern_count: list[list[int]], pattern_colors: list[list[str]], file_path: str):
    with open(file_path, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        for row in range(len(pattern_count)):
            writer.writerow(pattern_colors[row])
            writer.writerow(pattern_count[row])

def find_closest_color(start_color: tuple[int, int, int], comp_colors: list[tuple[int, int, int]]):
    closest_color = comp_colors[0]
    min_distance = 100
    for curr_color in comp_colors:
        curr_distance = compute_color_distance(start_color, curr_color)
        if curr_distance < min_distance:
            closest_color = curr_color
            min_distance = curr_distance
    return closest_color

def compute_color_distance(color1: tuple[int, int, int], color2: tuple[int, int, int]):
    rmean = (color1[0] + color2[0]) / 2
    change_r = color1[0] - color2[0]
    change_g = color1[1] - color2[1]
    change_b = color1[2] - color2[2]
    return math.sqrt(((2 + (rmean / 256)) * pow(change_r, 2)) + (4 * pow(change_g, 2)) + (2 + ((255 - rmean)/256)) + pow(change_b, 2))

def print_banner(banner: list[str]):
    print()
    for line in banner:
        print(line)
    print()

def select_anchor_colors():
    pass

def select_DMC_colors():
    pass

def select_manual_RGB_colors():
    print("Please enter the red value for your first color: ", end="")
    red = int(input())
    print("green: ", end="")
    green = int(input())
    print("blue: ", end="")
    blue = int(input())
    colors = [(red, green, blue)]
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
        colors.append((red, green, blue))
        print("what is the name of your color (must be unique): ", end="")
        name = input()
        color_map[(red, green, blue)] = name
        print("Add another color? (y/n): ", end="")
        more_colors = input()
    return colors, color_map

def extract_rgb_from_img():
    print("Please enter the file path to you picture:")
    file_path = input()
    image = Image.open(file_path)
    width, height = image.size
    pixels = image.load()
    colors = []
    for row in range(height):
        for column in range(width):
            pixel = pixels[column, row]
            if pixel not in colors:
                colors.append(pixel)
    print("Please enter file path to desired output file:")
    file_path = input()
    with open(file_path, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        for color in colors:
            writer.writerow(color)

def extract_color_map_from_csv():
    print("Please enter the file path to you picture:")
    file_path = input()
    color_map = {}
    with open(file_path, mode='r') as file:
        csvFile = csv.reader(file)
        for line in csvFile:
            color_map[line[0]] = (line[1], line[2], line[3])
    print("Please enter file path to desired output file")
    file_path = input()
    with open(file_path, mode='w') as file:
        file.write("{\n")
        for color in color_map:
          file.write(f"\t{color} : ({color_map[color][0]}, {color_map[color][1]}, {color_map[color][2]}),\n")
        file.write("}") 

def main():
    print_banner(name_banner)
    print("please enter the file path to your picture:")
    file_path = input()
    print("What colors do you want to be extracted?")
    print_banner(color_options_menu)
    color_choice = int(input())
    if color_choice == 1:
        pass
    elif color_choice == 2:
        pass
    elif color_choice == 3:
        pass
    elif color_choice == 4:
        pass
    elif color_choice == 5:
        colors, color_map = select_manual_RGB_colors()
    else:
        pass
    pattern_count, pattern_colors = translate_image(file_path, colors, color_map)
    print("Write to what file?: ", end="")
    file_path = input()
    write_pattern_to_file(pattern_count, pattern_colors, file_path)

# def main():
#     print("please enter the absolute path to your picture:")
#     file_path = input()
#     print("You will now be prompted for the colors in your pattern.") 
#     print("Please enter the red value for your first color: ", end="")
#     red = int(input())
#     print("green: ", end="")
#     green = int(input())
#     print("blue: ", end="")
#     blue = int(input())
#     colors = [(red, green, blue)]
#     print("what is the name of your color (must be unique): ", end="")
#     name = input()
#     color_map = {(red, green, blue) : name}
#     print("Add another color? (y/n): ", end="")
#     more_colors = input()
#     while more_colors == "y":
#         print("Please enter the red value for your next color: ", end="")
#         red = int(input())
#         print("green: ", end="")
#         green = int(input())
#         print("blue: ", end="")
#         blue = int(input())
#         colors.append((red, green, blue))
#         print("what is the name of your color (must be unique): ", end="")
#         name = input()
#         color_map[(red, green, blue)] = name
#         print("Add another color? (y/n): ", end="")
#         more_colors = input()
#     pattern_count, pattern_colors = translate_image(file_path, colors, color_map)
#     print("Write to what file?: ", end="")
#     file_path = input()
#     write_pattern_to_file(pattern_count, pattern_colors, file_path)

if __name__ == "__main__":
    main()