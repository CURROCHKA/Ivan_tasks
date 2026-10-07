#pragma once
#include "Damageable.h"
#include "Tradable.h"

// Деталь корабля (абстрактный класс)
class Part : public Damageable, public Tradable {
protected:
    double mass;

public:
    Part();
    Part(const std::string& name, double mass, int maxDurability, int price);

    double getMass() const;
    virtual double getTotalMass() const;
    virtual std::string getTypeName() const = 0;
};
