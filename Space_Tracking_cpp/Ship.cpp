#include "Ship.h"
#include "Planet.h"
#include <cmath>
#include <stdexcept>

Ship::Ship() : Entity(), hull(), location(nullptr), destination(nullptr), turnsLeft(0) {}

Ship::Ship(const std::string& name, const Hull& hull, Planet* location)
    : Entity(name), hull(hull), location(location), destination(nullptr), turnsLeft(0) {}

Ship::~Ship() {
    for (size_t i = 0; i < engines.size(); i++)
        delete engines[i];
    for (size_t i = 0; i < tanks.size(); i++)
        delete tanks[i];
    for (size_t i = 0; i < holds.size(); i++)
        delete holds[i];
}

const Hull& Ship::getHull() const { return hull; }

std::vector<Part*> Ship::getParts() {
    std::vector<Part*> parts;
    parts.push_back(&hull);
    for (size_t i = 0; i < engines.size(); i++)
        parts.push_back(engines[i]);
    for (size_t i = 0; i < tanks.size(); i++)
        parts.push_back(tanks[i]);
    for (size_t i = 0; i < holds.size(); i++)
        parts.push_back(holds[i]);
    return parts;
}

Planet* Ship::getLocation() const { return location; }

bool Ship::isInFlight() const { return destination != nullptr; }

int Ship::getFreeSlots() const {
    return hull.getSlots() - (int)(engines.size() + tanks.size() + holds.size());
}

void Ship::installEngine(Engine* engine) {
    if (engine == nullptr)
        throw std::invalid_argument("Ship: нет двигателя");
    if (getFreeSlots() == 0)
        throw std::logic_error("Ship: на корпусе нет свободных мест");
    engines.push_back(engine);
}

void Ship::installFuelTank(FuelTank* tank) {
    if (tank == nullptr)
        throw std::invalid_argument("Ship: нет бака");
    if (getFreeSlots() == 0)
        throw std::logic_error("Ship: на корпусе нет свободных мест");
    tanks.push_back(tank);
}

void Ship::installCargoHold(CargoHold* hold) {
    if (hold == nullptr)
        throw std::invalid_argument("Ship: нет трюма");
    if (getFreeSlots() == 0)
        throw std::logic_error("Ship: на корпусе нет свободных мест");
    holds.push_back(hold);
}

double Ship::getTotalMass() const {
    // Для каждой детали через указатель Part* вызывается getTotalMass() её класса
    std::vector<const Part*> parts;
    parts.push_back(&hull);
    for (size_t i = 0; i < engines.size(); i++)
        parts.push_back(engines[i]);
    for (size_t i = 0; i < tanks.size(); i++)
        parts.push_back(tanks[i]);
    for (size_t i = 0; i < holds.size(); i++)
        parts.push_back(holds[i]);

    double sum = 0;
    for (size_t i = 0; i < parts.size(); i++)
        sum += parts[i]->getTotalMass();
    return sum;
}

double Ship::getSpeed() const {
    double mass = getTotalMass();
    double speed = 0;
    for (size_t i = 0; i < engines.size(); i++)
        speed += engines[i]->getSpeed(mass);
    return speed;
}

double Ship::getFuel() const {
    double sum = 0;
    for (size_t i = 0; i < tanks.size(); i++)
        sum += tanks[i]->getFuel();
    return sum;
}

double Ship::refuel(double amount) {
    double added = 0;
    for (size_t i = 0; i < tanks.size() && added < amount; i++) {
        if (!tanks[i]->isBroken())
            added += tanks[i]->refuel(amount - added);
    }
    return added;
}

bool Ship::loadCargo(const Cargo& c) {
    for (size_t i = 0; i < holds.size(); i++) {
        if (!holds[i]->isBroken() && holds[i]->getFreeCapacity() >= c.getMass())
            return holds[i]->loadCargo(c);
    }
    return false;
}

