#pragma once
#include "Part.h"

// Корпус
class Hull : public Part {
private:
    int armor;
    int slots;

public:
    Hull();
    Hull(const std::string& name, double mass, int maxDurability, int price, int armor, int slots);

    int getArmor() const;
    int getSlots() const;
    void takeDamage(int damage);
    std::string getTypeName() const;
};
