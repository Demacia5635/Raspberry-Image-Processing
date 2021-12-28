import cv2
import numpy as np
import networktables_handler

def process_image(frame : np.ndarray) -> None:
    #TODO : put in the processing algorithm (not in a loop)
    pass

def output_vision(distance : float, angle : float) -> None:
    networktables_handler.smart_dashboard.putNumber('vision_distance', distance)
    networktables_handler.smart_dashboard.putNumber('vision_angle', angle)