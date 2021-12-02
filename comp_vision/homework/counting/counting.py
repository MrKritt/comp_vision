from matplotlib import pyplot as plt
import numpy as np
from skimage.measure import label
from scipy.ndimage.morphology import binary_opening


masks = np.array([
                  np.array([
                            [1, 1, 1, 1, 1, 1],
                            [1, 1, 1, 1, 1, 1],
                            [1, 1, 1, 1, 1, 1],
                            [1, 1, 1, 1, 1, 1]
                  ]),
                  np.array([
                            [1, 1, 0, 0, 1, 1],
                            [1, 1, 0, 0, 1, 1],
                            [1, 1, 1, 1, 1, 1],
                            [1, 1, 1, 1, 1, 1]
                  ]),
                  np.array([
                            [1, 1, 1, 1, 1, 1],
                            [1, 1, 1, 1, 1, 1],
                            [1, 1, 0, 0, 1, 1],
                            [1, 1, 0, 0, 1, 1]
                  ]),
                  np.array([
                            [1, 1, 1, 1],
                            [1, 1, 1, 1],
                            [1, 1, 0, 0],
                            [1, 1, 0, 0],
                            [1, 1, 1, 1],
                            [1, 1, 1, 1]
                  ]),
                  np.array([
                            [1, 1, 1, 1],
                            [1, 1, 1, 1],
                            [0, 0, 1, 1],
                            [0, 0, 1, 1],
                            [1, 1, 1, 1],
                            [1, 1, 1, 1]
                  ])
], dtype=object)



image = np.load('ps.npy.txt')
labeled_image = label(image)
print(f'Всего: {np.max(labeled_image)} объектов')

for mask in masks:
    masked_image = binary_opening(image, mask)
    labeled_masked_image = label(masked_image)
    print(f' {np.max(labeled_masked_image.ravel())} объектов для {mask}')
    plt.imshow(masked_image)
    plt.show()