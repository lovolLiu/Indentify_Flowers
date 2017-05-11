# -*- coding:utf-8 -*-
import os
import tensorflow as tf
from slim.nets import inception_v4
from slim.preprocessing import inception_preprocessing
from flower_manager import FlowerManager

flower_manager = FlowerManager()


def upload(dir_path, uploaded_file):
    try:
        filename = uploaded_file.filename
        path = dir_path + "/" + filename
        uploaded_file.save(path)
        checkpoints_dir = '/private/tmp/checkpoint'

        slim = tf.contrib.slim

        # We need default size of image for a particular network.
        # The network was trained on images of that size -- so we
        # resize input image later in the code.
        image_size = inception_v4.inception_v4.default_image_size

        with tf.Graph().as_default():

            image_string = open(path).read()

            # Decode string into matrix with intensity values
            image = tf.image.decode_jpeg(image_string, channels=3)

            # Resize the input image, preserving the aspect ratio
            # and make a central crop of the resulted image.
            # The crop will be of the size of the default image size of
            # the network.
            processed_image = inception_preprocessing.preprocess_image(image,
                                                                       image_size,
                                                                       image_size,
                                                                       is_training=False)

            # Networks accept images in batches.
            # The first dimension usually represents the batch size.
            # In our case the batch size is one.
            processed_images = tf.expand_dims(processed_image, 0)

            # Create the model, use the default arg scope to configure
            # the batch norm parameters. arg_scope is a very conveniet
            # feature of slim library -- you can define default
            # parameters for layers -- like stride, padding etc.
            with slim.arg_scope(inception_v4.inception_v4_arg_scope()):
                logits, _ = inception_v4.inception_v4(processed_images,
                                                      num_classes=5,
                                                      is_training=False)

            # In order to get probabilities we apply softmax on the output.
            probabilities = tf.nn.softmax(logits)

            # Create a function that reads the network weights
            # from the checkpoint file that you downloaded.
            # We will run it in session later.
            init_fn = slim.assign_from_checkpoint_fn(
                os.path.join(checkpoints_dir, 'model.ckpt-500'),
                slim.get_model_variables('InceptionV4'))
            with tf.Session() as sess:
                # Load weights
                init_fn(sess)

                # We want to get predictions, image as numpy matrix
                # and resized and cropped piece that is actually
                # being fed to the network.
                np_image, network_input, probabilities = sess.run([image,
                                                                   processed_image,
                                                                   probabilities])
                probabilities = probabilities[0, 0:]
                sorted_inds = [i[0] for i in sorted(enumerate(-probabilities),
                                                    key=lambda x: x[1])]

            names = {0: u'雏菊', 1: u'蒲公英', 2: u'玫瑰', 3: u'向日葵', 4: u'郁金香'}
            result = {}
            flower_names = []
            flower_probabilities = []
            for i in range(5):
                index = sorted_inds[i]
                # Now we print the top-5 predictions that the network gives us with
                # corresponding probabilities. Pay attention that the index with
                # class names is shifted by 1 -- this is because some networks
                # were trained on 1000 classes and others on 1001. VGG-16 was trained
                # on 1000 classes.
                flower_names.append(names[index])
                flower_probabilities.append(str("%.4f" % probabilities[index]))
        result["status"] = "ok"
        result["user_upload"] = "static/data/" + filename
        result["names"] = flower_names
        result["probabilities"] = flower_probabilities
        return result
    except Exception, e:
        print e
        return {"status": "fail"}


def detail(flower_name):
    flower_info = flower_manager.get_flower_info(flower_name)
    return flower_info.dump()
