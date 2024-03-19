#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <stdbool.h>
#include <string.h>
#include <time.h>

void arr_init(int *arr, int cnt)
{
    int i = 0;
    // 使用当前时间作为随机数生成器的种子
    srand(time(NULL));
    for (i = 0; i < cnt; i++)
    {
        /* Return a random integer between 0 and RAND_MAX inclusive.  */
        arr[i] = (rand() + 5) % 100;
    }
}

int arr_get(int *arr, int idx)
{
    if (!arr)
        return -UINT16_MAX;
    return arr[idx];
}

int arr_insert(int *arr, int len, int idx, int val)
{
    int last = arr[len - 1], i = 0;
    for (i = len - 2; i >= idx; i--)
    {
        arr[i + 1] = arr[i];
    }
    arr[idx] = val;
    return last;
}

int arr_remove(int *arr, int len, int idx)
{
    int last = arr[idx], i = 0;
    for (i = idx; i < len - 1; i++)
    {
        arr[i] = arr[i + 1];
    }
    return last;
}

void arr_print(int *arr, int len)
{
    for (int i = 0; i < len; i++)
    {
        printf("%2d ", arr[i]);
    }
    printf("\n");
}

int arr_traverse(int *arr, int len)
{
    int sum = 0, i = 0;
    for (i = 0; i < len; i++)
    {
        sum += arr[i];
    }
    return sum;
}

int arr_search(int *arr, int len, int elem)
{
    for (int i = 0; i < len; i++)
    {
        if (arr[i] == elem)
            return i;
    }
    return -1;
}

/**
 * 更新单重指针指向的地址而不是指针的值实际上是不可能的，因为单重指针本身就是存储地址的变量。
 * 当你改变单重指针的值时，你实际上是在改变它指向的地址。如果你想要在函数内部改变一个指针
 * 指向的地址，而又不希望改变原始指针本身的值，那么你需要传递指针的地址（即双重指针）。
*/
int arr_expansion(int **arr, int len, int relen)
{
    int i = 0, *temp = malloc(sizeof(int) * relen);
    memcpy(temp, *arr, sizeof(int) * len);
    free(*arr);
    *arr = temp;
    return relen;
}

int main(int argc, char const *argv[])
{
    /** “增删改查”是数据库操作中的四个基本操作
     *
     * 数组
     *
     * 编写数组的如下操作函数
     *
     * 1 初始化
     * 2 访问元素
     * 3 插入元素  增
     * 4 删除元素  删
     * 5 遍历数组
     * 6 查找元素  查
     * 7 扩容数组
     */
    int *arr = NULL, cnt = 10, val = 0, idx = 0, ret = 0;

    arr = malloc(sizeof(int) * cnt);
    // 1 数组初始化
    arr_init(arr, cnt);
    arr_print(arr, cnt);
    // 2 访问元素
    idx = rand() % cnt;
    val = arr_get(arr, idx);
    printf("[%d] %d\n", idx, val);
    // 3 插入元素
    idx = rand() % cnt;
    val = rand() % cnt;
    ret = arr_insert(arr, cnt, idx, val);
    arr_print(arr, cnt);
    printf("in %d %d ret %d\n", idx, val, ret);
    // 4 删除元素
    idx = rand() % cnt;
    ret = arr_remove(arr, cnt, idx);
    arr_print(arr, cnt);
    printf("out %d ret %d\n", idx, ret);
    // 5 遍历数组
    val = arr_traverse(arr, cnt);
    printf("traverse sum %d\n", val);
    // 6 查找元素
    val = rand() % cnt;
    idx = arr_search(arr, cnt, val);
    printf("elem %d %d %s\n", val, idx, idx == -1 ? "no exist" : "exist");
    // 7 扩容数组
    cnt = arr_expansion(&arr, cnt, cnt + 5);
    arr_print(arr, cnt);
    printf("new %d\n", cnt);

    free(arr);

    return 0;
}

#if 0
在C语言的stdint.h头文件中，常用的整型最大值宏定义如下：
INT8_MAX: 有符号8位整型的最大值，即127。
INT16_MAX: 有符号16位整型的最大值，即32767。
INT32_MAX: 有符号32位整型的最大值，即2147483647。
INT64_MAX: 有符号64位整型的最大值，即9223372036854775807。

对于无符号整型，最大值的宏定义以"UINT"开头，例如：
UINT8_MAX: 无符号8位整型的最大值，即255。
UINT16_MAX: 无符号16位整型的最大值，即65535。

#define EPERM 1    /* Operation not permitted */
#define ENOENT 2   /* No such file or directory */
#define ESRCH 3    /* No such process */
#define EINTR 4    /* Interrupted system call */
#define EIO 5      /* I/O error */
#define ENXIO 6    /* No such device or address */
#define E2BIG 7    /* Argument list too long */
#define ENOEXEC 8  /* Exec format error */
#define EBADF 9    /* Bad file number */
#define ECHILD 10  /* No child processes */
#define EAGAIN 11  /* Try again */
#define ENOMEM 12  /* Out of memory */
#define EACCES 13  /* Permission denied */
#define EFAULT 14  /* Bad address */
#define ENOTBLK 15 /* Block device required */
#define EBUSY 16   /* Device or resource busy */
#define EEXIST 17  /* File exists */
#define EXDEV 18   /* Cross-device link */
#define ENODEV 19  /* No such device */
#define ENOTDIR 20 /* Not a directory */
#define EISDIR 21  /* Is a directory */
#define EINVAL 22  /* Invalid argument */
#define ENFILE 23  /* File table overflow */
#define EMFILE 24  /* Too many open files */
#define ENOTTY 25  /* Not a typewriter */
#define ETXTBSY 26 /* Text file busy */
#define EFBIG 27   /* File too large */
#define ENOSPC 28  /* No space left on device */
#define ESPIPE 29  /* Illegal seek */
#define EROFS 30   /* Read-only file system */
#endif
