//
// Created by Dominik on 11.12.2025.
//

#ifndef ZADANIE_SMARTPOINTER_H
#define ZADANIE_SMARTPOINTER_H


#include <vector>
#include <map>

#include "RefCounter.h"
using namespace std;

#endif //ZADANIE_SMARTPOINTER_H

class Product;

template<typename T>
class SmartPointer {
public:
    SmartPointer();
    explicit SmartPointer(T* pointer);
    ~SmartPointer();
    SmartPointer(const SmartPointer& other);

    SmartPointer(SmartPointer&& other) noexcept;

    T& operator *();
    T* operator ->();
    SmartPointer& operator =(const SmartPointer& other);
    SmartPointer& operator =(SmartPointer&& other) noexcept;

    RefCounter* getRefcounter() const;
    T* get() const;

private:
    RefCounter* counter;
    T* pointer;
};


template<typename T>
SmartPointer<T>::SmartPointer() {
    pointer = nullptr;
    counter = nullptr;
}

template<typename T>
SmartPointer<T>::SmartPointer(T *pointer) {
    this->pointer = pointer;
    this->counter = new RefCounter();
    counter->add();
}

template<typename T>
SmartPointer<T>::~SmartPointer() {
    if (counter!=nullptr) {
        if (counter->dec() == 0 ) {
            delete pointer;
            delete counter;
            pointer = nullptr;
            counter = nullptr;
        }
    }
}

template<typename T>
SmartPointer<T>::SmartPointer(const SmartPointer &other) {
    pointer = other.pointer;
    counter = other.counter;
    if (counter!=nullptr) counter->add();
}

template<typename T>
SmartPointer<T>::SmartPointer(SmartPointer &&other) noexcept {
    pointer = other.pointer;
    counter = other.counter;
    other.counter = nullptr;
    other.pointer = nullptr;
}

template<typename T>
SmartPointer<T> & SmartPointer<T>::operator=(const SmartPointer &other) {
    if (this == &other) {
        return *this;
    }

    if (counter!=nullptr) {
        if (counter->dec() == 0) {
            delete pointer;
            delete counter;
            pointer = nullptr;
            counter = nullptr;
        }
    }

    pointer = other.pointer;
    counter = other.counter;

    if (counter != nullptr) counter->add();

    return *this;
}

template<typename T>
SmartPointer<T> & SmartPointer<T>::operator=(SmartPointer &&other) noexcept {
    if (this == &other) return *this;

    if (counter != nullptr) {
        if (counter->dec() == 0) {
            delete pointer;
            delete counter;
            pointer = nullptr;
            counter = nullptr;
        }
    }

    pointer = other.pointer;
    counter = other.counter;
    other.pointer = nullptr;
    other.counter = nullptr;

    return *this;
}

template<typename T>
T & SmartPointer<T>::operator*() {
    return *pointer;
}

template<typename T>
T * SmartPointer<T>::operator->() {
    return pointer;
}

template<typename T>
RefCounter* SmartPointer<T>:: getRefcounter() const {
    return counter;
}


template<typename T>
T* SmartPointer<T>::get() const {
    return pointer;
}


struct ElfReport {
    int validGifts;
    int lostInstructions;
    int productsWithMissing;
};

ElfReport analyzeInstructions(std::vector<SmartPointer<Product> >& instructions){
    ElfReport report{};
    report.validGifts = 0;
    report.lostInstructions = 0;
    report.productsWithMissing = 0;

    map<Product*, RefCounter*> productMap;

    for (size_t i = 0; i < instructions.size(); i++) {
        Product* p = instructions[i].get();
        if (p != nullptr) {
            productMap[p] = instructions[i].getRefcounter();
        }
    }

    for (auto & it : productMap){
        int refCount = it.second->get();

        // 1 produkt - 1 prezent
        report.validGifts++;

        if (refCount > 1) {
            report.lostInstructions += (refCount - 1);
            report.productsWithMissing++;
        }
        else if (refCount == 0) {
            //wszystkie zgubuone
            report.lostInstructions++;
            report.productsWithMissing++;
        }
    }

    return report;
}

