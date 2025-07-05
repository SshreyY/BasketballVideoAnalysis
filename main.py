from ultralytics import YOLO

model = YOLO("models/player_detector.pt")

results = model.predict("input_video/StephLayupVid.mp4", save=True)

print(results)
print("--------------------------------")
for box in results[0].boxes:
    print(box)




