#pragma once
#include <vector>
#include "Part.h"
#include "Cargo.h"

// Грузовой трюм
class CargoHold : public Part {
private:
    double cargoCapacity;
    std::vector<Cargo> cargo;

public:
    CargoHold();
    CargoHold(const std::string& name, double mass, int maxDurability, int price, double cargoCapacity);

    double getCargoCapacity() const;
    const std::vector<Cargo>& getCargo() const;
    double getCargoMass() const;
    double getFreeCapacity() const;
    bool loadCargo(const Cargo& c);
    Cargo unloadCargo(const std::string& productName, int quantity);
    void loseCargo(int percent);
    double getTotalMass() const;
    std::string getTypeName() const;
};
