#include <iostream>
#include <vector>

#define ARRAY_LENGHT 9

std::ostream &operator<< (std::ostream &out, const std::vector<int> &in) {
    for (auto &i: in) {
        out << i << " ";
    }
    return out;
}

void factorialLeftComplementAlgorithm(std::vector<int> &array, int &globalCounter, int max) {
    int curDepth = array.size();
    std::vector<int> initArray = array;

    for (int m = 1; m != initArray.size() + 2; ++m) {
        array = initArray;
        array.insert(array.begin(), 1, m);

        for (int i = 1; i != curDepth + 1; ++i) {
            array[i] += array[i] >= m ? 1 : 0;
        }

        if (array.size() == max) {
            std::cout << globalCounter++ << ") " << array << std::endl;
            continue;
        }

        if (m == array.size() + 1) {
            return;
        }

        factorialLeftComplementAlgorithm(array, globalCounter, max);
    }
}

int main() {
    int globalCounter = 1;
    std::vector<int> array;
    array.push_back(1);

    factorialLeftComplementAlgorithm(array, globalCounter, ARRAY_LENGHT);
}