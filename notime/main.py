import os
import sys

from conans.client.conan_api import ConanAPIV1

api, _, _ = ConanAPIV1.factory()


def run():
    if sys.argv[1:]:
        create(sys.argv[1])
        return

    directory = os.fsencode("packages")
    for file in os.listdir(directory):
        create(os.fsdecode(file))
        print("\n-------------------\n")


def create(name):
    api.create("packages/%s" % name, user="notime", channel="stable")


if __name__ == '__main__':
    run()
