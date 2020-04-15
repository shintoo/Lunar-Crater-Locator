import cv2
import numpy as np
import sys
import argparse


path = sys.argv[1]
blur = int(sys.argv[2])
canny_high_threshold = int(sys.argv[3])
accumulator_threshold = int(sys.argv[4])
max_radius = int(sys.argv[5])
max_distance = int(sys.argv[6])
canny_low_threshold = canny_high_threshold / 2

img = cv2.imread(path,0)
circle_image = cv2.medianBlur(img,blur)
cv2.imwrite(path.split('.')[0] + "_blur.png", circle_image)
img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)

print(f"Max circle_image: {np.max(circle_image)}")

edges = cv2.Canny(circle_image, canny_low_threshold, canny_high_threshold)
cv2.imwrite(path.split('.')[0] + "_edges.png", edges)

circles = cv2.HoughCircles(circle_image,cv2.HOUGH_GRADIENT,1,10,
                                    param1=canny_high_threshold, param2=accumulator_threshold, maxRadius=max_radius)

if circles is None:
    print("No circles found")
    quit()

print(circles)

circles = np.uint16(np.around(circles))
for i in circles[0,:]:
    # draw the outer circle
    cv2.circle(img,(i[0],i[1]),i[2],(255,220,100),2)
#    cv2.line(img, (i[0],i[1]), (i[0] + i[2], i[1]), (255, 220, 100), 2)
    # draw the center of the circle
    cv2.circle(img,(i[0],i[1]),1,(100, 100, 255),2)

cv2.imwrite(path.split('.')[0] + f"_blur{blur}_canny{canny_high_threshold}_acc{accumulator_threshold}_mr{max_radius}_md{max_distance}.png", img)


def circle_distances_standard_dev(circles):
    pass

def circle_distances(circles):
    distances = []

    for i in circles:
        for j in circles:
            if i == j:
                continue
            distances.append(np.linalg.norm(circles[i][:2] - circles[j][:2]))

    return distances

# TODO
#if __name__ == '__main__':
#    import argparse

#    parser = argparse.ArgumentParser("Find craters!")
#    parser.add_argument("image-path", help="path to the image file")
#    parser.add_argument("blur-size", help="Size of median blur kernel. The larger this is, the more smaller artifacts will be ignored.")
#    parser.add_argument("canny-threshold", help="Lower bound for edge detection. Edges below this edginess are dropped.")
#    parser.add_argument("accumulator-threshold", help="Hough transform accumulator threshold. The higher this is, the higher 'quality' circles found.")
#    parser.add_argument("max-radius", help="Maximum crater radius")
#    parser.add_argument("max-distance", help="Maximum distance between craters. Helps avoid redundant counting.")
