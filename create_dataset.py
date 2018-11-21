from random import shuffle
import glob
import sys
import cv2
import numpy as np
# import skimage.io as io
import tensorflow as tf
import os
import pickle


def _int64_feature(value):
    return tf.train.Feature(int64_list=tf.train.Int64List(value=[value]))


def _bytes_feature(value):
    return tf.train.Feature(bytes_list=tf.train.BytesList(value=[value]))


def load_image(addr):
    # read an image and resize to (256, 256)
    # cv2 load images as BGR, convert it to RGB
    img = cv2.imread(addr)
    if img is None:
        return None
    img = cv2.resize(img, (256, 256), interpolation=cv2.INTER_CUBIC)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    return img


def createDataRecord(out_filename, addrs, labels):
    # open the TFRecords file
    writer = tf.python_io.TFRecordWriter(out_filename)
    for i in range(len(addrs)):
        # print how many images are saved every 1000 images
        if not i % 1000:
            print('Train data: {}/{}'.format(i, len(addrs)))
            sys.stdout.flush()
        # Load the image
        img = load_image(addrs[i])
        # img = cv2.imread(addrs[i])

        label = labels[i]

        if img is None:
            continue

        # Create a feature
        feature = {
            'image_raw': _bytes_feature(img.tostring()),
            'label': _int64_feature(label)
        }
        # Create an example protocol buffer
        example = tf.train.Example(features=tf.train.Features(feature=feature))

        # Serialize to string and write on the file
        writer.write(example.SerializeToString())

    writer.close()
    sys.stdout.flush()


def main():
    folders_path = 'D:\\cygwin64\\home\\Bang\\wfdb-10.6.0\\afdb\\'

    folders = ['04015', '04043', '04048', '04126', '04746', '04908', '04936', '05091', '05121', '05261', '06426',
               '06453', '06995', '07162', '07859', '07879', '07910', '08215', '08219', '08378', '08405', '08434',
               '08455']

    # addrs = []
    # labels = []
    # for folder in folders:
    #     # print(os.listdir(folders_path + folder + '\\'))
    #     print(len(os.listdir(folders_path + folder + '\\')))
    #     addrs += os.listdir(folders_path + folder + '\\')
    #
    #     with open(folders_path + folder + '_labels' + '\\' + folder + "_labels.p", "rb") as fp:
    #         folder_labels = pickle.load(fp)
    #         labels += folder_labels

    spectrograms_path = 'D:\\cygwin64\\home\\Bang\\wfdb-10.6.0\\afdb\\spectrograms\\*.png'
    addrs = glob.glob(spectrograms_path)

    labels_path = 'D:\\cygwin64\\home\\Bang\\wfdb-10.6.0\\afdb\\spectrograms_labels\\spectrograms_labels.p'
    with open(labels_path, "rb") as fp:
        labels = pickle.load(fp)
    print('labels', labels)
    print('len(labels)', len(labels))
    print('set(labels)', set(labels))
    print('cv2.imread(addrs[0]).shape', cv2.imread(addrs[0]).shape) # (393, 536, 3)

    # Want to have equal number of AFIB and not-AFIB ############################
    count_afib = labels.count(1)
    print('count_afib', count_afib)
    # print(labels.count(1))
    labels = np.asarray(labels)
    print('labels.shape', labels.shape)

    afib_indices = np.where(labels == 1)[0]
    print('afib_indices.shape', afib_indices.shape)
    print('afib_indices', afib_indices)

    not_afib_indices = np.where(labels == 0)[0]
    print('not_afib_indices', not_afib_indices)
    np.random.shuffle(not_afib_indices)
    print('not_afib_indices.shape', not_afib_indices.shape)
    not_afib_indices_shuffled_subset = not_afib_indices[:count_afib]
    print('not_afib_indices_shuffled_subset.shape', not_afib_indices_shuffled_subset.shape)
    print('not_afib_indices_shuffled_subset', not_afib_indices_shuffled_subset)

    labels_subset = np.take(labels, np.concatenate((afib_indices, not_afib_indices_shuffled_subset), axis=None))
    print('labels_subset.shape', labels_subset.shape)

    addrs_subset = np.take(addrs, np.concatenate((afib_indices, not_afib_indices_shuffled_subset), axis=None))
    #############################################################################

    # to shuffle data
    c = list(zip(addrs_subset, labels_subset))
    shuffle(c)
    addrs, labels = zip(*c)

    # Divide the data into 60% train, 20% validation, and 20% test
    train_addrs = addrs[0:int(0.6 * len(addrs))]
    train_labels = labels[0:int(0.6 * len(labels))]
    val_addrs = addrs[int(0.6 * len(addrs)):int(0.8 * len(addrs))]
    val_labels = labels[int(0.6 * len(addrs)):int(0.8 * len(addrs))]
    test_addrs = addrs[int(0.8 * len(addrs)):]
    test_labels = labels[int(0.8 * len(labels)):]

    createDataRecord('train.tfrecords', train_addrs, train_labels)
    createDataRecord('val.tfrecords', val_addrs, val_labels)
    createDataRecord('test.tfrecords', test_addrs, test_labels)


if __name__ == "__main__":
    main()
