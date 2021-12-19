import cv2
import numpy as np
import math


count = 0
thresh = []

for i in range(12):
    right = []
    thresh.append(cv2.imread(f"img ({i + 1}).jpg", cv2.IMREAD_GRAYSCALE))
    thresh[i] = cv2.GaussianBlur(thresh[i], (89, 89), 0)
    _, thresh[i] = cv2.threshold(thresh[i], 126, 255, 0)
    contours, _ = cv2.findContours(thresh[i], cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    for cnts in contours:
        cnt = np.array(cv2.boxPoints(cv2.minAreaRect(cnts)))
        w = math.dist(cnt[0], cnt[1])
        h = math.dist(cnt[0], cnt[3])
        if w * 10 < h:
            right.append([cnts])
        if h * 10 < w:
            right.append([cnts])
    count += len(right)

print(f"На всех изображениях:{count} карандаш")
