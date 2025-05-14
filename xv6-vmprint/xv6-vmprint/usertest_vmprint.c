#include "types.h"
#include "stat.h"
#include "user.h"

int
main(void)
{
  printf(1, "Testing vmprint...\n");
  char *buf = malloc(8192);  // 分配两个页
  buf[0] = 1;
  buf[4096] = 2;

  vmprint();  // 调用内核中的页表打印
  free(buf);

  exit();
}