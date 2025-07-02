from ultralytics import YOLO

model = YOLO("yolov8x")

results = model.predict("input_video/Q2_m8-s37_Curry 5' Driving Reverse Layup (14 PTS).mp4", save=True)

print(results)
print("--------------------------------")
for box in results[0].boxes:
    print(box)




