#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <termios.h>
#include <stdio.h>

int textmode(int);
int randline();
int getch();

static char pattern[80];

int textmode(int mode){
    static struct termios con[2];
    if(mode > 0)
        return(tcsetattr(0, TCSAFLUSH, &con[1]));
    tcgetattr(0, &con[0]);
    tcgetattr(0, &con[1]);
    con[0].c_lflag &= ~(ICANON | ECHO | ISIG);
    con[0].c_iflag &= ~(ISTRIP | IXOFF | IXANY | IXON);
    con[0].c_oflag |= CS8;
    con[0].c_cc[VMIN] = 2;
    con[0].c_cc[VTIME] = 1;
    return(tcsetattr(0, TCSAFLUSH, &con[0]));
}

int getch()
{
    unsigned char c[2];
    static int len=0;
    /*if(len > 1)
	{
	  c[0] = len;
	  len = 0;
	  return(c[0]);
	}
  */

    c[0] = c[1] = 0;
    if((len = read(0, c, 2)) < 2)
        return(c[0]);
    if(c[0] == 27)
        c[0] = 0;
    /* len = c[1]; */
    ungetc(c[1], stdin);
    return(c[0]);
}

int randline(int len)
{
    int i=0;
    int r;
    srand(getpid());
    while(i < len)
    {
        r = rand() % (127 - 32);
        pattern[i++] = r + 32;
    }
    return(0);
}

int main(int argc, char* argv[])
{
    if (argc < 3)
    {
        write(1, "Не заданы параметры\n", 36);
        exit(0);
    }
    int r=0;
    int i = 0;
    int err = 0;
    unsigned char c;
    char *dr = argv[1];
    int len = atoi(argv[1]);
    int space = atoi(argv[2]);

    if (space > len)
    {
        write(1, "Количество пробелов больше длины строки\n", 74);
        return 0;
    }

    randline(len);
    write(1, pattern, len);
    write(1, "\n", 1);

    char us_input[80];
    strcpy(us_input, pattern);
    srand(getpid());
    for (int j = 0; j < space; j++)
    {
        int pos = rand() % len;
        us_input[pos] = ' ';
    }

    write(1, us_input, len);
    write(1, "\r", 1);

    textmode(0);
    while(i < len){
        switch(c = getch()){
            case 0:  c = '\007';
            switch(getch())
            {
                case 67: c = pattern[i];
                break;
                case 68: if(i == 0)
                    break;
                i--;
                write(1, "\b", 1);
                continue;
                default: break;
            }
            break;
            case 27: i = len;
            c = '\007';
            break;
            default: if(c != pattern[i])
                c = '\007';
            break;
        }
        (c == '\007') ? err++ : i++;
        write(1, &c, 1);
    }
    write(1, "\n", 1);
    textmode(1);
    return(err);
}
