class pixel {
protected:
    int roundPix(int value) {
        if (value > 255)
            return 255;
        if (value < 0)
            return 0;
        return value;
    }
    
    int newValue(float curr, float minN, float maxN, float supValue, float maxValue) {
        if (maxN > minN) {
            return maxValue * (curr - minN) * supValue;
        } else {
            return maxN;
        }
    }
    
public:
    pixel() {};
    virtual void refactorColors(float minN, float maxN, float supValue, float maxValue) = 0;
    virtual void print(ofstream& streamOut) = 0;
    virtual int getMin() = 0;
    virtual int getMax() = 0;
    virtual void testP() = 0;
    virtual void read(char v1, char v2, char v3) = 0;
    virtual void read(char value) = 0;
};

class pixelRGB : public pixel {
private:
    int r;
    int g;
    int b;
public:
    void refactorColors(float minN, float maxN, float supValue, float maxValue) {
        r = roundPix(newValue(r, minN, maxN, supValue, maxValue));
        g = roundPix(newValue(g, minN, maxN, supValue, maxValue));
        b = roundPix(newValue(b, minN, maxN, supValue, maxValue));
    }
    
    void read(char value) {};
    
    void read(char v1, char v2, char v3) {
        r = (bt) v1;
        g = (bt) v2;
        b = (bt) v3;
    }
    
    void print(ofstream& streamOut) {
        streamOut << (bt) r << (bt) g << (bt) b;
    }
    
    void testP() {
        cerr << r << " " << g << " " << b << endl;
    }
    
    int getMin() {
        return min(min(r, g), b);
    }
    
    int getMax() {
        return max(max(r, g), b);
    }
};

class pixelGray : public pixel {
private:
    int gray;
public:
    void refactorColors(float minN, float maxN, float supValue, float maxValue) {
        gray = roundPix(newValue(gray, minN, maxN, supValue, maxValue));
    }
    
    void read(char value) {
        gray = (bt) value;
    }
    
    void read(char v1, char v2, char v3) {};
    
    void print(ofstream& streamOut) {
        streamOut << (bt) gray;
    }
    
    void testP() {
        cerr << gray << endl;
    }
    
    int getMax() {
        return gray;
    }
    
    int getMin() {
        return gray;
    }
};
