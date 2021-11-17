#include <stdio.h>
#include <string.h>
#include <dirent.h>
#include <sys/stat.h>
#include <sys/types.h>
#include <stdlib.h>

unsigned long fsize(const char *filename) {
    FILE * f = fopen(filename, "rb");
    fseek(f, 0, SEEK_END);
    unsigned long len = (unsigned long)ftell(f);
    fclose(f);
    return len;
}

int main(int argc, char **argv) {
    int min_size;
    char *dir, init_dir;

    if (argc > 2) {
        dir = argv[1];
        min_size = atoi(argv[2]);
    }

    DIR *folder;
    struct dirent *entry;
    int files = 0;

    folder = opendir(dir);
    if (folder == NULL) {
        perror("Unable to read directory");
        return (1);
    }

    while ((entry = readdir(folder))) {
        files++;
        char *file_path;
        sprintf(file_path, "%s/%s", dir, entry->d_name);
        unsigned long size = fsize(file_path);
        if (size > min_size) {
            printf("%3d: %s\n",
                   files,
                   entry->d_name
                   );
        }
    }

    return 0;
}