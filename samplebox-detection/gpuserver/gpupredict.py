#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
import os
import sys
import tensorflow as tf
from time import time
import cv2
from standard_color import STANDARD_COLOR

import save_predictions
from lxml import etree, objectify

def parse_label_files(file_path):
    f = open(file_path)
    lines = f.read().splitlines()
    lines = [l.strip() for l in lines]
    f.close()
    try:
        lines.remove("")
    except ValueError:
        pass

    ids = []
    classes = []

    for line in lines:
        if ":" in line:
            current_line_split = line.split(" ")
            try:
                current_line_split.remove("")
            except ValueError:
                pass

            if "id:" in current_line_split:
                ids.append(current_line_split[1])
            if "name:" in current_line_split:
                classes.append(current_line_split[1].strip("'"))

    result = {}
    for i in range(len(ids)):
        result[i + 1] = {"id": ids[i], "name": classes[i]}

    return result, classes

def bbox_result(img_width, img_height, boxes, classes, scores, category_index, use_normalized_coordinates=False, max_boxes_to_draw=20, min_score_thresh=.7, agnostic_mode = False):

    import collections
    box_to_display_str_map = collections.defaultdict(list)
    if not max_boxes_to_draw:
        max_boxes_to_draw = boxes.shape[0]
            
    for i in range(min(max_boxes_to_draw, boxes.shape[0])):
        if scores is None or scores[i] > min_score_thresh:
            box = tuple(boxes[i].tolist())
            if scores is None:
                return None
            else:
                if not agnostic_mode:
                    if classes[i] in category_index.keys():
                        class_name = category_index[classes[i]]['name']
                    else:
                        class_name = 'N/A'
                    display_str = '{}: {}%'.format(
                        class_name,
                        int(100*scores[i]))
                else:
                    display_str = 'score: {}%'.format(int(100 * scores[i]))
                box_to_display_str_map[box].append(display_str)

                results = []
    for _key, _val in box_to_display_str_map.items():
        y_min, x_min, y_max, x_max = _key

        name_confidence = _val[0]
        name_confidence_split = name_confidence.split(":")
        class_name = name_confidence_split[0]
        confidence = int(name_confidence_split[1][:-1])
        if use_normalized_coordinates:
            (x_min, x_max, y_min, y_max) = (x_min * img_width, x_max * img_width,
                                            y_min * img_height, y_max * img_height)

        results.append({'className':class_name, 'confidence':confidence, 'xMin':x_min, 'yMin':y_min, 'xMax':x_max, 'yMax':y_max})

    return results

def box_inside_box(box1, box2):
    '''
    Check if box2 is in box1
    '''
    if (box1['xMin'] < box2['xMin']  and box1['xMax'] > box2['xMax']
        and box1['yMin'] < box2['yMin'] and box1['yMax'] > box2['yMax']):
        return True

    return False

def bb_intersection_over_union(box1, box2):
    xA = max(box1['xMax'], box2['xMax'])
    yA = max(box1['yMax'], box2['yMax'])
    xB = min(box1['xMin'], box2['xMin'])
    yB = min(box1['yMin'], box2['yMin'])

    interArea = (xB - xA + 1) * (yB - yA + 1)

    box1Area = (box1['xMax'] - box1['xMin'] + 1) * (box1['yMax'] - box1['yMin'] + 1)
    box2Area = (box2['xMax'] - box2['xMin'] + 1) * (box2['yMax'] - box2['yMin'] + 1)

    iou = interArea / float(box1Area + box2Area - interArea)

    return iou