Cargo Ship::unloadCargo(const std::string& productName, int quantity) {
    if (quantity <= 0)
        throw std::invalid_argument("Ship: количество не больше 0");

    // Сколько товара есть во всех трюмах
    int available = 0;
    for (size_t i = 0; i < holds.size(); i++) {
        const std::vector<Cargo>& list = holds[i]->getCargo();
        for (size_t j = 0; j < list.size(); j++)
            if (list[j].getProduct()->getName() == productName)
                available += list[j].getQuantity();
    }
    if (available < quantity)
        throw std::out_of_range("Ship: товара в трюмах меньше, чем нужно");

    // Вынимаем товар из трюмов по очереди и складываем партии
    Cargo result;
    int left = quantity;
    for (size_t i = 0; i < holds.size() && left > 0; i++) {
        const std::vector<Cargo>& list = holds[i]->getCargo();
        int inHold = 0;
        for (size_t j = 0; j < list.size(); j++)
            if (list[j].getProduct()->getName() == productName)
                inHold = list[j].getQuantity();
        if (inHold == 0)
            continue;
        int take = inHold < left ? inHold : left;
        Cargo part = holds[i]->unloadCargo(productName, take);
        if (result.getProduct() == nullptr)
            result = part;
        else
            result = result + part;
        left -= take;
    }
    return result;
}

bool Ship::hasBrokenParts() {
    std::vector<Part*> parts = getParts();
    for (size_t i = 0; i < parts.size(); i++)
        if (parts[i]->isBroken())
            return true;
    return false;
}

std::string Ship::getTypeName() const { return "Корабль"; }

bool Ship::canFlyTo(const Planet& target) {
    if (isInFlight() || location == nullptr || location == &target)
        return false;
    if (engines.empty() || tanks.empty() || hasBrokenParts())
        return false;
    double distance = location->distanceTo(target);
    double needFuel = 0;
    for (size_t i = 0; i < engines.size(); i++)
        needFuel += engines[i]->getFuelForDistance(distance);
    return getFuel() >= needFuel && getSpeed() > 0;
}

void Ship::startFlight(Planet* target) {
    if (target == nullptr || !canFlyTo(*target))
        throw std::logic_error("Ship: перелёт невозможен");

    double distance = location->distanceTo(*target);
    double needFuel = 0;
    for (size_t i = 0; i < engines.size(); i++)
        needFuel += engines[i]->getFuelForDistance(distance);

    // Списываем топливо из баков по очереди
    for (size_t i = 0; i < tanks.size() && needFuel > 0; i++) {
        double take = tanks[i]->getFuel() < needFuel ? tanks[i]->getFuel() : needFuel;
        tanks[i]->consumeFuel(take);
        needFuel -= take;
    }

    turnsLeft = (int)std::ceil(distance / getSpeed());
    if (turnsLeft < 1)
        turnsLeft = 1;
    destination = target;
    location = nullptr;
}

void Ship::nextTurn() {
    if (!isInFlight())
        return;
    turnsLeft--;
    if (turnsLeft <= 0) {
        turnsLeft = 0;
        location = destination;
        destination = nullptr;
    }
}

void Ship::takeDamage(int damage) {
    // Для каждой детали вызывается takeDamage() её класса
    std::vector<Part*> parts = getParts();
    for (size_t i = 0; i < parts.size(); i++)
        parts[i]->takeDamage(damage);
}

void Ship::applyHazard(HazardType type, int power) {
    if (power < 0)
        throw std::invalid_argument("Ship: сила опасности меньше 0");
    switch (type) {
    case HazardType::Pirates:
        takeDamage(power);
        for (size_t i = 0; i < holds.size(); i++)
            holds[i]->loseCargo(power > 100 ? 100 : power);
        break;
    case HazardType::Asteroids:
        takeDamage(2 * power);
        break;
    case HazardType::Anomaly:
        if (isInFlight())
            turnsLeft++;
        break;
    }
}
