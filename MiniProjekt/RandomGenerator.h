// File: RandomGenerator.h
#ifndef MINIPROJEKT_RANDOMGENERATOR_H
#define MINIPROJEKT_RANDOMGENERATOR_H

#include <random>

class RandomGenerator {
public:
    RandomGenerator();
    int nextInt(int min, int max);
    double nextDouble(double min, double max);

private:
    std::mt19937_64 engine;
};

#endif //MINIPROJEKT_RANDOMGENERATOR_H
