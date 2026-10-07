#include "Hull.h"
#include <stdexcept>

Hull::Hull() : Part(), armor(0), slots(3) {}

Hull::Hull(const std::string& name, double mass, int maxDurability, int price, int armor, int slots)
    : Part(name, mass, maxDurability, price), armor(armor), slots(slots) {
    if (armor < 0 || armor > 80)
        throw std::invalid_argument("Hull: броня вне диапазона 0..80");
    if (slots < 1)
        throw std::invalid_argument("Hull: мест меньше 1");
}

int Hull::getArmor() const { return armor; }

int Hull::getSlots() const { return slots; }

void Hull::takeDamage(int damage) {
    if (damage < 0)
        throw std::invalid_argument("Hull: урон меньше 0");
    int reduced = damage * (100 - armor) / 100;
    Damageable::takeDamage(reduced);
}

std::string Hull::getTypeName() const { return "Корпус"; }
