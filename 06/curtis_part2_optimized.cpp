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
    tracks.reserve(12);
    tracks.insert(guard);

    while (true) {
        Vec2 step = guard.loc + guard.face;
        if (!grid.on_grid(step)) {
            break;
        }
        if (grid.at(step) != '#') {
            guard.loc = guard.loc + guard.face;
        } else {
            if (std::find(tracks.begin(), tracks.end(), guard) != tracks.end()) {
                return true;
            }
            tracks.insert(guard);
            guard.turn_right();
        }
    }

    return false;
}

vector<Vec2> get_walk(Grid &grid, Guard &walker) {
    grid.at(walker.loc) = 'X';

    while (true) {
        Vec2 step = walker.loc + walker.face;
        if (!grid.on_grid(step)) {
            break;
        }
        if (grid.at(step) != '#') {
            walker.loc = walker.loc + walker.face;
            grid.at(walker.loc) = 'X';
        } else {
            walker.turn_right();
        }
    }
    return grid.all('X');
}

int main (int argc, char *argv[]) {
    std::ifstream ifs2(argv[1]);
    Grid grid(ifs2);
    vector<Vec2> visited_tiles;
    {
        Grid walk = grid;
        Guard walker;
        walker.loc = walk.first('^');
        walker.face = {0, -1};
        visited_tiles = get_walk(walk, walker);
    }
    Guard guard;
    guard.loc = grid.first('^');
    guard.face = {0, -1};

    int acc = 0;
    for (const Vec2 &v : visited_tiles) {
        if (grid.at(v) != '#') {
            Grid test = grid;
            test.at(v) = '#';
            if (creates_loop(test, guard)) {
                ++acc;
            }
        }
    }

    std::printf("Solution: %d!\n", acc);

    return 0;
}

