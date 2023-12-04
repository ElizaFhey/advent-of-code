#include <boost/spirit/home/qi.hpp>
#include <boost/phoenix.hpp>
#include <boost/fusion/adapted/struct.hpp>
#include <boost/fusion/adapted/std_tuple.hpp>
#include <iostream>
#include <fstream>
#include <string_view>
#include <map>
#include <tuple>
#include <utility>

struct hand
{
    int red = 0;
    int green = 0;
    int blue = 0;
};

//using hand = std::map<std::string, int>;

struct game
{
    int game_num;
    std::vector<hand> hands;
};

BOOST_FUSION_ADAPT_STRUCT(game,
    (int, game_num)
    (std::vector<hand>, hands)
);

game parse_game(std::string_view text)
{
    namespace qi = boost::spirit::qi;
    namespace phx = boost::phoenix;

    auto action = [](std::vector<std::tuple<int, std::string>> val) -> hand
    {
        hand h;
        for(auto const& crule : val)
        {
            auto [value, name] = crule;
            if(name == "red")
                h.red += value;
            else if(name == "green")
                h.green += value;
            else if(name == "blue")
                h.blue += value;
        }

        return h;
    };

    using it = std::string_view::iterator;

    qi::rule<it, std::string(), qi::ascii::space_type> string_rule = +qi::ascii::alpha;
    qi::rule<it, std::tuple<int, std::string>(), qi::ascii::space_type> color_rule = qi::int_ >> string_rule;
    qi::rule<it, hand(), qi::ascii::space_type> hand_rule = (color_rule % ",")[qi::_val = phx::bind(action, qi::_1)];
    qi::rule<it, game(), qi::ascii::space_type> game_rule = qi::lit("Game") >> qi::int_ >> ":" >> (hand_rule % ";");

    // game out;
    auto b = text.begin(), e = text.end();
    game out;
    qi::phrase_parse(b, e, game_rule, qi::ascii::space, out);
    return out;
}

int main(int argc, char** argv)
{
    std::ifstream finp{"Problem 2/input.txt"};
    std::string line;
    int total = 0;
    while(std::getline(finp, line))
    {
        game g = parse_game(line);
        std::cout << "Found game " << g.game_num << "\n";
        for(auto h : g.hands)
        {
            std::cout << "\tHand " << h.blue << " blue, " << h.green << " green, " << h.red << " red\n";
        }

        if(argv[1] == "part1")
        {   
            if(std::all_of(g.hands.begin(), g.hands.end(), [](hand const& h) { return h.red <= 12 && h.green <= 13 && h.blue <= 14; }))
            {
                total += g.game_num;
            }
        }
        else
        {
            #define CHECK_COLOR(color) int color = std::max_element(g.hands.begin(), g.hands.end(), [](hand const& l, hand const& r) { return l.color < r.color; })->color
            CHECK_COLOR(red);
            CHECK_COLOR(green);
            CHECK_COLOR(blue);
            total += red * green * blue;
        }
    }

    std::cout << "Found solution: " << total << std::endl;
    return 0;
}