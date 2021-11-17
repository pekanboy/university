#include <unistd.h>
#include <errno.h>
#include <string.h>
#include <stdio.h>
#include <stdlib.h>
#include <fcntl.h>

// Перекодировка из WIN в KOI

int diag(char* ,const char* , int); //функция диагностики
unsigned char* recode(int);    //функция перекодировки
static unsigned char buf[BUFSIZ * 10]; //буфер чтения записи


int diag(char* name,const char* mes, int code){
    int len;    //общая длина диагностической строки вывода
    strcpy(buf, name);
    strncat(buf, ": ", 2);
    strcat(buf, mes);
    len = strlen(buf);
    buf[len] = '\n';
    write(2, buf, len + 1);
    return (code);
}

unsigned char* recode(int n){
    unsigned char c;
    int i = 0;
    static char tab[32] = {
            /*ю  а  б  ц   д  е  ф   г   х  и  й  к    л   м   н  о*/
            30, 0, 1, 22, 4, 5, 20, 3, 21, 8, 9, 10, 11, 12, 13, 14,
            /*п  я    р  с    т   у  ж  в   ь   ы  з   ш   э  щ    ч  ъ*/
            15, 31, 16, 17, 18, 19, 6, 2, 28, 27, 7, 24, 29, 25, 23, 26
    };
    for (i = 0; i < n; i++)
    {
        c = buf[i];
        if (c < 192) //ASCII
            continue;
        if (c < 224) {
            buf[i] = tab[c - 192] + 224;
        } else {
            buf[i] = tab[c - 224] + 192;
        }
    }
    return (buf);
}


int main(int argc, char* argv[])
{
    int fds;
    int fdt;
    int num;
    int key = 0;

    if (argc < 2)
        exit(diag(argv[0], "Source target file name?", 127));
    if (argc < 3)
        exit(diag(argv[0], "Target file name?",63));
    if (argc > 3)
        key = 1;
    if (key == 1 && strcmp(argv[3], "-r") != 0)
        exit(diag(argv[0], "wrong key",63));


    if ((fds = open(argv[1], 0)) < 0)
        exit(diag(argv[1], sys_errlist[errno], errno));

    //Проверка существования результирующего файла и ключа
    if (access(argv[2], 0) == 0 && key == 0)
        exit(diag(argv[2], "Target file already exists", 255));

    errno = 0;

    if ((fdt = creat(argv[2], 0644))< 0)
        exit(diag(argv[2], sys_errlist[errno], errno));

    while ((num = read(fds, buf, BUFSIZ)) > 0)
    {
        write(fdt, recode(num), num);
    }
    close(fdt);
    close(fds);
    exit(0);
}
