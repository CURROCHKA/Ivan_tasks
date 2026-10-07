#pragma once
#include <vector>
#include "Entity.h"
#include "Hull.h"
#include "Engine.h"
#include "FuelTank.h"
#include "CargoHold.h"
#include "Cargo.h"
#include "Enums.h"

class Planet;

// Корабль игрока
class Ship : public Entity {
private:
    Hull hull;
    std::vector<Engine*> engines;
    std::vector<FuelTank*> tanks;
    std::vector<CargoHold*> holds;
    Planet* location;
    Planet* destination;
    int turnsLeft;

public:
    Ship();
    Ship(const std::string& name, const Hull& hull, Planet* location);
    ~Ship();

    const Hull& getHull() const;
    std::vector<Part*> getParts();
    Planet* getLocation() const;
    bool isInFlight() const;
    int getFreeSlots() const;

    void installEngine(Engine* engine);
    void installFuelTank(FuelTank* tank);
    void installCargoHold(CargoHold* hold);

    double getTotalMass() const;
    double getSpeed() const;
    double getFuel() const;
    double refuel(double amount);

    bool loadCargo(const Cargo& c);
    Cargo unloadCargo(const std::string& productName, int quantity);

    bool hasBrokenParts();
    std::string getTypeName() const;

    bool canFlyTo(const Planet& target);
    void startFlight(Planet* target);
    void nextTurn();
    void takeDamage(int damage);
    void applyHazard(HazardType type, int power);

    friend class Shipyard;
};
