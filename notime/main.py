import os

from conans import tools


def run():
    directory = os.fsencode("packages")
    # api, _, _ = ConanAPIV1.factory()

    for file in os.listdir(directory):
        filename = os.fsdecode(file)
        print(filename)
        # api.create(file)


if __name__ == '__main__':
    run()
