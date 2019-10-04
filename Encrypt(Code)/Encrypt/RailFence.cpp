#include "RailFence.h"

RailFence::RailFence(string key, string plaintext) : Encrypt(key, plaintext)
{
	Cipher();
}

void RailFence::Cipher()
{
	int row = atoi(key.c_str()), col;
	col = plaintext.length();
	rail = new char*[row]();
	for (int i = 0; i < row; i++)
	{
		rail[i] = new char[col]();
	}
	for (int i = 0, j = 0, k = 0, dir = 1; i < plaintext.length(); i++)
	{
		rail[j][k] = plaintext[i];
		j += dir;
		if (j == row)
		{
			dir = -1;
			j = row - 2;
			k++;
		}
		else if (j == -1)
		{
			j = 1;
			dir = 1;
			k++;
		}
	}
	for (int i = 0; i < row; i++)
	{
		for (int j = 0; j < col; j++)
		{
			if (rail[i][j] != 0)
				ciphertext += toUpperCase(rail[i][j]);
		}
	}
}
