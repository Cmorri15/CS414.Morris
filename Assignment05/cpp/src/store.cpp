#include "store.hpp"

#include <fstream>
#include <stdexcept>

namespace {
bool has_bad_char(const std::string& s) {
    return s.find_first_of("\t\n\r") != std::string::npos;
}
}  // namespace

void Store::set(const std::string& key, const std::string& value) {
    if (key.empty() || has_bad_char(key) || has_bad_char(value)) {
        throw std::invalid_argument(
            "key must be non-empty; key/value may not contain tabs or newlines");
    }
    data_[key] = value;
}

std::optional<std::string> Store::get(const std::string& key) const {
    auto it = data_.find(key);
    if (it == data_.end()) return std::nullopt;
    return it->second;
}

bool Store::remove(const std::string& key) {
    return data_.erase(key) > 0;
}

std::vector<std::pair<std::string, std::string>> Store::list() const {
    return {data_.begin(), data_.end()};
}

std::size_t Store::size() const {
    return data_.size();
}

void Store::save(const std::string& filename) const {
    std::ofstream out{filename};  // RAII: file closes when `out` goes out of scope
    if (!out) throw std::runtime_error("cannot open file for writing: " + filename);

    for (const auto& [key, value] : data_) {
        out << key << '\t' << value << '\n';
    }
    if (!out) throw std::runtime_error("write failed: " + filename);
}

void Store::load(const std::string& filename) {
    std::ifstream in{filename};  // RAII again
    if (!in) throw std::runtime_error("cannot open file for reading: " + filename);

    // Parse into a temporary so a bad file never leaves the store half-loaded.
    std::map<std::string, std::string> loaded;
    std::string line;
    while (std::getline(in, line)) {
        if (line.empty()) continue;
        auto tab = line.find('\t');
        if (tab == std::string::npos || tab == 0) {
            throw std::runtime_error("malformed line in " + filename + ": " + line);
        }
        loaded[line.substr(0, tab)] = line.substr(tab + 1);
    }

    data_ = std::move(loaded);  // commit only after a fully successful parse
}