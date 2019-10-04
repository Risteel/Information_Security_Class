#include "RowTrans.h"

RowTrans::RowTrans(string key, string plaintext) : Encrypt(key, plaintext)
{
	Cipher();
}

void RowTrans::Cipher()
{
	int len = key.length();
	for (int i = 0; i < len; i++)
	{
		pos[key[i] - '1'] = i;
	}
	for (int i = 0; i < len; i++)
	{
		int row = 0;
		while ((pos[i] + row * len) < plaintext.length())
		{
			ciphertext += toUpperCase(plaintext[pos[i] + row * len]);
			row++;
		}
	}
}
