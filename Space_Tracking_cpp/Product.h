#pragma once
#include "Entity.h"
#include "Tradable.h"

// Товар каталога
class Product : public Entity, public Tradable {
private:
    double unitMass;

public:
    Product();
    Product(const std::string& name, int baseCost, double unitMass);

    double getUnitMass() const;
    bool operator==(const Product& other) const;
    std::string getTypeName() const;
};
