#include <iostream>
#include <cmath>

int transposition(int &seq, int count) {
    int loser = 1;

    bool isPrevOne;
    bool isZero;

    for (int i = 0; i < count - 1; ++i) {
        isPrevOne = seq & loser;
        isZero = ~seq & (loser << 1);

        if (isPrevOne && isZero) {
//          swap bits
            seq -= pow(2, i) - pow(2, i + 1);
            return i;
        }
        loser = loser << 1;
    }
    return -1;
}

int shift(int seq, int count) {
    int res = seq;
    for (int i = 0; i < count; ++i) {
        if (~(seq >> i) & 1) {
            res -= pow(2, count - i - 1) - pow(2, i);
        } else {
            return res;
        }
    }

    return res;
}

void printSequence(int sequence, int count, std::string word) {
    std::cout << '{';
    for(int i = 0; i < count; ++i) {
        bool digit = (sequence >> i) & 1;
        if (digit) {
            std::cout << word[i];
        }
    }
    std::cout << "} ";
}

unsigned char nextSequence(int seq, int count) {
    int index = transposition(seq, count);
    seq = shift(seq, index);
    return seq;
}

int main() {
    std::string word = "INTEGRAL";
    int cells = 4;

    int count = word.size();

    int sequence = pow(2, cells) - 1;
    int curr_sequence = sequence;
    sequence = sequence << cells;

    int i = 0;
    do {
        ++i;
        printSequence(curr_sequence, count, word);
        curr_sequence = nextSequence(curr_sequence, count);
        if (i % 5 == 0) {
            std::cout << std::endl;
        }
    } while(sequence != curr_sequence);
    printSequence(curr_sequence, count, word);

    std::cout << "\nCombinations displayed:" << ++i << std::endl;
    return 0;
}