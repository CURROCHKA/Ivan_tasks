#pragma once
#include "Entity.h"
#include "Enums.h"
#include "Market.h"
#include "Shipyard.h"

// Планета: точка на карте с рынком и верфью
class Planet : public Entity {
private:
    double x;
    double y;
    EconomyType economy;
    EventType event;
    int eventTurnsLeft;
    Market market;
    Shipyard shipyard;

public:
    Planet();
    Planet(const std::string& name, double x, double y, EconomyType economy);

    double getX() const;
    double getY() const;
    EconomyType getEconomy() const;
    EventType getEvent() const;
    double distanceTo(const Planet& other) const;
    void startEvent(EventType event, int turns);
    void nextTurn();
    Market& getMarket();
    Shipyard& getShipyard();
    std::string getTypeName() const;
};
