#pragma once
#include "encrypt.h"

class PlayFair : public Encrypt
{
public:
	PlayFair(string key, string plaintext);
private:
	void setMatrix();
	virtual void Cipher();
private:
	char playfairMatrix[5][5];
	map<char, int> check, pos;
};