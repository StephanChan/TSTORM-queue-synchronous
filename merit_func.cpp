// merit_func.cpp : 定义 DLL 应用程序的导出函数。
//
#define DLLEXPORT extern "C" __declspec(dllexport)
#include "stdafx.h"
#include<stdio.h>
#include<math.h>

DLLEXPORT void merit_func(double *, double *, int, int, double *, double *);

void merit_func(double *real, double *imag, int size_x, int size_y, double *merit_up, double *merit_down) {
	int i;
	int row, column;
	float dis;
	for (i = 0; i < size_x*size_y; i++) {
		row = i / 2048;
		column = i%2048;
		dis = (pow(row + 0.5 - 1024, 2) + pow(column + 0.5 - 1024, 2));
		*merit_down += pow(pow(real[i], 2) + pow(imag[i], 2), 0.5);
		*merit_up += dis*(*merit_down);

	}
}

