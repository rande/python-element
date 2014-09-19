#
# Copyright 2014 Thomas Rabaix <thomas.rabaix@gmail.com>
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

import element.node
import os, hashlib, pickle

try:
    from PIL import Image, ImageOps
except ImportError:
    import Image
    import ImageOps

class StaticHandler(element.node.NodeHandler):
    def __init__(self, base_dir, templating, temp_dir):
        self.base_dir = base_dir
        self.templating = templating
        self.temp_dir = temp_dir

    def get_defaults(self, node):
        return {}

    def get_name(self):
        return 'Static'

    def execute(self, request_handler, context):
        if not context.mode or context.mode == 'raw':
            file = os.path.realpath(context.node.file)

            if file[:len(self.base_dir)] != self.base_dir:
                request_handler.set_status(404)

            if request_handler.get_argument('mf', None):
                self.image_fit(request_handler, context, file)

                return

            if request_handler.get_argument('mr', None):
                self.image_resize(request_handler, context, file)

                return

            request_handler.send_file(file)

        if context.mode == "preview":
            params = {
                'context': context
            }

            self.render(request_handler, self.templating, 'element.plugins.static:preview.html', params)

    def image_fit(self, request_handler, context, file):
        """
        Crop and resize an image to match the provided parameter
            200,200,0.5,0.5 => Width,Height,CropCenterX,CropCenterY

        """
        request_handler.send_file_header(file)

        keys = {'mf': request_handler.get_argument('mf'), 'file': file}

        path, filename = self.compute_paths(keys)
        if not os.path.exists("%s/%s" % (path, filename)):
            image = Image.open(file)

            # ImageOps compatible mode
            if image.mode not in ("L", "RGB"):
                image = image.convert("RGB")

            request_handler.send_file_header(file)

            w, h, cx, cy = request_handler.get_argument('mf').split(',')

            imagefit = ImageOps.fit(image, (int(w), int(h)), Image.ANTIALIAS, centering=(float(cx), float(cy)))
            self.make_temp_path(path)
            imagefit.save("%s/%s" % (path, filename), image.format, quality=95)

        request_handler.send_file("%s/%s" % (path, filename))

    def image_resize(self, request_handler, context, file):
        """
        Resize an image to match the provided width value, the height is computed automatically
        if the image's width is lower than the width, then no resize will be done.
        """
        request_handler.send_file_header(file)

        w = int(request_handler.get_argument('mr'))
        keys = {'mr': w, 'file': file}

        path, filename = self.compute_paths(keys)
        if not os.path.exists("%s/%s" % (path, filename)):
            image = Image.open(file)

            # ImageOps compatible mode
            if image.mode not in ("L", "RGB"):
                image = image.convert("RGB")

            format = image.format

            if image.size[0] > w:
                image = ImageOps.fit(image, (w, int(w * image.size[1] / image.size[0])), Image.ANTIALIAS)

            self.make_temp_path(path)
            image.save("%s/%s" % (path, filename), format, quality=95)

        request_handler.send_file("%s/%s" % (path, filename))

    def compute_paths(self, keys):
        hash = hashlib.md5(pickle.dumps(keys)).hexdigest()

        return "%s/%s/%s" % (self.temp_dir, hash[0:2], hash[2:4]), hash[4:]

    def make_temp_path(self, path):
        if not os.path.exists(path):
            os.makedirs(path)

        return path