import cv2
import numpy as np

def floyd_steinberg(image, boarder):
    image = image.astype(float)

    height, width = image.shape

    for y in range(height):
        for x in range(width):

            old_pixel = image[y, x]

            if old_pixel < boarder:
                new_pixel = 0
            else:
                new_pixel = 255

            error = old_pixel - new_pixel

            image[y, x] = new_pixel

            if x + 1 < width:
                image[y, x + 1] += error * 7 / 16

            if y + 1 < height:

                if x - 1 >= 0:
                    image[y + 1, x - 1] += error * 3 / 16

                image[y + 1, x] += error * 5 / 16

                if x + 1 < width:
                    image[y + 1, x + 1] += error * 1 / 16


    return image.astype("uint8")


camera = cv2.VideoCapture(0)

while True:
    success, frame = camera.read()

    if not success:
        print("Не удалось получить изображение с камеры")
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    small = cv2.resize(gray, (100, 75))
    binary = floyd_steinberg(small, 100)

    binary = cv2.resize(binary, (100*5, 75*5), interpolation=cv2.INTER_NEAREST)

    cv2.imshow("My camera", binary)

    if cv2.waitKey(1) == ord("q"):
        break

camera.release()
cv2.destroyAllWindows()