def post_processing_iou(pre_results):
    remove_boxes = []
    final_boxes = []
    current_len = len(pre_results)
    IOU_THRESH = 0.9

    for i in range(current_len):
        if pre_results[i] not in remove_boxes:
            for j in range(i + 1, current_len - 1):
                if pre_results[j] not in remove_boxes:
                    if box_inside_box(pre_results[i], pre_results[j]):
                        remove_boxes.append(pre_results[j])
                    elif box_inside_box(pre_results[j], pre_results[i]):
                        remove_boxes.append(pre_results[i])
                        break
                    else:
                        if (bb_intersection_over_union(pre_results[i], pre_results[j]) > IOU_THRESH):
                            if (pre_results[i]['confidence'] <= pre_results[j]['confidence']):
                                remove_boxes.append(pre_results[i])
                                break
                            else:
                                remove_boxes.append(pre_results[j])

    final_boxes = [box for box in pre_results if box not in remove_boxes]

    return final_boxes

#########################################################################
# load model
MODELS_PATH = os.path.dirname(os.path.realpath(__file__)) + "/../models/"
PATH_TO_CKPT = MODELS_PATH + '/frozen_inference_graph.pb'
PATH_TO_LABELS = MODELS_PATH + '/sweets_label.pbtxt'
category_index = parse_label_files(PATH_TO_LABELS)

detection_graph = tf.Graph()
with detection_graph.as_default():
    od_graph_def = tf.GraphDef()
    with tf.gfile.GFile(PATH_TO_CKPT, 'rb') as fid:
        serialized_graph = fid.read()
        od_graph_def.ParseFromString(serialized_graph)
        tf.import_graph_def(od_graph_def, name='')
#########################################################################
def process_image(image_path):
    '''
    flask called function
    '''

    global category_index
    global detection_graph
    final_result = None

    print ('gpupredict called')
    
    with detection_graph.as_default():
        with tf.Session(graph=detection_graph) as sess:
            image_tensor = detection_graph.get_tensor_by_name('image_tensor:0')
            detection_boxes = detection_graph.get_tensor_by_name('detection_boxes:0')
            detection_scores = detection_graph.get_tensor_by_name('detection_scores:0')
            detection_classes = detection_graph.get_tensor_by_name('detection_classes:0')
            num_detections = detection_graph.get_tensor_by_name('num_detections:0')
        

            image_np = cv2.imread(image_path)
            image_np_expanded = np.expand_dims(image_np, axis=0)

            _start = time()
      
            # Actual detection.
            (boxes, scores, classes, num) = sess.run(
                [detection_boxes, detection_scores, detection_classes, num_detections],
                feed_dict={image_tensor: image_np_expanded})

            print (str((time() - _start)) + " [sec]")
      
            img_height, img_width = image_np.shape[:2]

            final_result = bbox_result(img_width, img_height, np.squeeze(boxes), np.squeeze(classes).astype(np.int32), np.squeeze(scores), category_index[0], use_normalized_coordinates=True)
            final_result = post_processing_iou(final_result)

            file_name_without_path = image_path.split("/")[-1]
            file_name = file_name_without_path.split(".")[0]
            annotation = save_predictions.root("folder", file_name_without_path, img_width, img_height)
            
            for result in final_result:
                class_name = result['className']
                color_index = category_index[1].index(class_name) % len(STANDARD_COLOR.values())
                _color = STANDARD_COLOR.values()[color_index]
                confidence = result['confidence']
                x_min = int(result['xMin'])
                y_min = int(result['yMin'])
                x_max = int(result['xMax'])
                y_max = int(result['yMax'])
                print (result)
                _text = class_name + "_" + str(confidence)

                cv2.rectangle(image_np, (x_min, y_min), (x_max, y_max), (0,0,255), 8)
                cv2.putText(image_np, _text, (x_min, y_min), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2)
                temp_label = save_predictions.instance_to_xml(class_name, x_min, y_min, x_max, y_max)
                annotation.append(temp_label)

            # debug: if need debug image uncomment below line
            # cv2.imshow("temp", image_np)
            # cv2.waitKey(0)

    return final_result

if __name__ == '__main__':
    TEST_IMAGE_PATHS = os.path.dirname(os.path.realpath(__file__)) + "/../images/"+ "/temp.jpg"

    temp = process_image(TEST_IMAGE_PATHS)
