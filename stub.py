import numpy as np
import time 
import tensorflow as tf
from skimage.draw import polygon
import object_detection
from PIL import Image

def load_image_into_numpy_array(image):
  (im_width, im_height) = image.size
  return np.array(image.getdata()).reshape(
      (im_height, im_width, 3)).astype(np.uint8)

image = Image.open("image4.jpg")
image_np = load_image_into_numpy_array(image)
image_np_expanded = np.expand_dims(image_np, axis=0)
#image size to tensor should be (1, h, w , 3 )

start = 0
end = 1
iter_size =1

sess, tensor_dict,image_tensor = object_detection.initialize()
print(object_detection.findIndex(image_np_expanded, 0.5, sess, tensor_dict,image_tensor))
