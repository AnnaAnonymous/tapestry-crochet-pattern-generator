from PIL import Image
import csv

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