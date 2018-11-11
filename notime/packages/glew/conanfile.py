from conans import ConanFile, CMake, tools
from conans.tools import download, unzip


class GlewConan(ConanFile):
    name = "glew"
    version = "2.1.0"
    license = "MIT"
    author = "Lachlan Krautz lachlan.krautz@gmail.com"
    url = "github.com/lachlankrautz/notime-conan"
    description = "The OpenGL Extension Wrangler Library (GLEW) " \
                  "is a cross-platform open-source C/C++ extension loading library "
    topics = ("OpenGL", "glew", "extensions")
    settings = "os", "compiler", "build_type", "arch"
    options = {
        "shared": [True, False],
    }
    default_options = {
        "shared": False,
    }
    generators = "cmake"
    folder = "glew-%s" % version

    def source(self):
        download("https://sourceforge.net/projects/glew/files/glew/%s/%s.zip/download"
                 % (self.version, self.folder), self.folder)
        unzip(self.folder)

    def build(self):
        cmake = CMake(self)
        cmake.configure(source_folder="hello")
        cmake.build()

        # Explicit way:
        # self.run('cmake %s/hello %s'
        #          % (self.source_folder, cmake.command_line))
        # self.run("cmake --build . %s" % cmake.build_config)

    def package(self):
        self.copy("*.h", dst="include", src="hello")
        self.copy("*hello.lib", dst="lib", keep_path=False)
        self.copy("*.dll", dst="bin", keep_path=False)
        self.copy("*.so", dst="lib", keep_path=False)
        self.copy("*.dylib", dst="lib", keep_path=False)
        self.copy("*.a", dst="lib", keep_path=False)

    def package_info(self):
        self.cpp_info.libs = ["hello"]

