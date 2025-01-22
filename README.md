# Interpreter-for-c-subset

## Prosty interpreter podzbioru języka c
Język programowania: Python\
Wymagana biblioteka: ply
```
pip install -r requirements.txt
```

Mój interpreter działa na podzbiorze języka c.\
Zaimplementowane własności:\
Pętla while,\
Instrukcje warunkowe,\
Funkcje,\
Typy zmiennych,\
Działania na liczbach,\
Wypisywanie,\
Zmiany wartości zmiennych,\
Porównywanie liczb\

Aby włączyć interpreter należy napisać swój program w pliku code.c i odpalic main.py
```
python main.py
```

Przykładowe programy:
## 1.
```
int main(){
    int i = 0;
    int b = 1;

    while(i < 10){
        b = b * 2;
        i = i + 1;
    }
    printf(b);
    return 0;
}
```
Output:
```
1024
```
## 2.

```
int mnozenie(int a, int b){
    return a * b;
}

int dodawanie(int a, int b){
    return a + b;
}

int main(){
    int a = 5;
    int b = 7;
    int c = 10;
    int d = 8;
    printf(dodawanie(mnozenie(a, b), mnozenie(c, d)));
    return 0;
}
```
Output:
```
115
```

## 3.

```
int mnozenie(int a, int b){
    return a * b;
}

int dodawanie(int a, int b){
    return a + b;
}

int main(){
    int a = 5.8;
    int b = 7;
    int c = 10;
    int d = 8;
    printf(dodawanie(mnozenie(a, b), mnozenie(c, d)));
    return 0;
}
```
Output:
```
RuntimeError: Expected type 'int', but got float.
```

## 4.
```
return 0;
```
Output:
```
Syntax error at token 'return' (line: 1)
```





