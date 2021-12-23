import numpy as np
from skimage import color
import matplotlib.pyplot as plt
from skimage.measure import label, regionprops
from skimage.filters import threshold_otsu

img = plt.imread('balls_and_rects.png')
thres = threshold_otsu(color.rgb2gray(img))
binar = img > thres
hsv_img = color.rgb2hsv(img)
labeled = label(binar)
regions = regionprops(labeled)

object = {
    'квадраты': {},
    'круги': {}
}


def get_colour(image):
    hue = np.unique(image[:, :, 0]) * 360
    hue = np.max(hue[hue > 0])
    if 0 < hue <= 20 or hue > 330:
        return 'Красные'
    elif 20 < hue <= 40:
        return 'Оранжевые'
    elif 40 < hue <= 75:
        return 'Желтые'
    elif 75 < hue <= 165:
        return 'Зеленые'
    elif 165 < hue <= 190:
        return 'Бирюзовые'
    elif 190 < hue <= 275:
        return 'Голубые'
    elif 275 < hue <= 330:
        return 'Фиолетовые'


for region in regions:
    y_min, x_min, _, y_max, x_max, _ = region.bbox
    colour_img = hsv_img[y_min:y_max, x_min:x_max]
    target_color = get_colour(colour_img)
    found_color = None
    target_object = ''
    if target_color is None:
        plt.imshow(colour_img)
        plt.show()

    if np.all(region.image):
        target_object = 'квадраты'
    else:
        target_object = 'круги'

    obj_color_keys = object[target_object].keys()
    for key_color in obj_color_keys:
        if key_color == target_color:
            found_color = key_color
            break

    if found_color:
        object[target_object].update({target_color: object[target_object][target_color] + 1})
    else:
        object[target_object].update({target_color: 1})

overall_amount = 0

for object_key in object.keys():
    figur = object[object_key]
    for object_color in figur.keys():
        overall_amount += figur[object_color]
        print(f'{object_color} {object_key} {figur[object_color]}')
print(f'Всего фигур {overall_amount}')
