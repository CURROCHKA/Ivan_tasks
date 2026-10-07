#pragma once
#include "Part.h"

// Топливный бак
class FuelTank : public Part {
private:
    double fuelCapacity;
    double fuel;

public:
    FuelTank();
    FuelTank(const std::string& name, double mass, int maxDurability, int price, double fuelCapacity);

    double getFuelCapacity() const;
    double getFuel() const;
    double refuel(double amount);
    bool consumeFuel(double amount);
    void takeDamage(int damage);
    double getTotalMass() const;
    std::string getTypeName() const;
};
