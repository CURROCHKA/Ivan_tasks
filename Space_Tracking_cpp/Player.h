#pragma once
#include <vector>
#include "Entity.h"

class Ship;

// Игрок: владелец кораблей и денег
class Player : public Entity {
private:
    int balance;
    std::vector<Ship*> fleet;

public:
    Player();
    Player(const std::string& name, int balance);
    ~Player();

    int getBalance() const;
    void setBalance(int balance);
    bool canPay(int amount) const;
    void pay(int amount);
    void earn(int amount);
    void addShip(Ship* ship);
    Ship& getShip(int index);
    int getFleetSize() const;
    std::string getTypeName() const;
};
