from detecto import core

# Constants used for training
TRAIN_DIR = "data/"
OBJECTS_TO_DETECT = ['church']


def train():
    """Train object detection model"""
    dataset = core.Dataset(TRAIN_DIR)
    model = core.Model(OBJECTS_TO_DETECT)

    model.fit(dataset)
    model.save('model_weights.pth')


if __name__ == "__main__":
    train()
