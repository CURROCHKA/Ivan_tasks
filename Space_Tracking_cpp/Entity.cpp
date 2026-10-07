#include "Entity.h"
#include <stdexcept>

int Entity::nextId = 1;

Entity::Entity() : id(nextId++), name("Без названия") {}

Entity::Entity(const std::string& name) : id(nextId++), name(name) {
    if (name.empty())
        throw std::invalid_argument("Entity: пустое название");
}

Entity::~Entity() {}

int Entity::getId() const { return id; }

std::string Entity::getName() const { return name; }

void Entity::setName(const std::string& name) {
    if (name.empty())
        throw std::invalid_argument("Entity: пустое название");
    this->name = name;
}

std::string Entity::getTypeName() const { return "Объект"; }
