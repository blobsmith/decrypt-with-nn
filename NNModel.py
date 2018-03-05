from abc import abstractmethod
from keras.models import model_from_json
import os


class NNModel():

    def __init__(self):
        self.model = None
        self.model_json_path = 'models/' + self.get_name() + '/model.json'
        self.model_weights_path = 'models/'+self.get_name()+'/model.h5'

    def get_name(self):
        return 'nn_model'

    @abstractmethod
    def train(self):
        pass

    @abstractmethod
    def definition(self, num_classes):
        pass

    def predict(self, data):
        """
        Check image from model to determine the prediction

        :param data:
        :return:
        """

        prediction = None
        if self.model is not None:
            prediction = self.model.predict(data)
        return prediction

    def load_model(self):
        if self.model is None:
            json_file = open(self.model_json_path, 'r')
            loaded_model_json = json_file.read()
            json_file.close()
            self.model = model_from_json(loaded_model_json)

            # load weights into new model
            self.model.load_weights(self.model_weights_path)

            # evaluate loaded model on test data
            self.model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

    def save_model(self, model):
        """
        Save trained model to files.

        :param model:
        :return:
        """
        # serialize model to JSON
        model_json = model.to_json()
        os.makedirs(os.path.dirname(self.model_json_path), exist_ok=True)
        with open(self.model_json_path, "w") as json_file:
            json_file.write(model_json)

        # serialize weights to HDF5
        model.save_weights(self.model_weights_path)
        print("Saved model to disk")
