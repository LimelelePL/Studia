//
// Created by Dominik on 02.01.2026.
//

#include "Individual.h"

#include "ConstantValues.h"
#include "RandomGenerator.h"

Individual::Individual(const std::vector<int>& genotype) {
    this-> genotype = genotype;
    this-> fitness = DEFAULT_FITNESS;
}

Individual::Individual(const Individual &other) {
    this -> genotype = other.genotype;
    this -> fitness = other.fitness;
}

// oblicza fitness dla każdego osobnika
double Individual::initFitness(const Evaluator &eval) {
    auto result = eval.evaluate(genotype);
    if(result.isSuccess()) {
        fitness = result.getValue();
    } else {
        fitness = DEFAULT_FITNESS;
    }
    return fitness;
}

std::pair<Individual, Individual> Individual::cross(const Individual& other, RandomGenerator& generator) const {
    const int size = static_cast<int>(genotype.size());
    const int cutPoint = generator.nextInt(1,size-1);

    // tworzymy dwoje dzieci
    Individual child1(*this);
    Individual child2(other);

    //wymiana genotypow od punktu przecieciecia
    for (int i = cutPoint; i<size; i++) {
        child1.genotype[i] = other.genotype[i];
        child2.genotype[i] = this->genotype[i];
    }

    // po modyfikacji genotypów należy ponownie policzyc funkcje przystosowania w algorytmie genetycznym
    child1.fitness = DEFAULT_FITNESS;
    child2.fitness = DEFAULT_FITNESS;

    return {child1, child2};
}

void Individual::mutate(const double mutProb, RandomGenerator& generator, const int numVehicles) {

    for (int &gene : genotype) {
        // mutuje tylko ten gen który spełnia warunek p<=mutProb
        const bool shouldMutate = generator.nextDouble(0,1) <= mutProb;
        if (shouldMutate) {
            const int newGen = generator.nextInt(0, numVehicles - 1);
            gene = newGen;
            // po zmianie choc jednego genu przystosowanie musi byc obliczone ponownie
            this->fitness = DEFAULT_FITNESS;
        }
    }
}

const std::vector<int> &Individual::getGenotype() const {
    return genotype;
}

double Individual::getFitnes() const {
    return fitness;
}

