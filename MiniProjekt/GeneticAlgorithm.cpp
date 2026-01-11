//
// Created by Dominik on 02.01.2026.
//

#include "GeneticAlgorithm.h"

#include <iostream>
#include <sstream>

#include "ConstantValues.h"

static void printGenotype(Individual& ind, const std::string& file) {
    const std::vector<int>& genotype = ind.getGenotype();
    std::ostringstream oss;
    oss << "Genotyp: ";
    for (size_t i = 0; i < genotype.size(); ++i) {
        oss << genotype[i];
        if (i < genotype.size() - 1) oss << ",";
    }
    oss << " | size: " << genotype.size() << std::endl;
    // wypisz na konsolę
    std::cout << oss.str();

    // zapisz do pliku (append), jeśli podano nazwę
    if (!file.empty()) {
        std::ofstream ofs(file, std::ios::app);
        if (!ofs) {
            std::cerr << "Nie można otworzyć pliku: " << file << std::endl;
        } else {
            ofs << oss.str();
        }
    }
}

GeneticAlgorithm::GeneticAlgorithm(Evaluator &eval, RandomGenerator& generator, int popSize, double crossProb, double mutProb, int maxIterations) :
crossProb(crossProb), mutProb(mutProb), maxIterations(maxIterations), bestSolution(nullptr), eval(eval), gen(generator) {

    if (mutProb > 1 || mutProb < 0) {
        this->mutProb = DEFAULT_PROB;
    }
    if (crossProb > 1 || crossProb < 0) {
        this->crossProb = DEFAULT_PROB;
    }
    if (popSize < MIN_POPSIZE) {
        this->popSize = DEFAULT_POPSIZE;
    } else {
        this->popSize = popSize;
    }
}

GeneticAlgorithm::~GeneticAlgorithm() {
    delete bestSolution;
}

void GeneticAlgorithm::run() {
    //generujemy popsize gotowych rozwiazan
    genRandomPopulation();

    for (int i = 0; i < maxIterations; i++) {

        // krzyzowanie ustawia fitness krzyzowanych na -1
        crossPopulation();

        for (size_t j = 1; j < population.size(); j++) {
            population[j].mutate(mutProb, gen, eval.getNumVehicles());
        }

        calcFitness();

        Individual &currentBest = currentIterationBestSolution();
        if (bestSolution == nullptr || currentBest.getFitnes() > bestSolution->getFitnes()) {
            delete bestSolution;
            bestSolution = new Individual(currentBest);

            cout<<"nowy najlepszy " << bestSolution->getFitnes() << endl;
            printGenotype(*bestSolution, "data/wyniki.txt");
        }

    }
}


void GeneticAlgorithm::crossPopulation() {
    vector<Individual> newPopulation;

    if (bestSolution != nullptr) {
        newPopulation.push_back(*bestSolution);
    }

    while (newPopulation.size() < popSize){
        double prob = gen.nextDouble(0,1);

        Individual& parent1 = selectParents();
        Individual& parent2 = selectParents();

        if (prob > crossProb) {
            newPopulation.push_back(parent1);
            newPopulation.push_back(parent2);
        } else {
            pair<Individual,Individual> crossed = parent1.cross(parent2, gen);

            newPopulation.push_back(crossed.first);
            newPopulation.push_back(crossed.second);

        }
    }

    // gdyby przekroczylo popsize
    if (newPopulation.size() > popSize) {
        newPopulation.pop_back();
    }

    this->population = std::move(newPopulation);

}

void GeneticAlgorithm::genRandomPopulation() {
    const int numVehicles = eval.getNumVehicles();
    const int numClients = eval.getNumClients();

    for (int i = 0; i<popSize; i++) {
        std::vector<int> randGenotype;
        // genotyp to przypisanie klientów
        for (int j = 0; j<numClients; j++) {
            // losujemy pojazd dla klienta
            int gene = gen.nextInt(0,numVehicles-1);
            randGenotype.push_back(gene);
        }
        Individual individual(randGenotype);
        individual.initFitness(eval);
        population.push_back(individual);
    }
    calcFitness();
}

Individual& GeneticAlgorithm::selectParents() {
    //losujemy 1 kandyata
    int bestIdx = gen.nextInt(0, popSize - 1);

    int minSize = 2;
    int optimalSize = 5;

    if (optimalSize > popSize) optimalSize = minSize;

    // Losujemy resztę zawodników turnieju (tutaj 4)
    for (int i = 1; i < optimalSize; i++) {
        int contenderIdx = gen.nextInt(0, popSize - 1);

        if (population[contenderIdx].getFitnes() > population[bestIdx].getFitnes()) {
            bestIdx = contenderIdx;
        }
    }
    return population[bestIdx];
}

Individual& GeneticAlgorithm::currentIterationBestSolution() {
    double bestFitness = -1;
    int bestIndex = 0;

    for (int i = 0; i<popSize; i++) {

        Individual& in = population[i];
        double inFitness = in.getFitnes();

        if (inFitness>=0 && inFitness >= bestFitness) {
            bestFitness = inFitness;
            bestIndex = i;
        }
    }

    return population[bestIndex];
}

void GeneticAlgorithm::calcFitness() {
    for (Individual &in: population) {
        if (in.getFitnes() < 0) {
            in.initFitness(eval);
        }
    }
}

void GeneticAlgorithm::printDetailedBest() {
    if (!bestSolution) return;

    int maxCap = eval.getCapacity();
    const std::vector<int>& genotype = bestSolution->getGenotype();
    const std::vector<int>& demands = eval.getDemands();
    const std::vector<int>& permutation = eval.getPermutation();

    std::vector<int> loads(eval.getNumVehicles(), 0);
    bool overallFeasible = true;

    for (int p : permutation) {
        if (p == eval.getDepotNode()) continue;
        int genotypeIdx = p - 2;
        int clientDistIdx = p - 1;

        if (genotypeIdx >= 0 && genotypeIdx < (int)genotype.size()) {
            int vehicleIdx = genotype[genotypeIdx];
            if (vehicleIdx >= 0 && vehicleIdx < (int)loads.size()) {
                loads[vehicleIdx] += demands[clientDistIdx];
            }
        }
    }

    std::cout << "\n=== SZCZEGOLOWY RAPORT DOPUSZCZALNOSCI ===" << std::endl;
    for (size_t i = 0; i < loads.size(); i++) {
        bool feasible = (loads[i] <= maxCap);
        if (!feasible) overallFeasible = false;

        if (loads[i] > 0) {
            std::cout << "Pojazd #" << i << ": Ladunek = " << loads[i]
                      << " / " << maxCap
                      << (feasible ? " [OK]" : " [PRZEKROCZONE!]") << std::endl;
        }
    }

    std::cout << "------------------------------------------" << std::endl;
    std::cout << "STATUS ROZWIAZANIA: " << (overallFeasible ? "DOPUSZCZALNE" : "NIEDOPUSZCZALNE") << std::endl;
    std::cout << "KONCOWY DYSTANS: " << (1.0 / bestSolution->getFitnes()) << std::endl;

    printGenotype(*bestSolution, "data/wyniki.txt");
}

