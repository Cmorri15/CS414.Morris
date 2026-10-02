#pragma once

#include <map>
#include <optional>
#include <string>
#include <utility>
#include <vector>

// Owns the key-value data. Contains no console I/O.
// The only I/O is in save()/load(), which use RAII file streams.
class Store {
public:
    // Throws std::invalid_argument if the key is empty or the key/value
    // contains a tab or newline (these would corrupt the save format).
    void set(const std::string& key, const std::string& value);

    std::optional<std::string> get(const std::string& key) const;

    // Returns true if the key existed.
    bool remove(const std::string& key);

    // Sorted (key, value) pairs. Returns a copy so the map is never exposed.
    std::vector<std::pair<std::string, std::string>> list() const;

    std::size_t size() const;

    // Side effects: file I/O. Both throw std::runtime_error on failure.
    void save(const std::string& filename) const;
    void load(const std::string& filename);

private:
    std::map<std::string, std::string> data_;
};