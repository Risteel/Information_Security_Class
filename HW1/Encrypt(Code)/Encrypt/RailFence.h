#pragma once
#include "encrypt.h"
#include <vector>

class RailFence : public Encrypt
{
public:
	RailFence(string key, string plaintext);
private:
	virtual void Cipher();
private:
	char **rail;
};