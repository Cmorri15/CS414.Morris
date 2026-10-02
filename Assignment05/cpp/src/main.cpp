#include "store.hpp"
#include "transaction.hpp"

#include <algorithm>
#include <cctype>
#include <iostream>
#include <optional>
#include <sstream>
#include <string>

namespace {

std::string to_upper(std::string s) {
    std::transform(s.begin(), s.end(), s.begin(),
                   [](unsigned char c) { return std::toupper(c); });
    return s;
}

// Handles one command line. Returns false when the program should stop.
// All console output happens here, never inside Store.
bool process(const std::string& line, Store& store,
             std::optional<Transaction>& tx) {
    std::istringstream in{line};
    std::string cmd, key;
    in >> cmd >> key;
    std::string rest;
    std::getline(in >> std::ws, rest);  // remainder of line (the value)
    cmd = to_upper(cmd);

    try {
        if (cmd.empty()) {
            // blank line: ignore
        } else if (cmd == "SET") {
            if (key.empty()) { std::cout << "usage: SET key value\n"; }
            else store.set(key, rest);
        } else if (cmd == "GET") {
            if (key.empty()) { std::cout << "usage: GET key\n"; }
            else if (auto v = store.get(key)) std::cout << *v << '\n';
            else std::cout << "(not found)\n";
        } else if (cmd == "DELETE") {
            if (key.empty()) { std::cout << "usage: DELETE key\n"; }
            else if (!store.remove(key)) std::cout << "(not found)\n";
        } else if (cmd == "LIST") {
            for (const auto& [k, v] : store.list())
                std::cout << k << " = " << v << '\n';
        } else if (cmd == "SAVE") {
            if (key.empty()) { std::cout << "usage: SAVE filename\n"; }
            else store.save(key);
        } else if (cmd == "LOAD") {
            if (key.empty()) { std::cout << "usage: LOAD filename\n"; }
            else store.load(key);
        } else if (cmd == "BEGIN") {
            if (tx) std::cout << "transaction already open\n";
            else tx.emplace(store);        // snapshot taken here
        } else if (cmd == "COMMIT") {
            if (!tx) std::cout << "no open transaction\n";
            else { tx->commit(); tx.reset(); }
        } else if (cmd == "ABORT") {
            if (!tx) std::cout << "no open transaction\n";
            else tx.reset();               // destructor rolls back
        } else if (cmd == "QUIT") {
            return false;
        } else {
            std::cout << "unknown command: " << cmd << '\n';
        }
    } catch (const std::exception& e) {
        std::cout << "error: " << e.what() << '\n';
    }
    return true;
}

}  // namespace

int main() {
    Store store;
    std::optional<Transaction> tx;  // empty = no open transaction

    std::string line;
    std::cout << "> " << std::flush;
    while (std::getline(std::cin, line)) {
        if (!process(line, store, tx)) break;
        std::cout << "> " << std::flush;
    }
    // If a transaction is still open here, `tx` is destroyed on return
    // and its destructor rolls the store back.
}