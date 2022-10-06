import cv2
import numpy as np


class Vision:
    # properties
    needle_img = None
    needle_w = 0
    needle_h = 0
    method = None

    # constructor
    def __init__(self, needle_img_path, method=cv2.TM_CCOEFF_NORMED):
        # load the image we're trying to match
        # https://docs.opencv2.org/4.2.0/d4/da8/group__imgcodecs.html
        self.needle_img = cv2.imread(needle_img_path, cv2.IMREAD_UNCHANGED)

        # Save the dimensions of the needle image
        self.needle_w = self.needle_img.shape[1]
        self.needle_h = self.needle_img.shape[0]

        # There are 6 methods to choose from:
        # TM_CCOEFF, TM_CCOEFF_NORMED, TM_CCORR, TM_CCORR_NORMED, TM_SQDIFF, TM_SQDIFF_NORMED
        self.method = method

    def find(self, haystack_img, threshold=0.5, debug_mode=None):
        # run the OpenCV algorithm
        result = cv2.matchTemplate(haystack_img, self.needle_img, self.method)

        # Get the all the positions from the match result that exceed our threshold
        locations = np.where(result >= threshold)
        locations = list(zip(*locations[::-1]))
        # print(locations)

        # You'll notice a lot of overlapping rectangles get drawn. We can eliminate those redundant
        # locations by using groupRectangles().
        # First we need to create the list of [x, y, w, h] rectangles
        rectangles = []
        for loc in locations:
            rect = [int(loc[0]), int(loc[1]), self.needle_w, self.needle_h]
            # Add every box to the list twice in order to retain single (non-overlapping) boxes
            rectangles.append(rect)
            rectangles.append(rect)
        # Apply group rectangles.
        # The groupThreshold parameter should usually be 1. If you put it at 0 then no grouping is
        # done. If you put it at 2 then an object needs at least 3 overlapping rectangles to appear
        # in the result. I've set eps to 0.5, which is:
        # "Relative difference between sides of the rectangles to merge them into a group."
        rectangles, weights = cv2.groupRectangles(rectangles, groupThreshold=1, eps=0.5)
        # print(rectangles)

        points = []
        if len(rectangles):
            # print('Found needle.')

            line_color = (0, 255, 0)
            line_type = cv2.LINE_4
            marker_color = (255, 0, 255)
            marker_type = cv2.MARKER_CROSS

            # Loop over all the rectangles
            for (x, y, w, h) in rectangles:

                # Determine the center position
                center_x = x + int(w / 2)
                center_y = y + int(h / 2)
                # Save the points
                points.append((center_x, center_y))

                if debug_mode == 'rectangles':
                    # Determine the box position
                    top_left = (x, y)
                    bottom_right = (x + w, y + h)
                    # Draw the box
                    cv2.rectangle(haystack_img, top_left, bottom_right, color=line_color,
                                  lineType=line_type, thickness=2)
                elif debug_mode == 'points':
                    # Draw the center point
                    cv2.drawMarker(haystack_img, (center_x, center_y),
                                   color=marker_color, markerType=marker_type,
                                   markerSize=40, thickness=2)

        if debug_mode:
            cv2.imshow('Matches', haystack_img)
            # cv2.waitKey()
            # cv2.imwrite('result_click_point.jpg', haystack_img)

        return

    def is_on_screen(self, image_to_search, threshold=.6):
        # target_img = cv2.imread('image/target-monster-icon.jpg')
        # target_img = cv2.imread(self.needle_img)

        result = cv2.matchTemplate(self.needle_img, image_to_search, cv2.TM_CCOEFF_NORMED)
        # DEBUGER SHOW IMAGE
        # cv2.imshow('Result', screentest)
        # cv2.waitKey()
        min_val1, max_val1, min_loc1, max_loc1 = cv2.minMaxLoc(result)
        # print(max_val1)
        return max_val1 >= threshold
