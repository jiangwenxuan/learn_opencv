import cv2

model = cv2.ml.ANN_MLP_create()
model.setActivationFunction(cv2.ml.ANN_MLP_SIGMOID_SYM)
model.setLayerSizes(np.int32([38400, 32, 4]))
