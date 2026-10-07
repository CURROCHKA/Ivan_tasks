// Проверка классов предметной области «Space Tracking».
// Игрового цикла и интерфейса здесь нет: main создаёт объекты
// и по шагам вызывает их методы.
#include <cstdio>
#include <stdexcept>
#include <vector>
#include "Constants.h"
#include "Product.h"
#include "Cargo.h"
#include "Hull.h"
#include "Engine.h"
#include "FuelTank.h"
#include "CargoHold.h"
#include "Ship.h"
#include "Planet.h"
#include "Player.h"

#ifdef _WIN32
#include <windows.h>
#endif

static void printShip(Ship& ship) {
    std::printf("%s «%s»: масса %.2f т, скорость %.2f св. лет/ход, топливо %.1f\n",
                ship.getTypeName().c_str(), ship.getName().c_str(),
                ship.getTotalMass(), ship.getSpeed(), ship.getFuel());
    std::vector<Part*> parts = ship.getParts();
    for (size_t i = 0; i < parts.size(); i++) {
        std::printf("  %-14s %-22s прочность %3d/%-3d масса с содержимым %.2f т\n",
                    parts[i]->getTypeName().c_str(), parts[i]->getName().c_str(),
                    parts[i]->getDurability(), parts[i]->getMaxDurability(),
                    parts[i]->getTotalMass());
    }
}

static void printStock(Market& market, const char* planetName) {
    std::printf("Рынок планеты %s:\n", planetName);
    const std::vector<Cargo>& stock = market.getStock();
    for (size_t i = 0; i < stock.size(); i++) {
        const Product* p = stock[i].getProduct();
        std::printf("  %-22s %4d шт.  продажа %4d  покупка %4d\n", p->getName().c_str(),
                    stock[i].getQuantity(), market.getSellPrice(*p), market.getBuyPrice(*p));
    }
}

int main() {
#ifdef _WIN32
    SetConsoleOutputCP(CP_UTF8);
#endif
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
        std::printf("После покупки деталей баланс: %d\n", player.getBalance());

        ship->refuel(100);
        printShip(*ship);

        // Покупка товара
        printStock(terra.getMarket(), terra.getName().c_str());
        if (terra.getMarket().sellToPlayer("Еда", 60, player, *ship))
            std::printf("Куплено 60 ед. еды. Баланс: %d\n", player.getBalance());

        // Перелёт
        std::printf("Расстояние Терра — Нова: %.2f св. лет\n", terra.distanceTo(nova));
        ship->startFlight(&nova);
        ship->applyHazard(HazardType::Pirates, 10);
        std::printf("Нападение пиратов во время перелёта.\n");
        while (ship->isInFlight())
            ship->nextTurn();
        std::printf("Корабль прибыл на планету %s.\n", ship->getLocation()->getName().c_str());
        printShip(*ship);

        // Событие на планете и продажа товара
        nova.startEvent(EventType::Catastrophe, 3);
        if (nova.getMarket().buyFromPlayer("Еда", 54, player, *ship))
            std::printf("Продано 54 ед. еды. Баланс: %d\n", player.getBalance());

        // Ремонт
        std::printf("Цена ремонта: %d\n", nova.getShipyard().getRepairCost(*ship));
        if (nova.getShipyard().repairShip(*ship, player))
            std::printf("Корабль отремонтирован. Баланс: %d\n", player.getBalance());

        // Операторы класса Cargo
        Cargo a(&food, 10, 100);
        Cargo b(&food, 30, 60);
        Cargo c = a + b;
        ++c;
        c -= 5;
        std::printf("Партия: %d шт., состояние %d%%\n", c.getQuantity(), c.getCondition());

        std::printf("Цель игры: %d кредитов за %d ходов.\n", TARGET_BALANCE, MAX_TURNS);
    } catch (const std::exception& e) {
        std::printf("Ошибка: %s\n", e.what());
        return 1;
    }
    return 0;
}
