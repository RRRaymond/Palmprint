

from PIL import Image
import numpy as np
import tensorflow as tf

import facenet

import yolo.python.darknet as dn

from flask import Flask, request
from werkzeug.utils import secure_filename
import os
from math import acos, sin, cos

app = Flask(__name__)
# model = '/Users/raymondchen/PycharmProjects/palm_verify/20180624-160529'
model = '/Users/raymondchen/PycharmProjects/palm_verify/20180623-205519'
thr = 0.02


@app.route('/')
def hello_world():
    return "Hello World!"


@app.route('/compare')
def compare():
    i1 = '/Users/raymondchen/Documents/Homework/palmprint/my_roi/%05d.png' % int(request.args.get('im1'))
    i2 = '/Users/raymondchen/Documents/Homework/palmprint/my_roi/%05d.png' % int(request.args.get('im2'))
    # read image using tf
    file_contents = tf.read_file(image_file_placeholder)
    image = tf.image.decode_image(file_contents, 3)
    image = (tf.cast(image, tf.float32) - 127.5) / 128.0

    image_1 = sess.run(image, feed_dict={image_file_placeholder: i1})
    image_2 = sess.run(image, feed_dict={image_file_placeholder: i2})
    image_1 = image_1[np.newaxis, ...]
    image_2 = image_2[np.newaxis, ...]

    feature_1 = sess.run(embeddings, feed_dict={phase_train_placeholder: False, image_batch: image_1})
    feature_2 = sess.run(embeddings, feed_dict={phase_train_placeholder: False, image_batch: image_2})

    distance = np.sum(np.sqrt((feature_1 - feature_2) ** 2)) / feature_1.shape[1]
    if distance < thr:
        return 'the same persons, distance: %f' % distance
    else:
        return 'different persons,  distance: %f' % distance


@app.route('/verify', methods=['POST'])
def verify():
    uploadfile = request.files['image']
    im_path = os.path.join(app.root_path, 'temp.png')
    uploadfile.save(im_path)

    roi = get_roi(im_path)

    if roi == 'fail':
        return 'bad palm'
    roi.save(os.path.join(app.root_path, 'tempROI.png'))

    i1 = os.path.join(app.root_path, 'tempROI.png')
    i2 = os.path.join(app.root_path, '%d.png' % int(request.form['id']))
    # read image using tf
    file_contents = tf.read_file(image_file_placeholder)
    image = tf.image.decode_image(file_contents, 3)
    # image = (tf.cast(image, tf.float32) - 127.5) / 128.0
    image = (tf.cast(image, tf.float32) - tf.reduce_mean(tf.cast(image, tf.float32))) / 128.0

    image_1 = sess.run(image, feed_dict={image_file_placeholder: i1})
    image_2 = sess.run(image, feed_dict={image_file_placeholder: i2})
    image_1 = image_1[np.newaxis, ...]
    image_2 = image_2[np.newaxis, ...]

    feature_1 = sess.run(embeddings, feed_dict={phase_train_placeholder: False, image_batch: image_1})
    feature_2 = sess.run(embeddings, feed_dict={phase_train_placeholder: False, image_batch: image_2})

    distance = np.sum(np.sqrt((feature_1 - feature_2) ** 2)) / feature_1.shape[1]
    if distance < thr:
        return 'the same persons, distance: %f' % distance
    else:
        return 'different persons,  distance: %f' % distance


@app.route('/signup', methods=['POST'])
def sign_up():
    uploadfile = request.files['image']
    uid = request.form['id']
    filename = secure_filename(uploadfile.filename)
    filetype = os.path.splitext(filename)[1]
    im_path = os.path.join(app.root_path, uid + filetype)
    if os.path.isfile(im_path):
        return 'already sign up'
    else:
        uploadfile.save(im_path)
        roi = get_roi(im_path)
        if roi == 'fail':
            return 'sign up fail'
        roi.save(os.path.join(app.root_path, uid + '.png'))
        if filetype != '.png':
            os.remove(im_path)
        return 'sign up successfully'


