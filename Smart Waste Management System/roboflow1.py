from roboflow import Roboflow
import supervision as sv
import cv2
import numpy as np
import matplotlib.pyplot as plt 
from supervision.annotators.utils import Position


imgpath = "newdataset/val/plastic/plastic_004.jpg"

rf = Roboflow(api_key = "s92952864nuTEq6I57GW")

Project = rf.workspace().project("smart-waste-management-h5yif-mwcpw")
model = Project.version(1).model

result = model.predict(imgpath,confidence=40, overlap=30).json()

predictions=result["predictions"] 

Unique_classes =set(pred['class'] for pred in predictions)

print("unique classes: ",Unique_classes)

for cls in Unique_classes:
    print(f"-{cls} " )

xyxy =[]
confidences = []
labels=[]
class_id=[]

"""for pred in predictions:
    x1 = int(pred["x"]-pred["width"]/2)
    y1 = int(pred["y"]-pred["height"]/2)
    x2 = int(pred["x"]+pred["width"]/2)
    y2 = int(pred["y"]+pred["height"]/2)
    xyxy.append([x1,y1,x2,y2])
    confidences.append(pred["confidence"])
    class_ids.append(pred('class_ids',0))
    labels.append(pred['class'])"""


for pred in predictions:
    x1 = int(pred["x"] - pred["width"] / 2)
    y1 = int(pred["y"] - pred["height"] / 2)
    x2 = int(pred["x"] + pred["width"] / 2)
    y2 = int(pred["y"] + pred["height"] / 2)
    
    xyxy.append([x1, y1, x2, y2])
    confidences.append(pred["confidence"])
    class_id.append(pred.get("class_id", 0))  # FIXED
    labels.append(pred["class"])


detections = sv.Detections(
    xyxy=np.array(xyxy),
    confidence=np.array(confidences),
    class_id=np.array(class_id),
    )

img = cv2.imread(imgpath)
image_rgb = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)

box_annotator = sv.BoxAnnotator()
label_annotator = sv.LabelAnnotator(text_position= Position.BOTTOM_LEFT)
annotated_image = box_annotator.annotate(scene=image_rgb.copy(),detections=detections)
annotated_image = label_annotator.annotate(scene=annotated_image,detections=detections,labels=labels)


plt.figure(figsize=(10,10))
plt.imshow(annotated_image)
plt.axis("off")
plt.title("Annotated Image")
plt.show()

cv2.imwrite("output.jpg",cv2.cvtColor(annotated_image,cv2.COLOR_RGB2BGR))
print("output.jpg")


