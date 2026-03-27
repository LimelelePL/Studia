//
// Created by Dominik on 17.12.2025.
//

#include "Product.h"

#include <utility>

Product::Product(std::string name) {
    this->name = std::move(name);
}

std::string Product::getProduct() {
    return name;
}




