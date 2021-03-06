cmake_minimum_required(VERSION 2.8.11)
project(test_package)

include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup()

set(CROSS_PLATFORM_LIBS "")
if(MINGW)
    set(CROSS_PLATFORM_LIBS mingw32)
endif()

add_executable(${PROJECT_NAME} test_package.cpp)
target_link_libraries(${PROJECT_NAME} ${CROSS_PLATFORM_LIBS} ${CONAN_LIBS})

function(add_option option)
    if(${option})
        target_compile_definitions(${CMAKE_PROJECT_NAME} PRIVATE "${option}")
    endif()
endfunction()

add_option(WITH_X11)
add_option(WITH_ALSA)
add_option(WITH_PULSE)
add_option(WITH_ESD)
add_option(WITH_ARTS)
add_option(WITH_DIRECTFB)
add_option(WITH_DIRECTX)
