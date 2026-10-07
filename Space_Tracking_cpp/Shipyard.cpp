#include "Shipyard.h"
#include "Ship.h"
#include "Player.h"
#include <stdexcept>

Shipyard::Shipyard() : repairCostPerPoint(5) {}

Shipyard::Shipyard(int repairCostPerPoint) : repairCostPerPoint(repairCostPerPoint) {
    if (repairCostPerPoint <= 0)
        throw std::invalid_argument("Shipyard: цена ремонта не больше 0");
}

Shipyard::~Shipyard() {
    for (size_t i = 0; i < engines.size(); i++)
        delete engines[i];
    for (size_t i = 0; i < tanks.size(); i++)
        delete tanks[i];
    for (size_t i = 0; i < holds.size(); i++)
        delete holds[i];
}

void Shipyard::addEngine(Engine* engine) {
    if (engine == nullptr)
        throw std::invalid_argument("Shipyard: нет двигателя");
    engines.push_back(engine);
}

void Shipyard::addFuelTank(FuelTank* tank) {
    if (tank == nullptr)
        throw std::invalid_argument("Shipyard: нет бака");
    tanks.push_back(tank);
}

void Shipyard::addCargoHold(CargoHold* hold) {
    if (hold == nullptr)
        throw std::invalid_argument("Shipyard: нет трюма");
    holds.push_back(hold);
}

const std::vector<Engine*>& Shipyard::getEngines() const { return engines; }

const std::vector<FuelTank*>& Shipyard::getFuelTanks() const { return tanks; }

const std::vector<CargoHold*>& Shipyard::getCargoHolds() const { return holds; }

bool Shipyard::sellEngine(int index, Player& player, Ship& ship) {
    if (index < 0 || index >= (int)engines.size())
        return false;
    if (ship.isInFlight() || ship.getFreeSlots() == 0 || !player.canPay(engines[index]->getPrice()))
        return false;
    Engine* engine = engines[index];
    player.pay(engine->getPrice());
    engines.erase(engines.begin() + index);
    ship.installEngine(engine);
    return true;
}

bool Shipyard::sellFuelTank(int index, Player& player, Ship& ship) {
    if (index < 0 || index >= (int)tanks.size())
        return false;
    if (ship.isInFlight() || ship.getFreeSlots() == 0 || !player.canPay(tanks[index]->getPrice()))
        return false;
    FuelTank* tank = tanks[index];
    player.pay(tank->getPrice());
    tanks.erase(tanks.begin() + index);
    ship.installFuelTank(tank);
    return true;
}

bool Shipyard::sellCargoHold(int index, Player& player, Ship& ship) {
    if (index < 0 || index >= (int)holds.size())
        return false;
    if (ship.isInFlight() || ship.getFreeSlots() == 0 || !player.canPay(holds[index]->getPrice()))
        return false;
    CargoHold* hold = holds[index];
    player.pay(hold->getPrice());
    holds.erase(holds.begin() + index);
    ship.installCargoHold(hold);
    return true;
}

int Shipyard::getRepairCost(const Ship& ship) const {
    // Shipyard — дружественный класс Ship, поэтому читает закрытые поля корабля
    int missing = ship.hull.getMaxDurability() - ship.hull.getDurability();
    for (size_t i = 0; i < ship.engines.size(); i++)
        missing += ship.engines[i]->getMaxDurability() - ship.engines[i]->getDurability();
    for (size_t i = 0; i < ship.tanks.size(); i++)
        missing += ship.tanks[i]->getMaxDurability() - ship.tanks[i]->getDurability();
    for (size_t i = 0; i < ship.holds.size(); i++)
        missing += ship.holds[i]->getMaxDurability() - ship.holds[i]->getDurability();
    return missing * repairCostPerPoint;
}

bool Shipyard::repairShip(Ship& ship, Player& player) {
    if (ship.isInFlight())
        return false;
    int cost = getRepairCost(ship);
    if (!player.canPay(cost))
        return false;
    player.pay(cost);
    std::vector<Part*> parts = ship.getParts();
    for (size_t i = 0; i < parts.size(); i++)
        parts[i]->repair(parts[i]->getMaxDurability());
    return true;
}
