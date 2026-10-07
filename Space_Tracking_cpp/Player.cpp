#include "Player.h"
#include "Ship.h"
#include <stdexcept>

Player::Player() : Entity(), balance(0) {}

Player::Player(const std::string& name, int balance) : Entity(name), balance(balance) {
    if (balance < 0)
        throw std::invalid_argument("Player: баланс меньше 0");
}

Player::~Player() {
    for (size_t i = 0; i < fleet.size(); i++)
        delete fleet[i];
}

int Player::getBalance() const { return balance; }

void Player::setBalance(int balance) {
    if (balance < 0)
        throw std::invalid_argument("Player: баланс меньше 0");
    this->balance = balance;
}

bool Player::canPay(int amount) const { return balance >= amount; }

void Player::pay(int amount) {
    if (amount < 0)
        throw std::invalid_argument("Player: сумма меньше 0");
    if (!canPay(amount))
        throw std::runtime_error("Player: не хватает денег");
    balance -= amount;
}

void Player::earn(int amount) {
    if (amount < 0)
        throw std::invalid_argument("Player: сумма меньше 0");
    balance += amount;
}

void Player::addShip(Ship* ship) {
    if (ship == nullptr)
        throw std::invalid_argument("Player: нет корабля");
    fleet.push_back(ship);
}

Ship& Player::getShip(int index) {
    if (index < 0 || index >= (int)fleet.size())
        throw std::out_of_range("Player: нет корабля с таким номером");
    return *fleet[index];
}

int Player::getFleetSize() const { return (int)fleet.size(); }

std::string Player::getTypeName() const { return "Игрок"; }
