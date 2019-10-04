#pragma once
#include "encrypt.h"

class Caesar : public Encrypt
{
public:
	Caesar(string key, string plaintext);
private:
	virtual void Cipher();
};