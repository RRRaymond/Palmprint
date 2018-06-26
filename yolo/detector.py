import python.darknet as dn

dn.set_gpu(0)
net = dn.load_net(str.encode("cfg/tiny-yolo.cfg"),
                  str.encode("weights/tiny-yolo.weights"), 0)
meta = dn.load_meta(str.encode("cfg/coco.data"))
r = dn.detect(net, meta, str.encode("data/dog.jpg"))
print(r)

# And then down here you could detect a lot more images like:
# r = dn.detect(net, meta, "data/eagle.jpg")
# print(r)
# r = dn.detect(net, meta, "data/giraffe.jpg")
# print(r)
# r = dn.detect(net, meta, "data/horses.jpg")
# print(r)
# r = dn.detect(net, meta, "data/person.jpg")
# print(r)
