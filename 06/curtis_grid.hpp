#include <algorithm>
#include <cassert>
#include <cmath>
#include <cstddef>
#include <cstdio>
#include <cstdlib>
#include <functional>
#include <istream>
#include <iterator>
#include <list>
#include <numeric>
#include <queue>
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

template<>
struct std::hash<Vec2> {
    std::size_t operator()(const Vec2 &v) const {
        return (v.x << (sizeof(std::size_t) / 2)) ^ v.y;
    }
};

struct Border {
    Vec2 begin, end;

    Border(const Vec2 &v1, const Vec2 &v2) : begin(v1), end(v2) {
        assert(v1.x == v2.x || v1.y == v2.y);
        assert(v1.x != v2.x || v1.y != v2.y);
    }

    /*
     * This is only guaranteed to work if the Borders have valid values
     */
    std::optional<Border> combine(const Border &b) const {
        bool this_y_aligned = (this->begin.y == this->end.y);
        bool other_y_aligned = (b.begin.y == b.end.y);
        bool this_sign_pos, other_sign_pos;
        int min_begin, min_end, max_begin, max_end;
        int t_begin, t_end, o_begin, o_end;

        // This first section will check if the borders are orthogonal to each other
        // If they are, we end. If not, we move on to check...
        if (this_y_aligned && other_y_aligned && (this->begin.y == b.begin.y)) {
            this_sign_pos = (this->end.x - this->begin.x) > 0;
            other_sign_pos = (b.end.x - b.begin.x) > 0;
            t_begin = this->begin.x, t_end = this->end.x;
            o_begin = b.begin.x, o_end = b.end.x;
        } else if (!this_y_aligned && !other_y_aligned && (this->begin.x == b.begin.x)) {
            this_sign_pos = (this->end.y - this->begin.y) > 0;
            other_sign_pos = (b.end.y - b.begin.y) > 0;
            t_begin = this->begin.y, t_end = this->end.y;
            o_begin = b.begin.y, o_end = b.end.y;
        } else {
            // the borders aren't even on the same axis - too bad
            return {};
        }

        // ...if they are facing the same direction on that same axis
        // If they are, we also test if there is overlap between the borders
        if (this_sign_pos && other_sign_pos) {
            if (t_begin < o_begin) {
                min_begin = t_begin, min_end = t_end;
                max_begin = o_begin, max_end = o_end;
            } else {
                min_begin = o_begin, min_end = o_end;
                max_begin = t_begin, max_end = t_end;
            }

            if (max_begin > min_end) {
                // they are aligned on the same axis and direction, but no overlap
                return {};
            }
        } else if (!this_sign_pos && !other_sign_pos) {
            if (t_begin > o_begin) {
                min_begin = t_begin, min_end = t_end;
                max_begin = o_begin, max_end = o_end;
            } else {
                min_begin = o_begin, min_end = o_end;
                max_begin = t_begin, max_end = t_end;
            }

            if (max_begin < min_end) {
                // they are aligned on the same axis and direction, but no overlap
                return {};
            }
        } else {
            // Even though they are aligned on the same axis,
            // the borders go in opposite directions
            return {};
        }

        // If there is overlap, then we return a new border object
        if (this_y_aligned) {
            if (this_sign_pos) {
                return {Border{{min_begin, this->begin.y}, {std::max(min_end, max_end), this->begin.y}}};
            } else {
                return {Border{{min_begin, this->begin.y}, {std::min(min_end, max_end), this->begin.y}}};
            }
        } else {
            if (this_sign_pos) {
                return {Border{{this->begin.x, min_begin}, {this->begin.x, std::max(min_end, max_end)}}};
            } else {
                return {Border{{this->begin.x, min_begin}, {this->begin.x, std::min(min_end, max_end)}}};
            }
        }
    }
};

struct Region {
    std::unordered_set<Vec2> locations;

    Region() {}

    template<typename C>
    explicit Region(C container) : locations(container.begin(), container.end()) {}

    int size() const {
        return locations.size();
    }

    /*
    * rewrite to transform again.
    * TODO: lol there is a much better way to find a perimeter lolll
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

    // TODO: this is possibly one of the worst ways to find the sides lol
    int sides() const {
        std::list<Border> borders;
        // first get every individual border into the list
        for (const Vec2 &v : this->locations) {
            if (!this->locations.contains(v + Vec2{1, 0}))  {
                borders.emplace_back(v, v + Vec2{0, -1});
            }
            if (!this->locations.contains(v + Vec2{0, 1}))  {
                borders.emplace_back(v, v + Vec2{1, 0});
            }
            if (!this->locations.contains(v + Vec2{-1, 0}))  {
                borders.emplace_back(v, v + Vec2{0, 1});
            }
            if (!this->locations.contains(v + Vec2{0, -1}))  {
                borders.emplace_back(v, v + Vec2{-1, 0});
            }
        }

        // then we start combining them with each other from the front on
        std::list<Border>::iterator combine_attempt = borders.begin();
        while (combine_attempt != borders.end()) {
        try_to_combine:
            for (
                auto combine_with = std::next(combine_attempt);
                combine_with != borders.end();
                std::advance(combine_with, 1)
            ) {
                std::optional<Border> combined = combine_attempt->combine(*combine_with);
                if (combined) {
                    if (combine_attempt != borders.begin()) {
                        auto temp = std::prev(combine_attempt);
                        borders.erase(combine_attempt);
                        borders.erase(combine_with);
                        borders.push_back(*combined);
                        combine_attempt = temp;
                    } else {
                        borders.erase(combine_attempt);
                        borders.erase(combine_with);
                        borders.push_back(*combined);
                        combine_attempt = borders.begin();
                        goto try_to_combine;
                    }
                    break;
                }
            }
            std::advance(combine_attempt, 1);
        }

        return borders.size();
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

