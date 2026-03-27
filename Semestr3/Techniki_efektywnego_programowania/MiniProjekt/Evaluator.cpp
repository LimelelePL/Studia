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
    //pierwszy klient w permutacji ma ID2 a ostatni ma ID = clientsCount + 1 (bo id = 1 to magazyn)
    int firstClientID = 2;
    int lastClientID = data.getCustomerCount() + 1;
    std::vector<bool> seen(data.getCustomerCount() + firstClientID, false);
    for (const int clientID : data.getVisitOrder()) {
        if (clientID == getDepotNode() || clientID < firstClientID || clientID > lastClientID) {
            return Result<void, Error>::fail(new Error("INVALID_PERMUTATION"));
        }
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
    const int depot = data.getDepotNode() - 1; // indeks magazynu = 0 (ID1)
    const vector<int>& demands = data.getDemands(); // indeks 0 = magazyn (ID1), indeks 1 klient (ID 2)
    const vector<int>& permutation = data.getVisitOrder(); // kolejność klientów (pierwszy klient ID 2)

    vector<int> loads(numVehicles, 0); //aktualny ładunek kazdego samochodu
    vector<double> distances(numVehicles, 0.0); //aktualny dystans kazdego samochcodu
    vector<int> lastPos(numVehicles, depot); // ostatnia pozycja kazdego samochodu
    vector<bool> used(numVehicles, false); // czy dany samochod zostal zuzyty

    const bool hasDistanceLimit = data.hasDistanceLimit();
    const double maxDistance = data.getMaxDistance();

    if (static_cast<int>(genotype.size()) != data.getCustomerCount() || genotype.size() != permutation.size())
        return Result<double, Error>::fail(new Error("GENOTYPE_SIZE_MISMATCH"));

    for (int p : permutation) {
        // indeks w macierzy dystansu/obciążeń = ID - 1
        // indeks 0 = magazyn (ID1), indeks 1 = pierwszy klient (ID 2), indeks 2 drugi klient (ID 3)
        int clientDataIdx = p - 1;

        //indeks w genotypie (samochodu dla klienta) p-2 bo i-ty indeks w permutacji to ID - 2;
        //genotype[0] -> samochód dla klienta pierwszego z permutacji (ID 2)
        //genotype[1] -> samochód dla drugiego klienta z permutacji (ID3)
        int genotypeIdx = p - 2;

        /* PRZYKŁAD
        * genotyp [0,1,1,5]
        * permutacja [2,4,3,5]

        * p = 2 -> genotypeIdx = 0 -> v = 0
        * p = 4 -> genotypeIdx = 2 -> v = 1
        * p = 3 -> genotypeIdx = 1 -> v = 1
        * p = 5 -> genotypeIdx = 3 -> v = 5
        */

        //samochód dla klienta
        int v = genotype[genotypeIdx];

        // dla samochodu v, który jedzie do klienta p doliczamy statysyki
        if (v >= 0 && v < numVehicles) {
            distances[v] += data.calculateDistance(lastPos[v], clientDataIdx);
            loads[v] += demands[clientDataIdx];
            lastPos[v] = clientDataIdx;
            used[v] = true;
        }
    }

    double totalDist = 0;
    double totalPenalty = 0;

    for (int v = 0; v < numVehicles; v++) {
        //dla kazdego użytego samochodu doliczamy dystans od ostatniego odwiedzonego klienta do magazynu
        if (used[v]) {
            double vehicleFullRouteDist = distances[v] + data.calculateDistance(lastPos[v], depot);
            totalDist += vehicleFullRouteDist;

        // kara za przekroczenie dystansu przejechanego przez samochód
            if (hasDistanceLimit && vehicleFullRouteDist > maxDistance) {
                totalPenalty += (vehicleFullRouteDist - maxDistance) * DEFAULT_PENALTY/DISTANCE_PENALTY_SCALER;
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




