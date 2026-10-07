#include "Cargo.h"
#include <stdexcept>

Cargo::Cargo() : product(nullptr), quantity(0), condition(100) {}

Cargo::Cargo(const Product* product, int quantity, int condition)
    : product(product), quantity(quantity), condition(condition) {
    if (quantity < 0)
        throw std::invalid_argument("Cargo: количество меньше 0");
    if (condition < 0 || condition > 100)
        throw std::invalid_argument("Cargo: состояние вне диапазона 0..100");
}

const Product* Cargo::getProduct() const { return product; }

int Cargo::getQuantity() const { return quantity; }

int Cargo::getCondition() const { return condition; }

void Cargo::setQuantity(int quantity) {
    if (quantity < 0)
        throw std::invalid_argument("Cargo: количество меньше 0");
    this->quantity = quantity;
}

double Cargo::getMass() const {
    if (product == nullptr)
        return 0;
    return quantity * product->getUnitMass();
}

Cargo& Cargo::operator++() {
    quantity++;
    return *this;
}

Cargo Cargo::operator++(int) {
    Cargo old = *this;
    quantity++;
    return old;
}

Cargo& Cargo::operator--() {
    if (quantity > 0)
        quantity--;
    return *this;
}

Cargo Cargo::operator--(int) {
    Cargo old = *this;
    if (quantity > 0)
        quantity--;
    return old;
}

Cargo& Cargo::operator-=(int amount) {
    if (amount < 0)
        throw std::invalid_argument("Cargo: количество меньше 0");
    if (amount > quantity)
        throw std::out_of_range("Cargo: в партии меньше товара");
    quantity -= amount;
    return *this;
}

Cargo operator+(const Cargo& a, const Cargo& b) {
    if (a.product == nullptr || b.product == nullptr || !(*a.product == *b.product))
        throw std::invalid_argument("Cargo: сложение партий разных товаров");
    int total = a.quantity + b.quantity;
    int cond = 100;
    if (total > 0)
        cond = (a.condition * a.quantity + b.condition * b.quantity) / total;
    return Cargo(a.product, total, cond);
}
