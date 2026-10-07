#include "Part.h"
#include <stdexcept>

Part::Part() : Damageable(), Tradable(), mass(1) {}

Part::Part(const std::string& name, double mass, int maxDurability, int price)
    : Damageable(name, maxDurability), Tradable(price), mass(mass) {
    if (mass <= 0)
        throw std::invalid_argument("Part: масса не больше 0");
}

double Part::getMass() const { return mass; }

double Part::getTotalMass() const { return mass; }
