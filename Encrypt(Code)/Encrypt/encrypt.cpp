#include "encrypt.h"

Encrypt::Encrypt( string key, string plaintext)
	: key(key), plaintext(plaintext)
{
	
}

string Encrypt::GetCipherText()
{
	return ciphertext;
}


