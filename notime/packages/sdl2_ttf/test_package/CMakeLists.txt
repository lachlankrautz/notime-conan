cmake_minimum_required(VERSION 3.12)
project(test_package)

set(CMAKE_VERBOSE_MAKEFILE TRUE)

include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup()

add_executable(${PROJECT_NAME} test_package.c)
target_compile_definitions(${PROJECT_NAME} PRIVATE
  FONT_PATH="${CMAKE_CURRENT_LIST_DIR}/OpenSans-Bold.ttf")
target_link_libraries(${PROJECT_NAME} ${CONAN_LIBS})
