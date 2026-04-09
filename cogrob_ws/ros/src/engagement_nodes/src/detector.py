import tensorflow as tf
assert(int(tf.__version__.split('.')[0]) >= 2)
import numpy as np

class Detector():
    def __init__(self,model_path):
        self.detect_fn = tf.saved_model.load(model_path)

    def __call__(self, img, threshold=0.5):
        img = img[:,:,::-1]
        input_tensor = tf.convert_to_tensor(img)
        input_tensor = input_tensor[tf.newaxis, ...]
        detections = self.detect_fn(input_tensor)
        num_above_thresh = np.sum( detections['detection_scores'] > threshold )
        print ("%d objects found" % num_above_thresh)
        detections.pop('num_detections')
        detections = {key: value[0, :num_above_thresh].numpy() for key, value in detections.items()}
        detections['detection_classes'] = detections['detection_classes'].astype(np.int64)
        return detections

if __name__ == "__main__":
    import os
    import numpy as np

    DET_PATH=os.path.join(os.path.dirname(__file__),'efficientdet_d1_coco17_tpu-32')
    test = np.zeros((256, 256, 3))
    det = Detector(DET_PATH)
    pred = det(test)
    print(pred)