# Format for gps_data.txt:
# image_filename latitude longitude altitude
import cv2
import numpy as np
import random
from math import ceil
import imutils

#final_height, final_width = (1152 * 2, 2048 * 2)
aspect_ratio = (2.5,2)

size = 201
# Percent of images that are needed to confirm that a tree is there
SURETY = .75

# Area is within rectangle (0, 0), (final_width, final_height)
def generate_testcolor(foldername, img_width_2, img_height_2, hor_waypoints, vert_waypoints):

    ori = cv2.imread(foldername + 'original.png')
    final_height, final_width, _ = ori.shape
#    print(final_width, final_height)
#    assert(img_width_2 / img_height_2 == aspect_ratio[0] / aspect_ratio[1])
#    scale = img_width_2 // aspect_ratio[0]
#    scale = int(scale)
    scaleX = 1
    scaleY = 1

    img_width = img_width_2 // 2
    img_height = img_height_2 // 2

#    ori = np.random.randint(0, 255, size=(final_height, final_width, 3), dtype=np.uint8)

    img_datas = []
    start_hor = img_width
    start_vert = img_height
    end_hor = final_width - img_width
    end_vert = final_height - img_height
    dist_width = (end_hor - start_hor) // (hor_waypoints - 1)
    dist_height = (end_vert - start_vert) // (vert_waypoints - 1)

#    print(img_width, img_height)

#    print(vert_waypoints)
#    print(1/0)
    for i in range(vert_waypoints):
        for j in range(hor_waypoints):
            x = start_hor + j * dist_width
            y = start_vert + i * dist_height
#            print(x,y)
            img_datas.append(((x,y), img_height))

#    print(1/0)

#    cv2.imwrite(foldername + "original.png", ori)

    file = open(foldername + "gps_data.txt", "w+")

    for i, data in enumerate(img_datas):
        position, _ = data
        x,y = position
        minX = x - img_width
        minY = y - img_height
        maxX = x + img_width
        maxY = y + img_height
#        print(minX, maxX, minY, maxY)
        crop = ori[minY:maxY + 1, minX:maxX + 1]
        cv2.imwrite(foldername + "Image" + str(i) + ".png", crop)
        file.write("Image" + str(i) + ".png " + str(x) + " " + str(y) + " " + str(scaleX) + " " + str(scaleY) + "\n")

    file.close()

def stitch_colored(foldername):

    file = open(foldername + "gps_data.txt", "r")
    lines = file.readlines()
    lines = [line.strip().split(" ") for line in lines]
    data = [(line[0], float(line[1]), float(line[2]), float(line[3]), float(line[4]), float(line[5])) for line in lines]

#    (final_width, final_height) = (400, 300)
    (final_width, final_height) = (2200, 2600)

    count = np.zeros((final_height + 1, final_width + 1, 3))
    visited = np.zeros((final_height + 1, final_width + 1, 3))

    for img_data in data:
        filename, x, y, scaleX, scaleY, angle = img_data
        x *= scaleX
        y *= scaleY
        x = int(x)
        y = int(y)
        img = cv2.imread(foldername + filename)
        img = imutils.rotate_bound(img, angle)
        img_height, img_width, _ = img.shape
        h = img_height
        w = img_width

        # Add 1 to all coordinates
        coords = np.where((img != [0,0,0]).all(axis=2))
        newCoords = (coords[0] + y - h // 2, coords[1] + x - w // 2)
#        newCoords = (list(filter(lambda a: a >= 0, newCoords[0])), list(filter(lambda a: a >= 0, newCoords[1])))
#        newCoords = (coords[0], coords[1])
        visited[newCoords] += 1
        count[newCoords] += img[coords]
    
    # Avoid divide by 0 error that occurs when area isn't surveyed completely
    notfound = np.where(visited == 0)
    visited[notfound] = 1

    # Get percent of detections for each pixel and count the ones above the SURETY rate to be trees
    stitched = count / visited
#    stitched *= 255
#    _, stitched = cv2.threshold(stitched, 255 * SURETY, 255, cv2.THRESH_BINARY)
    cv2.imwrite(foldername + 'stitched.png', stitched)


# Use this function to create a test case that mimics masks from drone footage
#generate_testmask('Masks/RealTest/', 12, 25, 20)
#generate_testcolor('Masks/Test3/', 150, 100, 4, 3)

# Use this function to stitch together the stuff in a given folder
#stitch_colored('Masks/Test3/')
#stitch_colored('../Masks/Westgate/')
stitch_colored('../Masks/Separate/')
#2048 x 1152
#1920 x 1080

#Frame0.png 1 1 960 540 0
#Frame39.png 1.15 1.3 960 540 -3
#Frame54.png 1.06 1.6 960 540 -0.6
#Frame61.png .93 1.85 960 540 0.5