#!/usr/bin/env python
# -*- coding: utf-8 -*-

from conans import ConanFile, CMake, tools, AutoToolsBuildEnvironment
import os


class FreetypeConan(ConanFile):
    name = "freetype"
    version = "2.9.0"
    description = "FreeType is a freely available software library to render fonts."
    url = "http://github.com/bincrafters/conan-freetype"
    homepage = "https://www.freetype.org"
    license = "BSD"
    author = "Bincrafters <bincrafters@gmail.com>"
    exports = ["LICENSE.md", "FindFreetype.cmake"]
    exports_sources = ["CMakeLists.txt", "freetype.pc.in"]
    generators = "cmake"
    settings = "os", "arch", "compiler", "build_type"
    options = {
        "shared": [True, False],
        "fPIC": [True, False],
        "with_png": [True, False],
        "with_zlib": [True, False],
        "with_harfbuzz": [True, False],
    }
    default_options = {
        'shared': False,
        'fPIC': True,
        'with_png': True,
        'with_zlib': True,
        'with_harfbuzz': False,
    }
    _source_subfolder = "source_subfolder"
    _build_subfolder = "build_subfolder"

    def requirements(self):
        if self.options.with_png:
            self.requires.add("libpng/1.6.34@bincrafters/stable")
        if self.options.with_zlib:
            self.requires.add("bzip2/1.0.6@conan/stable")
        if self.options.with_harfbuzz:
            self.requires.add("harfbuzz/1.7.6@bincrafters/stable")

    def config_options(self):
        if self.settings.os == "Windows":
            del self.options.fPIC

    def configure(self):
        del self.settings.compiler.libcxx

    def source(self):
        source_url = "https://download.savannah.gnu.org/releases/"
        version = self.version[:-2]
        archive_file = '{0}-{1}.tar.gz'.format(self.name, version)
        source_file = '{0}/{1}/{2}'.format(source_url, self.name, archive_file)
        tools.get(source_file)
        os.rename('{0}-{1}'.format(self.name, version), self._source_subfolder)
        self._patch_windows()

    def _patch_windows(self):
        if self.settings.os == "Windows":
            pattern = 'if (WIN32 AND NOT MINGW AND BUILD_SHARED_LIBS)\n' + \
                      '  message(FATAL_ERROR "Building shared libraries on Windows needs MinGW")\n' + \
                      'endif ()\n'
            cmake_file = os.path.join(self._source_subfolder, 'CMakeLists.txt')
            tools.replace_in_file(cmake_file, pattern, '')

    def _patch_msvc_mt(self):
        if self.settings.os == "Windows" and \
           self.settings.compiler == "Visual Studio" and \
           "MT" in self.settings.compiler.runtime:
            header_file = os.path.join(self._source_subfolder, "include", "freetype", "config", "ftconfig.h")
            tools.replace_in_file(header_file, "#ifdef _MSC_VER", "#if 0")

    def _configure_cmake(self):
        cmake = CMake(self)
        system_libraries = ''
        if self.settings.os == 'Linux':
            system_libraries = '-lm'
        cmake.definitions["PC_SYSTEM_LIBRARIES"] = system_libraries
        cmake.definitions["PC_FREETYPE_LIBRARY"] = '-lfreetyped' if self.settings.build_type == 'Debug' \
            else '-lfreetype'

        if self.options.with_png:
            cmake.definitions["PC_PNG_LIBRARY"] = '-l%s' % self.deps_cpp_info['libpng'].libs[0]
        else:
            cmake.definitions["PC_PNG_LIBRARY"] = ''

        if self.options.with_zlib:
            cmake.definitions["PC_ZLIB_LIBRARY"] = '-l%s' % self.deps_cpp_info['zlib'].libs[0]
            cmake.definitions["PC_BZIP2_LIBRARY"] = '-l%s' % self.deps_cpp_info['bzip2'].libs[0]
        else:
            cmake.definitions["PC_ZLIB_LIBRARY"] = ''
            cmake.definitions["PC_BZIP2_LIBRARY"] = ''

        # if self.options.with_harfbuzz:
        #     cmake.definitions["<harfbuzz_lib>"] = '-l%s' % self.deps_cpp_info['<erm>'].libs[0]
        # else:
        #     cmake.definitions["<harfbuzz_lib>"] = '-l%s' % self.deps_cpp_info['<erm>'].libs[0]

        cmake.definitions["PROJECT_VERSION"] = self.version
        cmake.definitions["WITH_ZLIB"] = self.options.with_zlib
        cmake.definitions["WITH_PNG"] = self.options.with_png
        cmake.definitions["WITH_HARFBUZZ"] = self.options.with_harfbuzz
        cmake.configure(build_dir=self._build_subfolder)
        return cmake

    def build(self):
        # configure with autotools even though we're building with cmake
        # need to generate sdl-config
        # win_bash = tools.os_info.detect_windows_subsystem() == "msys2"
        # autotools = AutoToolsBuildEnvironment(self, win_bash=win_bash)
        # autotools.configure(configure_dir=self._source_subfolder)

        self._patch_msvc_mt()
        cmake = self._configure_cmake()
        cmake.build()

    def package(self):
        win_bash = tools.os_info.detect_windows_subsystem() == "msys2"
        freetype_config = 'freetype-config.exe' if (self.settings.os == 'Windows' and not win_bash) else 'freetype-config'
        self.copy(pattern=freetype_config, dst="bin")

        cmake = self._configure_cmake()
        cmake.install()
        self.copy("FindFreetype.cmake")
        self.copy("FTL.TXT", dst="licenses", src=os.path.join(self._source_subfolder, "docs"))
        self.copy("GPLv2.TXT", dst="licenses", src=os.path.join(self._source_subfolder, "docs"))
        self.copy("LICENSE.TXT", dst="licenses", src=os.path.join(self._source_subfolder, "docs"))

    def package_info(self):
        win_bash = tools.os_info.detect_windows_subsystem() == "msys2"
        freetype_config = 'freetype-config.exe' if (self.settings.os == 'Windows' and not win_bash) else 'freetype-config'
        freetype_config = os.path.join(self.package_folder, 'bin', freetype_config)
        self.output.info('Creating Freetype config environment variable: %s' % freetype_config)
        self.env_info.FREETYPE_CONFIG = freetype_config

        self.cpp_info.libs = tools.collect_libs(self)
        if self.settings.os == "Linux":
            self.cpp_info.libs.append("m")
        self.cpp_info.includedirs.append(os.path.join("include", "freetype2"))
