import pickle


def save(user_data):
    with open('{0}_data.pickle'.format(user_data.name), 'wb') as f:
        pickle.dump(user_data, f, pickle.HIGHEST_PROTOCOL)


def load(user_name):
    print('loading from cache...')
    with open('{0}_data.pickle'.format(user_name), 'rb') as f:
        LoadedUndergraduate = pickle.load(f)
    return LoadedUndergraduate
