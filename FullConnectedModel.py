import NNModel as abstract_model

import numpy
from numpy import genfromtxt
from keras.models import Sequential
from keras.layers import Dense
from keras.utils import np_utils
import csv

class FullConnectedModel(abstract_model.NNModel):
    """
    Fully connected Neural Network for the MNIST Dataset
    """

    def __init__(self):
        super(FullConnectedModel, self).__init__()
        self.prepare_data()

    def prepare_data(self):
        self.num_bits = 36

        # load data
        data = genfromtxt('data.csv', delimiter=',')
        modified_data = []
        format_str = '{0:0'+str(self.num_bits)+'b}'

        for line in data:
            modified_data.append(numpy.append(numpy.array(list(format_str.format(int(line[0])))), numpy.array(int(line[1]))))

        data = numpy.array(modified_data)

        train = data[:70000]
        test = data[70000:]

        self.X_train = train[:,0:36]
        self.y_train = np_utils.to_categorical(train[:,36:37])

        self.X_test = test[:,0:36]
        self.y_test = np_utils.to_categorical(test[:,36:37])

        self.num_classes = 2

    def train(self):
        # build the model
        model = self.definition(self.num_classes)
        # Fit the model
        model.fit(self.X_train, self.y_train, validation_data=(self.X_test, self.y_test), nb_epoch=50, batch_size=200,
                  verbose=2)
        # Final evaluation of the model
        scores = model.evaluate(self.X_test, self.y_test, verbose=0)
        print("Baseline Error: %.2f%%" % (100 - scores[1] * 100))

        self.save_model(model)

    def predict(self, code):
        format_str = '{0:0' + str(self.num_bits) + 'b}'
        code_to_bits = numpy.array(list(format_str.format(int(code))))
        code_to_bits = numpy.array([code_to_bits])
        return super().predict(code_to_bits)

    # define the larger model
    def definition(self, num_classes):
        # create model
        model = Sequential()
        model.add(Dense(700, input_dim=self.num_bits, init='normal', activation='relu'))
        model.add(Dense(50, input_dim=700, init='normal', activation='relu'))
        model.add(Dense(2, input_dim=50, init='normal', activation='relu'))
        model.add(Dense(num_classes, init='normal', activation='softmax'))
        # Compile model
        model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
        return model

    def get_name(self):
        return 'full_connected'


model = FullConnectedModel()
# model.train()

model.load_model()
data = [
    (657863796,1),
    (1311253967,1),
    (73004672,1),
    (1228935656,1),
    (5742162869,1),
    (520294385,1),
    (129728263,0),
    (308657584,0),
    (658180536,0),
    (69056312,0),
    (1170627896,0),
    (56968332,0)
]

for line in data:
    result = model.predict(line[0])
    if result[0][0] > result[0][1]:
        result = '0'
    else:
        result = '1'
    print('code: ', line[0], 'réponse: ', line[1], 'Prédiction: ', result)