import tensorflow as tf
import scipy
from scipy import misc
import numpy as np
import argparse

def load_graph(frozen_graph_filename):
    # We load the protobuf file from the disk and parse it to retrieve the 
    # unserialized graph_def
    with tf.gfile.GFile(frozen_graph_filename, "rb") as f:
        graph_def = tf.GraphDef()
        graph_def.ParseFromString(f.read())

    # Then, we import the graph_def into a new Graph and returns it 
    with tf.Graph().as_default() as graph:
        # The name var will prefix every op/nodes in your graph
        # Since we load everything in a new graph, this is not needed
        tf.import_graph_def(graph_def, name="prefix")
    return graph

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--graph", type=str, default="./frozen_model.pb", help="Path to frozen Graph")
    parser.add_argument("--img", type=str, default="", help="The path to the image to do inferencing")
    args = parser.parse_args()



    graph = load_graph(args.graph)

    # We can verify that we can access the list of operations in the graph
    
# for op in graph.get_operations():
#     print(op.name)

    x = graph.get_tensor_by_name('prefix/input_tensor:0')
    y = graph.get_tensor_by_name('prefix/output_pred:0')

    with tf.Session(graph=graph) as sess:

        image = scipy.misc.imread(args.img)
        image = scipy.misc.imresize(image,(224,224,3))
        image = image.astype(float)
        Input_image_shape=image.shape
        height,width,channels = Input_image_shape
        
        image_np = np.expand_dims(image, 0)
    # Note: we don't nee to initialize/restore anything
    # There is no Variables in this graph, only hardcoded constants 
        y_out = sess.run(y, feed_dict={
            x: image_np 
        })

        if y_out[0][0] >= 0.5:
            print("Its a Cat, with confidence {}%".format(y_out[0][0]*100))
        elif(y_out[0][1]>=0.5):
            print("Its a Dog, with confidence {}%".format(y_out[0][1]*100))
        else:
            print("No Pet")
        scipy.misc.imshow(image)