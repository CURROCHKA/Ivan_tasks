#pragma once

// Объект с ценой
class Tradable {
protected:
    int price;

public:
    Tradable();
    Tradable(int price);
    virtual ~Tradable();

    int getPrice() const;
    void setPrice(int price);
};
