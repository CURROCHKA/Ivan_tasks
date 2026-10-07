#include <cmath>
#include <cstdio>
#include <map>
#include <stdexcept>
#include <string>
#include <vector>
#include <locale>

using namespace std;

// ===== Объявления классов =====

// ----- Enums -----
// Тип экономики планеты
enum class EconomyType { Agrarian, Industrial, Tech };

// Глобальное событие на планете
enum class EventType { None, War, Catastrophe, Epidemic };

// Опасность во время перелёта
enum class HazardType { Pirates, Asteroids, Anomaly };

// Вид рынка
enum class MarketKind { Shop, Warehouse };

// ----- Constants -----
// Склад продаёт товар партиями не меньше WHOLESALE_MIN единиц
const int WHOLESALE_MIN = 10;

// Доля цены продажи, по которой рынок покупает товар у игрока
const double BUY_RATIO = 0.8;

// Масса одной единицы топлива в тоннах
const double FUEL_UNIT_MASS = 0.01;

// Цель игры
const int TARGET_BALANCE = 100000;
const int MAX_TURNS = 100;

// Размер карты в световых годах
const int MAP_SIZE = 10;

// ----- Entity -----
// Объект игры: уникальный номер и название (абстрактный класс)
class Entity {
protected:
    int id;
    string name;

private:
    static int nextId;

public:
    Entity();
    Entity(const string& name);
    virtual ~Entity();

    int getId() const;
    string getName() const;
    void setName(const string& name);
    virtual string getTypeName() const = 0;
};

// ----- Tradable -----
// Объект с ценой (абстрактный класс)
class Tradable : virtual public Entity {
protected:
    int price;

public:
    Tradable();
    Tradable(const string& name, int price);
    virtual ~Tradable();

    int getPrice() const;
    void setPrice(int price);
    virtual string getTypeName() const = 0;
};

// ----- Damageable -----
// Объект с прочностью (абстрактный класс)
class Damageable : virtual public Entity {
protected:
    int maxDurability;
    int durability;

public:
    Damageable();
    Damageable(const string& name, int maxDurability);

    int getDurability() const;
    int getMaxDurability() const;
    double getDurabilityPercent() const;
    bool isBroken() const;
    virtual void takeDamage(int damage);
    void repair(int points);
    Damageable& operator-=(int damage);
    virtual string getTypeName() const = 0;
};

// ----- Part -----
// Деталь корабля (абстрактный класс)
class Part : public Damageable, public Tradable {
protected:
    double mass;

public:
    Part();
    Part(const string& name, double mass, int maxDurability, int price);

    double getMass() const;
    virtual double getTotalMass() const;
    virtual string getTypeName() const = 0;
};

// ----- Hull -----
// Корпус
class Hull : public Part {
private:
    int armor;
    int slots;

public:
    Hull();
    Hull(const string& name, double mass, int maxDurability, int price, int armor, int slots);

    int getArmor() const;
    int getSlots() const;
    void takeDamage(int damage);
    string getTypeName() const;
};

// ----- Engine -----
// Двигатель
class Engine : public Part {
private:
    double power;
    double fuelConsumption;

public:
    Engine();
    Engine(const string& name, double mass, int maxDurability, int price,
        double power, double fuelConsumption);

    double getPower() const;
    double getFuelConsumption() const;
    double getFuelForDistance(double distance) const;
    double getSpeed(double shipMass) const;
    string getTypeName() const;
};

// ----- FuelTank -----
// Топливный бак
class FuelTank : public Part {
private:
    double fuelCapacity;
    double fuel;

public:
    FuelTank();
    FuelTank(const string& name, double mass, int maxDurability, int price, double fuelCapacity);

    double getFuelCapacity() const;
    double getFuel() const;
    double refuel(double amount);
    bool consumeFuel(double amount);
    void takeDamage(int damage);
    double getTotalMass() const;
    string getTypeName() const;
};

// ----- Product -----
// Товар каталога
class Product : public Tradable {
private:
    double unitMass;

public:
    Product();
    Product(const string& name, int baseCost, double unitMass);

    double getUnitMass() const;
    bool operator==(const Product& other) const;
    string getTypeName() const;
};

// ----- Cargo -----
// Партия груза: количество единиц одного товара и их состояние
class Cargo {
private:
    const Product* product;
    int quantity;
    int condition;

public:
    Cargo();
    Cargo(const Product* product, int quantity, int condition = 100);

    const Product* getProduct() const;
    int getQuantity() const;
    int getCondition() const;
    void setQuantity(int quantity);
    double getMass() const;

