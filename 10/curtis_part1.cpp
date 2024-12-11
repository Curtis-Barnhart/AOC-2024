#include <cstdio>
#include <fstream>
#include <unordered_set>
#include <ranges>
#include <numeric>

#include "../06/curtis_grid.hpp"

using std::ranges::views::transform;

int th_score(const Vec2 &th, const Grid &g) {
    std::unordered_set<Vec2> visited;
    vector<Vec2> stack;
    visited.insert(th);
    stack.push_back(th);
    int score = 0;

    while (!stack.empty()) {
        Vec2 next = stack.back();
        stack.pop_back();

        if (g.at(next) == '9') {
            ++score;
        } else {
            vector<Vec2> neighbors = g.filter_on_grid(next.near_taxicab());
            for (const Vec2 &n : neighbors) {
                if (
                    visited.find(n) == visited.end()
                    && g.at(n) - g.at(next) == 1
                ) {
                    visited.insert(n);
                    stack.push_back(n);
                }
            }
        }
    }

    return score;
}

int main (int argc, char *argv[]) {
    std::ifstream input(argv[1]);
    Grid grid(input);

    auto scores = grid.all('0')
        | transform([&](const Vec2 &v) { return th_score(v, grid); });
    int score_sum = std::accumulate(scores.begin(), scores.end(), 0);

    std::printf("Solution: %d!\n", score_sum);
    return 0;
}

