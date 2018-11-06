from conans import ConanFile, CMake, tools
from conans.tools import download, unzip
from conans.client.tools.oss import os_info


class SdlConan(ConanFile):
    name = "hello"
    version = "2.0.9"
    license = "MIT"
    author = "Lachlan Krautz lachlan.krautz@gmail.com"
    url = "github.com/lachlankrautz/notime-conan"
    description = "SDL"
    topics = ("SDL", "games", "opengl")
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False]}
    default_options = "shared=False"
    generators = "cmake"

    def source(self):
        zip_name = "SDL-%s.zip" % self.version
        download("https://www.libsdl.org/release/%s" % zip_name, zip_name)
        unzip(zip_name)

        self.run("chmod +x ./SDL-%s/configure" % self.version)

        # This small hack might be useful to guarantee proper /MT /MD linkage
        # in MSVC if the packaged project doesn't have variables to set it
        # properly
        tools.replace_in_file("hello/CMakeLists.txt", "PROJECT(MyHello)",
                              '''PROJECT(MyHello)
include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup()''')

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
        if self.options.shared:
            self.cpp_info.libs = ['SDL2-2.0']
        else:
            self.cpp_info.libs = ['SDL2']

        self.cpp_info.libs.extend(["m", "dl", "pthread"])

        if os_info.is_linux:
            self.cpp_info.libs.append("rt")

