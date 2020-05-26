from detecto import core, utils, visualize


def main():
    # dataset = core.Dataset('data/')
    # model = core.Model(['church'])
    #
    # model.fit(dataset)
    # model.save('model_weights.pth')
    model = core.Model.load('model_weights.pth', ['church'])

    # Specify the path to your image
    image = utils.read_image('data/75068_75694_.png')
    predictions = model.predict(image)

    # predictions format: (labels, boxes, scores)
    labels, boxes, scores = predictions

    # ['alien', 'bat', 'bat']
    print(labels)

    #           xmin       ymin       xmax       ymax
    # tensor([[ 569.2125,  203.6702, 1003.4383,  658.1044],
    #         [ 276.2478,  144.0074,  579.6044,  508.7444],
    #         [ 277.2929,  162.6719,  627.9399,  511.9841]])
    print(boxes)

    # tensor([0.9952, 0.9837, 0.5153])
    print(scores)


if __name__ == "__main__":
    main()
