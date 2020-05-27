import os

from detecto import core, utils, visualize

# Constants used for training and evaluation
TRAIN_DIR = "data/"
OBJECTS_TO_DETECT = ['church']
DETECTION_THRESHOLD = 0.95


def train_model():
    """Train church detection model"""
    dataset = core.Dataset(TRAIN_DIR)
    model = core.Model(OBJECTS_TO_DETECT)

    model.fit(dataset)
    model.save('model_weights.pth')


def main():
    """Load model and evaluate it"""
    print("Loading object-detection model...")
    model = core.Model.load('model/model_weights.pth', OBJECTS_TO_DETECT)

    correct_classifications = 0

    # Check church detection
    for filename in os.listdir("validation-data/church"):
        if filename.endswith(".png"):
            image = utils.read_image('validation-data/church/{}'.format(filename))
            predictions = model.predict(image)

            # predictions format: (labels, boxes, scores)
            labels, boxes, scores = predictions
            filtered_scores = list(filter(lambda score: score > DETECTION_THRESHOLD, scores))

            # increment correct classifications if churches were found
            if len(filtered_scores) > 0:
                correct_classifications += 1

            print("Scores for church image {} are {}".format(filename, filtered_scores))

    # Check absence of churches
    for filename in os.listdir("validation-data/non-church"):
        if filename.endswith(".png"):
            image = utils.read_image('validation-data/non-church/{}'.format(filename))
            predictions = model.predict(image)

            # predictions format: (labels, boxes, scores)
            labels, boxes, scores = predictions
            filtered_scores = list(filter(lambda score: score > DETECTION_THRESHOLD, scores))

            # increment correct classifications if churches were not found
            if len(filtered_scores) == 0:
                correct_classifications += 1

            print("Scores for non-church image {} are {}".format(filename, filtered_scores))

    image_count = len(os.listdir("validation-data/non-church")) + len(os.listdir("validation-data/church"))
    classification_ratio = correct_classifications / image_count

    # Write last accuracy
    f = open("model/last_accuracy.txt", 'w')
    f.write(str(classification_ratio))
    f.close()

    print("Accuracy of this model is {}%".format(classification_ratio * 100))


if __name__ == "__main__":
    main()
