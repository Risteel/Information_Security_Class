#include "DecryptDES.h"
#include <iostream>
DecryptDES::DecryptDES(U64 ciphertext, U64 key) : ciphertext(ciphertext), key(key)
{
	plaintext = 0;
	Decrypt();
}

void DecryptDES::Decrypt()
{

	//plaintext do IP table
	IP_Table(false);


	//key do PC1 table to 56bit
	PC_Table(one);

	//split text to left 32bit and right 32bit
	U64 left, right;
	left = (plaintext >> 32) & (((U64)1 << 32) - 1);
	right = (plaintext) & (((U64)1 << 32) - 1);


	for (int i = 0; i < 16; i++)
	{
		U64 temp = right;
		//funtion F
		right = left ^ F(right, i + 1);
		left = temp;
	}
	U64 temp = right;
	right = left;
	left = temp;
	plaintext = (left << 32) | right;
	IP_Table(true);
}

U64 DecryptDES::F(U64 right, int round)
{
	//do DES function F content

	right = E_Table(right);

	KeySchedule(round);

	right = right ^ key_PC2;

	U64 temp = 0;

	//sbox do 48bit data to 32bit 
	for (int i = 0; i < 8; i++)
	{
		temp |= Box_Table((right >> ((7 - i) * 6)) & ((1 << 6) - 1), i);
		temp = temp << 4;
	}
	temp = temp >> 4;
	right = P_Table(temp);
	return right;
}

void DecryptDES::Rotate(int round)
{
	if (1 == round || 16 < round) return;
	//split 56bit key to left 28bit and right 28bit
	U64 right, left;
	right = key & ((1 << 28) - 1);
	left = (key >> 28) & ((1 << 28) - 1);
	if (2 == round || 9 == round || 16 == round)
	{
		//rotate right 1bit
		U64 warpLeft, warpRight;
		warpLeft = (left & 1) << 27;
		warpRight = (right & 1) << 27;
		right = (right >> 1) | warpRight;
		left = (left >> 1) | warpLeft;
	}
	else
	{
		//rotate right 2bit
		U64 warpLeft, warpRight;
		warpLeft = (left & 3) << 26;
		warpRight = (right & 3) << 26;
		right = (right >> 2) | warpRight;
		left = (left >> 2) | warpLeft;
	}
	key = (left << 28) | right;
}

void DecryptDES::IP_Table(bool inverse)
{
	U64 temp = 0;
	// plaintext do initail pertumation
	if (!inverse)
	{
		//do IP table
		for (int i = 0; i < 64; i++)
		{
			temp = (temp << 1) | ((ciphertext >> (64 - IP[i])) & 1);
		}
		plaintext = temp;
	}
	else
	{
		//do inverse IP table
		for (int i = 0; i < 64; i++)
		{
			temp = (temp << 1) | ((plaintext >> (64 - InverseIP[i])) & 1);
		}
		plaintext = temp;
	}
}

void DecryptDES::PC_Table(int id)
{
	// key do pc table
	U64 temp = 0;
	if (id == one)
	{
		//pc1
		for (int i = 0; i < 56; i++)
		{
			temp |= ((key >> (64 - PC1[i])) & 1);
			temp = temp << 1;
		}
		key = temp >> 1;
	}
	else if (id == two)
	{
		//pc2
		for (int i = 0; i < 48; i++)
		{
			temp |= ((key >> (56 - PC2[i])) & 1);
			temp = temp << 1;
		}
		key_PC2 = temp >> 1;
	}
}

int DecryptDES::Box_Table(int cipher, int id)
{
	//return sbox[id] value
	int row = (cipher & 1) | (((cipher >> 5) & 1) << 1);
	int col = (cipher >> 1) & 15;
	return sbox[id][row][col];
}

void DecryptDES::KeySchedule(int round)
{
	//rotate key and do key pc2 table
	Rotate(round);
	PC_Table(two);
}

U64 DecryptDES::P_Table(U64 right)
{
	// do permutation table (P table)
	U64 temp = 0;
	for (int i = 0; i < 32; i++)
	{
		temp |= (right >> (32 - P[i])) & 1;
		temp = temp << 1;
	}
	return temp >> 1;
}

U64 DecryptDES::E_Table(U64 right)
{
	// do exapansion table (E table)
	U64 temp = 0;
	for (int i = 0; i < 48; i++)
	{
		temp |= (right >> (32 - E[i])) & 1;
		temp = temp << 1;
	}
	return temp >> 1;
}
