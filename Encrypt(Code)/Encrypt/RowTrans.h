#pragma once
#pragma once
#include "encrypt.h"

class RowTrans : public Encrypt
{
public:
	RowTrans(string key, string plaintext);
private:
	virtual void Cipher();
private:
	map<int, int> pos;
};