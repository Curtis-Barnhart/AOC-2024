#include <cmath>
#include <istream>
#include <stdexcept>
#include <string>
#include <vector>

using std::vector;

struct Vec2 {
    int x, y;

    Vec2(int x, int y) : x(x), y(y) {}
    Vec2 operator+(const Vec2 &o) const { return {x + o.x, y + o.y}; }
    Vec2 operator-(const Vec2 &o) const { return {x - o.x, y - o.y}; }
    Vec2 operator*(const int s) const { return {s*x, s*y}; }
    int dot(const Vec2 &o) const { return x*o.x + y*o.y; }
    double norm() const { return std::sqrt(x*x + y*y); }
    double distance(const Vec2 &o) const {return (o - *this).norm(); }
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
    }

    char at(const Vec2 &v) const {
        return this->at(v.x, v.y);
    }

    char at(int x, int y) const {
        if (x >= this->X || y >= this->Y) {
            throw std::out_of_range("nope");
        }
        return this->values.at(y).at(x);
    }
};

