import cv2
import numpy as np

def computeAngle(frame,mtx,dist):
    # Get size
    h,  w = frame.shape[:2]
    # Get optimal new camera
    newcameramtx, roi = cv2.getOptimalNewCameraMatrix(mtx, dist, (w, h), 0, (w, h))

    # Undistort image
    dst = cv2.undistort(frame, mtx, dist, None, newcameramtx)

    # Convert image to gray
    grayImage = cv2.cvtColor(dst, cv2.COLOR_BGR2GRAY)

    # Applying binarization to the grayscale image using a threshold value.
    binarization = True
    if binarization:
        # Define the threshol value
        thresholdValue = 128
        # Convert the original image to the HSV color space for better color segmentation
        hsvImage = cv2.cvtColor(dst, cv2.COLOR_BGR2HSV)

        # Define the lower and upper bounds for the green color in HSV
        lower_green = np.array([50, 100, 100])  # Adjust these values as needed
        upper_green = np.array([70, 255, 255])

        # Create a mask to filter the green color
        green_mask = cv2.inRange(hsvImage, lower_green, upper_green)

        # Combine the grayscale image with the green mask
        combined_mask = cv2.bitwise_or(grayImage, green_mask)

        #Gamma
        c = 1
        gamma_value = 25.0
        rn = combined_mask/255
        img_gamma = c*(rn**gamma_value)
        img_proc = np.uint8((255/(np.max(img_gamma)-np.min(img_gamma)))*(img_gamma-np.min(img_gamma)))

        # Applying binarization to the combined mask using a threshold value.
        _,binaryImage = cv2.threshold(img_proc, thresholdValue, 255, cv2.THRESH_BINARY_INV)
        
    segmentation = True
    if segmentation:
        # find the contours
        # contours,hierarchy = cv2.findContours(binaryImage, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        # SE CAMBIO EL ULTIMO ARGUMENTO A "cv2.CHAIN_APPROX_NONE" para corregir el error con "pattern_T01.jpeg"
        contours,hierarchy = cv2.findContours(binaryImage, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    
        # Iterate through the contours and filter out small ones
        filtered_contours = [cnt for cnt in contours if cv2.contourArea(cnt) > 100]
        #print("Number of filtered contours detected:", len(filtered_contours))
        
        fIteration = len(filtered_contours)
        if fIteration > 1:
            filtered_last = filtered_contours[fIteration-1]            
            # Check if there are enough points to fit an ellipse
            if len(filtered_last) == 4: 
                average_point = np.mean(filtered_last[:, 0], axis=0, dtype=np.int32)
                filtered_last = np.vstack([filtered_last[:, 0], average_point.reshape(1, 2)])

            if len(filtered_last) >= 5:
                # compute the center of mass of the triangle
                originalImage = cv2.drawContours(dst, [filtered_last], -1, (0,255,255), 3)
                # compute the center of mass of the triangle
                M = cv2.moments(filtered_last)
                '''for num in cnt:
                    print(num)
                #print(M)'''
                if M['m00'] != 0.0:
                    centroidU = int(M['m10']/M['m00'])
                    centroidV = int(M['m01']/M['m00'])
                    # fit an ellipse to the largest contour to find its orientation
                    ellipsoidShape = cv2.fitEllipse(filtered_last)
                    # ellipsoidShape[0]  ->  (centroideCoordX, centroideCoordY)
                    # ellipsoidShape[1]  ->  (centroideWidth, centroideHeight)
                    # ellipsoidShape[2]  ->  Angulo que genera la elipse, los ejes no corresponden a los de un eje cordenado
                    #                        normal, su X corresponde al eje Y (normal), y, su Y corresponde al eje X (normal)
                    angle = ellipsoidShape[2]
                    # -------------------------------------------------------------
                    # -------------------------------------------------------------
                    
                    cv2.circle(dst, (centroidU, centroidV), 5, (0, 0, 255), -1)   # RED
                    #cv2.ellipse(dst, ellipsoidShape, (0, 255, 0), 2)              # GREEN
                    #print(f'Centroid (x,y): ({centroidU}, {centroidV})')
                    #print(f'Orientation angle: {angle} degrees')
                    # -------------------------------------------------------------
                    # AGREGADO
                    # -------------------------------------------------------------
                    cv2.drawContours(dst, [filtered_last], -1, (0, 255, 255), 3)         # YELLOW
                    # -------------------------------------------------------------
                    # If so, it is then visualised
                    #cv2.putText(dst, f'Angle:{round(average_angle,3)}', (centroidU, centroidV), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 0), 2)

                    return dst, angle, centroidU, centroidV
                else:
                    print('Error')
        else:
            return dst,360,w+10,h+10
