#include "Planet.h"
#include "Constants.h"
#include <cmath>
#include <stdexcept>

Planet::Planet()
    : Entity(), x(0), y(0), economy(EconomyType::Agrarian),
      event(EventType::None), eventTurnsLeft(0), market(), shipyard() {
    market.applyEconomy(economy);
}

Planet::Planet(const std::string& name, double x, double y, EconomyType economy)
    : Entity(name), x(x), y(y), economy(economy),
      event(EventType::None), eventTurnsLeft(0), market(), shipyard() {
    if (x < 0 || x > MAP_SIZE - 1 || y < 0 || y > MAP_SIZE - 1)
        throw std::invalid_argument("Planet: координаты вне карты");
    market.applyEconomy(economy);
}

double Planet::getX() const { return x; }

double Planet::getY() const { return y; }

EconomyType Planet::getEconomy() const { return economy; }

EventType Planet::getEvent() const { return event; }

double Planet::distanceTo(const Planet& other) const {
    double dx = x - other.x;
    double dy = y - other.y;
    return std::sqrt(dx * dx + dy * dy);
}

void Planet::startEvent(EventType event, int turns) {
    if (turns < 0)
        throw std::invalid_argument("Planet: число ходов меньше 0");
    this->event = event;
    eventTurnsLeft = (event == EventType::None) ? 0 : turns;
    market.applyEvent(this->event);
}

void Planet::nextTurn() {
    if (eventTurnsLeft == 0)
        return;
    eventTurnsLeft--;
    if (eventTurnsLeft == 0) {
        event = EventType::None;
        market.applyEvent(EventType::None);
    }
}

Market& Planet::getMarket() { return market; }

Shipyard& Planet::getShipyard() { return shipyard; }

std::string Planet::getTypeName() const { return "Планета"; }
