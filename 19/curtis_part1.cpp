#include <cassert>
#include <cstddef>
#include <cstdio>
#include <fstream>
#include <numeric>
#include <ranges>
#include <string>
#include <string_view>
#include <vector>

using std::vector;
using std::string;
using std::string_view;
using std::ranges::views::transform;

bool can_pattern(
    const std::string_view &pattern,
    const vector<string_view> &towels
) {
    assert(pattern.size() < 100);
    bool sub_probs[100] { true };

    for (size_t prob_ind = 1; prob_ind <= pattern.size(); ++prob_ind) {
        string_view prob_str = pattern.substr(pattern.size() - prob_ind, prob_ind);
        for (string_view towel : towels) {
            if (
                prob_str.starts_with(towel)
                && sub_probs[prob_str.size() - towel.size()]
            ) {
                sub_probs[prob_ind] = true;
                break;
            }
        }
    }
    
    return sub_probs[pattern.size()];
}

vector<string_view> split(const string_view &s, const string &delim) {
    vector<string_view> strings;
    size_t start = 0, end = -2;
    while (start = end + 2, (end = s.find(delim, start)) != string::npos) {
        strings.push_back(s.substr(start, end - start));
    }
    strings.push_back(s.substr(start, s.size() - start));
    return strings;
}

int main (int argc, char *argv[]) {
    std::ifstream input(argv[1]);

    string first_line;
    std::getline(input, first_line);
    string_view first_line_view(first_line);
    vector<string_view> towels = split(first_line_view, ", ");

    vector<string> pattern_strings;
    while (input >> pattern_strings.emplace_back());
    pattern_strings.pop_back();
    vector<string_view> pattern_views;
    for (const string &s : pattern_strings) {
        pattern_views.emplace_back(s);
    }

    auto possible = pattern_views
        | transform([&](const string_view &p){ return can_pattern(p, towels); });
    std::printf("Solution: %d!\n", std::accumulate(possible.begin(), possible.end(), 0));

    return 0;
}

