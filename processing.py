import cv2
import numpy as np
import networktables_handler
import math

def angle(px, x):
    px_to_angle = networktables_handler.aov / px
    return (px / 2 - x) * px_to_angle


def distance(beta):  # in
    return networktables_handler.ball_radius / math.sin(beta)

def process_image(image : np.ndarray) -> None:

    image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(image, networktables_handler.min_hsv, networktables_handler.max_hsv)
    kernal = np.ones((5, 5), np.uint8)
    mask = cv2.erode(mask, kernal, 2)
    mask = cv2.dilate(mask, kernal, 2)

    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if len(contours) > 0:
        for c in contours:
            ((x, y), radius) = cv2.minEnclosingCircle(c)
            if radius > 10 and radius <= x < image.shape[1] - radius and radius <= y < image.shape[0] - radius:
                radius /= 1.15
                pixels = []
                pixels.append(image[int(y - radius), int(x)])
                pixels.append(image[int(y), int(x + radius)])
                pixels.append(image[int(y), int(x - radius)])
                #cv2.circle(oldimage, (int(x), int(y - radius)), 3, (0, 0, 0), 3)
                #cv2.circle(oldimage, (int(x), int(y - radius)), 3, (0, 0, 0), 3)
                #cv2.circle(oldimage, (int(x), int(y - radius)), 3, (0, 0, 0), 3)
                draw = True
                for pixel in pixels:
                    if networktables_handler.min_hsv[0] > pixel[0] or pixel[0] > networktables_handler.max_hsv[0] or pixel[1] <= 50:
                        draw = False
                        break
                if draw:
                    radius *= 1.15
                    #cv2.circle(oldimage, (int(x), int(y)), int(radius), (252, 40, 3), 3)

                    beta = radius * networktables_handler.aov / image.shape[1]

                    dis = distance(beta)

                    alpha = ((image.shape[1] / 2) - x) * (math.degrees(networktables_handler.aov) / image.shape[1])

                    output_vision(dis, alpha)
                    #print("angle: " + str(alpha))
                    #print("distance: " + str(dis))
                #else:
                    #radius *= 1.15
                    #cv2.circle(oldimage, (int(x), int(y)), int(radius), (0, 0, 255), 3)

def output_vision(distance : float, angle : float) -> None:
    if (networktables_handler.smart_dashboard):
        networktables_handler.smart_dashboard.putNumber('vision_distance', distance)
        networktables_handler.smart_dashboard.putNumber('vision_angle', angle)