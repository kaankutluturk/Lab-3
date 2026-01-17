# Reverse Engineering (Decompile a C Binary)

**Task (from handout):**
1. Create `test.c` (hello world), compile it to `test`.
2. Decompile / reverse the compiled binary to recover the code (using a tool like radare2).

## Part 1 — Build the binary

`test.c`:

```c
#include <stdio.h>
int main(void) {
    printf("Hello World\n");
    return 0;
}
```

Compile:

```bash
gcc -o test test.c
file test
```

## Part 2 — Reverse / decompile

### With radare2 (Kali)

```bash
r2 -A ./test
# Show functions
afl
# Main
s sym.main
pdf
# Decompile (if r2dec plugin is installed)
pdd
```

### What to capture

- Screenshot / paste of `pdf` output for `main`
- Decompiler output (`pdd`) or equivalent pseudocode
- Explanation of how you identified `main`, strings, and imported libc calls

## Notes

- Small binaries may be optimized; compile with `-O0 -g` for easier reversing:
  ```bash
  gcc -O0 -g -o test test.c
  ```
