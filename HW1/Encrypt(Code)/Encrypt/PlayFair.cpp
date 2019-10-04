#include "PlayFair.h"

void PlayFair::Cipher()
{
	for (int i = 0, j; i < plaintext.length(); i++)
	{
		char t1, t2;
		int row1, row2, col1, col2;
		string temp = "";
		if (!isAlphabet(plaintext[i]))
		{
			ciphertext += plaintext[i];
			continue;
		}
		j = i;
		while (i + 1 < plaintext.length() && !isAlphabet(plaintext[i + 1]))
		{
			temp += plaintext[i + 1];
			i++;
		}
		if (i + 1 < plaintext.length() && plaintext[j] != plaintext[i + 1])
		{
			t1 = toUpperCase(plaintext[j]);
			t2 = toUpperCase(plaintext[i + 1]);
			i++;
		}
		else
		{
			t1 = toUpperCase(plaintext[j]);
			t2 = 'X';
		}
		row1 = pos[t1] / 5, col1 = pos[t1] % 5;
		row2 = pos[t2] / 5, col2 = pos[t2] % 5;
		if (row1 == row2)
		{
			ciphertext += playfairMatrix[row1][(col1 + 1) % 5];
			ciphertext += (j == i ? "" : temp);
			ciphertext += playfairMatrix[row2][(col2 + 1) % 5];
		}
		else if (col1 == col2)
		{
			ciphertext += playfairMatrix[(row1 + 1) % 5][col1];
			ciphertext += (j == i ? "" : temp);
			ciphertext += playfairMatrix[(row2 + 1) % 5][col2];
		}
		else
		{
			ciphertext += playfairMatrix[row1][col2];
			ciphertext += (j == i ? "" : temp);
			ciphertext += playfairMatrix[row2][col1];
		}
	}
}

PlayFair::PlayFair(string key, string plaintext) : Encrypt(key, plaintext)
{
	setMatrix();
	Cipher();
}

void PlayFair::setMatrix()
{
	for (int i = 0, j = 0; i < key.length(); i++)
	{
		int pos = (int)key.find(key[i]);
		if (key[i] == 'J') key[i] = 'I';
		if (check[key[i]] == 1 || !isAlphabet(key[i])) continue;
		playfairMatrix[j / 5][j % 5] = key[i];
		check[key[i]] = 1;
		this->pos[key[i]] = j;
		j++;
	}

	for (int i = 0, j = key.length(); i < 26; i++)
	{
		if (((int)key.find('A' + i) != -1) || (i + 'A') == 'J') continue;
		playfairMatrix[j / 5][j % 5] = i + 'A';
		this->pos['A' + i] = j;
		j++;
	}
	this->pos['J'] = this->pos['I'];
}