    Cargo& operator++();
    Cargo operator++(int);
    Cargo& operator--();
    Cargo operator--(int);
    Cargo& operator-=(int amount);

    friend Cargo operator+(const Cargo& a, const Cargo& b);
};

// ----- CargoHold -----
// Грузовой трюм
class CargoHold : public Part {
private:
    double cargoCapacity;
    vector<Cargo> cargo;

public:
    CargoHold();
    CargoHold(const string& name, double mass, int maxDurability, int price, double cargoCapacity);

    double getCargoCapacity() const;
    const vector<Cargo>& getCargo() const;
    double getCargoMass() const;
    double getFreeCapacity() const;
    bool loadCargo(const Cargo& c);
    Cargo unloadCargo(const string& productName, int quantity);
    void loseCargo(int percent);
    double getTotalMass() const;
    string getTypeName() const;
};

// ----- Ship -----
class Planet;

// Корабль игрока
class Ship : public Entity {
private:
    Hull hull;
    vector<Engine*> engines;
    vector<FuelTank*> tanks;
    vector<CargoHold*> holds;
    Planet* location;
    Planet* destination;
    int turnsLeft;

public:
    Ship();
    Ship(const string& name, const Hull& hull, Planet* location);
    ~Ship();

    const Hull& getHull() const;
    vector<Part*> getParts();
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
    Cargo unloadCargo(const string& productName, int quantity);

    bool hasBrokenParts();
    string getTypeName() const;

    bool canFlyTo(const Planet& target);
    void startFlight(Planet* target);
    void nextTurn();
    void takeDamage(int damage);
    void applyHazard(HazardType type, int power);

    friend class Shipyard;
};

// ----- Market -----
class Player;
class Ship;

// Рынок планеты: магазин или склад
class Market {
private:
    MarketKind kind;
    vector<Cargo> stock;
    map<string, double> priceFactors;
    EconomyType economy;  // нужен, чтобы вернуть коэффициенты после события

public:
    Market();
    Market(MarketKind kind);

    MarketKind getKind() const;
    void addStock(const Cargo& c);
    const vector<Cargo>& getStock() const;
    void setPriceFactor(const string& productName, double factor);
    int getSellPrice(const Product& p) const;
    int getBuyPrice(const Product& p) const;
    bool sellToPlayer(const string& productName, int quantity, Player& player, Ship& ship);
    bool buyFromPlayer(const string& productName, int quantity, Player& player, Ship& ship);
    void applyEconomy(EconomyType economy);
    void applyEvent(EventType event);
};

// ----- Shipyard -----
class Ship;
class Player;

// Верфь: продаёт детали и ремонтирует корабли
class Shipyard {
private:
    vector<Engine*> engines;
    vector<FuelTank*> tanks;
    vector<CargoHold*> holds;
    int repairCostPerPoint;

public:
    Shipyard();
    Shipyard(int repairCostPerPoint);
    ~Shipyard();

    void addEngine(Engine* engine);
    void addFuelTank(FuelTank* tank);
    void addCargoHold(CargoHold* hold);

    const vector<Engine*>& getEngines() const;
    const vector<FuelTank*>& getFuelTanks() const;
    const vector<CargoHold*>& getCargoHolds() const;

    bool sellEngine(int index, Player& player, Ship& ship);
    bool sellFuelTank(int index, Player& player, Ship& ship);
    bool sellCargoHold(int index, Player& player, Ship& ship);

    int getRepairCost(const Ship& ship) const;
    bool repairShip(Ship& ship, Player& player);
};

// ----- Planet -----
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
    Planet(const string& name, double x, double y, EconomyType economy);

    double getX() const;
    double getY() const;
    EconomyType getEconomy() const;
    EventType getEvent() const;
    double distanceTo(const Planet& other) const;
    void startEvent(EventType event, int turns);
    void nextTurn();
    Market& getMarket();
    Shipyard& getShipyard();
    string getTypeName() const;
};

// ----- Player -----
class Ship;

// Игрок: владелец кораблей и денег
class Player : public Entity {
private:
    int balance;
    vector<Ship*> fleet;

public:
    Player();
    Player(const string& name, int balance);
    ~Player();

    int getBalance() const;
    void setBalance(int balance);
    bool canPay(int amount) const;
    void pay(int amount);
    void earn(int amount);
    void addShip(Ship* ship);
    Ship& getShip(int index);
    int getFleetSize() const;
    string getTypeName() const;
};

// ===== Реализация методов =====

// ----- Entity -----
int Entity::nextId = 1;

