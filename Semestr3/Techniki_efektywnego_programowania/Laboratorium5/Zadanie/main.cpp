
#include <iostream>

#include "SmartPointer/SmartPointer.h"
#include "Tree/Interface.h"
int main() {
    Tree ta1;
    Tree ta2;
    Tree ta3;

    ta1.enter("+ a 1");
    ta2.enter("+ 3 a");
    ta3.enter("- 1 1");

    Tree::resetCounters();
    Tree ta4 = std::move(ta2);
    Tree::printCounters();

    Tree::resetCounters();
    Tree ta5 = std::move(ta1 + ta2);
    Tree::printCounters();

    Tree::resetCounters();
    ta2.join("+ 2 2");
    Tree::printCounters();

}
