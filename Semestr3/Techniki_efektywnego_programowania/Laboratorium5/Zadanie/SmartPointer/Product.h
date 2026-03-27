//
// Created by Dominik on 17.12.2025.
//

#ifndef ZADANIE_PRODUCT_H
#define ZADANIE_PRODUCT_H
#include <string>
#include <vector>

#include "SmartPointer.h"


class Product {
public:
    explicit Product(std::string name);

    std::string getProduct();
private:
    std::string name;
};


#endif //ZADANIE_PRODUCT_H