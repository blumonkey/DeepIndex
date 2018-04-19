import tensorflow as tf
import numpy as np

def initialize():
    sess=tf.Session(config=tf.ConfigProto(allow_soft_placement=True))  
    #First let's load meta graph and restore weights

    saver = tf.train.import_meta_graph('checkpoint/model.ckpt.meta')
    saver.restore(sess,'checkpoint/model.ckpt')
    ops = tf.get_default_graph().get_operations()
    all_tensor_names = {output.name for op in ops for output in op.outputs}
    tensor_dict = {}
    for key in ['num_detections', 'detection_boxes', 'detection_scores','detection_classes']:
        tensor_name = key + ':0'
        if tensor_name in all_tensor_names:
            tensor_dict[key] = tf.get_default_graph().get_tensor_by_name(tensor_name)

    image_tensor = tf.get_default_graph().get_tensor_by_name('image_tensor:0')
    return sess, tensor_dict,image_tensor

"""
image - image file 
#image_tensor - obtained from intialize()
#score - threshold score for detection
"""
def findIndex(image,score, sess, tensor_dict,image_tensor):
    (n,h,w,c) = image.shape
    
    pred_Y = [] 
    pred_B = [] 
    output_dict = sess.run(tensor_dict,feed_dict={image_tensor: image})
    num_detections = output_dict['num_detections']
    detection_boxes = output_dict['detection_boxes']
    detection_classes = output_dict['detection_classes']
    detection_scores = output_dict['detection_scores']
    #print(num_detections)
    #print(detection_boxes)
    #print(detection_classes)
    #print(detection_scores)
    for i in range(int(num_detections[0])):
        if(detection_scores[0][i]>score):
            
            pred_Y.append(detection_classes[0][i])
            bbox = detection_boxes[0][i]
            bbox[0] = bbox[0]*h
            bbox[1] = bbox[1]*w
            bbox[2] = bbox[2]*h
            bbox[3] = bbox[3]*w
            bbox[2] = bbox[2]-bbox[0]
            bbox[3] = bbox[3]-bbox[1]
            
            pred_B.append(bbox)    

    pred_Y = np.array(pred_Y).astype(np.uint8)
    pred_B = np.array(pred_B)
    return pred_Y, pred_B        
    

