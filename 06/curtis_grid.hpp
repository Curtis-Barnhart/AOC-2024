#include <cmath>
#include <cstddef>
#include <cstdlib>
#include <functional>
#include <istream>
#include <stdexcept>
#include <string>
#include <vector>

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
            neighbors.reserve((radius + 1) * (radius) / 2 + 1);
            neighbors.push_back(*this);
        } else {
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

struct Grid {

    int X, Y;
    vector<vector<char>> values;

    Grid(std::istream &i) {
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
            throw std::out_of_range("nope");
        }
        return this->values.at(y).at(x);
    }

    char &at(const Vec2 &v) {
        return this->at(v.x, v.y);
    }

    char &at(int x, int y) {
        if (x >= this->X || y >= this->Y) {
            throw std::out_of_range("nope");
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

