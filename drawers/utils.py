import cv2
import sys
sys.path.append("../")
from utils import get_center_of_bbox, get_bbox_width


def draw_ellipse(frame, bbox, color, track_id=None):
    x_center, y_center = get_center_of_bbox(bbox)
    width = get_bbox_width(bbox)
    cv2.ellipse(frame, center=(int(x_center), int(y_center)),
                axes=(int(width), int(0.35*width)),
                angle=0, startAngle=-45, endAngle=235, color=color, thickness=2)


    rectangle_width = 40
    rectangle_height = 20
    x1_rect = x_center - rectangle_width//2
    x2_rect = x_center + rectangle_width//2
    y1_rect = (y_center - rectangle_height//2)+15
    y2_rect = (y_center + rectangle_height//2)+15

    if track_id is not None:
        # Draw text positioned lower and closer to the ellipse
        text = str(track_id)
        font = cv2.FONT_HERSHEY_SIMPLEX
        font_scale = 0.7
        thickness = 2
        
        # Get text size to center it
        (text_width, text_height), baseline = cv2.getTextSize(text, font, font_scale, thickness)
        
        # Position text lower and closer to the ellipse
        text_x = int(x_center - text_width // 2)
        text_y = int(y_center + width * 0.3)  # Position lower, closer to ellipse
        
        # Draw red background box
        padding = 4
        box_x1 = text_x - padding
        box_y1 = text_y - text_height - padding
        box_x2 = text_x + text_width + padding
        box_y2 = text_y + padding
        
        cv2.rectangle(frame, (box_x1, box_y1), (box_x2, box_y2), (0, 0, 255), cv2.FILLED)
        
        # Draw white text
        cv2.putText(frame, text, (text_x, text_y), font, font_scale, (255, 255, 255), thickness)


    return frame