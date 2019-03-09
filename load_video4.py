# -*- coding: utf-8 -*-
# file: to_video.py
# author: JinTian
# time: 16/03/2018 2:24 PM
# Copyright 2018 JinTian. All Rights Reserved.
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
# ------------------------------------------------------------------------
import os
import cv2

import numpy as np
import sys


class VideoCombiner(object):
    def __init__(self, img_dir):
        self.img_dir = img_dir
        self._get_video_shape()

    def _get_video_shape(self):
        self.all_images = [os.path.join(self.img_dir, i) for i in os.listdir(self.img_dir)]
        sample_img = np.random.choice(self.all_images)
        img = cv2.imread(sample_img)
        self.video_shape = img.shape


    def combine(self, target_file='combined.mp4'):
        size = (self.video_shape[1], self.video_shape[0])
        video_writer = cv2.VideoWriter(target_file, cv2.VideoWriter_fourcc(*'DIVX'), 24, size)
        i = 0
        print('=> Solving, be patient.')
        for img in self.all_images:
            i += 1
            # print('=> Solving: ', i)
            video_writer.write(img)
        video_writer.release()
        print('Done!')



