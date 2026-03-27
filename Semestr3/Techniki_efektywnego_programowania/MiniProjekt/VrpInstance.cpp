#include "VrpInstance.hpp"
#include <cmath>
#include <algorithm>

Coordinate::Coordinate() : xPos(0.0), yPos(0.0) {}
Coordinate::Coordinate(double x, double y) : xPos(x), yPos(y) {}

VrpInstance::VrpInstance()
    : totalNodes(0), capacityLimit(0), fleetSize(0),
      depotNode(1), maxDistance(0.0), hasDistLimit(false) {}

double VrpInstance::computeEuclidean(const Coordinate& a, const Coordinate& b) {
    double dx = a.xPos - b.xPos;
    double dy = a.yPos - b.yPos;
    return std::sqrt(dx * dx + dy * dy);
}

// zwraca odleglosc miedzy dwoma klientami
// indeks = ID - 1
double VrpInstance::calculateDistance(int i, int j) const {
    if (i < 0 || j < 0 || i >= totalNodes || j >= totalNodes) return -1.0;
    if (i == j) return 0.0;

        return distanceTable[i][j];
}

//na podstawie koordynatów generuje macierz zawierajaca odleglosci miedzy dwoma klientami (dla EUC2d tylko)
void VrpInstance::generateDistanceTable() {
    if (distanceType != "EUC_2D") return;

    distanceTable.assign(totalNodes, std::vector<double>(totalNodes, 0.0));
    for (int i = 0; i < totalNodes; i++)
        for (int j = i + 1; j < totalNodes; j++) {
            double d = computeEuclidean(coordinates[i], coordinates[j]);
            distanceTable[i][j] = d;
            distanceTable[j][i] = d;
        }
}

void VrpInstance::setInstanceName(const std::string& name) { instanceName = name; }
void VrpInstance::setDistanceType(const std::string& type) { distanceType = type; }
void VrpInstance::setMaxDistance(const double dist) { maxDistance = dist; hasDistLimit = true; }
void VrpInstance::setTotalNodes(const int tNodes) {this->totalNodes = tNodes;}
void VrpInstance::setCapacityLimit(const int cLimit) {this->capacityLimit = cLimit;}
void VrpInstance::setVehicleFleet(const int vFleet) { this -> fleetSize = vFleet;}
void VrpInstance::setDepotNode(const int dNode) {this->depotNode = dNode;}

void VrpInstance::assignCoordinates(const std::vector<Coordinate>& coords) { coordinates = coords; }
void VrpInstance::assignDemands(const std::vector<int>& dems) { demands = dems; }
void VrpInstance::assignVisitOrder(const std::vector<int>& order) { visitOrder = order; }
void VrpInstance::assignDistanceTable(const std::vector<std::vector<double>>& table) { distanceTable = table; }

std::string VrpInstance::getInstanceName() const { return instanceName; }
int VrpInstance::getTotalNodes() const { return totalNodes; }
int VrpInstance::getCapacityLimit() const { return capacityLimit; }
int VrpInstance::getFleetSize() const { return fleetSize; }
int VrpInstance::getDepotNode() const { return depotNode; }
int VrpInstance::getCustomerCount() const { return totalNodes > 0 ? totalNodes - 1 : 0; }

bool VrpInstance::hasDistanceLimit() const { return hasDistLimit; }
double VrpInstance::getMaxDistance() const { return hasDistanceLimit() ? maxDistance : -1 ; }

std::string VrpInstance::getDistanceType() const { return distanceType; }

const std::vector<Coordinate>& VrpInstance::getCoordinates() const { return coordinates; }
const std::vector<int>& VrpInstance::getDemands() const { return demands; }
const std::vector<int>& VrpInstance::getVisitOrder() const { return visitOrder; }
const std::vector<std::vector<double>>& VrpInstance::getDistanceTable() const { return distanceTable; }

