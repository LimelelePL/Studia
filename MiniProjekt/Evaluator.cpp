//
// Created by Dominik on 02.01.2026.
//


// Z PLIKOW
// ID 1 to DEPOT
// ID 2... to KLIENCi
// GENOTYP MA MIEC ROZMIAR ROWNY LICZBIE KLIENTÓW
// DLA KAZDEGO GENU STOSUJEMY PRZESUNIECIE -2: TZN klient 2 = genotype [0]
// MACIERZ DEMANDS[0] to magazyn
// PRERMUTACJA[0] = k oznacza ze pierwszym klientem jest klient k

#include "Evaluator.h"
#include <chrono>
#include <iostream>
using namespace std;

#include "ConstantValues.h"

Evaluator::Evaluator() {
    this->numVehicles = DEFAULT_NUMVEHICLES;
}

Result<void,Error> Evaluator::loadFromFile(const std::string &folder, const std::string &name) {
    InstanceReader loader(folder, name);

    auto loadResult = loader.readInstance();

    if (!loadResult.isSuccess()) return Result<void, Error>::fail(loadResult.getErrors());

    this->data = loadResult.getValue();

    if (data.getTotalNodes() <= 0)
        return Result<void, Error>::fail(new Error("INVALID_DIMENSION"));
    if (data.getFleetSize() <= 0)
        return Result<void, Error>::fail(new Error("INVALID_NUM_GROUPS"));
    if (data.getCapacityLimit() <= 0)
        return Result<void, Error>::fail(new Error("INVALID_CAPACITY"));

    // walidacja permutacjii
    if ((int)data.getVisitOrder().size() != data.getCustomerCount())
        return Result<void, Error>::fail(new Error("PERMUTATION_WRONG_SIZE"));

    std::vector<bool> seen(data.getCustomerCount() + 2, false);
    for (const int i : data.getVisitOrder()) {
        if (i < 2 || i>=data.getCustomerCount()+2) return Result<void, Error>::fail(new Error("INVALID_PERMUTATION"));
        if (seen[i]) {
            return Result<void, Error>::fail(new Error("PERMUTATION_DUPLICATE"));
        }
            seen[i] = true;
    }

    if (!checkIfProblemIsSolvable())
        return Result<void, Error>::fail(new Error("PROBLEM_UNSOLVABLE"));


    numVehicles = data.getFleetSize();

    return Result<void, Error>::ok();
}

Result<double, Error> Evaluator::evaluate(const std::vector<int>& genotype) const {
    const int maxCapacity = data.getCapacityLimit();
    const int depot = data.getDepotNode() - 1;
    const vector<int>& demands = data.getDemands();
    const vector<int>& permutation = data.getVisitOrder();

    vector<int> loads(numVehicles, 0);
    vector<double> distances(numVehicles, 0.0);
    vector<int> lastPos(numVehicles, depot);
    vector<bool> used(numVehicles, false);

    const bool hasDistanceLimit = data.hasDistanceLimit();
    const double maxDistance = data.getMaxDistance();

    if (static_cast<int>(genotype.size()) != data.getCustomerCount())
        return Result<double, Error>::fail(new Error("GENOTYPE_SIZE_MISMATCH"));


    for (int p : permutation) {
        if (p == data.getDepotNode()) continue;

        int clientDistIdx = p - 1;
        int genotypeIdx = p - 2; // Klient nr 2 (pierwszy) to gen[0]
        int v = genotype[genotypeIdx];

        if (v >= 0 && v < numVehicles) {

            distances[v] += data.calculateDistance(lastPos[v], clientDistIdx);
            loads[v] += demands[clientDistIdx];
            lastPos[v] = clientDistIdx;
            used[v] = true;
        }
    }

    double totalDist = 0;
    long totalPenalty = 0;

    for (int v = 0; v < numVehicles; v++) {
        if (used[v]) {
            double vehicleFullRouteDist = distances[v] + data.calculateDistance(lastPos[v], depot);
            totalDist += vehicleFullRouteDist;

        // kara za przekroczenie dystansu przejechanego przez samochód
            if (hasDistanceLimit && vehicleFullRouteDist > maxDistance) {
                totalPenalty += (vehicleFullRouteDist - maxDistance) * DEFAULT_PENALTY/100;
            }
        }

        //kara za przeladowanie
        if (loads[v] > maxCapacity) totalPenalty += (loads[v] - maxCapacity) * DEFAULT_PENALTY;
    }

    return Result<double, Error>::ok(1.0 / (totalDist + (double)totalPenalty));
}
// zwraca false gdy dany demand z pliku bedzie wiekszy od capacity
bool Evaluator::checkIfProblemIsSolvable() {
    const int cap = data.getCapacityLimit();
    const std::vector<int>& demands = data.getDemands();

    for (int d : demands) {
        if (d > cap) {
            return false;
        }
    }
    return true;
}

int Evaluator::getNumVehicles() const {
    return numVehicles;
}

int Evaluator::getNumClients() const {
    return data.getCustomerCount();
}




