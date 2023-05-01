import numpy as np
import pickle
import cv2
from sklearn.preprocessing import LabelBinarizer
from keras.preprocessing.image import img_to_array
from os import listdir
from matplotlib import pyplot as plt
from keras.models import load_model
leaf_cascade = cv2.CascadeClassifier('E:/Official purpose/Sprint - 5/haarcascade_botany.xml')
EPOCHS = 20
INIT_LR = 1e-3
BS = 32
default_image_size = tuple((224, 224))
image_size = 0
directory_root = 'E:/Official purpose/Sprint - 10/HealthyMango_vs_NonMango'
width = 224
height = 224
depth = 3


def convert_image_to_array(image_dir):
    try:
        image = cv2.imread(image_dir)
        if image is not None:
            image = cv2.resize(image, default_image_size)
            return img_to_array(image)
        else:
            return np.array([])
    except Exception as e:
        print(f"Error : {e}")
        return None


listdir(directory_root)
image_list, label_list = [], []
try:
    print("[INFO] Loading images ...")
    root_dir = listdir(directory_root)
    for directory in root_dir:
        # remove .DS_Store from list
        if directory == ".DS_Store":
            root_dir.remove(directory)

    for plant_folder in root_dir:
        plant_disease_folder_list = listdir(f"{directory_root}/{plant_folder}")

        for disease_folder in plant_disease_folder_list:
            # remove .DS_Store from list
            if disease_folder == ".DS_Store":
                plant_disease_folder_list.remove(disease_folder)

        for plant_disease_folder in plant_disease_folder_list:
            print(f"[INFO] Processing {plant_disease_folder} ...")
            plant_disease_image_list = listdir(f"{directory_root}/{plant_folder}/{plant_disease_folder}/")

            for single_plant_disease_image in plant_disease_image_list:
                if single_plant_disease_image == ".DS_Store":
                    plant_disease_image_list.remove(single_plant_disease_image)

            for image in plant_disease_image_list:
                image_directory = f"{directory_root}/{plant_folder}/{plant_disease_folder}/{image}"
                if image_directory.endswith(".jpg") == True or image_directory.endswith(".JPG") == True:
                    image_list.append(convert_image_to_array(image_directory))
                    label_list.append(plant_disease_folder)
    print("[INFO] Image loading completed")
except Exception as e:
    print(f"Error : {e}")
image_size = len(image_list)
print(image_size)
label_binarizer = LabelBinarizer()
image_labels = label_binarizer.fit_transform(label_list)
pickle.dump(label_binarizer, open('E:/Official purpose/Sprint - 10/Mango_NotMango_DetectionLabels.pkl', 'wb'))
n_classes = len(label_binarizer.classes_)
print(label_binarizer.classes_)
loaded_model = load_model('E:/Official purpose/Sprint - 10/Mango_NotMango_model_inception.h5')
model_disease = loaded_model
image_dir = "F:/Official purpose/Collections/IMG_20181010_161305.jpg"
img = plt.imread('F:/Official purpose/Collections/IMG_20181010_161305.jpg')
im = convert_image_to_array(image_dir)
np_image_li = np.array(im, dtype=np.float16) / 255.0
npp_image = np.expand_dims(np_image_li, axis=0)
result = model_disease.predict(npp_image)
print(result)
itemindex = np.where(result == np.max(result))
print("probability:" + str(np.max(result)) + "\n" + label_binarizer.classes_[itemindex[1][0]])
plt.imshow(img)
plt.show()
img = cv2.imread('F:/Official purpose/Collections/IMG_20181010_161305.jpg')
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
leaf = leaf_cascade.detectMultiScale(gray, 1.08, 2)
for (x, y, w, h) in leaf:
    img = cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
    cv2.putText(img, label_binarizer.classes_[itemindex[1][0]], (x + 20, y - 60), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2, cv2.LINE_AA)
cv2.imshow('img', img)
cv2.waitKey(0)
cv2.destroyAllWindows()
