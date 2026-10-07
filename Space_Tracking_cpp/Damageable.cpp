#include "Damageable.h"
#include <stdexcept>

Damageable::Damageable() : Entity(), maxDurability(100), durability(100) {}

Damageable::Damageable(const std::string& name, int maxDurability)
    : Entity(name), maxDurability(maxDurability), durability(maxDurability) {
    if (maxDurability < 1)
        throw std::invalid_argument("Damageable: прочность меньше 1");
}

int Damageable::getDurability() const { return durability; }

int Damageable::getMaxDurability() const { return maxDurability; }

double Damageable::getDurabilityPercent() const {
    return (double)durability / maxDurability * 100.0;
}

bool Damageable::isBroken() const { return durability == 0; }

void Damageable::takeDamage(int damage) {
    if (damage < 0)
        throw std::invalid_argument("Damageable: урон меньше 0");
    durability -= damage;
    if (durability < 0)
        durability = 0;
}

void Damageable::repair(int points) {
    if (points < 0)
        throw std::invalid_argument("Damageable: ремонт меньше 0");
    durability += points;
    if (durability > maxDurability)
        durability = maxDurability;
}

Damageable& Damageable::operator-=(int damage) {
    takeDamage(damage);
    return *this;
}
