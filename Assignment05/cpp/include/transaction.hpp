#pragma once

#include "store.hpp"

// RAII transaction: snapshots the store on construction and restores the
// snapshot on destruction unless commit() was called.
class Transaction {
public:
    explicit Transaction(Store& store);

    // Keeps the changes. After this, the destructor does nothing.
    void commit() noexcept;

    // Rolls back if not committed.
    ~Transaction();

    // A transaction owns a unique responsibility; copying it would be wrong.
    Transaction(const Transaction&) = delete;
    Transaction& operator=(const Transaction&) = delete;

private:
    Store& store_;
    Store backup_;
    bool committed_{false};
};