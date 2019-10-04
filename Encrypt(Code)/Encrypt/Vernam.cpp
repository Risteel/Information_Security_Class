#include "Vernam.h"

Vernam::Vernam(string key, string plaintext) : Encrypt(key, plaintext)
{
	Cipher();
}

void Vernam::Cipher()
{
	for (int i = 0; i < plaintext.length(); i++)
	{
		int temp;
		if (isAlphabet(plaintext[i]))
		{
			temp = plaintext[i] - 'a';
			ciphertext +=(temp ^ (key[i % key.length()] - 'A')) + 'A';
		}
		else
			ciphertext += plaintext[i];
	}
}
