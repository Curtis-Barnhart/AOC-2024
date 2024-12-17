#include <cstdio>
#include <fstream>
#include <numeric>
#include <ranges>

#include "../06/curtis_grid.hpp"

using std::ranges::views::filter;
using std::ranges::views::transform;

/*
* This could be memoized for extra speed
* or is that called dynamic programming?
*/
int tile_rating(const Vec2 &tile, const Grid &grid) {
    if (grid.at(tile) == '9') {
        return 1;
    }

    std::unordered_map<Vec2, int> map_fil;
    auto filtered = tile.near_taxicab()
        | filter([&](const Vec2 &v){ return grid.on_grid(v); })
        | filter([&](const Vec2 &v){ return grid.at(v) - grid.at(tile) == 1; })
        | transform([&](const Vec2 &v){ return tile_rating(v, grid); });
    return std::accumulate(filtered.begin(), filtered.end(), 0);
}

int main (int argc, char *argv[]) {
    std::ifstream input(argv[1]);
    Grid grid(input);

    auto scores = grid.all('0')
        | transform([&](const Vec2 &v){ return tile_rating(v, grid); });
    int score_sum = std::accumulate(scores.begin(), scores.end(), 0);

    std::printf("Solution: %d!\n", score_sum);
    return 0;
}