Entity::Entity() : id(nextId++), name("Без названия") {}

Entity::Entity(const string& name) : id(nextId++), name(name) {
    if (name.empty())
        throw invalid_argument("Entity: пустое название");
}

Entity::~Entity() {}

int Entity::getId() const { return id; }

string Entity::getName() const { return name; }

void Entity::setName(const string& name) {
    if (name.empty())
        throw invalid_argument("Entity: пустое название");
    this->name = name;
}


// ----- Tradable -----
Tradable::Tradable() : Entity(), price(0) {}

Tradable::Tradable(const string& name, int price) : Entity(name), price(price) {
    if (price < 0)
        throw invalid_argument("Tradable: цена меньше 0");
}

Tradable::~Tradable() {}

int Tradable::getPrice() const { return price; }

void Tradable::setPrice(int price) {
    if (price < 0)
        throw invalid_argument("Tradable: цена меньше 0");
    this->price = price;
}

// ----- Damageable -----
Damageable::Damageable() : Entity(), maxDurability(100), durability(100) {}

Damageable::Damageable(const string& name, int maxDurability)
    : Entity(name), maxDurability(maxDurability), durability(maxDurability) {
    if (maxDurability < 1)
        throw invalid_argument("Damageable: прочность меньше 1");
}

int Damageable::getDurability() const { return durability; }

int Damageable::getMaxDurability() const { return maxDurability; }

double Damageable::getDurabilityPercent() const {
    return (double)durability / maxDurability * 100.0;
}

bool Damageable::isBroken() const { return durability == 0; }

void Damageable::takeDamage(int damage) {
    if (damage < 0)
        throw invalid_argument("Damageable: урон меньше 0");
    durability -= damage;
    if (durability < 0)
        durability = 0;
}

void Damageable::repair(int points) {
    if (points < 0)
        throw invalid_argument("Damageable: ремонт меньше 0");
    durability += points;
    if (durability > maxDurability)
        durability = maxDurability;
}

Damageable& Damageable::operator-=(int damage) {
    takeDamage(damage);
    return *this;
}

// ----- Part -----
Part::Part() : Entity(), Damageable(), Tradable(), mass(1) {}

// Entity — виртуальный базовый класс для Damageable и Tradable.
// В объекте Part один подобъект Entity. Его конструктор вызывает
// самый производный класс, поэтому Entity(name) стоит первым в списке
// инициализации. Вызовы Entity(name) внутри Damageable и Tradable при этом
// не выполняются.
Part::Part(const string& name, double mass, int maxDurability, int price)
    : Entity(name), Damageable(name, maxDurability), Tradable(name, price), mass(mass) {
    if (mass <= 0)
        throw invalid_argument("Part: масса не больше 0");
}

double Part::getMass() const { return mass; }

double Part::getTotalMass() const { return mass; }

// ----- Hull -----
Hull::Hull() : Part(), armor(0), slots(3) {}

// Hull — самый производный класс, поэтому он сам вызывает Entity(name)
Hull::Hull(const string& name, double mass, int maxDurability, int price, int armor, int slots)
    : Entity(name), Part(name, mass, maxDurability, price), armor(armor), slots(slots) {
    if (armor < 0 || armor > 80)
        throw invalid_argument("Hull: броня вне диапазона 0..80");
    if (slots < 1)
        throw invalid_argument("Hull: мест меньше 1");
}

int Hull::getArmor() const { return armor; }

int Hull::getSlots() const { return slots; }

void Hull::takeDamage(int damage) {
    if (damage < 0)
        throw invalid_argument("Hull: урон меньше 0");
    int reduced = damage * (100 - armor) / 100;
    Damageable::takeDamage(reduced);
}

string Hull::getTypeName() const { return "Корпус"; }

// ----- Engine -----
Engine::Engine() : Part(), power(100), fuelConsumption(1) {}

Engine::Engine(const string& name, double mass, int maxDurability, int price,
    double power, double fuelConsumption)
    : Entity(name), Part(name, mass, maxDurability, price), power(power), fuelConsumption(fuelConsumption) {
    if (power <= 0 || fuelConsumption <= 0)
        throw invalid_argument("Engine: мощность или расход не больше 0");
}

double Engine::getPower() const { return power; }

double Engine::getFuelConsumption() const { return fuelConsumption; }

double Engine::getFuelForDistance(double distance) const {
    return distance * fuelConsumption;
}

double Engine::getSpeed(double shipMass) const {
    if (isBroken() || shipMass <= 0)
        return 0;
    return power / shipMass;
}

