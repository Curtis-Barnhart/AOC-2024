#include <algorithm>
#include <cstdio>
#include <fstream>
#include <unordered_set>

#include "curtis_grid.hpp"

struct Guard {
    Vec2 loc{0, 0}, face{0, 0};

    bool operator==(const Guard &g) const { return loc == g.loc && face == g.face; }
    bool operator!=(const Guard &g) const { return loc != g.loc || face != g.face; }

    void turn_right() {
        if (this->face == Vec2{0, -1}) {
            this->face = {1, 0};
        } else if (this->face == Vec2{1, 0}) {
            this->face = {0, 1};
        } else if (this->face == Vec2{0, 1}) {
            this->face = {-1, 0};
        } else if (this->face == Vec2{-1, 0}) {
            this->face = {0, -1};
        }
    }
};

template<>
struct std::hash<Guard> {
    std::size_t operator()(const Guard &g) const {
        return (std::hash<Vec2>{}(g.loc) << (sizeof(std::size_t) / 2))
                ^ std::hash<Vec2>{}(g.face);
    }
};

bool creates_loop(const Grid &grid, Guard guard) {
    std::unordered_set<Guard> tracks;
    tracks.insert(guard);

    while (true) {
        step_action:
        Vec2 step = guard.loc + guard.face;
        if (!grid.on_grid(step)) {
            break;
        }
        if (grid.at(step) != '#') {
            guard.loc = guard.loc + guard.face;
            if (std::find(tracks.begin(), tracks.end(), guard) != tracks.end()) {
                return true;
            }
            tracks.insert(guard);
        } else {
            guard.turn_right();
            goto step_action;
        }
    }

    return false;
}

int main (int argc, char *argv[]) {
    std::ifstream ifs2(argv[1]);
    Grid grid2(ifs2);
    Guard guard2;
    guard2.loc = grid2.first('^');
    guard2.face = {0, -1};

    int acc = 0;
    for (int x = 0; x < grid2.X; ++x) {
        for (int y = 0; y < grid2.Y; ++y) {
            if (grid2.at(x, y) != '#') {
                // std::printf("Starting (%d, %d)\n", x, y);
                Grid test = grid2;
                test.at(x, y) = '#';
                if (creates_loop(test, guard2)) {
                    // std::printf("(%d, %d)\n", x, y);
                    ++acc;
                }
                // std::printf("Finishing (%d, %d)\n", x, y);
            }
        }
    }

    std::printf("Solution: %d!\n", acc);

    return 0;
}

