#include "Engine.h"
#include <stdexcept>

Engine::Engine() : Part(), power(100), fuelConsumption(1) {}

Engine::Engine(const std::string& name, double mass, int maxDurability, int price,
               double power, double fuelConsumption)
    : Part(name, mass, maxDurability, price), power(power), fuelConsumption(fuelConsumption) {
    if (power <= 0 || fuelConsumption <= 0)
        throw std::invalid_argument("Engine: мощность или расход не больше 0");
}

double Engine::getPower() const { return power; }

double Engine::getFuelConsumption() const { return fuelConsumption; }

double Engine::getFuelForDistance(double distance) const {
    return distance * fuelConsumption;
}

double Engine::getSpeed(double shipMass) const {
    if (isBroken() || shipMass <= 0)
        return 0;
    return power / shipMass;
}

std::string Engine::getTypeName() const { return "Двигатель"; }
