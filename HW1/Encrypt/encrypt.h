#pragma once
#include <string>
#include <map>
#include <iostream>
using namespace std;
class Encrypt
{
public:
	Encrypt(){ ciphertext = ""; }
	Encrypt(string key, string plaintext);
	string GetCipherText();
private:
	virtual void Cipher() = 0;
protected:
	bool isAlphabet(char ch)
	{
		return (ch >= 'a' && ch <= 'z') || (ch >= 'A' && ch <= 'Z');
	}
	char toUpperCase(char ch)
	{
		if (ch >= 'a' && ch <= 'z') return ch - 'a' + 'A';
		return ch;
	}
protected:
	string key;
	string plaintext;
	string ciphertext;
};