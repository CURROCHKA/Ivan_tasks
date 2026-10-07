#pragma once
#include "Product.h"

// Партия груза: количество единиц одного товара и их состояние
class Cargo {
private:
    const Product* product;
    int quantity;
    int condition;

public:
    Cargo();
    Cargo(const Product* product, int quantity, int condition = 100);

    const Product* getProduct() const;
    int getQuantity() const;
    int getCondition() const;
    void setQuantity(int quantity);
    double getMass() const;

    Cargo& operator++();
    Cargo operator++(int);
    Cargo& operator--();
    Cargo operator--(int);
    Cargo& operator-=(int amount);

    friend Cargo operator+(const Cargo& a, const Cargo& b);
};
