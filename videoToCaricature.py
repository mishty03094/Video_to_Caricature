import cv2



class Caricature:
    ''' First, downscale the image,
        then apply bilateral filter to it,
        then bring it back to original scale,
        then convert to gray scale,
        then blur the image,
        then outline the edges.
    '''

    def __init__(self):
        pass  # Constructor does nothing

    def toCartoon(self, image_rgb):



        #image_rgb = cv2.imread(image)






        image_rgb = cv2.resize(image_rgb, (1366, 768))


        numDownScaling = 2
        numBilateralSteps = 50

        # 1. Downscaling
        image_color = image_rgb
        for _ in range(numDownScaling):
            image_color = cv2.pyrDown(image_color)
            cv2.imshow("Step 1", image_color)

        # 2. Applying Bilateral Filter
        for _ in range(numBilateralSteps):
            image_color = cv2.bilateralFilter(image_color, 9, 9, 7)
            cv2.imshow("Step 2", image_color)

        # 3. Upscaling the image to original
        for _ in range(numDownScaling):
            image_color = cv2.pyrUp(image_color)
            cv2.imshow("Step 3", image_color)

        # 4. Convert to gray scale
        gray_image = cv2.cvtColor(image_color, cv2.COLOR_RGB2GRAY)
        cv2.imshow("Step 4", gray_image)

        # 5. Apply median blur
        blur_image = cv2.medianBlur(gray_image, 3)
        cv2.imshow("Step 5", blur_image)

        # 6. Detect and enhance edges (outlining)
        image_edge = cv2.adaptiveThreshold(blur_image, 255,
                                           cv2.ADAPTIVE_THRESH_MEAN_C,
                                           cv2.THRESH_BINARY, 9, 2)
        cv2.imshow("Step 6", image_edge)

        # 7. Convert back to color and bitwise_and for caricatue effect
        (x, y, z) = image_color.shape
        image_edge = cv2.resize(image_edge, (y, x))
        image_edge = cv2.cvtColor(image_edge, cv2.COLOR_GRAY2RGB)
        cv2.imshow("Step 7", image_edge)

        #cv2.waitKey(0)


        (x, y, z) = image_color.shape
        img_edge = cv2.resize(image_edge, (y, x))


        return cv2.bitwise_and(image_color, img_edge)



tmp_canvas = Caricature()
cap = cv2.VideoCapture(0)

while True:
    ret, img = cap.read()
    if not ret:
        break  # If frame not read correctly, break the loop


    res = tmp_canvas.toCartoon(img)


    cv2.imshow("Cartoon version", res)




    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()  # Release the webcam
cv2.destroyAllWindows()

