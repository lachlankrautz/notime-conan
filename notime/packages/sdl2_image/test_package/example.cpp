#include <iostream>
#include <SDL_image.h>

int main(int argc, char* argv[]) {
    std::cout << "Loading image " << argv[1] << "\n";;
    SDL_Surface* img = IMG_Load(argv[1]);
    if (img == nullptr) {
        std::cout << "Error: " << SDL_GetError() << "\n";
        return 1;
    } else {
        std::cout << "Image loaded (" << img << ")\n";
    }

    return 0;
}
