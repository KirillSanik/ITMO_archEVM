#include <iostream>
#include <sstream>
#include <string>
#include <vector>
#include <cmath>
#include <fstream>
#include <chrono>

#include "omp.h"

using namespace std;

typedef unsigned char bt;

#include "Pixel.cpp"

int main(int argc, char *argv[]) {
    // коэфицент
    float koef = stof(argv[4]);
    // количество тредов
    int cntTreads = stoi(argv[1]);
    
    // открытие картинки
    //ifstream fin("/Users/sanik/Desktop/с++/EVMdz5/EVMdz5/picsTest/picTest14.ppm");
    ifstream fin(argv[2]);
    
    // тип файла P6 или P5
    string typeP;
    fin >> typeP;
    cout << typeP << endl;
    
    // размер файла и макс значение
    string hight, widht, maxS;
    fin >> widht >> hight >> maxS;
    
    // перевод в целочисленые типы
    int h, w;
    int maxAll;
    h = stoi(hight);
    w = stoi(widht);
    maxAll = stoi(maxS);
    cout << "hight: " << h << endl << "widht: " << w << endl << "max value: " << maxS << endl;
    
    // создание служебной информации
    int minN = maxAll;
    int maxN = 0;
    // количество пикселей
    size_t cntPixels = h * w;
    // вектор пикселей
    pixel** input = new pixel*[cntPixels];
    //vector<pixel*> input(cntPixels);
    // размер буфера
    size_t buffSize = cntPixels;
    if (typeP == "P6") {
        buffSize = cntPixels * 3;
    }
    // создание буффера
    char* buff = new char[buffSize];
    // чтение буффера
    fin.read(buff, 1);
    fin.read(buff, buffSize);
    
    // закрытие файла чтения
    fin.close();
    
    // старт таймера
    auto start = chrono::high_resolution_clock::now();
    
    // создание массива подсчета цветов
    vector<vector<size_t>> colors(1, vector<size_t> (256, 0));
    if (typeP == "P6") {
        colors.push_back(vector<size_t> (256,0));
        colors.push_back(vector<size_t> (256,0));
    }
    
    int onePix[3];
    if (typeP == "P6") {
        onePix[0] = (int)(bt)buff[0];
        onePix[1] = (int)(bt)buff[1];
        onePix[2] = (int)(bt)buff[2];
    } else {
        onePix[0] = (int)(bt)buff[0];
    }
    
    bool isOneCol = true;
    
    #pragma omp parallel num_threads(cntTreads)
    {
        //cerr << omp_get_num_threads() << endl;
        vector<vector<size_t>> colorsTemp(1, vector<size_t> (256, 0));
        if (typeP == "P6") {
            colorsTemp.push_back(vector<size_t> (256,0));
            colorsTemp.push_back(vector<size_t> (256,0));
        }
        //int currMin = 255;
        //int currMax = 0;
        // подсчет цветов + нахождение максимума минимума
        #pragma omp for schedule(static)
        for (size_t i = 0; i < cntPixels; i++) {
            if (typeP == "P6") {
                input[i] = new pixelRGB;
                size_t tempInd = i * 3;
                colorsTemp[0][(int)(bt)buff[tempInd]]++;
                colorsTemp[1][(int)(bt)buff[tempInd + 1]]++;
                colorsTemp[2][(int)(bt)buff[tempInd + 2]]++;
                input[i]->read(buff[tempInd], buff[tempInd + 1], buff[tempInd + 2]);
                if (!(onePix[0] == (int)(bt)buff[tempInd] && onePix[1] == (int)(bt)buff[tempInd + 1] && onePix[2] == (int)(bt)buff[tempInd + 2])) {
                    isOneCol = false;
                }
            }
            else {
                input[i] = new pixelGray;
                colorsTemp[0][(int)(bt)buff[i]]++;
                input[i]->read(buff[i]);
                if (!(onePix[0] == (int)(bt)buff[i])) {
                    isOneCol = false;
                }
            }
            // минимум как оказалось из-за подсчета потеряал необходимость
            /*
            // min
            currMin = min(currMin, input[i]->getMin());
            // max
            currMax = max(currMax, input[i]->getMax());
             */
        }
        // тот же минимум
        /*
        #pragma omp critical
        {
            minN = min(currMin, minN);
        }
        #pragma omp critical
        {
            maxN = max(currMax, maxN);
        }*/
        int sizeColors = typeP == "P6" ? 3 : 1;
        for (int j = 0; j < sizeColors; j++) {
            for (int i = 0; i < 256; i++) {
                #pragma omp atomic
                colors[j][i] += colorsTemp[j][i];
            }
        }
    }
    // удаление массива с картинкой(изначальной)
    // delete[] buff;
    //cerr << "old: " << minN << " " << maxN << endl;
    
    // если один цвет
    if(isOneCol) {
        // вывод времени работы алгоритма
        auto end = chrono::high_resolution_clock::now();
        //Time (%i thread(s)): %g ms\n
        cerr << "algo time:" << endl;
        cerr << "Time(thread(" << cntTreads << ")): " << chrono::duration_cast<std::chrono::milliseconds>(end - start).count() << " ms" <<  endl;
        
        // вывод + создание
        //ofstream fout("/Users/sanik/Desktop/с++/EVMdz5/EVMdz5/picsOut/picOut14.ppm");
        ofstream fout(argv[3]);
        fout << typeP << endl;
        fout << w << " " << h << endl;
        fout << maxS << endl;
        
        // вывод в файл
        for (size_t i = 0; i < cntPixels; i++) {
            input[i]->print(fout);
        }
        
        //закрытия файла вывода
        fout.close();
        
        //вывод времени конца программы
        end = chrono::high_resolution_clock::now();
        cerr << "prog time:" << endl;
        cerr << "Time(thread(" << cntTreads << ")): " << chrono::duration_cast<std::chrono::milliseconds>(end - start).count() << " ms" <<  endl;
        cerr << "done" << endl;
        return 0;
    }
    
    // поиск нового максимума минимума
    size_t minMaxInd = float(cntPixels) * koef;
    int sizeMinMax = typeP == "P6" ? 3 : 1;
    int mins[sizeMinMax], maxs[sizeMinMax];
    
    #pragma omp parallel for schedule(static) num_threads(cntTreads)
    for (int j = 0; j < sizeMinMax; j++) {
        int sumV = 0;
        //cerr << minMaxInd << endl;
        for (int i = 0; i < 256; i++) {
            sumV += colors[j][i];
            //cerr << "i: " << i << " " << sumV << " : " << colors[j][i] << endl;
            if (minMaxInd < sumV) {
                mins[j] = i;
                break;
            }
        }
    }
    
    #pragma omp parallel for schedule(static) num_threads(cntTreads)
    for (int j = 0; j < sizeMinMax; j++) {
        int sumV = 0;
        //cerr << minMaxInd << endl;
        for (int i = 255; i >= 0; i--) {
            sumV += colors[j][i];
            //cerr << "i: " << i << " " << sumV << " : " << colors[j][i] << endl;
            if (minMaxInd < sumV) {
                maxs[j] = i;
                break;
            }
        }
    }
    
    if (sizeMinMax == 1) {
        minN = mins[0];
        maxN = maxs[0];
    } else {
        minN = min(mins[0], min(mins[1], mins[2]));
        maxN = max(maxs[0], max(maxs[1], maxs[2]));
    }
    
    cerr << "min: " << minN << " max: " << maxN << endl;
    
    float supValue = 1.0 / (maxN - minN);
    
    #pragma omp parallel for schedule(static) num_threads(cntTreads)
    for (size_t i = 0; i < cntPixels; i++) {
        input[i]->refactorColors(minN, maxN, supValue, maxAll);
    }
    
    // вывод времени работы алгоритма
    auto end = chrono::high_resolution_clock::now();
    //Time (%i thread(s)): %g ms\n
    cerr << "algo time:" << endl;
    cerr << "Time(thread(" << cntTreads << ")): " << chrono::duration_cast<std::chrono::milliseconds>(end - start).count() << " ms" <<  endl;
    
    // вывод + создание
    //ofstream fout("/Users/sanik/Desktop/с++/EVMdz5/EVMdz5/picsOut/picOut14.ppm");
    ofstream fout(argv[3]);
    fout << typeP << endl;
    fout << w << " " << h << endl;
    fout << maxS << endl;
    
    // вывод в файл
    for (size_t i = 0; i < cntPixels; i++) {
        input[i]->print(fout);
    }
    // очищение файла пикселей
    //input.clear();
    delete[] input;
    delete[] buff;
    
    //закрытия файла вывода
    fout.close();
    
    //вывод времени конца программы
    end = chrono::high_resolution_clock::now();
    cerr << "prog time:" << endl;
    cerr << "Time(thread(" << cntTreads << ")): " << chrono::duration_cast<std::chrono::milliseconds>(end - start).count() << " ms" <<  endl;
    cerr << "done" << endl;
}
