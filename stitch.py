# Format for gps_data.txt:
# image_filename latitude longitude altitude
import cv2
import numpy as np
import random
from math import ceil

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

def stitch(foldername):
    file = open(foldername + "gps_data.txt", "r")
    lines = file.readlines()
    lines = [line.strip().split(" ") for line in lines]
    data = [(line[0], int(line[1]), int(line[2]), int(line[3])) for line in lines]
    count = np.zeros((size, size))
    visited = np.zeros((size,size))
    for img_data in data:
        filename, x, y, img_size = img_data
        img = cv2.imread(foldername + filename)

        # Add 1 to all coordinates where there's a tree detected
        treeCoords = np.where((img == [255,255,255]).all(axis=2))
        treeCoords = (treeCoords[0] + y - img_size, treeCoords[1] + x  - img_size)
        count[treeCoords] += 1

        # Add 1 to all coordinates
        allCoords = np.where((img != None).all(axis=2))
        allCoords = (allCoords[0] + y  - img_size, allCoords[1] + x  - img_size)
        visited[allCoords] += 1
    
    # Avoid divide by 0 error that occurs when area isn't surveyed completely
    notfound = np.where(visited == 0)
    visited[notfound] = 1

    # Get percent of detections for each pixel and count the ones above the SURETY rate to be trees
    stitched = count / visited
    stitched *= 255
    _, stitched = cv2.threshold(stitched, 255 * SURETY, 255, cv2.THRESH_BINARY)
    cv2.imwrite(foldername + 'stitched.png', stitched)

# Use this function to create a test case that mimics masks from drone footage
generate_testmask('Masks/Test1/', 12, 25, 20)

# Use this function to stitch together the stuff in a given folder
stitch('Masks/Test1/')