import numpy as np
import pickle
import cv2, joblib
from sklearn.preprocessing import LabelBinarizer
from keras.preprocessing.image import img_to_array
from os import listdir
from matplotlib import pyplot as plt
from keras.models import load_model

IMG_DIR = "F:/Official purpose/Sprint - 30/Jute bag/WhatsApp Image 2022-01-26 at 11.03.20 PM(7).jpeg"
DIRECTORY_ROOT = 'F:/Official purpose/Sprint - 30/Jute bag/JuteBag'
MODEL_FILE = 'F:/Official purpose/Sprint - 30/Jute bag/jute-bag_model_inception.h5'
LABEL_FILE = 'F:/Official purpose/Sprint - 30/Jute bag/jute-bag_model_inception_label.pkl'
EPOCHS = 100
INIT_LR = 1e-3
BS = 32
DEFAULT_IMAGE_SIZE = tuple((299, 299))
IMAGE_SIZE = 0
WIDTH = 299
HEIGHT = 299
DEPTH = 3


# image resizing
def convert_image_to_array_for_cv2_resizing(img_dir):
    try:
        cv2_image = cv2.imread(img_dir)
        if cv2_image is not None:
            resized_image = cv2.resize(cv2_image, DEFAULT_IMAGE_SIZE)
            return img_to_array(resized_image)
        else:
            return np.array([])
    except Exception as e:
        print(f"Error : {e}")
        return None


listdir(DIRECTORY_ROOT)
image_list, label_list = [], []

try:
    print("[INFO] Loading images ...")
    root_dir = listdir(DIRECTORY_ROOT)

    for directory in root_dir:
        # remove .DS_Store from list
        if directory == ".DS_Store":
            root_dir.remove(directory)

    for plant_folder in root_dir:
        plant_disease_folder_list = listdir(f"{DIRECTORY_ROOT}/{plant_folder}")

        for disease_folder in plant_disease_folder_list:
            # remove .DS_Store from list
            if disease_folder == ".DS_Store":
                plant_disease_folder_list.remove(disease_folder)

        for plant_disease_folder in plant_disease_folder_list:
            print(f"[INFO] Processing {plant_disease_folder} ...")
            plant_disease_image_list = listdir(f"{DIRECTORY_ROOT}/{plant_folder}/{plant_disease_folder}/")

            for single_plant_disease_image in plant_disease_image_list:
                if single_plant_disease_image == ".DS_Store":
                    plant_disease_image_list.remove(single_plant_disease_image)

            for labelled_image in plant_disease_image_list:
                labelled_image_image_directory = f"{DIRECTORY_ROOT}/{plant_folder}/{plant_disease_folder}/{labelled_image}"
                if labelled_image_image_directory.endswith(".jpg") == True or labelled_image_image_directory.endswith(".JPG") == True or labelled_image_image_directory.endswith(".jpeg") == True:
                    image_list.append(convert_image_to_array_for_cv2_resizing(labelled_image_image_directory))
                    label_list.append(plant_disease_folder)

    print("[INFO] Image loading completed")

except Exception as e:
    print(f"Error : {e}")

# image labelling
label_binarizer = LabelBinarizer()
image_labels = label_binarizer.fit_transform(label_list)
pickle.dump(label_binarizer, open(LABEL_FILE, 'wb'))
n_classes = len(label_binarizer.classes_)
print(label_binarizer.classes_)

loaded_model = load_model(MODEL_FILE)
model_disease = loaded_model

# image prediction testing - start
img_read_plt = plt.imread(IMG_DIR)
img_read_plt_arr = convert_image_to_array_for_cv2_resizing(IMG_DIR)
imgReadPltArrNp = np.array(img_read_plt_arr, dtype=np.float16) / 255.0
imgReadPltArrNpDimension = np.expand_dims(imgReadPltArrNp, axis=0)
imgReadPltResult = model_disease.predict(imgReadPltArrNpDimension)
print(imgReadPltResult)

imgReadPltResultIndex = np.where(imgReadPltResult == np.max(imgReadPltResult))
print("probability:" + str(np.max(imgReadPltResult)) + "\n" + label_binarizer.classes_[imgReadPltResultIndex[1][0]])

plt.imshow(img_read_plt)
plt.show()
# image prediction testing - end

# image testing with ROI
imgReadCv2 = cv2.imread(IMG_DIR)
imgReadCv2ToGray = cv2.cvtColor(imgReadCv2, cv2.COLOR_BGR2GRAY)
imgReadCv2 = cv2.rectangle(imgReadCv2, (200, 250), (400, 325), (0, 255, 0), 2)
cv2.putText(imgReadCv2, label_binarizer.classes_[imgReadPltResultIndex[1][0]], (300, 300), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2, cv2.LINE_AA)
cv2.imshow('Detected Image Response', imgReadCv2)
cv2.waitKey(0)
cv2.destroyAllWindows()



