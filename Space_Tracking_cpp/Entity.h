#pragma once
#include <string>

// Объект игры: уникальный номер и название
class Entity {
protected:
    int id;
    std::string name;

private:
    static int nextId;

public:
    Entity();
    Entity(const std::string& name);
    virtual ~Entity();

    int getId() const;
    std::string getName() const;
    void setName(const std::string& name);
    virtual std::string getTypeName() const;
};
