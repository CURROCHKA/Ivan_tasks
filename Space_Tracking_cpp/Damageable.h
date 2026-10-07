#pragma once
#include "Entity.h"

// Объект с прочностью
class Damageable : public Entity {
protected:
    int maxDurability;
    int durability;

public:
    Damageable();
    Damageable(const std::string& name, int maxDurability);

    int getDurability() const;
    int getMaxDurability() const;
    double getDurabilityPercent() const;
    bool isBroken() const;
    virtual void takeDamage(int damage);
    void repair(int points);
    Damageable& operator-=(int damage);
};
