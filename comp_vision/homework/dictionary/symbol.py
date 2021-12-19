import numpy as np
import matplotlib.pyplot as plt
from skimage.measure import label, regionprops


def lakes_and_bays(image):
    binary = ~image
    labeled_binary = label(binary)
    regs = regionprops(labeled_binary)
    count_lakes = 0
    count_bays = 0
    for reg in regs:
        on_bound = False
        for y, x in reg.coords:
            if y == 0 or x == 0 or y == image.shape[0] - 1 or x == image.shape[1] - 1:
                on_bound = True
                break
        if not on_bound:
            count_lakes += 1
        else:
            count_bays += 1
    return count_lakes, count_bays


def has_vline(region):
    lines = np.sum(region.image, 0) // region.image.shape[0]
    return 1 in lines


def filling_factor(region):
    return np.sum(region.image) / region.image.size


def get_area(region, label):
    return np.array(np.where(region == label, region)).flatten().size


def recognize(region):
    if np.all(region.image):
        return '-'
    cl, cb = lakes_and_bays(region.image)
    if cl == 2:
        if has_vline(region):
            return 'B'
        else:
            return '8'
    if cl == 1:
        if cb == 3:
            return 'A'
        elif cb:
            cut_cl, cut_cb = lakes_and_bays(region.image[0:14, 0:-1])
            if cut_cl > 0:
                return "P"
            return "D"
        else:
            return '0'
    if cl == 0:
        if has_vline(region):
            return '1'
        if cb == 2:
            return '/'
        _, cut_cb = lakes_and_bays(region.image[2:-2, 2:-2])
        if cut_cb == 4:
            return 'X'
        if cut_cb == 5:
            cy = region.image.shape[0] // 2
            cx = region.image.shape[1] // 2
            if region.image[cy, cx] != 0:
                return '*'
            else:
                return 'W'
    return None


img = plt.imread('symbols.png')
img_gray = np.sum(img, 2)
img_gray[img_gray > 0] = 1

labeled_img = label(img_gray)
regions = regionprops(labeled_img)
print(np.max(labeled_img))

count = {}
for region in regions:
    symbol = recognize(region)
    if symbol not in count:
        count[symbol] = 0
    count[symbol] += 1
print(count)

for symbol in count:
    print(f"Символ: {symbol} : {round(count[symbol] / sum(count.values()) * 100, 2)}%")
