#include <iostream>
#include "PlayFair.h"
#include "Caesar.h"
#include "Vernam.h"
#include "RowTrans.h"
#include "RailFence.h"

int main(int argc, char *argv[])
{
	string key ;
	string text;
	string output;
	if (argc == 4)
	{
		key = argv[2];
		text = argv[3];
		if (strcmp(argv[1], "caesar") == 0)
		{
			output = Caesar(key, text).GetCipherText();
		}
		else if (strcmp(argv[1], "playfair") == 0)
		{
			output = PlayFair(key, text).GetCipherText();
		}
		else if (strcmp(argv[1], "vernam") == 0)
		{
			output = Vernam(key, text).GetCipherText();
		}
		else if (strcmp(argv[1], "row") == 0)
		{
			output = RowTrans(key, text).GetCipherText();
		}
		else if (strcmp(argv[1], "rail_fence") == 0)
		{
			output = RailFence(key, text).GetCipherText();
		}
		cout << output;
	}
	return 0;
}