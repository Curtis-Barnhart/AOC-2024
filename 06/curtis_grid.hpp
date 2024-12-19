#include <cassert>
#include <cmath>
#include <cstddef>
#include <cstdio>
#include <cstdlib>
#include <functional>
#include <istream>
#include <numeric>
#include <queue>
#include <stdexcept>
#include <string>
#include <unordered_set>
#include <utility>
#include <vector>
#include <ranges>

using std::ranges::views::filter;
using std::ranges::views::transform;
using std::vector;

struct Vec2 {
    int x, y;

    Vec2(int x, int y) : x(x), y(y) {}
    bool operator==(const Vec2 &o) const { return x == o.x && y == o.y; }
    bool operator!=(const Vec2 &o) const { return x != o.x || y != o.y; }
    Vec2 operator+(const Vec2 &o) const { return {x + o.x, y + o.y}; }
    Vec2 operator-(const Vec2 &o) const { return {x - o.x, y - o.y}; }
    Vec2 operator*(const int s) const { return {s*x, s*y}; }
    int dot(const Vec2 &o) const { return x*o.x + y*o.y; }
    double norm() const { return std::sqrt(x*x + y*y); }
    double distance(const Vec2 &o) const { return (o - *this).norm(); }
    int taxicab(const Vec2 &o=Vec2::origin) const { return std::abs(x - o.x) + std::abs(y - o.y); }

    vector<Vec2> near_taxicab(int radius=1, bool contain_self=false) const {
        vector<Vec2> neighbors;
        if (contain_self) {
            // TODO: is this correct?
            neighbors.reserve((radius + 1) * (radius) / 2 + 1);
            neighbors.push_back(*this);
        } else {
            // TODO: is this correct?
            neighbors.reserve((radius + 1) * (radius) / 2);
        }

        radius = std::abs(radius);
        Vec2 rd{1, -1}, ld{-1, -1}, lu{-1, 1}, ru{1, 1};
        while (radius) {
            Vec2 start{this->x, this->y + radius};
            for (int e = radius; e--> 0;) {
                start = start + rd;
                neighbors.emplace_back(start);
            }
            for (int e = radius; e--> 0;) {
                start = start + ld;
                neighbors.emplace_back(start);
            }
            for (int e = radius; e--> 0;) {
                start = start + lu;
                neighbors.emplace_back(start);
            }
            for (int e = radius; e--> 0;) {
                start = start + ru;
                neighbors.emplace_back(start);
            }
            --radius;
        }
        return neighbors;
    }

    vector<Vec2> near_square(int radius=1) {
        // TODO: add way to delete self
        vector<Vec2> neighbors;
        neighbors.reserve((2 * radius + 1) * (2 * radius + 1));
        for (int x = this->x - radius; x <= this->x + radius; ++x) {
            for (int y = this->y - radius; y <= this->y + radius; ++x) {
                neighbors.emplace_back(x, y);
            }
        }
        return neighbors;
    }

    const static Vec2 origin;

};
// yeah uh I'll remove this one day
const Vec2 Vec2::origin{0, 0};

template<>
struct std::hash<Vec2> {
    std::size_t operator()(const Vec2 &v) const {
        return (v.x << (sizeof(std::size_t) / 2)) ^ v.y;
    }
};

struct Border {
    enum ORIENTATION { VERT, HORI };
    Vec2 begin = Vec2::origin, end = Vec2::origin;
    ORIENTATION orientation;

    Border(const Vec2 &v, ORIENTATION o) : begin(v), orientation(o) {}
    Border(const Vec2 &v1, const Vec2 &v2) {
        assert(v1.x == v2.x || v1.y == v2.y);
        assert(v1.x != v2.x || v1.y != v2.y);
        if (v1.x == v2.x) {
            assert(std::abs(v1.y - v2.y) == 1);
            begin = v1.y < v2.y ? v1 : v2;
            orientation = HORI;
        } else {
            begin = v1.x < v2.x ? v1 : v2;
            orientation = HORI;
        }
    }

    bool can_combine(const Border &b) const {
        if (b.orientation != this->orientation) {
            return false;
        }
        if (this->orientation == VERT) {
            
        } else {

        }
    }
};

struct Region {
    std::unordered_set<Vec2> locations;

    Region() {}

    template<typename C>
    explicit Region(C container) {
        this->locations = {container.begin(), container.end()};
    }

    int size() const {
        return locations.size();
    }

    /*
    * rewrite to transform again.
    */
    int perimeter() const {
        int p = 0;
        for (const Vec2 &v : this->locations) {
            auto sides = v.near_taxicab()
                | filter([&](const Vec2 &n){ return !this->locations.contains(n); })
                | transform([&](const Vec2 &n){ return 1; });
            p += std::accumulate(sides.begin(), sides.end(), 0);
        }

        return p;
    }

    bool contains(const Vec2 &v) const {
        return this->locations.contains(v);
    }
};

struct Grid {

    int X, Y;
    vector<vector<char>> values;

    explicit Grid(int size, char fill = ' ') : Grid(size, size, fill) {}

    explicit Grid(int size_x, int size_y, char fill = ' ') {
        this->X = size_x;
        this->Y = size_y;
        this->values.reserve(size_y);
        while (size_y-->0) {
            this->values.emplace_back();
            this->values.back().reserve(size_x);
            int x_cp = size_x;
            while (x_cp-->0) {
                this->values.back().emplace_back(fill);
            }
        }
    }

    explicit Grid(std::istream &i) {
        std::string line;
        while (std::getline(i, line)) {
            this->values.emplace_back();
            for (const char &c : line) {
                this->values.back().push_back(c);
            }
            this->values.back().shrink_to_fit();
        }
        this->values.shrink_to_fit();

        this->Y = this->values.size();
        this->X = this->values.back().size();
    }

