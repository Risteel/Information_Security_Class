#include "Caesar.h"
#include <iostream>
Caesar::Caesar(string key, string plaintext) : Encrypt(key, plaintext)
{
	Cipher();
}

void Caesar::Cipher()
{
	ciphertext = "";
	int shift = atoi(key.c_str());
	for (int i = 0; i < plaintext.length(); i++)
	{
		int temp;
		if (isAlphabet(plaintext[i]))
		{
			temp = plaintext[i] - 'a';
			ciphertext += toUpperCase((temp + shift) % 26 + 'a');
		}
		else
			ciphertext += plaintext[i];
	}
}
