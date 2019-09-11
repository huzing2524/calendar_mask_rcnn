"""
Usage: import the module (see Jupyter notebooks for examples), or run from
       the command line as such:

    train your own dataset with pre-trained weights mask_rcnn_coco.h5
    !CUDA_VISIBLE_DEVICES=0 python3 topview_training.py train --dataset=/content/drive/foxconn-aoi/test/dataset --weights=/content/drive/foxconn-aoi/test/mask_rcnn_coco.h5

    predict one image
    python3 test/topview_training.py inference --weights=/home/dsd/Desktop/foxconn-aoi/test/mask_rcnn_foxconn_0030.h5 --image=/home/dsd/Desktop/foxconn-aoi/test/dataset/01_topview_zom.png

    predict directory for many images
    !CUDA_VISIBLE_DEVICES=0 python3 /content/drive/foxconn/test/topview_training.py inference --weights=/content/drive/foxconn/test/mask_rcnn_foxconn_0030.h5 --path=/content/drive/foxconn/test/dataset/slice
"""
import os
import sys
import time
import numpy as np
import imgaug  # https://github.com/aleju/imgaug (pip3 install imgaug)
import json
import skimage

# Root directory of the project
ROOT_DIR = os.path.abspath("../")

# Import Mask RCNN
sys.path.append(ROOT_DIR)  # To find local version of the library
from mrcnn.config import Config
from mrcnn import model as modellib, utils
from mrcnn import visualize

# Path to trained weights file
COCO_WEIGHTS_PATH = os.path.join(ROOT_DIR, "mask_rcnn_coco.h5")

# Directory to save logs and model checkpoints, if not provided
# through the command line argument --logs
DEFAULT_LOGS_DIR = os.path.join(ROOT_DIR, "logs")

class_names = ['BG', "date_1", "date_2", "date_3", "date_4", "date_5", "date_6", "date_7", "date_8", "date_9",
               "date_10", "date_11", "date_12", "date_13", "date_14", "date_15", "date_16", "date_17", "date_18",
               "date_19", "date_20", "date_21", "date_22", "date_23", "date_24", "date_25", "date_26", "date_27",
               "date_28", "date_29", "date_30", "date_31"]  # inference


class CalendarConfig(Config):
    """Configuration for training on MS COCO.
    Derives from the base Config class and overrides values specific
    to the COCO dataset.
    """
    # Give the configuration a recognizable name
    NAME = "calendar"

    # We use a GPU with 12GB memory, which can fit two images.
    # Adjust down if you use a smaller GPU.
    IMAGES_PER_GPU = 1

    # Uncomment to train on 8 GPUs (default is 1)
    # GPU_COUNT = 8

    # Number of classes (including background)
    NUM_CLASSES = 1 + 31

    STEPS_PER_EPOCH = 100


