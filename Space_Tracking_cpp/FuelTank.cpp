#include "FuelTank.h"
#include "Constants.h"
#include <stdexcept>

FuelTank::FuelTank() : Part(), fuelCapacity(100), fuel(0) {}

FuelTank::FuelTank(const std::string& name, double mass, int maxDurability, int price, double fuelCapacity)
    : Part(name, mass, maxDurability, price), fuelCapacity(fuelCapacity), fuel(0) {
    if (fuelCapacity <= 0)
        throw std::invalid_argument("FuelTank: объём не больше 0");
}

double FuelTank::getFuelCapacity() const { return fuelCapacity; }

double FuelTank::getFuel() const { return fuel; }

double FuelTank::refuel(double amount) {
    if (amount < 0)
        throw std::invalid_argument("FuelTank: количество меньше 0");
    double added = fuelCapacity - fuel;
    if (amount < added)
        added = amount;
    fuel += added;
    return added;
}

bool FuelTank::consumeFuel(double amount) {
    if (amount < 0)
        throw std::invalid_argument("FuelTank: количество меньше 0");
    if (fuel < amount)
        return false;
    fuel -= amount;
    return true;
}

void FuelTank::takeDamage(int damage) {
    Damageable::takeDamage(damage);
    if (isBroken())
        fuel = 0;
}

double FuelTank::getTotalMass() const {
    return mass + fuel * FUEL_UNIT_MASS;
}

std::string FuelTank::getTypeName() const { return "Топливный бак"; }
