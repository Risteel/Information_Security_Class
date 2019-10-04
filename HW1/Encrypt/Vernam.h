#pragma once
#include "encrypt.h"

class Vernam : public Encrypt
{
public:
	Vernam(string key, string plaintext);
private:
	virtual void Cipher();
};