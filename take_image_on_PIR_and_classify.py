# Parts of this code have the following license, since they are written
# by TensorFlow authors. Explicitly, load_graph, read_tensor_from_image_file, load_labels
# which I have taken from label_image.py
#
# Copyright 2017 The TensorFlow Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import argparse
import sys
import time
import picamera
import RPi.GPIO as GPIO

import numpy as np
import tensorflow as tf

def CheckPIR():
    # dependencies are RPi.GPIO and time
    # returns PIR_IS with either 0 or 1 depending if high or low
    time.sleep(1)
    #don't rush the PIR!
    GPIO.setmode(GPIO.BOARD)
    # set numbering system for GPIO PINs are BOARD
    GPIO.setup(7, GPIO.IN)
    # set up number 7 PIN for input from the PIR
    # need to adjust if you connected PIR to another GPIO PIN
    try:
        val = GPIO.input(7)
        if (val == True):
            PIR_IS = 1
            #PIR returned HIGH to GPIO PIN, so something here!
        if (val == False):
            PIR_IS = 0
            #PIR returned LOW to GPIO PIN, so something here!
            GPIO.cleanup()

    except:
        GPIO.cleanup()

    return PIR_IS


def load_graph(model_file):
  graph = tf.Graph()
  graph_def = tf.GraphDef()

  with open(model_file, "rb") as f:
    graph_def.ParseFromString(f.read())
  with graph.as_default():
    tf.import_graph_def(graph_def)

  return graph

def read_tensor_from_image_file(file_name, input_height=299, input_width=299,
				input_mean=0, input_std=255):
  input_name = "file_reader"
  output_name = "normalized"
  file_reader = tf.read_file(file_name, input_name)
  if file_name.endswith(".png"):
    image_reader = tf.image.decode_png(file_reader, channels = 3,
                                       name='png_reader')
  elif file_name.endswith(".gif"):
    image_reader = tf.squeeze(tf.image.decode_gif(file_reader,
                                                  name='gif_reader'))
  elif file_name.endswith(".bmp"):
    image_reader = tf.image.decode_bmp(file_reader, name='bmp_reader')
  else:
    image_reader = tf.image.decode_jpeg(file_reader, channels = 3,
                                        name='jpeg_reader')
  float_caster = tf.cast(image_reader, tf.float32)
  dims_expander = tf.expand_dims(float_caster, 0);
  resized = tf.image.resize_bilinear(dims_expander, [input_height, input_width])
  normalized = tf.divide(tf.subtract(resized, [input_mean]), [input_std])
  sess = tf.Session()
  result = sess.run(normalized)

  return result

def load_labels(label_file):
  label = []
  proto_as_ascii_lines = tf.gfile.GFile(label_file).readlines()
  for l in proto_as_ascii_lines:
    label.append(l.rstrip())
  return label

if __name__ == "__main__":
    
    #here we will check PIR first
    while True:
        PIR = CheckPIR()
        if PIR == 0:
            print("Nothing detected by PIR")
        elif PIR == 1:
            print("Something has been detected")
            camera = picamera.PiCamera()
            print("Capture an image")
            camera.start_preview()
            time.sleep(1)
            # ok capture image to image1.jpg
            camera.capture('image1.jpg')
            camera.stop_preview()
            time.sleep(1)
            break
    file_name = "image1.jpg"
    # set the image for classification to image1.jpg as we just captured from pi camera!
    model_file = "inception_v3_2016_08_28_frozen.pb"
    label_file = "labels_incep.txt"
    input_height = 299
    input_width = 299
    input_mean = 0
    input_std = 255
    input_layer = "input"
    output_layer = "InceptionV3/Predictions/Reshape_1"
    graph = load_graph(model_file)
    t = read_tensor_from_image_file(file_name,
                                  input_height=input_height,
                                  input_width=input_width,
                                  input_mean=input_mean,
                                  input_std=input_std)
    input_name = "import/" + input_layer
    output_name = "import/" + output_layer
    input_operation = graph.get_operation_by_name(input_name);
    output_operation = graph.get_operation_by_name(output_name);
    
    with tf.Session(graph=graph) as sess:
        results = sess.run(output_operation.outputs[0],{input_operation.outputs[0]: t})
        results = np.squeeze(results)
        
    top_k = results.argsort()[-5:][::-1]
    labels = load_labels(label_file)
    # we are just taking the top result and its label
    first = top_k[0]
    top_label = str(labels[first])
    top_result = str(results[first])
    print(top_label)
    print(top_result)
  
