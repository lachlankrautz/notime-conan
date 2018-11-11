import os
from conans import ConanFile, tools, AutoToolsBuildEnvironment
from conans.tools import download, unzip
from conans.client.tools.oss import os_info


class SdlConan(ConanFile):
    name = "sdl2"
    version = "2.0.9"
    license = "MIT"
    author = "Lachlan Krautz lachlan.krautz@gmail.com"
    url = "github.com/lachlankrautz/notime-conan"
    description = "SDL2"
    topics = ("SDL2", "games", "opengl")
    settings = "os", "compiler", "build_type", "arch"
    options = {
        "shared": [True, False],
        "windows_console": [True, False]
    }
    default_options = {
        "shared": False,
        "windows_console": True,
    }
    generators = "cmake"
    folder = "SDL2-%s" % version

    def source(self):
        zip_name = "%s.zip" % self.folder
        download("https://www.libsdl.org/release/%s" % zip_name, zip_name)
        unzip(zip_name)
        os.chmod("%s/configure" % self.folder, 0o755)

    def build(self):
        with tools.chdir(self.folder):
            env_build = AutoToolsBuildEnvironment(self, win_bash=os_info.is_windows)
            env_build.configure()
            env_build.make()

    def package(self):
        self.copy("*.h", dst="include", src="%s/include" % self.folder, keep_path=True)
        self.copy("*.lib", dst="lib", keep_path=False)
        self.copy("*.dll", dst="bin", keep_path=False)
        self.copy("*.so", dst="lib", keep_path=False)
        self.copy("*.dylib", dst="lib", keep_path=False)
        self.copy("*.a", dst="lib", keep_path=False)

    def package_info(self):
        if self.settings.get_safe("os.subsystem") == "msys2":
            self.cpp_info.libs.append("mingw32")
            # not sure if needed
            # self.cpp_info.cppflags.append("-pthread")
            if not self.options.windows_console:
                self.cpp_info.cppflags.append("-mwindows")

        self.cpp_info.libs.extend(["SDL2main", "SDL2"])
