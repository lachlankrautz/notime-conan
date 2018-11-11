#include <iostream>
#include <SDL.h>

int main(int argc, char* argv[]) {
    SDL_Log("hello sdl logs");
    std::cout << "hello stdout\n";

    return 0;
}
