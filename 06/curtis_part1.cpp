#include <cstdio>
#include <fstream>

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

int main (int argc, char *argv[]) {
    std::ifstream ifs(argv[1]);
    Grid grid(ifs);
    Guard guard;
    guard.loc = grid.first('^');
    guard.face = {0, -1};
    grid.at(guard.loc) = 'X';

    while (true) {
        step_action:
        Vec2 step = guard.loc + guard.face;
        if (!grid.on_grid(step)) {
            break;
        }
        if (grid.at(step) != '#') {
            guard.loc = guard.loc + guard.face;
            grid.at(guard.loc) = 'X';
        } else {
            guard.turn_right();
            goto step_action;
        }
    }

    printf("Solution: %d!\n", grid.count('X'));

    return 0;
}

