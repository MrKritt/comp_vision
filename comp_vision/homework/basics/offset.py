import numpy as np


def coord(image):
    for y in range(image.shape[0]):
        for x in range(image.shape[1]):
            if image[y, x] == 1:
                return np.array([y, x])


def offset(image_1, image_2):
    return coord(image_2) - coord(image_1)


images = []
for i in range(1, 3):
    image = open(f'figure{i}.txt')
    [size, image] = image.read().split('#')
    image_c = image.split('\n')
    image = []

    for line in image_c:
        if line:
            image.append(list(map(float, line.split())))

    image = np.array(image)
    images.append(image)

print(f"Смещение {offset(*images)}")
