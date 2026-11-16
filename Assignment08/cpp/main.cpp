
#include "file_handle.hpp"

#include <iostream>
#include <stdexcept>
#include <string>

int count_matches_cpp(const std::string& path,
                      const std::string& needle,
                      bool fail_after_first_line = false) {
    if (needle.empty()) {
        throw std::invalid_argument("Search string cannot be empty");
    }

    FileHandle file(path);

    int count = 0;
    std::string line;
    int ch;
    
    while ((ch = std::fgetc(file.get())) != EOF) {
        if (ch == '\n') {
            if (line.find(needle) != std::string::npos) {
                ++count;
            }

            line.clear();

            if (fail_after_first_line) {
                throw std::runtime_error("Simulated failure");
            }
        } else {
            line += static_cast<char>(ch);
        }
    }

    if (!line.empty()) {
        if (line.find(needle) != std::string::npos) {
            ++count;
        }

        if (fail_after_first_line) {
            throw std::runtime_error("Simulated failure");
        }
    }

    return count;
}

int main() {
    try {
        std::string path = "data/sample.txt";

        std::cout << "Matches for red: "
                  << count_matches_cpp(path, "red") << '\n';

        std::cout << "Matches for orange: "
                  << count_matches_cpp(path, "orange") << '\n';

        std::cout << "Matches for empty file: "
                  << count_matches_cpp("data/empty.txt", "red") << '\n';

        try {
            count_matches_cpp("data/missing.txt", "red");
        } catch (const std::exception& e) {
            std::cout << "Missing file: " << e.what() << '\n';
        }

        try {
            count_matches_cpp(path, "");
        } catch (const std::exception& e) {
            std::cout << "Empty needle: " << e.what() << '\n';
        }

         std::cout << "Matches for long line: "
                  << count_matches_cpp("data/long.txt", "red") << '\n';

        std::cout << "Testing forced failure:\n";
        count_matches_cpp(path, "red", true);

    } catch (const std::exception& e) {
        std::cout << "Error: " << e.what() << '\n';
    }

    return 0;
}
