import tensorflow as tf
import cPickle


## define DeepCnn model for handwritten digits recognition

def deepnn(x):
    x_image = tf.reshape(x, [-1, 28, 28, 1])
    
# First convolutional layer - maps one grayscale image to 32 feature maps.
    W_conv1 = weight_variable([5, 5, 1, 32])
    b_conv1 = bias_variable([32])
    h_conv1 = tf.nn.relu(conv2d(x_image, W_conv1) + b_conv1)

# Pooling layer - downsamples by 2X.
    h_pool1 = max_pool_2x2(h_conv1)

# Second convolutional layer -- maps 32 feature maps to 64.
    W_conv2 = weight_variable([5, 5, 32, 64])
    b_conv2 = bias_variable([64])
    h_conv2 = tf.nn.relu(conv2d(h_pool1, W_conv2) + b_conv2)

# Second pooling layer.
    h_pool2 = max_pool_2x2(h_conv2)

# Fully connected layer 1 -- after 2 round of downsampling, our 28x28 image
# is down to 7x7x64 feature maps -- maps this to 1024 features.
    W_fc1 = weight_variable([7 * 7 * 64, 1024])
    b_fc1 = bias_variable([1024])

    h_pool2_flat = tf.reshape(h_pool2, [-1, 7*7*64])
    h_fc1 = tf.nn.relu(tf.matmul(h_pool2_flat, W_fc1) + b_fc1)

# Dropout - controls the complexity of the model, prevents co-adaptation of
# features.
    keep_prob = tf.placeholder(tf.float32)
    h_fc1_drop = tf.nn.dropout(h_fc1, keep_prob)

# Map the 1024 features to 10 classes, one for each digit
    W_fc2 = weight_variable([1024, 10])
    b_fc2 = bias_variable([10])

    y_conv = tf.matmul(h_fc1_drop, W_fc2) + b_fc2
    return y_conv, keep_prob

# define four functions for this neural network by refering 
# to tensorflow calsses

def conv2d(x, W):
    """conv2d returns a 2d convolution layer with full stride."""
    return tf.nn.conv2d(x, W, strides=[1, 1, 1, 1], padding='SAME')


def max_pool_2x2(x):
    """max_pool_2x2 downsamples a feature map by 2X."""
    return tf.nn.max_pool(x, ksize=[1, 2, 2, 1], strides=[1, 2, 2, 1], padding='SAME')


def weight_variable(shape):
    """weight_variable generates a weight variable of a given shape."""
    initial = tf.truncated_normal(shape, stddev=0.1)
    return tf.Variable(initial)


def bias_variable(shape):
    """bias_variable generates a bias variable of a given shape."""
    initial = tf.constant(0.1, shape=shape)
    return tf.Variable(initial)


## load test datas[0:1000] which are extracted from mnist data
## fully test datas is too large to read by Raspberry Pi

pkl_file = open('test_datas.pkl', 'rb')
test_images,test_labels = cPickle.load(pkl_file)


## set the parameters for prediction of test datas

# define input name and its shape for test_images 
x = tf.placeholder(tf.float32, [None, 784])

# define output name and its shape for test_labels
# which are the correct numbers of test_images
y_ = tf.placeholder(tf.float32, [None, 10])

# Build the graph for the deep net
y_conv, keep_prob = deepnn(x)

# define the prediction criterion
correct_prediction = tf.equal(tf.argmax(y_conv, 1), tf.argmax(y_, 1))
accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))

## load the model for this network 
## the model is a kind of weighs and biases excactly which are optimized
## during training procedure on the faster computer such as GPU embedded
## cloud instance

sess = tf.InteractiveSession()
sess.run(tf.global_variables_initializer())
       
saver = tf.train.Saver()
saver.restore(sess, './model/model' )         


## print the prediction results of test datas
## 0.97 should be printed
## 

feed_dict = {x: test_images[:100], y_: test_labels[:100], keep_prob: 1.0}
print(accuracy.eval(feed_dict))
