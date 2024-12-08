#include <cmath>
#include <cstddef>
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
    double distance(const Vec2 &o) const {return (o - *this).norm(); }
};

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
        }
        this->Y = this->values.size();
        this->X = this->values.back().size();
        for (vector<char> &v : this->values) {
            v.shrink_to_fit();
        }
        this->values.shrink_to_fit();
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

    Vec2 first(char c) {
        for (int x = 0; x < this->X; ++x) {
            for (int y = 0; y < this->Y; ++y) {
                if (this->at(x, y) == c) {
                    return {x, y};
                }
            }
        }
        return {-1, -1};
    }

    vector<Vec2> all(char c) {
        vector<Vec2> instances;
        for (int x = 0; x < this->X; ++x) {
            for (int y = 0; y < this->Y; ++y) {
                if (this->at(x, y) == c) {
                    instances.emplace_back(x, y);
                }
            }
        }
        return instances;
    }

    int count(char c) {
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

