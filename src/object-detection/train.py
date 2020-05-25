from detecto import core, utils, visualize


def main():
    dataset = core.Dataset('data/')
    model = core.Model(['church'])

    model.fit(dataset)


if __name__ == "__main__":
    main()
