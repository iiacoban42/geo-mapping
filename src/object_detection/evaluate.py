import os

from detecto import core, utils
from src.core.models import AI_Tiles as AITilesTable
os.chdir('object_detection')

# Constants used for evaluation
OBJECTS_TO_DETECT = ['church']
DETECTION_THRESHOLD = 0.95

# saves ai classification in the database
def save_labels():
    tile = AITilesTable(x_coord=75065, y_coord=75510, year=2016)
    print(tile)
    # tile.save()
    # prediction = PredictionsTable(tiles_id=tile, water_prediction=water, land_prediction=land,
    #                               buildings_prediction=building)
    # prediction.save()


def main():
    """Load model and evaluate it"""
    print("Loading object_detection model...")
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
    save_labels()