def get_roi(image_path):
    im = Image.open(image_path)
    im_array = np.array(im)
    h, w, ch = im_array.shape

    # image_path = "/Users/raymondchen/PycharmProjects/palm_verify/yolo/palm/00013.png"
    r = dn.detect(net, meta, str.encode(image_path), thresh=0.1)
    p0 = (0, 0)
    p1 = []
    re = []
    flag = [0, 0]
    for i in range(len(r)):
        # if r[i][0] == b'gap0' and flag[0] == 0:
        #     re.append(r[i])
        # elif r[i][0] == b'gap1' and flag[1] == 0:
        #     re.append(r[i])
        # else:

        flag2 = True
        for j in range(len(re)):
            temp1 = np.array(r[i][2][0:2])
            temp2 = np.array(re[j][2][0:2])
            if np.linalg.norm(temp1 - temp2) < 0.07 * max(h, w):
                flag2 = False
                if r[i][1] > re[j][1]:
                    re[j] = r[i]
        if flag2:
            re.append(r[i])
    # for i in range(len(re)):
    #     if re[i][0] == b'gap1' and re[i][1] > max_gap1:
    #         max_gap1 = re[i][1]
    m_temp = [x[1] for x in re if x[0] == b'gap1']
    if not m_temp:
        return 'fail'
    max_gap1 = max(m_temp)
    re = [x for x in re if x[0] == b'gap0' or x[1] == max_gap1]
    # re = [x for x in r if x[1] > 0]
    #
    print(re)
    if len(re) is not 4:
        return 'fail'
    flag = [0, 0]

    for i in range(4):
        if re[i][0] == b'gap0':
            flag[0] = flag[0] + 1
            p1.append(np.array(re[i][2][0:2]))
        else:
            flag[1] = flag[1] + 1
            p0 = np.array(re[i][2][0:2])
    p1 = np.array(p1)
    if flag != [3, 1]:
        return 'fail'

    length = []
    for i in range(3):
        length.append(np.linalg.norm(p0 - p1[i]))
    if min(length) < 0.07 * max(h, w):
        return 'fail'
    close_point = p1[length.index(min(length))]
    far_point = p1[length.index(max(length))]
    rotate_matrix = np.array([[0, -1],
                              [1, 0]])
    v1 = np.dot(close_point - far_point, rotate_matrix)
    v2 = p0 - close_point
    is_right = False
    if np.dot(v1, v2) < 0:
        v1 = -v1 / np.linalg.norm(v1)
        is_right = True
    else:
        v1 = v1 / np.linalg.norm(v1)

    # v3 = (close_point - far_point) / np.linalg.norm(close_point - far_point)
    # mid_p = (close_point + far_point) / 2
    # l = np.linalg.norm(close_point - p0)
    # if is_right:
    #     p_origin = mid_p + 1.3 * l * v1 - 0.5 * l * v3
    #     p_top = mid_p + 0.3 * l * v1 + 0.5 * l * v3
    # else:
    #     p_origin = mid_p + 1.3 * l * v1 + 0.5 * l * v3
    #     p_top = mid_p + 0.3 * l * v1 - 0.5 * l * v3
    l = np.linalg.norm(close_point - far_point)
    if is_right:
        p_origin = far_point + 4 / 3 * l * v1
        p_top = close_point + 1 / 3 * l * v1
    else:
        p_origin = close_point + 4 / 3 * l * v1
        p_top = far_point + 1 / 3 * l * v1
    print(np.linalg.norm(p_origin - p_top))
    t1 = p_origin[0]
    t2 = p_origin[1]
    theta = acos(np.dot((1, 1), p_top - p_origin) / np.linalg.norm((1, 1)) / np.linalg.norm(p_top - p_origin))
    v = p_top - p_origin
    if v[1] < v[0]:
        theta = - theta
    s = (p_top[0] - p_origin[0]) / (cos(theta) * 160 - sin(theta) * 160)
    trans_matrix = np.array([[s * cos(theta), -s * sin(theta), t1],
                             [s * sin(theta), s * cos(theta), t2],
                             [0, 0, 1]])

    new_im = np.zeros((160, 160, 3))
    for i in range(160):
        for j in range(160):
            pos = np.dot(trans_matrix, (i, j, 1)).astype(np.int32)
            if pos[1] > h - 1:
                pos[1] = h - 1
            if pos[0] > w - 1:
                pos[0] = w - 1
            for k in range(3):
                new_im[159 - i, j, k] = im_array[pos[1], pos[0], k]

    final = Image.fromarray(new_im.astype(np.uint8))
    return final
    # final.save(os.path.join(app.root_path, 'tempROI.png'))
    #
    # return 'ok'


@app.route('/first')
def login():
    return app.send_static_file('index.html')


@app.route('/testpost', methods=['POST'])
def m_post():
    return request.form['a']


if __name__ == '__main__':
    with tf.Session() as sess:
        image_file_placeholder = tf.placeholder(tf.string, shape=(None), name='image_file')
        phase_train_placeholder = tf.placeholder(tf.bool, name='phase_train')

        # load model
        input_map = {'phase_train': phase_train_placeholder}
        facenet.load_model(model, input_map=input_map)

        # evaluate on test image
        graph = tf.get_default_graph()
        image_batch = graph.get_tensor_by_name("image_batch:0")
        embeddings = graph.get_tensor_by_name("embeddings:0")

        dn.set_gpu(0)
        net = dn.load_net(str.encode("/Users/raymondchen/PycharmProjects/palm_verify/yolo/palm/yolo-obj.cfg"),
                          str.encode("/Users/raymondchen/PycharmProjects/palm_verify/yolo/palm/yolo-obj_final.weights"),
                          0)
        meta = dn.load_meta(str.encode("/Users/raymondchen/PycharmProjects/palm_verify/yolo/palm/obj.data"))

        app.run(
            debug=True,
            host='0.0.0.0',
            port=7086,
            threaded=True
        )
