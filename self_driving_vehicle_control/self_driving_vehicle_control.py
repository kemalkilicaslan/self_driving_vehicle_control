# Self Driving Vehicle Control
# Sürücüsüz Araç Kontrolü

import pygame
import cv2
import numpy as np

# let's start pygame.
# pygame'i başlatalım.
pygame.init()

# let's create a pygame window.
# pygame penceresi oluşturalım.
win = pygame.display.set_mode((400, 400))

# let's start video capture.
# video yakalamayı başlatalım.
cap = cv2.VideoCapture(0)

# let's define the color ranges for color detection.
# renk tespiti için renk aralıklarını tanımlayalım.
lower = np.array([0, 0, 0])
upper = np.array([180, 255, 50])

while True:
    # frame reading part from video footage,
    # video çekiminden kare okuma kısmı,
    ret, frame = cap.read()

    # the part of turning the frame vertically,
    # çerçeveyi dikey olarak çevirme kısmı,
    frame = cv2.flip(frame, 1)

    # convert the frame to HSV color space.
    # çerçeveyi HSV renk uzayına dönüştürelim.
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # apply a color mask to the frame.
    # çerçeveye renk maskesi uyguluyalım.
    mask = cv2.inRange(hsv, lower, upper)

    # we find the contours in the masked frame.
    # maskelenmiş çerçevede konturları buluyoruz.
    contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # check if there are any contours.
    # herhangi bir kontur bulunup bulunmadığını kontrol edelim.
    if len(contours) > 0:
        # part to find the largest contour,
        # en büyük konturu bulma kısmı,
        largest_contour = max(contours, key=cv2.contourArea)

        # part of calculating the center of the largest contour,
        # en büyük konturun merkezini hesaplama kısmı,
        moments = cv2.moments(largest_contour)
        cx = int(moments["m10"] / moments["m00"])
        cy = int(moments["m01"] / moments["m00"])

        # the part of drawing a circle in the middle of the largest contour,
        # en büyük konturun ortasında daire çizme kısmı,
        cv2.circle(frame, (cx, cy), 5, (0, 0, 255), -1)

        # turn left if the center of the largest stroke is to the left of the frame center,
        # en büyük konturun merkezi çerçeve merkezinin solundaysa sola dönün,
        if cx < 200:
            print("Turn left")
        # turn right if the center of the largest contour is to the right of the center of the frame,
        # en büyük konturun merkezi çerçeve merkezinin sağındaysa sağa dönün,
        elif cx > 200:
            print("Turn right")
        # go straight if the center of the largest stroke is at the center of the frame,
        # en büyük konturun merkezi çerçevenin merkezindeyse düz gidin,
        else:
            print("Go straight")

    # image frame in pygame window
    # pygame penceresindeki görüntü çerçevesi
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    frame = np.rot90(frame)
    frame = pygame.surfarray.make_surface(frame)
    win.blit(frame, (0, 0))
    pygame.display.update()

    # controlling Pygame events,
    # pygame olaylarını kontrol edilme kısmı,
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            cap.release()
            cv2.destroyAllWindows()
            pygame.quit()
            quit()

# This code takes the image from the webcam and processes it using the OpenCV library. It then detects the image that Pygame is displaying. Calculates the center of the stroke and moves it to the left if the center of the window is to the left, to the right if it is to the right, and straight if it is exactly in the middle of the window. In this way, it is a driverless vehicle control application.
# Bu kod, görüntüyü web kamerasından alır ve OpenCV kitaplığını kullanarak işler. Daha sonra Pygame'in gösterdiği görüntüyü algılar. Konturun merkezini hesaplar ve pencerenin merkezi solundaysa sola, sağındaysa sağa ve tam olarak pencerenin ortasındaysa düz olarak hareket ettirir. Bu sayede sürücüsüz araç kontrol uygulamasıdır.