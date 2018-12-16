project(test_package)
cmake_minimum_required(VERSION 2.8.11)

set(CMAKE_VERBOSE_MAKEFILE TRUE)

include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup()

set(CROSS_PLATFORM_LIBS "")
if(MINGW)
    set(CROSS_PLATFORM_LIBS mingw32)
endif()

file(GLOB SOURCE_FILES *.cpp)

add_executable(${PROJECT_NAME} ${SOURCE_FILES})
target_link_libraries(${PROJECT_NAME} ${CROSS_PLATFORM_LIBS} ${CONAN_LIBS})