class CalendarDataset(utils.Dataset):
    def load_pins(self, dataset_dir, subset):
        """Load a subset of the pins dataset.
        dataset_dir: Root directory of the dataset.
        subset: Subset to load: train or val
        """
        # Add classes.
        self.add_class("date", 1, "date_1")
        self.add_class("date", 2, "date_2")
        self.add_class("date", 3, "date_3")
        self.add_class("date", 4, "date_4")
        self.add_class("date", 5, "date_5")
        self.add_class("date", 6, "date_6")
        self.add_class("date", 7, "date_7")
        self.add_class("date", 8, "date_8")
        self.add_class("date", 9, "date_9")
        self.add_class("date", 10, "date_10")
        self.add_class("date", 11, "date_11")
        self.add_class("date", 12, "date_12")
        self.add_class("date", 13, "date_13")
        self.add_class("date", 14, "date_14")
        self.add_class("date", 15, "date_15")
        self.add_class("date", 16, "date_16")
        self.add_class("date", 17, "date_17")
        self.add_class("date", 18, "date_18")
        self.add_class("date", 19, "date_19")
        self.add_class("date", 20, "date_20")
        self.add_class("date", 21, "date_21")
        self.add_class("date", 22, "date_22")
        self.add_class("date", 23, "date_23")
        self.add_class("date", 24, "date_24")
        self.add_class("date", 25, "date_25")
        self.add_class("date", 26, "date_26")
        self.add_class("date", 27, "date_27")
        self.add_class("date", 28, "date_28")
        self.add_class("date", 29, "date_29")
        self.add_class("date", 30, "date_30")
        self.add_class("date", 31, "date_31")

        # Train or validation dataset?
        # assert subset in ["train", "val"]
        # dataset_dir = os.path.join(dataset_dir, subset)

        """Load annotations
        VGG Image Annotator saves each image in the form:
        { 'filename': '28503151_5b5b7ec140_b.jpg',
          'regions': {
              '0': {
                  'region_attributes': {},
                  'shape_attributes': {
                      'all_points_x': [...],
                      'all_points_y': [...],
                      'name': 'polygon'}},
              ... more regions ...
          },
          'size': 100202
        }"""

        # We mostly care about the x and y coordinates of each region
        annotations = json.load(open('/content/drive/calendar_mask_rcnn/dataset/train/calendar.json'))
        annotations = list(annotations.values())  # don't need the dict keys

        # The VIA tool saves images in the JSON even if they don't have any
        # annotations. Skip unannotated images.
        annotations = [a for a in annotations if a['regions']]

        # Add images
        for a in annotations:
            # Get the x, y coordinaets of points of the rects that make up
            # the outline of each object instance. There are stores in the
            # shape_attributes (see json format above)
            rects = [r['shape_attributes'] for r in a['regions']]
            class_id = [r['region_attributes']['type'] for r in a['regions']]
            # name_dict = {"area_3": 3, "area_4": 4, "area_5": 5, "area_7": 7}
            # name_id = [name_dict[a] for a in name]

            # load_mask() needs the image size to convert rects to masks.
            # Unfortunately, VIA doesn't include it in JSON, so we must read
            # the image. This is only managable since the dataset is tiny.
            image_path = os.path.join(dataset_dir, a['filename'])
            image = skimage.io.imread(image_path)
            height, width = image.shape[:2]

            self.add_image(
                "date",
                image_id=a['filename'],  # use file name as a unique image id
                path=image_path,
                class_id=class_id,
                width=width, height=height,
                polygons=rects)

    def load_mask(self, image_id):
        """Generate instance masks for an image.
       Returns:
        masks: A bool array of shape [height, width, instance count] with
            one mask per instance.
        class_ids: a 1D array of class IDs of the instance masks.
        """
        # Convert polygons to a bitmap mask of shape [height, width, instance_count]
        info = self.image_info[image_id]
        class_id = info["class_id"]
        mask = np.zeros([info["height"], info["width"], len(info["polygons"])], dtype=np.uint8)

        for i, p in enumerate(info["polygons"]):
            # Get indexes of pixels inside the polygon and set them to 1
            if p["name"] == "polygon" or p["name"] == "polyline":
                rr, cc = skimage.draw.polygon(p['all_points_y'], p['all_points_x'])
                mask[rr, cc, i] = 1
            elif p["name"] == "circle":
                rr, cc = skimage.draw.circle(p["cy"], p["cx"], p["r"])
                mask[rr, cc, i] = 1

        # Return mask, and array of class IDs of each instance.
        return mask.astype(np.bool), np.array([self.class_names.index(i) for i in class_id], dtype=np.int32)

    def image_reference(self, image_id):
        """Return the path of the image."""
        info = self.image_info[image_id]
        if info["source"] == "date":
            return info["path"]
        else:
            super(self.__class__, self).image_reference(image_id)


def train(model):
    """Train the model."""
    # Training dataset.
    dataset_train = CalendarDataset()
    dataset_train.load_pins(args.dataset, "train")
    dataset_train.prepare()

    # Validation dataset
    dataset_val = CalendarDataset()
    dataset_val.load_pins(args.dataset, "val")
    dataset_val.prepare()

    # Image Augmentation
    # Right/Left flip 50% of the time
    # augmentation = imgaug.augmenters.Fliplr(0.5)

    # *** This training schedule is an example. Update to your needs ***
    # Since we're using a very small dataset, and starting from
    # COCO trained weights, we don't need to train too long. Also,
    # no need to train all layers, just the heads should do it.
    print("Training network heads")
    model.train(dataset_train, dataset_val,
                learning_rate=config.LEARNING_RATE,
                epochs=30,
                layers='heads')


