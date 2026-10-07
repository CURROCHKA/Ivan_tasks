#include "Market.h"
#include "Constants.h"
#include "Player.h"
#include "Ship.h"
#include <stdexcept>

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
        throw std::invalid_argument("Market: партия без товара");
    for (size_t i = 0; i < stock.size(); i++) {
        if (*stock[i].getProduct() == *c.getProduct()) {
            stock[i] = stock[i] + c;
            return;
        }
    }
    stock.push_back(c);
}

const std::vector<Cargo>& Market::getStock() const { return stock; }

void Market::setPriceFactor(const std::string& productName, double factor) {
    if (factor <= 0)
        throw std::invalid_argument("Market: коэффициент не больше 0");
    priceFactors[productName] = factor;
}

int Market::getSellPrice(const Product& p) const {
    double factor = 1.0;
    std::map<std::string, double>::const_iterator it = priceFactors.find(p.getName());
    if (it != priceFactors.end())
        factor = it->second;
    return (int)(p.getPrice() * factor + 0.5);
}

int Market::getBuyPrice(const Product& p) const {
    return (int)(getSellPrice(p) * BUY_RATIO);
}

bool Market::sellToPlayer(const std::string& productName, int quantity, Player& player, Ship& ship) {
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

bool Market::buyFromPlayer(const std::string& productName, int quantity, Player& player, Ship& ship) {
    if (quantity <= 0)
        return false;
    Cargo sold;
    try {
        sold = ship.unloadCargo(productName, quantity);
    } catch (const std::out_of_range&) {
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
