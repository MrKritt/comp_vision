import cv2
from tensorflow.keras.models import load_model
import tensorflow as tf
import numpy as np

widthh = 180
heightt = 120


def iou(bbox1, bbox2):
    x1, x2, y1, y2 = bbox1[:, 0], bbox1[:, 1], bbox1[:, 2], bbox1[:, 3]
    x3, x4, y3, y4 = bbox2[:, 0], bbox2[:, 1], bbox2[:, 2], bbox2[:, 3]
    inter_w = tf.reduce_min(tf.stack([x2, x4]), 0) - tf.reduce_max(tf.stack([x1, x3]), 0)
    inter_h = tf.reduce_min(tf.stack([y2, y4]), 0) - tf.reduce_max(tf.stack([y1, y3]), 0)
    pos = tf.logical_or(inter_w <= 0, inter_h <= 0)
    inter_area = inter_w * inter_h
    union_area = (y2 - y1) * (x2 - x1) + (y4 - y3) * (x4 - x3) - inter_area
    result = tf.where(pos, 0.0, inter_area / union_area)
    return 1 - result


def resize_img(img, width, height):
    resized_img = cv2.resize(src=img, dsize=(width, height), interpolation=cv2.INTER_AREA)
    if resized_img.shape[0] > resized_img.shape[1]:
        resized_img = np.rot90(resized_img, 1)
    return resized_img


model = load_model(
    r"C:\Users\artem\PycharmProjects\university\AI_and_CV\balls\model\model_1",
    custom_objects={"iou": iou})
model.summary()

width, height = None, None
config = model.get_config()
heightt, widthh = config["layers"][0]["config"]["batch_input_shape"][1:-1]

cam = cv2.VideoCapture(0)

while cam.isOpened():
    _, frame = cam.read()
    frame = cv2.flip(frame, 1)
    height, width = frame.shape[:-1]
    resized_frame = resize_img(frame, widthh, heightt)
    predict, box = model.predict(resized_frame.reshape(1, *resized_frame.shape))
    predict = predict.squeeze()
    box = box.squeeze()

    if predict > 0.4:
        xmin, xmax = (box[:2] * width).astype(int)
        ymin, ymax = (box[2:] * height).astype(int)
        cv2.rectangle(frame, (xmin, ymin), (xmax, ymax), (0, 0, 255), 2)

    cv2.imshow("cam", frame)
    key = cv2.waitKey(1)
    if key == ord('q'):
        break

cam.release()
cv2.destroyAllWindows()
