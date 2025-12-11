#include <stdio.h>
#include <stdlib.h> 
#include <unistd.h>
#include <fcntl.h>
#include <linux/input.h>

/*
 * A simple, fast benchmark which takes a path to an evdev device as its
 * argument and reads from that device into a static buffer. The CPU usage of
 * this benchmark can be used as a best case upper-bound for performance i.e.
 * at best, Gamepadify could be as performant as this benchmark but will never
 * be faster/use less CPU time.
 * 
 */

#define BUFCOUNT 1

int main(int argc, char *argv[])
{
  printf("ARGC = %d\n", argc);

  if (argc < 2)
    return 1;

  int fd = open(argv[1], O_RDONLY);
  printf("FD = %d\n", fd);

  struct input_event buf[BUFCOUNT];

  while (1)
  {
    int rc = read(fd, buf, BUFCOUNT*sizeof(buf[0]));
    // printf("RC = %d\n", rc);
  }
}
