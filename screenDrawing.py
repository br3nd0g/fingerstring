import cv2
import numpy as np

class Hand:
    def __init__(self, handData, frame_width=None, frame_height=None):
        self.handData = handData
        self.handDataScaled = self.scaleHandData(frame_width, frame_height)
        self.rightHand = self.determineHand()
        self.magnitude = self.determinePinchMagnitude()
        self.segment = self.determineSegment(frame_height)

    def determineHand(self):

        if self.handData['thumb']['x'] > 0.5:
            return True
        else:
            return False

    def scaleHandData(self, frame_width, frame_height):

        def scale_finger_points(fingerTip):

            points = int(fingerTip['x'] * frame_width), int(fingerTip['y'] * frame_height)

            return  {
                'x': points[0],
                'y': points[1]
            }
        
        handDataScaled = {
            'index': scale_finger_points(self.handData['index']),
            'thumb': scale_finger_points(self.handData['thumb'])
        }

        return handDataScaled

    def determinePinchMagnitude(self):

        def get_line_length(point1, point2):
            return ((point1['x'] - point2['x']) ** 2 + (point1['y'] - point2['y']) ** 2) ** 0.5
        
        index = self.handData['index']
        thumb = self.handData['thumb']

        distance = get_line_length(index, thumb)

        # scale the distance to a range of 1-5
        # 0.38 is highest, 0.05 is lowest

        pinch_ranges = np.linspace(0.05, 0.38, 5)

        closest_idx = (np.abs(pinch_ranges - distance)).argmin()
        magnitude = closest_idx + 1

        return magnitude

    def determineSegment(self, frame_height):

        thumb_y = self.handDataScaled['thumb']['y']
        section_height = frame_height // 4
        thumb_segment = 4 - (thumb_y // section_height)
        thumb_segment = max(1, min(4, thumb_segment))

        return thumb_segment

    def get_scaled_xy_tuple(self, finger):
        return (self.handDataScaled[finger]['x'], self.handDataScaled[finger]['y'])
        
def processHandData(handDatas, frame_width, frame_height, frame):
    
    hands = {'left': None, 'right': None}

    if handDatas != None:
        for fingerTips in handDatas:

            hand = Hand(handData=fingerTips, frame_width=frame_width, frame_height=frame_height)

            if hand.rightHand:
                hands['right'] = hand
            else:
                hands['left'] = hand

            drawFingerLine(frame, hand)

    drawBoxes(frame, hands, frame_width, frame_height)

    return hands['left'], hands['right']

def drawFingerLine(frame, hand):

    cv2.circle(frame, hand.get_scaled_xy_tuple('index'), 5, (0, 225, 0), -1)
    cv2.circle(frame, hand.get_scaled_xy_tuple('thumb'), 5, (0, 225, 0), -1)

    cv2.line(frame, hand.get_scaled_xy_tuple('index'), hand.get_scaled_xy_tuple('thumb'), (0, 255, 0), 2) 

def drawBoxes(frame, hands, frame_width, frame_height):

    drawRightBoxes(frame, hands, frame_width, frame_height)
    drawLeftBoxes(frame, hands, frame_width, frame_height)

def drawRightBoxes(frame, hands, frame_width, frame_height):

    # Split the frame width in half
    right_start_x = frame_width // 2
    right_end_x = frame_width

    # Split the right half into 4 vertical segments
    segment_height = frame_height // 4

    for i in range(4):

        y1 = i * segment_height
        y2 = (i + 1) * segment_height if i < 3 else frame_height

        pt1 = (right_start_x, y1)
        pt2 = (right_end_x, y2 - 4)

        if hands['right'] and hands['right'].segment == 4 - i:
            cv2.rectangle(frame, pt1, pt2, (0, 255, 0), 4)
        else:
            cv2.rectangle(frame, pt1, pt2, (0, 0, 0), 4)

def drawLeftBoxes(frame, hands, frame_width, frame_height):

    end_x = frame_width // 2
    end_x -= 4

    if hands['left']:
        cv2.rectangle(frame, (0,0), (end_x, frame_height), (0, 255, 0), 4)
    else:
        cv2.rectangle(frame, (0,0), (end_x, frame_height), (0, 0, 0), 4)
    