string Engine::getTypeName() const { return "Двигатель"; }

// ----- FuelTank -----
FuelTank::FuelTank() : Part(), fuelCapacity(100), fuel(0) {}

FuelTank::FuelTank(const string& name, double mass, int maxDurability, int price, double fuelCapacity)
    : Entity(name), Part(name, mass, maxDurability, price), fuelCapacity(fuelCapacity), fuel(0) {
    if (fuelCapacity <= 0)
        throw invalid_argument("FuelTank: объём не больше 0");
}

double FuelTank::getFuelCapacity() const { return fuelCapacity; }

double FuelTank::getFuel() const { return fuel; }

double FuelTank::refuel(double amount) {
    if (amount < 0)
        throw invalid_argument("FuelTank: количество меньше 0");
    double added = fuelCapacity - fuel;
    if (amount < added)
        added = amount;
    fuel += added;
    return added;
}

bool FuelTank::consumeFuel(double amount) {
    if (amount < 0)
        throw invalid_argument("FuelTank: количество меньше 0");
    if (fuel < amount)
        return false;
    fuel -= amount;
    return true;
}

void FuelTank::takeDamage(int damage) {
    Damageable::takeDamage(damage);
    if (isBroken())
        fuel = 0;
}

double FuelTank::getTotalMass() const {
    return mass + fuel * FUEL_UNIT_MASS;
}

string FuelTank::getTypeName() const { return "Топливный бак"; }

// ----- Product -----
Product::Product() : Entity(), Tradable(), unitMass(1) {}

Product::Product(const string& name, int baseCost, double unitMass)
    : Entity(name), Tradable(name, baseCost), unitMass(unitMass) {
    if (unitMass <= 0)
        throw invalid_argument("Product: масса единицы не больше 0");
}

double Product::getUnitMass() const { return unitMass; }

bool Product::operator==(const Product& other) const {
    return name == other.name;
}

string Product::getTypeName() const { return "Товар"; }

// ----- Cargo -----
Cargo::Cargo() : product(nullptr), quantity(0), condition(100) {}

Cargo::Cargo(const Product* product, int quantity, int condition)
    : product(product), quantity(quantity), condition(condition) {
    if (quantity < 0)
        throw invalid_argument("Cargo: количество меньше 0");
    if (condition < 0 || condition > 100)
        throw invalid_argument("Cargo: состояние вне диапазона 0..100");
}

const Product* Cargo::getProduct() const { return product; }

int Cargo::getQuantity() const { return quantity; }

int Cargo::getCondition() const { return condition; }

void Cargo::setQuantity(int quantity) {
    if (quantity < 0)
        throw invalid_argument("Cargo: количество меньше 0");
    this->quantity = quantity;
}

double Cargo::getMass() const {
    if (product == nullptr)
        return 0;
    return quantity * product->getUnitMass();
}

Cargo& Cargo::operator++() {
    quantity++;
    return *this;
}

Cargo Cargo::operator++(int) {
    Cargo old = *this;
    quantity++;
    return old;
}

Cargo& Cargo::operator--() {
    if (quantity > 0)
        quantity--;
    return *this;
}

Cargo Cargo::operator--(int) {
    Cargo old = *this;
    if (quantity > 0)
        quantity--;
    return old;
}

Cargo& Cargo::operator-=(int amount) {
    if (amount < 0)
        throw invalid_argument("Cargo: количество меньше 0");
    if (amount > quantity)
        throw out_of_range("Cargo: в партии меньше товара");
    quantity -= amount;
    return *this;
}

Cargo operator+(const Cargo& a, const Cargo& b) {
    if (a.product == nullptr || b.product == nullptr || !(*a.product == *b.product))
        throw invalid_argument("Cargo: сложение партий разных товаров");
    int total = a.quantity + b.quantity;
    int cond = 100;
    if (total > 0)
        cond = (a.condition * a.quantity + b.condition * b.quantity) / total;
    return Cargo(a.product, total, cond);
}

// ----- CargoHold -----
CargoHold::CargoHold() : Part(), cargoCapacity(50) {}

CargoHold::CargoHold(const string& name, double mass, int maxDurability, int price, double cargoCapacity)
    : Entity(name), Part(name, mass, maxDurability, price), cargoCapacity(cargoCapacity) {
    if (cargoCapacity <= 0)
        throw invalid_argument("CargoHold: грузоподъёмность не больше 0");
}

double CargoHold::getCargoCapacity() const { return cargoCapacity; }

const vector<Cargo>& CargoHold::getCargo() const { return cargo; }

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
        throw invalid_argument("CargoHold: партия без товара");
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

