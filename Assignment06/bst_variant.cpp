#include <iostream>
#include <memory>
#include <utility>
#include <variant>
#include <vector>

// Combines several lambdas into one visitor so std::visit acts like
// OCaml's `match ... with` (one lambda per case).
template <class... Ts> struct overloaded : Ts... { using Ts::operator()...; };
template <class... Ts> overloaded(Ts...) -> overloaded<Ts...>;

// OCaml: type binary_tree = Empty | Node of int * binary_tree * binary_tree
template <typename T>
class BST {
    struct Empty {};
    struct Node;
    using Tree = std::variant<Empty, std::unique_ptr<Node>>;

    struct Node {
        T value;
        Tree left;
        Tree right;
        explicit Node(T v) : value(std::move(v)), left(Empty{}), right(Empty{}) {}
    };

    Tree root_ = Empty{};

    static void insert(Tree& t, T v) {
        std::visit(overloaded{
            [&](Empty&) { t = std::make_unique<Node>(std::move(v)); },
            [&](std::unique_ptr<Node>& n) {
                if (v < n->value)      insert(n->left, std::move(v));
                else if (n->value < v) insert(n->right, std::move(v));
            }
        }, t);
    }

    static bool contains(const Tree& t, const T& v) {
        return std::visit(overloaded{
            [](const Empty&) { return false; },
            [&](const std::unique_ptr<Node>& n) {
                if (v < n->value) return contains(n->left, v);
                if (n->value < v) return contains(n->right, v);
                return true;
            }
        }, t);
    }

    template <class F> static void inorder(const Tree& t, F& visit) {
        std::visit(overloaded{
            [](const Empty&) {},
            [&](const std::unique_ptr<Node>& n) {
                inorder(n->left, visit);
                visit(n->value);
                inorder(n->right, visit);
            }
        }, t);
    }

    template <class F> static void preorder(const Tree& t, F& visit) {
        std::visit(overloaded{
            [](const Empty&) {},
            [&](const std::unique_ptr<Node>& n) {
                visit(n->value);
                preorder(n->left, visit);
                preorder(n->right, visit);
            }
        }, t);
    }

    template <class F> static void postorder(const Tree& t, F& visit) {
        std::visit(overloaded{
            [](const Empty&) {},
            [&](const std::unique_ptr<Node>& n) {
                postorder(n->left, visit);
                postorder(n->right, visit);
                visit(n->value);
            }
        }, t);
    }

public:
    bool is_empty() const { return std::holds_alternative<Empty>(root_); }
    void insert(T v) { insert(root_, std::move(v)); }
    bool contains(const T& v) const { return contains(root_, v); }

    std::vector<T> inorder() const {
        std::vector<T> out;
        auto f = [&](const T& x) { out.push_back(x); };
        inorder(root_, f);
        return out;
    }
    std::vector<T> preorder() const {
        std::vector<T> out;
        auto f = [&](const T& x) { out.push_back(x); };
        preorder(root_, f);
        return out;
    }
    std::vector<T> postorder() const {
        std::vector<T> out;
        auto f = [&](const T& x) { out.push_back(x); };
        postorder(root_, f);
        return out;
    }
};

template <typename T>
void print(const char* label, const std::vector<T>& v) {
    std::cout << label << ":";
    for (const auto& x : v) std::cout << ' ' << x;
    std::cout << '\n';
}

int main() {
    BST<int> t;
    std::cout << std::boolalpha << "empty at start: " << t.is_empty() << "\n";

    for (int x : {5, 3, 8, 1, 4, 7, 9}) t.insert(x);

    print("inorder  ", t.inorder());
    print("preorder ", t.preorder());
    print("postorder", t.postorder());
    std::cout << "contains 4: " << t.contains(4) << "\n"
              << "contains 6: " << t.contains(6) << "\n";
}