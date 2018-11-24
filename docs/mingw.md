# Packaging mingw

## Statically link mingw

MinGW dlls are likely not present on target machine so link them statically.
Follow with `-dynamic` so that following libs don't default to static.

## Windows console

A cmd console window will open for std out unless you link with `-mwindows`.

```cmake
if (MINGW)
    target_link_libraries(
            <target>
            -mwindows
            -static gcc stdc++ winpthread -dynamic
    )
endif()
```

## Executable icon

Create an rc file referencing the icon file for the executable.

```rc
1 ICON "../images/icon.ico"
```

Use windres for rc and enable language.
Add rc file to list variable to compile later.

```cmake
set(RES_FILES "")
if(MINGW)
    get_filename_component(RES_FILES "path/to/rc/file/win32.rc" ABSOLUTE)
    set(CMAKE_RC_COMPILER_INIT windres)
    enable_language(RC)
    set(CMAKE_RC_COMPILE_OBJECT
        "<CMAKE_RC_COMPILER> <FLAGS> -O coff <DEFINES> -i <SOURCE> -o <OBJECT>")
endif(MINGW)

add_executable(
        <target>
        <sources>
        ${RES_FILES}
)
```
