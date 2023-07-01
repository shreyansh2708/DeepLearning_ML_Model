import cv2
import tensorflow as tf
import pathlib


def dent():
    model = 'E:\hack'
    session = tf.compat.v1.Session(graph=tf.Graph())
    tf.compat.v1.saved_model.loader.load(session, ['serve'], model)
    image = 'E:\hack\images'

    def draw_boxes(height, width, box, img):
        ymin = int(max(1, (box[0] * height)))
        xmin = int(max(1, (box[1] * width)))
        ymax = int(min(height, (box[2] * height)))
        xmax = int(min(width, (box[3] * width)))
        cv2.rectangle(img, (xmin, ymin), (xmax, ymax), (10, 255, 0), 10)

    for file in pathlib.Path(image).iterdir():
        curr = r"{}".format(file.resolve())
        bytes = open(curr, 'rb').read()
        result = session.run(['detection_boxes:0', 'detection_scores:0'], feed_dict={
                             'encoded_image_string_tensor:0': [bytes]})
        boxes = result[0][0]
        scores = result[1][0]
        print("File {} has result {}".format(*file.stem))
        img = cv2.imread(curr)
        imH, imW, _ = img.shape

        for i in range(len(scores)):
            if scores[i] > 0.50:
                print("The box {} has probability {}".format(
                    boxes[i], scores[i]))
                draw_boxes(imH, imW, boxes[i], img)

        new_img = cv2.resize(img, (1080, 1920))
        cv2.imshow("image", new_img)
        cv2.waitKey(0)
        return new_img
