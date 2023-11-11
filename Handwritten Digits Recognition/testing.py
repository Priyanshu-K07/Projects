import numpy as np

from keras.datasets import mnist
(train_images, train_labels), (test_images, test_labels) = mnist.load_data()

testerI = test_images.reshape(len(test_images),784)
testerL = np.eye(10)[test_labels]


# load weights and bias
data = np.load('digits.npz')
w_i_h_loaded = data['w_i_h']
b_i_h_loaded = data['b_i_h']
w_h_o_loaded = data['w_h_o']
b_h_o_loaded = data['b_h_o']

# testing loop
def classify():
    count = 1
    nr_correct = 0
    for img,label in zip(testerI,testerL):
        img = img / 255.0        # normalize input (0 to 1)
        img.shape+=(1,)          # reshape individual image array (28*28) to (784*1)  
        label.shape+=(1,)
        # Forward pass input -> hidden layer
        h_pre = b_i_h_loaded + w_i_h_loaded @ img
        h = 1 / (1 + np.exp(-h_pre))

        # Forward pass hidden layer -> output layer
        o_pre = b_h_o_loaded + w_h_o_loaded @ h
        output = 1 / (1 + np.exp(-o_pre))

        nr_correct += int(np.argmax(output)==np.argmax(label)) 
        if (count%1000==0):
            print('Accuracy: ',nr_correct/count*100)

        count+=1
    print("Percent correct: ", nr_correct/len(test_images)*100)

classify()