Cargo CargoHold::unloadCargo(const string& productName, int quantity) {
    for (size_t i = 0; i < cargo.size(); i++) {
        if (cargo[i].getProduct()->getName() == productName) {
            cargo[i] -= quantity;  // выбрасывает out_of_range, если товара мало
            Cargo result(cargo[i].getProduct(), quantity, cargo[i].getCondition());
            if (cargo[i].getQuantity() == 0)
                cargo.erase(cargo.begin() + i);
            return result;
        }
    }
    throw out_of_range("CargoHold: товара нет в трюме");
}

void CargoHold::loseCargo(int percent) {
    if (percent < 0 || percent > 100)
        throw invalid_argument("CargoHold: процент вне диапазона 0..100");
    for (size_t i = 0; i < cargo.size();) {
        int left = cargo[i].getQuantity() - cargo[i].getQuantity() * percent / 100;
        int cond = cargo[i].getCondition() - percent;
        if (cond < 0)
            cond = 0;
        if (left == 0) {
            cargo.erase(cargo.begin() + i);
        }
        else {
            cargo[i] = Cargo(cargo[i].getProduct(), left, cond);
            i++;
        }
    }
}

double CargoHold::getTotalMass() const {
    return mass + getCargoMass();
}

string CargoHold::getTypeName() const { return "Грузовой трюм"; }

// ----- Ship -----
Ship::Ship() : Entity(), hull(), location(nullptr), destination(nullptr), turnsLeft(0) {}

Ship::Ship(const string& name, const Hull& hull, Planet* location)
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

vector<Part*> Ship::getParts() {
    vector<Part*> parts;
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
        throw invalid_argument("Ship: нет двигателя");
    if (getFreeSlots() == 0)
        throw logic_error("Ship: на корпусе нет свободных мест");
    engines.push_back(engine);
}

void Ship::installFuelTank(FuelTank* tank) {
    if (tank == nullptr)
        throw invalid_argument("Ship: нет бака");
    if (getFreeSlots() == 0)
        throw logic_error("Ship: на корпусе нет свободных мест");
    tanks.push_back(tank);
}

void Ship::installCargoHold(CargoHold* hold) {
    if (hold == nullptr)
        throw invalid_argument("Ship: нет трюма");
    if (getFreeSlots() == 0)
        throw logic_error("Ship: на корпусе нет свободных мест");
    holds.push_back(hold);
}

