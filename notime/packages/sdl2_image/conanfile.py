import os
from conans import ConanFile, tools, AutoToolsBuildEnvironment
from conans.tools import download, unzip
from conans.client.tools.oss import os_info


class Sdl2imageConan(ConanFile):
    name = "sdl2_image"
    version = "2.0.4"
    license = "MIT"
    author = "Lachlan Krautz lachlan.krautz@gmail.com"
    url = "github.com/lachlankrautz/notime-conan"
    description = "SDL_image is an image loading library that is used with the SDL library, and almost as portable. " \
                  "It allows a programmer to use multiple image formats without having to code all the loading and " \
                  "conversion algorithms themselves. "
    topics = ("SDL2", "image", "png")
    settings = "os", "compiler", "build_type", "arch"
    options = {
        "shared": [True, False],
    }
    default_options = {
        "shared": False,
    }
    generators = "cmake"
    folder = "SDL2_image-%s" % version
    requires = "sdl2/2.0.9@notime/stable"

    def source(self):
        zip_name = "%s.zip" % self.folder
        download("https://www.libsdl.org/projects/SDL_image/release/%s"
                 % zip_name, zip_name)
        unzip(zip_name)
        os.chmod("%s/autogen.sh" % self.folder, 0o755)
        os.chmod("%s/configure" % self.folder, 0o755)

    def build(self):
        with tools.chdir(self.folder):
            env_build = AutoToolsBuildEnvironment(self, win_bash=os_info.is_windows)
            with tools.environment_append(env_build.vars):
                self.run("./autogen.sh", win_bash=os_info.is_windows)
            env_build.configure()
            env_build.make()

    def package(self):
        self.copy("*.h", dst="include", src=self.folder)
        self.copy("*hello.lib", dst="lib", keep_path=False)
        self.copy("*.dll", dst="bin", keep_path=False)
        self.copy("*.so", dst="lib", keep_path=False)
        self.copy("*.dylib", dst="lib", keep_path=False)
        self.copy("*.a", dst="lib", keep_path=False)

    def package_info(self):
        self.cpp_info.libs = ["SDL2_image"]

