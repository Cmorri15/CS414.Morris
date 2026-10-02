#include "transaction.hpp"

#include <utility>

Transaction::Transaction(Store& store)
    : store_{store}, backup_{store} {}  // copy of current state

void Transaction::commit() noexcept {
    committed_ = true;
}

Transaction::~Transaction() {
    if (!committed_) {
        store_ = std::move(backup_);  // rollback
    }
}