#include <fstream>
#include <iostream>
#include <iostream>
#include <string>
#include "Evaluator.h"
#include "GeneticAlgorithm.h"

// void manualTest() {
//     std::string folder = "Vrp-Set-A";
//     std::string file = "A-n31-mojTest";
//
//     Evaluator evaluator;
//     std::cout << "Laduje problem: " << file << "..." << std::endl;
//
//     if (!evaluator.loadFromFile(folder, file)) {
//         std::cerr << "nie udalo sie zaladowac pliku " << std::endl;
//     }
//
//     std::vector<int> testGenotype = {0, 1, 0};
//
//     Individual ind(testGenotype);
//     double fitness = ind.initFitness(evaluator);
//     std::cout << "Mianownik (Dystans + Kara): " << 1.0 / fitness << std::endl;
//     std::cout << "Oczekiwany wynik: 5020" << std::endl;
// }

int main() {

    // P-n19-k2 wynik 212
    // XML100_2174_01 wynik 16328
    // X-n209-k16 wynik 119957
    // Leuven2 4 811 620


    const std::string path = "data/wyniki.txt";
    std::ofstream ofs(path, std::ios::trunc);

    std::string folder = "Vrp-Set-A";
    std::string file = "A-n31-mojTest";

    Evaluator evaluator;

    Result<void, Error> loadResult = evaluator.loadFromFile(folder,file);

    if (!loadResult.isSuccess()) {
        std::cout << "BLAD KRYTYCZNY PODCZAS LADOWANIA:" << std::endl;
        for (const Error* err : loadResult.getErrors()) {
            std::cout << " -> " << err->getCode() << std::endl;
        }
        return 1;
    }

    int populationSize = 100;
    double crossoverProbability = 0.8;
    double mutationProbability = 0.05;
    int iterations = 500;
    RandomGenerator generator;

    GeneticAlgorithm ga(evaluator, generator, populationSize, crossoverProbability, mutationProbability, iterations);

    std::cout << "Rozpoczynam ewolucje!" << std::endl;
    ga.run();

    std::cout << "\n=== WYNIK KONCOWY ===" << std::endl;

    ga.printDetailedBest();

    //manualTest();
    return 0;
}
