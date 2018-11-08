import os

from conans.client.conan_api import ConanAPIV1


def run():
    directory = os.fsencode("packages")
    api, _, _ = ConanAPIV1.factory()

    for file in os.listdir(directory):
        filename = os.fsdecode(file)
        api.create("packages/%s" % filename, user="notime", channel="testing")
        print("\n-------------------\n")


if __name__ == '__main__':
    run()
