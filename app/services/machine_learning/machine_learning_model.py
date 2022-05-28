import pickle
import functools


@functools.cache
def get_machine_learning_model():
    _clf = pickle.load(open('machine_network.pkl', 'rb'))
    return _clf


def get_machine_learning_model_stub():
    raise NotImplementedError
