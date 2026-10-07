#include "Tradable.h"
#include <stdexcept>

Tradable::Tradable() : price(0) {}

Tradable::Tradable(int price) : price(price) {
    if (price < 0)
        throw std::invalid_argument("Tradable: цена меньше 0");
}

Tradable::~Tradable() {}

int Tradable::getPrice() const { return price; }

void Tradable::setPrice(int price) {
    if (price < 0)
        throw std::invalid_argument("Tradable: цена меньше 0");
    this->price = price;
}
