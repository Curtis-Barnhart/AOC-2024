#include <cstdio>
#include <fstream>
#include <unordered_set>

#include "../06/curtis_grid.hpp"


/*
* This could be memoized for extra speed
* or is that called dynamic programming?
*/
int tile_rating(const Vec2 &tile, const Grid &grid) {
    if (grid.at(tile) == '9') {
        return 1;
    }

    int rating_new = 0;
    const vector<Vec2> neighbors_new = grid.filter_on_grid(tile.near_taxicab());
    std::unordered_set<Vec2> set_new(neighbors_new.begin(), neighbors_new.end());

    for (const Vec2 &n : set_new) {
        if (grid.at(n) - grid.at(tile) == 1) {
            rating_new += tile_rating(n, grid);
        }
    }

    return rating_new;
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

