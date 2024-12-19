#include <cstdio>
#include <fstream>
#include <optional>

#include "../06/curtis_grid.hpp"

int main(int argc, char *argv[]) {
    std::ifstream input(argv[1]);
    Grid grid(71);

    int x, y, times = 1024;
    while (times-->0) {
        input >> x;
        input.seekg(1, std::ios_base::cur);
        input >> y;
        grid.at(x, y) = '#';
    }

    std::optional<vector<Vec2>> path = grid.path_shortest_breadth({0, 0}, {70, 70}, {'#'});
    for (const Vec2 &p : *path) {
        grid.at(p) = 'p';
    }

    while (path) {
        input >> x;
        input.seekg(1, std::ios_base::cur);
        input >> y;

        if (grid.at(x, y) == 'p') {
            grid.at(x, y) = '#';
            for (const Vec2 &v : grid.all('p')) {
                grid.at(v) = ' ';
            }
            path = grid.path_shortest_breadth({0, 0}, {70, 70}, {'#'});
            if (path) {
                for (const Vec2 &p : *path) {
                    grid.at(p) = 'p';
                }
            }
        } else {
            grid.at(x, y) = '#';
        }
    }

    std::printf("Solution: (%d, %d)!\n", x, y);
    return 0;
}

