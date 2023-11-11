from keras.datasets import mnist
import numpy as np


(train_images, train_labels), (test_images, test_labels) = mnist.load_data()

train_images=train_images.reshape(len(train_images),784)
train_labels = np.eye(10)[train_labels]

w_i_h = np.random.uniform(-0.5,0.5,(20,784))
w_h_o= np.random.uniform(-0.5,0.5,(10,20))

b_i_h = np.zeros((20,1))
b_h_o = np.zeros((10,1))

nr_correct = 0
learn_rate = 0.01

# training loop
epochs = 5          # no of training iterations 
for i in range(epochs):
    for img,l in zip(train_images,train_labels):
        img = img / 255.0        # normalize input (0 to 1)
        img.shape+=(1,)          # reshape individual image array (28*28) to (784*1)  
        l.shape+=(1,)

        # forward prop input->hidden
        h_pre = b_i_h + w_i_h @ img
        h = 1 / (1 + np.exp(-h_pre))

        # forward prop hidden->output
        o_pre = b_h_o + w_h_o @ h
        o = 1 / (1 + np.exp(-o_pre))

        e = 1/len(o) * np.sum((o-l)**2,axis=0)             # mean squared error cost function

        nr_correct += int(np.argmax(o)==np.argmax(l))      # track total correct classifications

        # Back prop output->hidden
        delta_o = o-l                             # some trick
        w_h_o += -learn_rate * delta_o @ np.transpose(h)
        b_h_o += -learn_rate * delta_o

        # Back prop hidden->input
        delta_h = np.transpose(w_h_o) @ delta_o * (h * (1-h))     # (h*(1-h)) is derivative of sigmoid  
        w_i_h += -learn_rate * delta_h @ np.transpose(img)
        b_i_h += -learn_rate * delta_h


    print(i+1, "Loop complete")
    print("Percent correct: ", nr_correct/len(train_images)*100)
    nr_correct = 0
print("Training complete")

# saving weight and bias 
np.savez('digits.npz', w_i_h=w_i_h, b_i_h=b_i_h, w_h_o=w_h_o, b_h_o=b_h_o)

