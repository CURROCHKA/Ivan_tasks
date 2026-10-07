#pragma once
#include "Part.h"

// Двигатель
class Engine : public Part {
private:
    double power;
    double fuelConsumption;

public:
    Engine();
    Engine(const std::string& name, double mass, int maxDurability, int price,
           double power, double fuelConsumption);

    double getPower() const;
    double getFuelConsumption() const;
    double getFuelForDistance(double distance) const;
    double getSpeed(double shipMass) const;
    std::string getTypeName() const;
};
