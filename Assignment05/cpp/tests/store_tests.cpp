#include "store.hpp"
#include "transaction.hpp"

#include <filesystem>
#include <fstream>
#include <iostream>
#include <stdexcept>
#include <string>
#include <utility>
#include <vector>

static int failures = 0;
#define CHECK(cond)                                                    \
    do {                                                               \
        if (!(cond)) {                                                 \
            std::cerr << "FAIL line " << __LINE__ << ": " #cond "\n";  \
            ++failures;                                                \
        }                                                              \
    } while (0)

void test_set_get() {
    Store s;
    s.set("name", "Ada");
    CHECK(s.get("name") == "Ada");
    s.set("name", "Grace");  // overwrite
    CHECK(s.get("name") == "Grace");
    CHECK(!s.get("missing").has_value());
}

void test_delete() {
    Store s;
    s.set("a", "1");
    CHECK(s.remove("a"));
    CHECK(!s.get("a").has_value());
    CHECK(!s.remove("a"));  // already gone
}

void test_list_sorted() {
    Store s;
    s.set("b", "2");
    s.set("a", "1");
    std::vector<std::pair<std::string, std::string>> expected{{"a", "1"}, {"b", "2"}};
    CHECK(s.list() == expected);
}

void test_invalid_input() {
    Store s;
    bool threw = false;
    try { s.set("", "v"); } catch (const std::invalid_argument&) { threw = true; }
    CHECK(threw);
    threw = false;
    try { s.set("k", "a\tb"); } catch (const std::invalid_argument&) { threw = true; }
    CHECK(threw);
}

void test_transaction_rollback() {
    Store s;
    s.set("x", "10");
    {
        Transaction tx{s};
        s.set("x", "20");
        s.set("y", "30");
        // no commit -> rollback at end of scope
    }
    CHECK(s.get("x") == "10");
    CHECK(!s.get("y").has_value());
}

void test_transaction_commit() {
    Store s;
    s.set("x", "10");
    {
        Transaction tx{s};
        s.set("x", "20");
        s.set("y", "30");
        tx.commit();
    }
    CHECK(s.get("x") == "20");
    CHECK(s.get("y") == "30");
}

void test_transaction_rollback_on_exception() {
    Store s;
    s.set("x", "10");
    try {
        Transaction tx{s};
        s.set("x", "20");
        s.set("", "bad");  // throws
        tx.commit();       // never reached
    } catch (const std::invalid_argument&) {}
    CHECK(s.get("x") == "10");
}

void test_save_load_roundtrip() {
    auto path = (std::filesystem::temp_directory_path() / "kv_test.txt").string();
    Store a;
    a.set("name", "Ada Lovelace");  // value with a space
    a.set("language", "C++");
    a.save(path);

    Store b;
    b.set("stale", "gone");
    b.load(path);
    CHECK(b.list() == a.list());
    CHECK(!b.get("stale").has_value());  // load replaces contents
    std::filesystem::remove(path);
}

void test_load_errors() {
    Store s;
    s.set("keep", "me");

    bool threw = false;
    try { s.load("/no/such/file.txt"); } catch (const std::runtime_error&) { threw = true; }
    CHECK(threw);

    auto path = (std::filesystem::temp_directory_path() / "kv_bad.txt").string();
    { std::ofstream out{path}; out << "no tab on this line\n"; }
    threw = false;
    try { s.load(path); } catch (const std::runtime_error&) { threw = true; }
    CHECK(threw);
    CHECK(s.get("keep") == "me");  // store untouched by failed load
    std::filesystem::remove(path);
}

int main() {
    test_set_get();
    test_delete();
    test_list_sorted();
    test_invalid_input();
    test_transaction_rollback();
    test_transaction_commit();
    test_transaction_rollback_on_exception();
    test_save_load_roundtrip();
    test_load_errors();

    if (failures == 0) std::cout << "All C++ tests passed\n";
    return failures == 0 ? 0 : 1;
}