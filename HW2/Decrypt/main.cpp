#define _CRT_SECURE_NO_WARNINGS
#include <iostream>
#include <string>
#include <sstream>
#include "DecryptDES.h"
using namespace std;

int main(int argc, char **argv)
{
	if (argc == 3)
	{
		unsigned long long int key, ciphertext;
		stringstream ss;
		string str;
		ss << argv[1] << " " << argv[2];
		ss >> std::hex >> key >> ciphertext;
		DecryptDES DES(ciphertext, key);
		cout << "0x" << std::hex << DES.GetCipherText();
	}
	return 0;
}
