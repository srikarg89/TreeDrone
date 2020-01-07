# Format for gps_data.txt:
# image_filename latitude longitude altitude
import cv2
import numpy as np
import random
from math import ceil

#final_height, final_width = (1152 * 2, 2048 * 2)
aspect_ratio = (2.5,2)

size = 201
# Percent of images that are needed to confirm that a tree is there
SURETY = .75

# Area is within rectangle (0,0), (size,size)
def generate_testmask(foldername, num_trees, img_size, img_distance):
    trees = []
    for i in range(num_trees):
        radius = random.randint(5, 15)
        x = random.randint(radius, size-radius)
        y = random.randint(radius, size-radius)
        trees.append(((x,y), radius))
    
    img_datas = []
    vert_waypoints = hor_waypoints = (size - img_size) // img_distance + 1
    start_hor = img_size
    start_vert = img_size
#    print(vert_waypoints)
#    print(1/0)
    for i in range(vert_waypoints):
        for j in range(hor_waypoints):
            x = start_hor + j * img_distance
            y = start_vert + i * img_distance
            img_datas.append(((x,y), img_size))
    
    ori = np.zeros((size,size))
    for position, radius in trees:
        cv2.circle(ori, position, radius, (255,255,255), -1)

    cv2.imwrite(foldername + "original.png", ori)

    file = open(foldername + "gps_data.txt", "w+")

    for i, data in enumerate(img_datas):
        position, _ = data
        x,y = position
        minX = x - img_size
        minY = y - img_size
        maxX = x + img_size
        maxY = y + img_size
        crop = ori[minY:maxY + 1, minX:maxX + 1]
        print(minX, minY, maxX, maxY)
        cv2.imwrite(foldername + "Image" + str(i) + ".png", crop)
        file.write("Image" + str(i) + ".png " + str(x) + " " + str(y) + " " + str(img_size) + "\n")

    file.close()

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

def stitch_mask(foldername):
    file = open(foldername + "gps_data.txt", "r")
    lines = file.readlines()
    lines = [line.strip().split(" ") for line in lines]
    data = [(line[0], int(line[1]), int(line[2]), int(line[3])) for line in lines]
    count = np.zeros((size, size))
    visited = np.zeros((final_height, final_width))

    for img_data in data:
        filename, x, y, img_size = img_data
        img = cv2.imread(foldername + filename)

        # Add 1 to all coordinates
        allCoords = np.where((img != None).all(axis=2))
        allCoords = (allCoords[0] + y  - img_size, allCoords[1] + x  - img_size)
        visited[allCoords] += 1
        count[allCoords] += 1
    
    # Avoid divide by 0 error that occurs when area isn't surveyed completely
    notfound = np.where(visited == 0)
    visited[notfound] = 1

    # Get percent of detections for each pixel and count the ones above the SURETY rate to be trees
    stitched = count / visited
    stitched *= 255
    _, stitched = cv2.threshold(stitched, 255 * SURETY, 255, cv2.THRESH_BINARY)
    cv2.imwrite(foldername + 'stitched.png', stitched)

def stitch_colored(foldername):

    file = open(foldername + "gps_data.txt", "r")
    lines = file.readlines()
    lines = [line.strip().split(" ") for line in lines]
    data = [(line[0], float(line[1]), float(line[2]), float(line[3]), float(line[4])) for line in lines]

#    (final_width, final_height) = (400, 300)
    (final_width, final_height) = (2048 * 2, 1152 * 2)

    count = np.zeros((final_height + 1, final_width + 1, 3))
    visited = np.zeros((final_height + 1, final_width + 1, 3))

    for img_data in data:
        filename, x, y, scaleX, scaleY = img_data
        x *= scaleX
        y *= scaleY
        x = int(x)
        y = int(y)
        img = cv2.imread(foldername + filename)
        img_height, img_width, _ = img.shape
        h = img_height
        w = img_width

        # Add 1 to all coordinates
        coords = np.where((img != None).all(axis=2))
        newCoords = (coords[0] + y - h // 2, coords[1] + x - w // 2)
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
stitch_colored('Masks/RealTest/')
#2048 x 1152