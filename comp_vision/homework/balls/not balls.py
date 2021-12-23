import cv2

cam = cv2.VideoCapture(0)
cv2.namedWindow('camera', cv2.WINDOW_KEEPRATIO)

balls_color_bondaries = [
    [(44, 100, 150), (85, 255, 255), 'green'],
    [(130, 120, 160), (180, 255, 255), 'red'],
    [(10, 120, 180), (50, 255, 255), 'yellow']
]

order = []
found = []
remembered = False
was_printed = False
confirmed = False
shown_order = []

while True:
    _, image = cam.read()
    image = cv2.flip(image, 1)
    blurred = cv2.GaussianBlur(image, (11, 11), 0)
    hsv_image = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)

    if not remembered or confirmed:
        found = []
        for color_bound in balls_color_bondaries:
            mask = cv2.inRange(hsv_image, color_bound[0], color_bound[1])
            mask = cv2.erode(mask, None, iterations=2)
            mask = cv2.dilate(mask, None, iterations=2)

            cnt, _ = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            if len(cnt) > 0:
                c_max = max(cnt, key=cv2.contourArea)
                (curr_x, curr_y), radius = cv2.minEnclosingCircle(c_max)
                if radius > 10:
                    cv2.circle(image, (int(curr_x), int(curr_y)), int(radius), (255, 255, 255), 2)
                    found.append({
                        'color': color_bound[2],
                        'center': (curr_x, curr_y)
                    })

    if not was_printed and len(found) == 3:
        found = sorted(found, key=lambda item: item['center'][0])
        order = []
        for item in found:
            order.append(item['color'])
        was_printed = True

    if confirmed and len(found) == 3:
        found = sorted(found, key=lambda item: item['center'][0])
        shown_order = []
        for item in found:
            shown_order.append(item['color'])
        if shown_order != order:
            print('Не верно')
        else:
            print('Верно')
        was_printed = True

    cv2.imshow('camera', image)

    key = cv2.waitKey(1)
    if key == ord('q'):
        break
    if key == ord('r') and len(found) == 3:
        remembered = True
    if key == ord('p'):
        was_printed = False
        confirmed = True

cam.release()
cv2.destroyAllWindows()
