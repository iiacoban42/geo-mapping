import os
import django
django.setup()

from detecto import core, utils
from core.models import AI_Objects as AIObjectsTable
from core.models import AI_Tiles as AITilesTable

# Constants used for evaluation
OBJECTS_TO_DETECT = ['church']
DETECTION_THRESHOLD = 0.95

# saves ai classification in the database
def save_labels():
    model = core.Model.load('model/model_weights.pth', OBJECTS_TO_DETECT)
    for filename in os.listdir("data"):
        separated_name = filename.split('_')
        if separated_name[2] == ".png":
            image = utils.read_image('data/{}'.format(filename))
            predictions = model.predict(image)

            # Save tile
            tile = AITilesTable(x_coord=int(separated_name[0]), y_coord=int(separated_name[1]), year=2016)
            tile.save()

            # Save prediction
            score = int(predictions[2][0] * 100)
            prediction = AIObjectsTable(tiles_id=tile, type="church",prediction=score)
            prediction.save()
            print(filename + "successfully saved & predicted")

    for filename in os.listdir("validation_data/church"):
        separated_name = filename.split('_')
        image = utils.read_image('validation_data/church/{}'.format(filename))
        predictions = model.predict(image)

        # Save tile
        tile = AITilesTable(x_coord=int(separated_name[0]), y_coord=int(separated_name[1]), year=2016)
        tile.save()

        # Save prediction
        score = int(predictions[2][0] * 100)
        prediction = AIObjectsTable(tiles_id=tile, type="church", prediction=score)
        prediction.save()
        print(filename + "successfully saved & predicted")


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
