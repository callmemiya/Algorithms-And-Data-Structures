#include <iostream>
#include <vector>
#include <string>
#include <iterator>
#include <algorithm>
 
int main(){
    std::string arr;
    long long sum = 0;
    while (std::getline(std::cin, arr)){
        int x = 0;
        for (int j = 0; j < arr.size(); j++){
            if (std::isdigit(arr[j])
                || (arr[j] == '-' && j < arr.size() - 1)){
                if (arr[j] == '-' && std::isdigit(arr[j+1])){
                    while (std::isdigit(arr[j+1]) && j + 1 < arr.size()){
                            j++;
                        int b = arr[j] - '0';
                        x = x * 10 + b;
                    }
                    if (j + 1 <  arr.size()) j++;
                    x *= -1;
                    sum += x;
                    x = 0;
                } else {
                    while (std::isdigit(arr[j])){
                        int b = arr[j] - '0';
                        x = x * 10 + b;
                        j++;
                    }
                    sum += x;
                    x = 0;
                }
            }
        }
    }
    std::cout << sum;
    return 0;
}
