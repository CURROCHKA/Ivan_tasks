#pragma once
#include <vector>
#include "Engine.h"
#include "FuelTank.h"
#include "CargoHold.h"

class Ship;
class Player;

// Верфь: продаёт детали и ремонтирует корабли
class Shipyard {
private:
    std::vector<Engine*> engines;
    std::vector<FuelTank*> tanks;
    std::vector<CargoHold*> holds;
    int repairCostPerPoint;

public:
    Shipyard();
    Shipyard(int repairCostPerPoint);
    ~Shipyard();

    void addEngine(Engine* engine);
    void addFuelTank(FuelTank* tank);
    void addCargoHold(CargoHold* hold);

    const std::vector<Engine*>& getEngines() const;
    const std::vector<FuelTank*>& getFuelTanks() const;
    const std::vector<CargoHold*>& getCargoHolds() const;

    bool sellEngine(int index, Player& player, Ship& ship);
    bool sellFuelTank(int index, Player& player, Ship& ship);
    bool sellCargoHold(int index, Player& player, Ship& ship);

    int getRepairCost(const Ship& ship) const;
    bool repairShip(Ship& ship, Player& player);
};
