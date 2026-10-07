#pragma once
#include <map>
#include <string>
#include <vector>
#include "Cargo.h"
#include "Enums.h"

class Player;
class Ship;

// Рынок планеты: магазин или склад
class Market {
private:
    MarketKind kind;
    std::vector<Cargo> stock;
    std::map<std::string, double> priceFactors;
    EconomyType economy;  // нужен, чтобы вернуть коэффициенты после события

public:
    Market();
    Market(MarketKind kind);

    MarketKind getKind() const;
    void addStock(const Cargo& c);
    const std::vector<Cargo>& getStock() const;
    void setPriceFactor(const std::string& productName, double factor);
    int getSellPrice(const Product& p) const;
    int getBuyPrice(const Product& p) const;
    bool sellToPlayer(const std::string& productName, int quantity, Player& player, Ship& ship);
    bool buyFromPlayer(const std::string& productName, int quantity, Player& player, Ship& ship);
    void applyEconomy(EconomyType economy);
    void applyEvent(EventType event);
};
