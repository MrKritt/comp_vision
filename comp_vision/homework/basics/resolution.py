import numpy as np


def nominal_resolution(image, size):
    right_angle = -1
    left_angle = image.shape[1] + 1

    for y in range(image.shape[0]):
        for x in range(image.shape[1]):
            if image[y, x] == 1:
                if x < left_angle:
                    left_angle = x
                if x > right_angle:
                    right_angle = x

    if left_angle == image.shape[1] + 1 and right_angle < 0:
        return
    else:
        return (right_angle - left_angle) / size


for i in range(1, 7):
    image = open(f'figure{i}.txt')
    [size, image] = image.read().split('#')
    image_c = image.split('\n')
    image = []

    for line in image_c:
        if line:
            image.append(list(map(float, line.split())))

    image = np.array(image)
    resolution = nominal_resolution(image, float(size))
    print(f'figure{i} разрешение = {resolution}')
