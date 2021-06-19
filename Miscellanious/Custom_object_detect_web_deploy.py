import cv2
import numpy as np
from flask import Flask, request, Response, jsonify
import io
from PIL import Image
import os


def get_predection(image, net, Lables, COLORS):
    Width = image.shape[1]
    Height = image.shape[0]
    get_output_layers(net)
    blob = cv2.dnn.blobFromImage(image, scale, (416, 416), (0, 0, 0), True, crop=False)
    net.setInput(blob)
    outs = net.forward(get_output_layers(net))
    class_ids = []
    confidences = []
    boxes = []
    for out in outs:
        for detection in out:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]
            if confidence > 0.5:
                center_x = int(detection[0] * Width)
                center_y = int(detection[1] * Height)
                w = int(detection[2] * Width)
                h = int(detection[3] * Height)
                x = center_x - w / 2
                y = center_y - h / 2
                class_ids.append(class_id)
                confidences.append(float(confidence))
                boxes.append([x, y, w, h])
    indices = cv2.dnn.NMSBoxes(boxes, confidences, conf_threshold, nms_threshold)
    for i in indices:
        i = i[0]
        box = boxes[i]
        x = box[0]
        y = box[1]
        w = box[2]
        h = box[3]
        draw_prediction(image, class_ids[i], confidences[i], round(x), round(y), round(x + w), round(y + h))
    return image


def image_to_byte_array(image: Image):
  imgByteArr = io.BytesIO()
  image.save(imgByteArr, format='PNG')
  imgByteArr = imgByteArr.getvalue()
  return imgByteArr


def get_output_layers(net):
    layer_names = net.getLayerNames()
    output_layers = [layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]
    return output_layers


def draw_prediction(img, class_id, confidence, x, y, x_plus_w, y_plus_h):
    label = str(classes[class_id])
    color = COLORS[class_id]
    cv2.rectangle(img, (x, y), (x_plus_w, y_plus_h), color, 2)
    cv2.putText(img, label, (x - 10, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)


image = cv2.imread('F:/Photos/Friends & Family(Dhaka)/received_1816118352028837.jpeg')
scale = 0.00392
classes = 'D:/Pycharm/Program/AI_Stat_ANN/yolov3.txt'
weights = 'D:/Pycharm/Program/AI_Stat_ANN/yolov3.weights'
config = 'D:/Pycharm/Program/AI_Stat_ANN/yolov3.cfg'
Lables = os.path.sep.join([classes])
CFG = os.path.sep.join([config])
Weights = os.path.sep.join([weights])
with open(classes, 'r') as f:
    classes = [line.strip() for line in f.readlines()]
COLORS = np.random.uniform(0, 255, size=(len(Lables), 3))
net = cv2.dnn.readNet(CFG, Weights)
conf_threshold = 0.5
nms_threshold = 0.4
app = Flask(__name__)
# route http posts to this method
@app.route('/api/test', methods=['POST'])
def main():
    # load our input image and grab its spatial dimensions
    #image = cv2.imread("./test1.jpg")
    img = request.files["image"].read()
    img = Image.open(io.BytesIO(img))
    npimg = np.array(img)
    image = npimg.copy()
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    res = get_predection(image, net, Lables, COLORS)
    # image=cv2.cvtColor(image,cv2.COLOR_BGR2RGB)
    # show the output image
    #cv2.imshow("Image", res)
    #cv2.waitKey()
    image = cv2.cvtColor(res, cv2.COLOR_BGR2RGB)
    np_img = Image.fromarray(image)
    img_encoded = image_to_byte_array(np_img)
    return Response(response=img_encoded, status=200, mimetype="image/jpeg")
    # start flask app


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
