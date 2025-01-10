#include <cstdio>
#include <fstream>
#include <ranges>

#include "../06/curtis_grid.hpp"

using std::ranges::views::transform;

int main (int argc, char *argv[]) {
    std::ifstream input(argv[1]);
    Grid grid(input);

    vector<Region> regions;

    for (int x = 0; x < grid.X; ++x) {
        for (int y = 0; y < grid.Y; ++y) {
            if (!std::any_of(
                regions.begin(),
                regions.end(),
                [=](const Region &r){ return r.contains({x, y}); }
            )) {
                regions.push_back(grid.region({x, y}));
            }
        }
    }

    auto fences = regions
        | transform([&](const Region &r){ return r.size() * r.sides(); });
    int solution = std::accumulate(fences.begin(), fences.end(), 0);

    std::printf("Solution: %d!\n", solution);
    return 0;
}

