import numpy as np
import cv2 as cv


def preprocess(cloth, cloth_mask):
    masked = cv.bitwise_AND(cloth, cloth, mask=cloth_mask)
    img = np.full((masked.shape[0], masked.shape[1], 3), (0, 0, 255), dtype=np.uint8)  # create
    answer = img + masked
    return answer
