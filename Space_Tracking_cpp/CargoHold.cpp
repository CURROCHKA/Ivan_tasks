#include "CargoHold.h"
#include <stdexcept>

CargoHold::CargoHold() : Part(), cargoCapacity(50) {}

CargoHold::CargoHold(const std::string& name, double mass, int maxDurability, int price, double cargoCapacity)
    : Part(name, mass, maxDurability, price), cargoCapacity(cargoCapacity) {
    if (cargoCapacity <= 0)
        throw std::invalid_argument("CargoHold: грузоподъёмность не больше 0");
}

double CargoHold::getCargoCapacity() const { return cargoCapacity; }

const std::vector<Cargo>& CargoHold::getCargo() const { return cargo; }

double CargoHold::getCargoMass() const {
    double sum = 0;
    for (size_t i = 0; i < cargo.size(); i++)
        sum += cargo[i].getMass();
    return sum;
}

double CargoHold::getFreeCapacity() const {
    return cargoCapacity - getCargoMass();
}

bool CargoHold::loadCargo(const Cargo& c) {
    if (c.getProduct() == nullptr)
        throw std::invalid_argument("CargoHold: партия без товара");
    if (c.getMass() > getFreeCapacity())
        return false;
    for (size_t i = 0; i < cargo.size(); i++) {
        if (*cargo[i].getProduct() == *c.getProduct()) {
            cargo[i] = cargo[i] + c;
            return true;
        }
    }
    cargo.push_back(c);
    return true;
}

Cargo CargoHold::unloadCargo(const std::string& productName, int quantity) {
    for (size_t i = 0; i < cargo.size(); i++) {
        if (cargo[i].getProduct()->getName() == productName) {
            cargo[i] -= quantity;  // выбрасывает std::out_of_range, если товара мало
            Cargo result(cargo[i].getProduct(), quantity, cargo[i].getCondition());
            if (cargo[i].getQuantity() == 0)
                cargo.erase(cargo.begin() + i);
            return result;
        }
    }
    throw std::out_of_range("CargoHold: товара нет в трюме");
}

void CargoHold::loseCargo(int percent) {
    if (percent < 0 || percent > 100)
        throw std::invalid_argument("CargoHold: процент вне диапазона 0..100");
    for (size_t i = 0; i < cargo.size();) {
        int left = cargo[i].getQuantity() - cargo[i].getQuantity() * percent / 100;
        int cond = cargo[i].getCondition() - percent;
        if (cond < 0)
            cond = 0;
        if (left == 0) {
            cargo.erase(cargo.begin() + i);
        } else {
            cargo[i] = Cargo(cargo[i].getProduct(), left, cond);
            i++;
        }
    }
}

double CargoHold::getTotalMass() const {
    return mass + getCargoMass();
}

std::string CargoHold::getTypeName() const { return "Грузовой трюм"; }