    const char &at(const Vec2 &v) const {
        return this->at(v.x, v.y);
    }

    const char &at(int x, int y) const {
        if (x >= this->X || y >= this->Y) {
            throw std::out_of_range("Grid access out of range.");
        }
        return this->values.at(y).at(x);
    }

    char &at(const Vec2 &v) {
        return this->at(v.x, v.y);
    }

    char &at(int x, int y) {
        if (x >= this->X || y >= this->Y) {
            throw std::out_of_range("Grid access out of range.");
        }
        return this->values.at(y).at(x);
    }

    bool on_grid(const Vec2 &v) const {
        return this->on_grid(v.x, v.y);
    }

    bool on_grid(int x, int y) const {
        return (x < this->X && x >= 0 && y < this->Y && y >= 0);
    }

    vector<Vec2> filter_on_grid(vector<Vec2> &&locations) const {
        vector<Vec2>::iterator reader = locations.begin(),
                               writer = reader;
        while (reader < locations.end()) {
            if (this->on_grid(*reader)) {
                *writer++ = *reader++;
            } else {
                ++reader;
            }
        }
        locations.erase(writer, locations.end());
        return locations;
    }

    vector<Vec2> &filter_on_grid(vector<Vec2> &locations) const {
        vector<Vec2>::iterator reader = locations.begin(),
                               writer = reader;
        while (reader < locations.end()) {
            if (this->on_grid(*reader)) {
                *writer++ = *reader++;
            } else {
                ++reader;
            }
        }
        locations.erase(writer, locations.end());
        return locations;
    }

    Vec2 first(char c) const {
        for (int x = 0; x < this->X; ++x) {
            for (int y = 0; y < this->Y; ++y) {
                if (this->at(x, y) == c) {
                    return {x, y};
                }
            }
        }
        return {-1, -1};
    }

    vector<Vec2> all(char c) const {
        vector<Vec2> instances;
        instances.reserve(this->X * this->Y);
        for (int x = 0; x < this->X; ++x) {
            for (int y = 0; y < this->Y; ++y) {
                if (this->at(x, y) == c) {
                    instances.emplace_back(x, y);
                }
            }
        }
        instances.shrink_to_fit();
        return instances;
    }
    
    template<typename F>
    vector<Vec2> select_where(F &&lambda) const {
        vector<Vec2> vecs;
        vecs.reserve(this->X * this->Y);
        for (int x = 0; x < this->X; ++x) {
            for (int y = 0; y < this->Y; ++y) {
                if (lambda(Vec2(x, y))) {
                    vecs.emplace_back(x, y);
                }
            }
        }
        vecs.shrink_to_fit();
    }

    Region region(const Vec2 &v) const {
        assert(this->on_grid(v));

        vector<Vec2> stack;
        std::unordered_set<Vec2> counted;

        stack.push_back(v);
        counted.insert(v);
        while (!stack.empty()) {
            Vec2 current = stack.back();
            stack.pop_back();

            auto neighs = current.near_taxicab()
                | filter([&](const Vec2 &n){ return this->on_grid(n); })
                | filter([&](const Vec2 &n){ return !counted.contains(n); })
                | filter([&](const Vec2 &n){ return this->at(n) == this->at(v); });
            stack.insert(stack.end(), neighs.begin(), neighs.end());
            counted.insert(neighs.begin(), neighs.end());
        }

        return Region(counted);
    }

    std::optional<vector<Vec2>> path_shortest_breadth(
        const Vec2 &src,
        const Vec2 &dst,
        const vector<char> &wall_types
    ) const {
        assert(this->on_grid(src));
        assert(this->on_grid(dst));

        std::unordered_map<Vec2, Vec2> path_links;
        path_links.reserve(this->X * this->Y);

        Grid visited = *this;
        for (char t : wall_types) {
            for (const Vec2 &v : this->all(t)) {
                visited.at(v) = '-';
            }
        }

        std::queue<Vec2> frontier;
        frontier.push(src);
        visited.at(src) = '-';

        while (!frontier.empty()) {
            Vec2 cur = frontier.front();
            frontier.pop();

            if (cur == dst) {
                vector<Vec2> path{dst};
                path.reserve((src - dst).taxicab());

                Vec2 trail = dst;
                while (path_links.contains(trail)) {
                    path.push_back(path_links.at(trail));
                    trail = path.back();
                }

                return {std::move(path)};
            } else {
                for (const Vec2 &neigh : cur.near_taxicab()
                    | filter([&](const Vec2 &v){ return this->on_grid(v); })
                    | filter([&](const Vec2 &v){ return visited.at(v) != '-'; })
                ) {
                    visited.at(neigh) = '-';
                    path_links.insert({neigh, cur});
                    frontier.push(neigh);
                }
            }
        }

        return {};
    }

    // Region path_shortest(
    //     const Vec2 &src,
    //     const Vec2 &dst,
    //     const std::unordered_set<char> &wall_types
    // ) {
    //     struct Vec2Cost {
    //         Vec2 v;
    //         int cost;
    //     };

    //     struct CostEstimate {
    //         bool operator()(const Vec2Cost &v1, const Vec2Cost &v2) const {
    //             return v1.cost < v2.cost;
    //         }
    //     };

    //     std::priority_queue<Vec2Cost, vector<Vec2Cost>, CostEstimate> heap(CostEstimate{});
    //     heap.push({src, (dst - src).taxicab()});
    // }

    int count(char c) const {
        int acc = 0;
        for (int x = 0; x < this->X; ++x) {
            for (int y = 0; y < this->Y; ++y) {
                if (this->at(x, y) == c) {
                    ++acc;
                }
            }
        }
        return acc;
    }
};

