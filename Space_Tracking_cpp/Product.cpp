#include "Product.h"
#include <stdexcept>

Product::Product() : Entity(), Tradable(), unitMass(1) {}

Product::Product(const std::string& name, int baseCost, double unitMass)
    : Entity(name), Tradable(baseCost), unitMass(unitMass) {
    if (unitMass <= 0)
        throw std::invalid_argument("Product: масса единицы не больше 0");
}

double Product::getUnitMass() const { return unitMass; }

bool Product::operator==(const Product& other) const {
    return name == other.name;
}

std::string Product::getTypeName() const { return "Товар"; }
