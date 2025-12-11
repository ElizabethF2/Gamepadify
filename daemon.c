#include <stdio.h>
#include <stdlib.h> 
#include <unistd.h>
#include <sys/inotify.h>

//      OK_PYTHON       0
//      ERROR_PYTHON    1
#define ERROR_INIT      2
#define ERROR_ADD_WATCH 3
#define ERROR_READ      4
#define ERROR_EXEC      5

#define BUFFER_SIZE 32

int main(int argc, char *argv[])
{
  int fd = inotify_init();
  if ( fd < 0 )
  {
    return ERROR_INIT;
  }

  int wd = inotify_add_watch(fd, "/dev/input", IN_CREATE);
  if (wd == -1)
  {
    return ERROR_ADD_WATCH;
  }

  char buffer[BUFFER_SIZE];
  int length = read(fd, buffer, BUFFER_SIZE);
  if (length < 0) 
  {
    return ERROR_READ;
  }
  close(fd);
  execlp(argv[1], argv[1], (char*)NULL);
  return ERROR_EXEC;
}
