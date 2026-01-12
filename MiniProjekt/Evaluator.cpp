//
// Created by Dominik on 02.01.2026.
//


// Z PLIKOW
// ID 1 to DEPOT
// ID 2... to KLIENCi
// GENOTYP MA MIEC ROZMIAR ROWNY LICZBIE KLIENTÓW
// DLA KAZDEGO GENU STOSUJEMY PRZESUNIECIE -2: TZN pierwszy klient (ID 2) = genotype [0]
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
    if (static_cast<int>(data.getVisitOrder().size()) != data.getCustomerCount())
        return Result<void, Error>::fail(new Error("PERMUTATION_WRONG_SIZE"));

    // sprawdzenie czy klient nie zostanie przyporządkowany dwa razy do jednego samochodu
    std::vector<bool> seen(data.getCustomerCount(), false);
    for (const int clientID : data.getVisitOrder()) {
        //pierwszy klient ma ID2 a ostatni ma ID = clientsCount + 1 (bo id = 1 to magazyn)
        if (clientID < 2 || clientID>data.getCustomerCount()+1) return Result<void, Error>::fail(new Error("INVALID_PERMUTATION"));
        if (seen[clientID]) {
            return Result<void, Error>::fail(new Error("PERMUTATION_DUPLICATE"));
        }
            seen[clientID] = true;
    }

    if (!checkIfProblemIsSolvable())
        return Result<void, Error>::fail(new Error("PROBLEM_UNSOLVABLE"));


    numVehicles = data.getFleetSize();

    return Result<void, Error>::ok();
}

Result<double, Error> Evaluator::evaluate(const std::vector<int>& genotype) const {
    const int maxCapacity = data.getCapacityLimit();
    const int depot = data.getDepotNode() - 1; // indeks magazynu = 0
    const vector<int>& demands = data.getDemands(); // indeks 0 = magazyn
    const vector<int>& permutation = data.getVisitOrder(); // kolejność klientów (pierwszy klient ID 2)

    vector<int> loads(numVehicles, 0); //aktualny ładunek kazdego samochodu
    vector<double> distances(numVehicles, 0.0); //aktualny dystans kazdego samochcodu
    vector<int> lastPos(numVehicles, depot); // ostatnia pozycja kazdego samochodu
    vector<bool> used(numVehicles, false); // czy dany samochod zostal zuzyty

    const bool hasDistanceLimit = data.hasDistanceLimit();
    const double maxDistance = data.getMaxDistance();

    if (static_cast<int>(genotype.size()) != data.getCustomerCount())
        return Result<double, Error>::fail(new Error("GENOTYPE_SIZE_MISMATCH"));

    for (int p : permutation) {
        if (p == data.getDepotNode()) continue;

        // indeks w macierzy dystansu/obciążeń -> indeks 0 = magazyn (ID1), indeks 1 = pierwszy klient (ID 2)
        int clientDistIdx = p - 1;

        //indeks w genotypie (samochodu) dla klienta, p-2 bo i-ty indeks w genotypie to ID = i + 2,
        //np genotype[0] -> samochód dla klienta pierwszego (ID 2), genotype[1] -> samochód dla drugiego klienta (ID3)
        int genotypeIdx = p - 2;

        //samochód dla klienta
        int v = genotype[genotypeIdx];

        // dla samochodu v, który jedzie do klienta p doliczamy statysyki
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
        //dla kazdego użytego samochodu doliczamy dystans od ostatniego odwiedzonego klienta do magazynu
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

    return Result<double, Error>::ok(1.0 / (totalDist + static_cast<double>(totalPenalty)));
}

// zwraca false gdy kazdy demand z pliku bedzie wiekszy od capacity
bool Evaluator::checkIfProblemIsSolvable() const {
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




