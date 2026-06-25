//github.com/ANSH-ind
//owner name: ansh raj
//part of: ansh_tokinizer
//from: india
#include <iostream>
#include <cstdint>
#include <cmath>
#include <utility>
#include <string>

void find_magical_hexdecimal(){
    long double magical_form = (sqrt(5.0L)-1)/2.0L;
    uint64_t magical_num = magical_form*std::pow(2.0L,64);
    std::cout<<std::showbase<<std::hex<<magical_num;
}

struct Pairhash{
    template<typename T1, typename T2>
    size_t operator()(const std::pair<T1,T2>& p){
        size_t H1 = std::hash<T1>{}(p.first);
        size_t H2 = std::hash<T2>{}(p.second);
        return H1^(H2+0x9e3779b97f4a7c15+(H1<<6)+(H1>>2));
    }
};

int main(){
    find_magical_hexdecimal();
    Pairhash hasher;
    std::pair<std::string, std::string> pair1 = {"ansh", "raj"};
    std::pair<std::string, std::string> pair2 = {"raj", "ansh"};
    std::pair<std::string, std::string> pair3 = {"ansh","raj"};
    std::cout<<"hash value"<<std::endl;
    size_t hash1 = hasher(pair1);
    size_t hash2 = hasher(pair2);
    size_t hash3 = hasher(pair3);
    
    std::cout<<"hash 1: "<<hash1<<std::endl;
    std::cout<<"hash 2: "<<hash2<<std::endl;
    std::cout<<"hash 3: "<<hash3<<std::endl;
    if(hash1 == hash2 or hash1 == hash3 or hash2 == hash3){
        std::cout<<"two hashes are same"<<std::endl;
    }else{
        std::cout<<"hash 1 and hash 2 aren't same"<<std::endl;
    }
}
