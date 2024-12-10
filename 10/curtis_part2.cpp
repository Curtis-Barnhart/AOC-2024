#include <cstdio>
#include <fstream>

#include "../06/curtis_grid.hpp"

vector<Vec2> valid_neighbors(const Vec2 &loc, const Grid &g) {
    vector<Vec2> neighbors;
    if (g.on_grid(loc + Vec2(1, 0))) {
        neighbors.push_back(loc + Vec2(1, 0));
    }
    if (g.on_grid(loc + Vec2(0, 1))) {
        neighbors.push_back(loc + Vec2(0, 1));
    }
    if (g.on_grid(loc + Vec2(-1, 0))) {
        neighbors.push_back(loc + Vec2(-1, 0));
    }
    if (g.on_grid(loc + Vec2(0, -1))) {
        neighbors.push_back(loc + Vec2(0, -1));
    }
    return neighbors;
}

/*
* This could be memoized for extra speed
* or is that called dynamic programming?
*/
int tile_rating(const Vec2 &tile, const Grid &grid) {
    if (grid.at(tile) == '9') {
        return 1;
    }

    int rating = 0;
    vector<Vec2> neighbors = valid_neighbors(tile, grid);
    for (const Vec2 &n : neighbors) {
        if (grid.at(n) - grid.at(tile) == 1) {
            rating += tile_rating(n, grid);
        }
    }

    return rating;
}

int main (int argc, char *argv[]) {
    std::ifstream input(argv[1]);
    Grid grid(input);

    int score_sum = 0;
    vector<Vec2> trailheads = grid.all('0');
    for (const Vec2 &th : trailheads) {
        score_sum += tile_rating(th, grid);
    }

    std::printf("Solution: %d!\n", score_sum);
    return 0;
}