double Ship::getTotalMass() const {
    // Для каждой детали через указатель Part* вызывается getTotalMass() её класса
    vector<const Part*> parts;
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

Cargo Ship::unloadCargo(const string& productName, int quantity) {
    if (quantity <= 0)
        throw invalid_argument("Ship: количество не больше 0");

    // Сколько товара есть во всех трюмах
    int available = 0;
    for (size_t i = 0; i < holds.size(); i++) {
        const vector<Cargo>& list = holds[i]->getCargo();
        for (size_t j = 0; j < list.size(); j++)
            if (list[j].getProduct()->getName() == productName)
                available += list[j].getQuantity();
    }
    if (available < quantity)
        throw out_of_range("Ship: товара в трюмах меньше, чем нужно");

    // Вынимаем товар из трюмов по очереди и складываем партии
    Cargo result;
    int left = quantity;
    for (size_t i = 0; i < holds.size() && left > 0; i++) {
        const vector<Cargo>& list = holds[i]->getCargo();
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
    vector<Part*> parts = getParts();
    for (size_t i = 0; i < parts.size(); i++)
        if (parts[i]->isBroken())
            return true;
    return false;
}

string Ship::getTypeName() const { return "Корабль"; }

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
        throw logic_error("Ship: перелёт невозможен");

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

    turnsLeft = (int)ceil(distance / getSpeed());
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
    vector<Part*> parts = getParts();
    for (size_t i = 0; i < parts.size(); i++)
        parts[i]->takeDamage(damage);
}

void Ship::applyHazard(HazardType type, int power) {
    if (power < 0)
        throw invalid_argument("Ship: сила опасности меньше 0");
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

// ----- Market -----
// Названия товаров каталога
static const char* const PRODUCT_NAMES[] = {
    "Еда", "Минералы", "Медикаменты", "Материалы", "Топливо",
    "Бытовая техника", "Промышленная техника", "Предметы роскоши"
};
static const int PRODUCT_COUNT = 8;

// Коэффициент цены товара, который производит планета
static const double CHEAP_FACTOR = 0.6;
// Коэффициент цены товара во время события
static const double EVENT_FACTOR = 1.5;

Market::Market() : kind(MarketKind::Shop), economy(EconomyType::Agrarian) {
    for (int i = 0; i < PRODUCT_COUNT; i++)
        priceFactors[PRODUCT_NAMES[i]] = 1.0;
}

Market::Market(MarketKind kind) : kind(kind), economy(EconomyType::Agrarian) {
    for (int i = 0; i < PRODUCT_COUNT; i++)
        priceFactors[PRODUCT_NAMES[i]] = 1.0;
}

MarketKind Market::getKind() const { return kind; }

void Market::addStock(const Cargo& c) {
    if (c.getProduct() == nullptr)
        throw invalid_argument("Market: партия без товара");
    for (size_t i = 0; i < stock.size(); i++) {
        if (*stock[i].getProduct() == *c.getProduct()) {
            stock[i] = stock[i] + c;
            return;
        }
    }
    stock.push_back(c);
}

const vector<Cargo>& Market::getStock() const { return stock; }

void Market::setPriceFactor(const string& productName, double factor) {
    if (factor <= 0)
        throw invalid_argument("Market: коэффициент не больше 0");
    priceFactors[productName] = factor;
}

int Market::getSellPrice(const Product& p) const {
    double factor = 1.0;
    map<string, double>::const_iterator it = priceFactors.find(p.getName());
    if (it != priceFactors.end())
        factor = it->second;
    return (int)(p.getPrice() * factor + 0.5);
}

int Market::getBuyPrice(const Product& p) const {
    return (int)(getSellPrice(p) * BUY_RATIO);
}

bool Market::sellToPlayer(const string& productName, int quantity, Player& player, Ship& ship) {
    if (quantity <= 0)
        return false;
    if (kind == MarketKind::Warehouse && quantity < WHOLESALE_MIN)
        return false;

    for (size_t i = 0; i < stock.size(); i++) {
        if (stock[i].getProduct()->getName() != productName)
            continue;
        if (stock[i].getQuantity() < quantity)
            return false;
        int cost = getSellPrice(*stock[i].getProduct()) * quantity;
        if (!player.canPay(cost))
            return false;
        Cargo bought(stock[i].getProduct(), quantity, stock[i].getCondition());
        if (!ship.loadCargo(bought))
            return false;
        player.pay(cost);
        stock[i] -= quantity;
        if (stock[i].getQuantity() == 0)
            stock.erase(stock.begin() + i);
        return true;
    }
    return false;
}

bool Market::buyFromPlayer(const string& productName, int quantity, Player& player, Ship& ship) {
    if (quantity <= 0)
        return false;
    Cargo sold;
    try {
        sold = ship.unloadCargo(productName, quantity);
    }
    catch (const out_of_range&) {
        return false;
    }
    int income = getBuyPrice(*sold.getProduct()) * sold.getQuantity() * sold.getCondition() / 100;
    player.earn(income);
    addStock(sold);
    return true;
}

void Market::applyEconomy(EconomyType economy) {
    this->economy = economy;
    for (int i = 0; i < PRODUCT_COUNT; i++)
        priceFactors[PRODUCT_NAMES[i]] = 1.0;

    switch (economy) {
    case EconomyType::Agrarian:
        priceFactors["Еда"] = CHEAP_FACTOR;
        break;
    case EconomyType::Industrial:
        priceFactors["Минералы"] = CHEAP_FACTOR;
        priceFactors["Материалы"] = CHEAP_FACTOR;
        priceFactors["Промышленная техника"] = CHEAP_FACTOR;
        break;
    case EconomyType::Tech:
        priceFactors["Бытовая техника"] = CHEAP_FACTOR;
        priceFactors["Медикаменты"] = CHEAP_FACTOR;
        priceFactors["Предметы роскоши"] = CHEAP_FACTOR;
        break;
    }
}

void Market::applyEvent(EventType event) {
    applyEconomy(economy);
    switch (event) {
    case EventType::None:
        break;
    case EventType::War:
        priceFactors["Топливо"] *= EVENT_FACTOR;
        priceFactors["Бытовая техника"] *= EVENT_FACTOR;
        priceFactors["Промышленная техника"] *= EVENT_FACTOR;
        break;
    case EventType::Epidemic:
        priceFactors["Медикаменты"] *= EVENT_FACTOR;
        break;
    case EventType::Catastrophe:
        priceFactors["Еда"] *= EVENT_FACTOR;
        priceFactors["Материалы"] *= EVENT_FACTOR;
        break;
    }
}

// ----- Shipyard -----
Shipyard::Shipyard() : repairCostPerPoint(5) {}

Shipyard::Shipyard(int repairCostPerPoint) : repairCostPerPoint(repairCostPerPoint) {
    if (repairCostPerPoint <= 0)
        throw invalid_argument("Shipyard: цена ремонта не больше 0");
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
        throw invalid_argument("Shipyard: нет двигателя");
    engines.push_back(engine);
}

void Shipyard::addFuelTank(FuelTank* tank) {
    if (tank == nullptr)
        throw invalid_argument("Shipyard: нет бака");
    tanks.push_back(tank);
}

void Shipyard::addCargoHold(CargoHold* hold) {
    if (hold == nullptr)
        throw invalid_argument("Shipyard: нет трюма");
    holds.push_back(hold);
}

const vector<Engine*>& Shipyard::getEngines() const { return engines; }

const vector<FuelTank*>& Shipyard::getFuelTanks() const { return tanks; }

const vector<CargoHold*>& Shipyard::getCargoHolds() const { return holds; }

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
    vector<Part*> parts = ship.getParts();
    for (size_t i = 0; i < parts.size(); i++)
        parts[i]->repair(parts[i]->getMaxDurability());
    return true;
}

// ----- Planet -----
Planet::Planet()
    : Entity(), x(0), y(0), economy(EconomyType::Agrarian),
    event(EventType::None), eventTurnsLeft(0), market(), shipyard() {
    market.applyEconomy(economy);
}

Planet::Planet(const string& name, double x, double y, EconomyType economy)
    : Entity(name), x(x), y(y), economy(economy),
    event(EventType::None), eventTurnsLeft(0), market(), shipyard() {
    if (x < 0 || x > MAP_SIZE - 1 || y < 0 || y > MAP_SIZE - 1)
        throw invalid_argument("Planet: координаты вне карты");
    market.applyEconomy(economy);
}

double Planet::getX() const { return x; }

double Planet::getY() const { return y; }

EconomyType Planet::getEconomy() const { return economy; }

EventType Planet::getEvent() const { return event; }

double Planet::distanceTo(const Planet& other) const {
    double dx = x - other.x;
    double dy = y - other.y;
    return sqrt(dx * dx + dy * dy);
}

void Planet::startEvent(EventType event, int turns) {
    if (turns < 0)
        throw invalid_argument("Planet: число ходов меньше 0");
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

string Planet::getTypeName() const { return "Планета"; }

// ----- Player -----
Player::Player() : Entity(), balance(0) {}

Player::Player(const string& name, int balance) : Entity(name), balance(balance) {
    if (balance < 0)
        throw invalid_argument("Player: баланс меньше 0");
}

Player::~Player() {
    for (size_t i = 0; i < fleet.size(); i++)
        delete fleet[i];
}

int Player::getBalance() const { return balance; }

void Player::setBalance(int balance) {
    if (balance < 0)
        throw invalid_argument("Player: баланс меньше 0");
    this->balance = balance;
}

bool Player::canPay(int amount) const { return balance >= amount; }

void Player::pay(int amount) {
    if (amount < 0)
        throw invalid_argument("Player: сумма меньше 0");
    if (!canPay(amount))
        throw runtime_error("Player: не хватает денег");
    balance -= amount;
}

void Player::earn(int amount) {
    if (amount < 0)
        throw invalid_argument("Player: сумма меньше 0");
    balance += amount;
}

void Player::addShip(Ship* ship) {
    if (ship == nullptr)
        throw invalid_argument("Player: нет корабля");
    fleet.push_back(ship);
}

Ship& Player::getShip(int index) {
    if (index < 0 || index >= (int)fleet.size())
        throw out_of_range("Player: нет корабля с таким номером");
    return *fleet[index];
}

int Player::getFleetSize() const { return (int)fleet.size(); }

string Player::getTypeName() const { return "Игрок"; }

// ===== Проверка классов =====
// Проверка классов предметной области «Space Tracking».
// Игрового цикла и интерфейса здесь нет: main создаёт объекты
// и по шагам вызывает их методы.


static void printShip(Ship& ship) {
    printf("%s «%s»: масса %.2f т, скорость %.2f св. лет/ход, топливо %.1f\n",
        ship.getTypeName().c_str(), ship.getName().c_str(),
        ship.getTotalMass(), ship.getSpeed(), ship.getFuel());
    vector<Part*> parts = ship.getParts();
    for (size_t i = 0; i < parts.size(); i++) {
        printf("  %-14s %-22s прочность %3d/%-3d масса с содержимым %.2f т\n",
            parts[i]->getTypeName().c_str(), parts[i]->getName().c_str(),
            parts[i]->getDurability(), parts[i]->getMaxDurability(),
            parts[i]->getTotalMass());
    }
}

static void printStock(Market& market, const char* planetName) {
    printf("Рынок планеты %s:\n", planetName);
    const vector<Cargo>& stock = market.getStock();
    for (size_t i = 0; i < stock.size(); i++) {
        const Product* p = stock[i].getProduct();
        printf("  %-22s %4d шт.  продажа %4d  покупка %4d\n", p->getName().c_str(),
            stock[i].getQuantity(), market.getSellPrice(*p), market.getBuyPrice(*p));
    }
}

int main() {
    setlocale(LC_ALL, "Russian");
    try {
        // Каталог товаров
        Product food("Еда", 20, 0.5);
        Product meds("Медикаменты", 80, 0.2);
        Product luxury("Предметы роскоши", 200, 0.1);

        // Планеты
        Planet terra("Терра", 1, 1, EconomyType::Agrarian);
        Planet nova("Нова", 7, 5, EconomyType::Tech);

        terra.getMarket().addStock(Cargo(&food, 200));
        terra.getMarket().addStock(Cargo(&meds, 50));
        nova.getMarket().addStock(Cargo(&luxury, 30));

        terra.getShipyard().addEngine(new Engine("Ионный И-1", 3, 50, 800, 60, 0.5));
        terra.getShipyard().addFuelTank(new FuelTank("Бак Б-100", 2, 40, 300, 100));
        terra.getShipyard().addCargoHold(new CargoHold("Трюм Т-50", 4, 60, 500, 50));

        // Игрок и корабль
        Player player("Капитан", 5000);
        Ship* ship = new Ship("Ласточка", Hull("Корпус К-3", 10, 100, 1000, 20, 3), &terra);
        player.addShip(ship);

        Shipyard& yard = terra.getShipyard();
        yard.sellEngine(0, player, *ship);
        yard.sellFuelTank(0, player, *ship);
        yard.sellCargoHold(0, player, *ship);
        printf("После покупки деталей баланс: %d\n", player.getBalance());

        ship->refuel(100);
        printShip(*ship);

        // Покупка товара
        printStock(terra.getMarket(), terra.getName().c_str());
        if (terra.getMarket().sellToPlayer("Еда", 60, player, *ship))
            printf("Куплено 60 ед. еды. Баланс: %d\n", player.getBalance());

        // Перелёт
        printf("Расстояние Терра — Нова: %.2f св. лет\n", terra.distanceTo(nova));
        ship->startFlight(&nova);
        ship->applyHazard(HazardType::Pirates, 10);
        printf("Нападение пиратов во время перелёта.\n");
        while (ship->isInFlight())
            ship->nextTurn();
        printf("Корабль прибыл на планету %s.\n", ship->getLocation()->getName().c_str());
        printShip(*ship);

        // Событие на планете и продажа товара
        nova.startEvent(EventType::Catastrophe, 3);
        if (nova.getMarket().buyFromPlayer("Еда", 54, player, *ship))
            printf("Продано 54 ед. еды. Баланс: %d\n", player.getBalance());

        // Ремонт
        printf("Цена ремонта: %d\n", nova.getShipyard().getRepairCost(*ship));
        if (nova.getShipyard().repairShip(*ship, player))
            printf("Корабль отремонтирован. Баланс: %d\n", player.getBalance());

        // Виртуальный базовый класс: в детали один подобъект Entity.
        // Через Damageable и через Tradable видны одни и те же id и name.
        Engine testEngine("Плазменный П-2", 4, 70, 1500, 120, 0.8);
        Damageable* asDamageable = &testEngine;
        Tradable* asTradable = &testEngine;
        printf("Через Damageable: id %d, %s. Через Tradable: id %d, %s.\n",
            asDamageable->getId(), asDamageable->getName().c_str(),
            asTradable->getId(), asTradable->getName().c_str());

        // Операторы класса Cargo
        Cargo a(&food, 10, 100);
        Cargo b(&food, 30, 60);
        Cargo c = a + b;
        ++c;
        c -= 5;
        printf("Партия: %d шт., состояние %d%%\n", c.getQuantity(), c.getCondition());

        printf("Цель игры: %d кредитов за %d ходов.\n", TARGET_BALANCE, MAX_TURNS);
    }
    catch (const exception& e) {
        printf("Ошибка: %s\n", e.what());
        return 1;
    }
    return 0;
}