def inference(model, image_path=None, dir_path=None):
    """inference a image or a directory path and return the predict result"""
    assert image_path or dir_path
    if image_path:
        if os.path.isfile(image_path):
            # Run model detection and generate the color splash effect
            print("Running on image {}".format(image_path))
            # Read image
            '''sample.png 是4维数组 shape (318, 606, 4)...
            矩阵形状不匹配，报错 ValueError: operands could not be broadcast together with shapes (1024,1024,4) (3,)
            '''
            image = skimage.io.imread(image_path)
            if image.shape[2] == 4:
                print('rgba2rgb...')
                image = skimage.color.rgba2rgb(image)

            # Detect objects
            # r = model.detect([image], verbose=1)[0]
            start_time = int(round(time.time() * 1000))
            r = model.detect([image], verbose=1)[0]
            end_time = int(round(time.time() * 1000))
            print("Detection time: {}ms".format(end_time - start_time))
            print("rois: ", r["rois"])
            print("class_ids: ", r["class_ids"])
            visualize.display_instances(image, r['rois'], r['masks'], r['class_ids'], class_names, r['scores'],
                                        image_path=image_path)
            e_time = int(round(time.time() * 1000))
            print("Total process time: {}ms".format(e_time - s_time))
        else:
            print("--image need a image with file path")
    elif dir_path:
        if os.path.isdir(dir_path):
            print("Running on directory {}".format(dir_path))
            images_list = sorted(os.listdir(dir_path))
            for image in images_list:
                print('image', image)
                img_path = os.path.join(dir_path, image)
                if os.path.isfile(img_path) and image.split(".")[-1] in ['jpg', 'jpeg', 'png', 'bmp']:
                    image = skimage.io.imread(img_path)
                    start_time = int(round(time.time() * 1000))
                    r = model.detect([image], verbose=1)[0]
                    end_time = int(round(time.time() * 1000))
                    print("Detection time: {}ms".format(end_time - start_time))
                    print("rois: ", r["rois"])
                    visualize.display_instances(image, r['rois'], r['masks'], r['class_ids'], class_names, r['scores'],
                                                image_path=img_path)
            e_time = int(round(time.time() * 1000))
            print("Total process time: {}ms".format(e_time - s_time))
        else:
            print("--path need a directory path")


if __name__ == '__main__':
    s_time = int(round(time.time() * 1000))
    import argparse

    # Parse command line arguments
    parser = argparse.ArgumentParser(
        description='Train Mask R-CNN to detect images.')
    parser.add_argument("command",
                        metavar="train or inference",
                        help="train or inference")
    parser.add_argument('--dataset', required=False,
                        metavar="/path/to/balloon/dataset/",
                        help='Directory of the Balloon dataset')
    parser.add_argument('--weights', required=True,
                        metavar="/path/to/weights.h5",
                        help="Path to weights .h5 file or 'coco'")
    parser.add_argument('--logs', required=False,
                        default=DEFAULT_LOGS_DIR,
                        metavar="/path/to/logs/",
                        help='Logs and checkpoints directory (default=logs/)')
    parser.add_argument('--image', required=False,
                        metavar="path to image",
                        help='Image path to predict')
    parser.add_argument('--path', required=False,
                        metavar='path to dir',
                        help='A directory path with many images to predict')
    args = parser.parse_args()

    # Validate arguments
    if args.command == "train":
        assert args.dataset, "Argument --dataset is required for training"

        config = CalendarConfig()
        model = modellib.MaskRCNN(mode="training", config=config, model_dir=args.logs)

    elif args.command == "inference":
        assert args.image or args.path, "Provide --image or --path"

        config = CalendarConfig()
        model = modellib.MaskRCNN(mode="inference", config=config, model_dir=args.logs)

    else:
        raise Exception("'{}' is not recognized. Use 'train' or 'inference'".format(args.command))

    # config.display()

    # Select weights file to load
    if args.weights.lower() == "coco":
        weights_path = COCO_WEIGHTS_PATH
        # Download weights file
        if not os.path.exists(weights_path):
            utils.download_trained_weights(weights_path)
    elif args.weights.lower() == "last":
        # Find last trained weights
        weights_path = model.find_last()
    elif args.weights.lower() == "imagenet":
        # Start from ImageNet trained weights
        weights_path = model.get_imagenet_weights()
    else:
        weights_path = args.weights

    # Load weights
    print("Loading weights ", weights_path)
    if args.weights.lower() == "coco":
        # Exclude the last layers because they require a matching
        # number of classes
        model.load_weights(weights_path, by_name=True, exclude=[
            "mrcnn_class_logits", "mrcnn_bbox_fc",
            "mrcnn_bbox", "mrcnn_mask"])
    else:
        l_time = int(round(time.time() * 1000))
        # This condition below is important!
        if args.command == "train":
            model.load_weights(weights_path, by_name=True, exclude=[
                "mrcnn_class_logits", "mrcnn_bbox_fc",
                "mrcnn_bbox", "mrcnn_mask"])
        elif args.command == "inference":
            model.load_weights(weights_path, by_name=True)

        l_time_ = int(round(time.time() * 1000))
        print("Loading weights: {}ms".format(l_time_ - l_time))

    # Train or evaluate
    if args.command == "train":
        train(model)
    elif args.command == "inference":
        inference(model, image_path=args.image, dir_path=args.path)
