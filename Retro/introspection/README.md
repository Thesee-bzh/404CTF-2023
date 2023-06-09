# Retro / Introspection

## Challenge
Cela fait un moment déjà que vous avez remarqué un personnage qui reste en retrait dans le café. Il s'agit d'une femme qui semble plongée dans ses pensées.

Vous décidez enfin de vous approcher.

« Bonjour, je me permet de vous déranger. Je n'ai pu m'empêcher de remarquer votre présence. Vous êtes soucieuse ? »

La femme lâche un long et franc soupir. Vous remarquez son nom écrit sur son mouchoir, Marceline Desbordes-Valmore.

Elle finit par retorquer :

« Savez vous vraiment qui vous êtes ? Ce qui est au fond de vous même ? Je crois qu'il est important de faire un effort pour se découvrir vraiment.

— Je ne sais pas, je ne crois pas avoir déjà fait un effort semblable.

— Et bien dans ce cas, j'ai une expérience à vous soummettre, afin que vous compreniez ce qu'il y au plus profond de votre subconscient, au délà des nombreuses couches qui vous séparent du monde matériel. »

Dans ce challenge vous devez trouver le mot de passe qui valide le crackme. L'exécution est un peu lente et peut donc faire bugger certain émulateurs de terminaux, vous pouvez par exemple rediriger stdout vers cat pour vous assurer d'avoir un output correct. Bonne introspection !

> Format : 404CTF{password}

## Inputs
- binary:  [introspection](./introspection)


## Solution
Here's the `main()` function below, as decompiled by `Ghidra`. The `ptrace()` system call forbids the debugging... A file descriptor is opened, some data manipulated and written to it, then `fexecve()` is called onto the file descriptor. This means that the output of the data manipulation is some kind of embedded program that is executed in a spawned child forked by the parent program. Hence the `Introspection`, kind of `Inception`.

```c
ulong FUN_0010120d(byte param_1,char **param_2,char **param_3)

{
  byte bVar1;
  __pid_t _Var2;
  uint uVar3;
  int __fd;
  ulong uVar4;
  long lVar5;
  long lVar6;
  undefined7 extraout_var;
  uint local_c;

  _Var2 = fork();
  if (_Var2 == -1) {
    puts("Error");
    uVar4 = 0xffffffff;
  }
  else if (_Var2 == 0) {
    lVar5 = ptrace(PTRACE_TRACEME,0,0);
    lVar6 = ptrace(PTRACE_TRACEME,0,0);
    if ((int)lVar5 == 0) {
      __fd = FUN_001011a9(&DAT_0010200d,1);
      for (local_c = 0; local_c < DAT_0028eec8; local_c = local_c + 1) {
        (&DAT_00104060)[(int)local_c] =
             (char)lVar6 + (char)lVar5 + (&DAT_0028eee0)[local_c % DAT_0028f2fc] + 1U ^
             (&DAT_00104060)[(int)local_c];
      }
      write(__fd,&DAT_00104060,(ulong)DAT_0028eec8);
      fexecve(__fd,param_2,param_3);
      uVar4 = 0;
    }
    else {
      uVar3 = getpid();
      bVar1 = FUN_001011d3(param_1,uVar3);
      puts(":(");
      uVar4 = CONCAT71(extraout_var,bVar1) & 0xffffffff;
    }
  }
  else {
    wait((void *)0x0);
    uVar4 = 0;
  }
  return uVar4;
}
```

The first call to `ptrace(PTRACE_TRACEME, 0, 0)` should return 0. After that, the program is already traced, so no more tracer allowed and the 2nd call should return -1. So `lVar5 = 0` and `lVar6 = -1` in the core of the program below. Also, *0x0028f2fc = 0x41c and *0x0028eec8 = 0x18ae68. Byte arrays DAT_00104060[] and DAT_0028eee0[] have to be dumped.

```c
      for (local_c = 0; local_c < DAT_0028eec8; local_c = local_c + 1) {
        (&DAT_00104060)[(int)local_c] =
             (char)lVar6 + (char)lVar5 + (&DAT_0028eee0)[local_c % DAT_0028f2fc] + 1U ^
             (&DAT_00104060)[(int)local_c];
      }
```

We can manually extract both byte arrays using `pwntools`, like so:

```console
$ python3
>>> from pwn import *
>>> e = ELF('introspection')
>>> e.read(0x0018eee0, 0x41c)
b'\xf5\xfe\x8fQ\x83\xb76\xe7c\xd3\xdf?\xe7H\xa1\x1e\xc3=\x86\xd7{*\xc9:Zp\xdb\xf2\x89P\x96s\xa4\xd1)\x89\xc0\x1e\xea\xe4\xe1\x917\xd5\xf9|\x8e*w\xffsw0\x07g\xe4\x92\x84\xcdR\xe7\xdc\x97n,\n\xa5\x97\xe7\xe6o)l7\x13\xef\xd2\x1f|$3\xa8\xff#\x88V\xa6P\x9e\xa9O\xad\x13\xe9[\xe9\xb6$\x18\xe0\xb6\x98\x80LV:\xb9\x93r\x14T\x89\xbf_q\x80*@\xdc\xd6\xaeVf\x8e\x9f\xd0\rN\x12\xb3\x88\x90\xe4\x18t\xc6:"\x0b\xccON\xcb\x0f\xb3\x12\xa0\xc7\x08\xe7\n\x8e\xd0\x12\x9e.\xc7\xbe\x0b\xc8\x8cY\xbcQ\xa8p\xd25`f\xc8\xa6%\xfd\xed\x90\xcb3glX\xf0\xcb\'\xc7\x05N\xa9\x89\xc05\x9ebp\x95z"\\\x02u\xc1,\x96\x9bF\xb1t\xd6^a\x83\xca\xad\x07\xf3\xbc!\xbc\x9e\x95\xddI\xe8\xa1\x1c\xfd\x81A\xc2PJ(\xe9\xda\xfc\x01#\xf6\xc9\x85e\xfc\x89\xcdJ\x00\x0c\x1c\xdc\x9645\xa5pa\x8dk\x01&\xe5\x8c6CQ\xe8\xdbJr\xea\xa3:iU"\xcay\xd4\xe5\x1e\x1f\x13\xe1\x0f\xb7\xea\x8fL\x99\x8a]_K\xfes\xed\x11\xf1\xb8\xd4=\xe4\xfe\x1c]\xbdot\x89*\x93\xb4\xbc[\xad\r\x87\xa0P\x85lL"\x80\x86\\\xff\x88K\x85g\x9a\'1Z{`\xba\x826\x19\xca\xbd\xd5\xac,\x9c\x9f\x94gD\x17\xc10,\x12\xb4]\xa4V\xb5\x9c\xf0\xc5z\x081\x8f\xf8\xa4\x1b\xb1}i\xd5\xf7\xef\xf2\xf4,!\xcbg\xd8=[\xed\x1fB\xd5\xc7k\x1d;\x83\x13l\xfd\xe8\xf8P\xbdC\xb7\xfc\xc2\xae\xb3\xb1]\x83G\x81ut\x82d\xa7\x0f&\x86\xd8\xe7Ah}\xf5\x90\x08\xa9m\\\xae"\x1c\x0flU\xea\x80\xd0\xc1\\<\x8c\xdf\x81a\xe2&\xa5\xe4\xdb\x9abo\xfd\xa1\xdd\x85V\x19\x8a\xbd\x91\x0b"7H(\x12n\x91\xaa/u\xf4^\xc3\xca1\xb0\xb6\xdaPp:\xe5\xab\x82\x11\xb4"*\xe1\xa5[?\xa4\x8c\xe4\xb8H,\xcc\x9e\x94\\Q\x91u\x0ep\x1f\x10\xc5\xa4-\xfa{\xa7\xf6\xce\xfb\xc1\xf0[\xa4G\xb9\xd8\xe7Jva\xdf=\xd5\xbf\x1fb\x1f\xdf\'n\n\x90\xa4l\x04\x8cwG\xf4eA\xb1V\xdbNm{E\x93\x07\xcbC\xaec\xe3\xf3\xb1\xa6\xceJ1\xf4-\xeeR$\xa6\x88\x17e\xa0\xdak\x9d\x18\xb1g\xcc\xca\xcd\xaeP\xa4j\x01\xfc\x95\xe5\xfb\xacw~JU\xe8\xc5U\xc4\xe8\xe2\xf7\xa2\xb3\xd5\x93r\xfb\xadZ\x00\x9ff\xb3z\x08\xe6\xe4\xd2Yr\xedt\x9c<\x08\xb7\xf3\x80X\xe5f\x91\xf1f\x06n\x87f-\xf2\xd0\xa9\'\x1eY\xe3\x1e]e\x05+\x02\xc6<\x93\xffBE\xdaP\x88e\x86\x12$\x90[i@ry\xff\xe5\xbd\x15\x1a\x19 \xdbHH\xb8\x80\x14\x01R#\x95I\x1f\xfaCj\x04_\xd7\xf5\xbe\x81\xa0\xe1|\x9a,h\xd3z\xfd\xcb\n\x14\xd7\xc9\x95\xda;-Y\xfa\xb9*}\xb0\xfc\xd9\r/\n\x88\xecU&\x1a\xf4\x1aB?J\x11\xd6\x16)WQ\x10\xbf \xc7\xf0\x81\xdd\x0c\xb6\xae\x0b\xb9V\x9fYbt*\x87\xf3.\x02\xb4\x9a\xd6\x92\xa7\xe2~\xdf"\xd5\xd3\x87\xc4J\xe8\xf3\xd3\xee*\xedu\xcc\xd8)\x01\x12\xd6\xab\xfd\x91B\x15AW\xaeP\xd9\xc9\xe5\xf1\xb2\xf0\x82\x18=\xea;}\xc7\x023\xa0\xf8~\x7fy.\xd7\xe6\xb5\x11\x0bb\xf3.\n\xb2\nK\x92~\xbc\xfa\xbaN\x8e\xdd\x9b\xebo\xe8\xd9\x11F\x8c\xb50\x00dg{W\x04k\x83:\xaf\xaa\x87\xfb\x0c\xb9yW\xeb\xcdtQ\x1dS\xc4r\xaa\xd7\xa6\x19m\x84\x85CO^[&\xa2\xc5K\x9bY\xe7NT\xb5\xe5\x92H\xb0P\xbf\xb9\x1c:\x87NWg\xde\xd5k\xc0\x0b\xeb\x02Y\x80\x9a~:@\xf9\xa0%\xcc\x88(/B\xe5\xa7\x14C\xee?\xa2N\x06\x81\xae<\x12:\xc9\x93\xbc\xce&\xa7\x05K4Z\x1f9UQ \xea:\x86lU\xc0\x9b\xa5&\x87\x14\xf2A\xe7&\x98\xff\xb1\xd8\x80\xa7\x9f({\x8a3^g\xa8\x10\xc7\xd1\x0c\xad\xee\x14\xc6\xe9[\x1b\x14}\xfa?\xa4\' \x18[\x98\xe9\x83\xe2\x80\xe3\xe6\xc8pl\x98\x00x\r\x9a\xf3\xed\xca\x06\x0f\x14u\xeat\x02\x97\t'
>>>
```

We're now ready to mimic the core of the program and write the output binary to `extracted`, which we know should be another binary:

```python
def mimic(data1, len1, data2, len2):
    lVar5 = 0
    lVar6 = -1
    data1 = list(data1)
    for i in range(len1):
        data1[i] = lVar6 + lVar5 + data2[i % len2] + 1^data1[i]
    return bytes(data1)

def store(filename, data):
    with open(filename, 'wb') as f:
        f.write(data)

store('extracted', mimic(data1, len1, data2, len2))
```

```console
$ file extracted
extracted_elf: ELF 64-bit LSB pie executable, x86-64, version 1 (SYSV), dynamically linked, interpreter /lib64/ld-linux-x86-64.so.2, BuildID[sha1]=964dc2f2e52ec2b0b9125f82a87e62cb6804a88b, for GNU/Linux 3.2.0, stripped
```

Let's reiterate the same process for this extracted `ELF`. And, surprise, we fall into exact same `main` function as in the original binary. Ok, we're in `Inception`... Only difference is the byte arrays that are manipulated (and their size). Here we need to extract:
- DAT_00104060[], size 0x186e68
- DAT_0028aee0[], size 0x712

We adapt our scripts and extract the new payload, to reveal... yet another level in the `Inception`.

```
$ file extracted_elf2
extracted_elf2: ELF 64-bit LSB pie executable, x86-64, version 1 (SYSV), dynamically linked, interpreter /lib64/ld-linux-x86-64.so.2, BuildID[sha1]=7eea50728fe5a271bb5647b5e6e64d0ec0a9a331, for GNU/Linux 3.2.0, stripped
```

Now, we don't know how deep the rabbit hole goes, so we have to automate the all process... Let's play a bit with `pwntools` disassembly feature to extract the `main` function address:

```console
$ python3
>>> from pwn import *
>>> e = ELF('introspection')
>>> hex(e.entry)
'0x10c0'
>>> print(e.disasm(e.entry, 30))
    10c0:       31 ed                   xor    ebp, ebp
    10c2:       49 89 d1                mov    r9, rdx
    10c5:       5e                      pop    rsi
    10c6:       48 89 e2                mov    rdx, rsp
    10c9:       48 83 e4 f0             and    rsp, 0xfffffffffffffff0
    10cd:       50                      push   rax
    10ce:       54                      push   rsp
    10cf:       45 31 c0                xor    r8d, r8d
    10d2:       31 c9                   xor    ecx, ecx
    10d4:       48 8d 3d 32 01 00 00    lea    rdi, [rip+0x132]        # 0x120d
    10db:       ff                      .byte 0xff
    10dc:       15                      .byte 0x15
    10dd:       df                      .byte 0xdf
>>> offset = 0x10d4-e.entry
>>> hex(offset)
'0x14'
>>> print(e.disasm(entry_addr+offset, 7))
    10d4:       48 8d 3d 32 01 00 00    lea    rdi, [rip+0x132]        # 0x120d
>>> print(e.disasm(entry_addr+offset, 7).split('# ')[1])
0x120d
>>>
```

Then we can disassemble the `main` function and chase for the globals we need (both byte arrays and their respective size):

```console
>>> main_addr = 0x120d
>>> print(e.disasm(main_addr, 50))
    120d:       55                      push   rbp
    120e:       48 89 e5                mov    rbp, rsp
    1211:       48 83 ec 40             sub    rsp, 0x40
    1215:       89 7d dc                mov    DWORD PTR [rbp-0x24], edi
    1218:       48 89 75 d0             mov    QWORD PTR [rbp-0x30], rsi
    121c:       48 89 55 c8             mov    QWORD PTR [rbp-0x38], rdx
    1220:       e8 7b fe ff ff          call   0x10a0
    1225:       89 45 f8                mov    DWORD PTR [rbp-0x8], eax
    1228:       83 7d f8 ff             cmp    DWORD PTR [rbp-0x8], 0xffffffff
    122c:       75 19                   jne    0x1247
    122e:       48 8d 05 cf 0d 00 00    lea    rax, [rip+0xdcf]        # 0x2004
    1235:       48 89 c7                mov    rdi, rax
    1238:       e8 f3 fd ff ff          call   0x1030
    123d:       b8                      .byte 0xb8
    123e:       ff                      .byte 0xff
>>>
```

Eventually we find them a bit further in the disassembled `main` function:
```
- 12e8:       48 8d 15 71 2d 00 00    lea    rdx, [rip+0x2d71]             # 0x4060    // offset from main() start
- 12f8:       8b 0d fe df 18 00       mov    ecx, DWORD PTR [rip+0x18dffe] # 0x18f2fc  // offset+0x10
- 1309:       48 8d 05 d0 db 18 00    lea    rax, [rip+0x18dbd0]           # 0x18eee0  // offset+0x21
- 133b:       8b 05 87 db 18 00       mov    eax, DWORD PTR [rip+0x18db87] # 0x18eec8  // offset+0x53
```

We can extract them like we did above for the address of the `main` function:

```console
>>> hex(0x12e8-main_addr)
'0xdb'
>>> offset = 0xdb
>>> data1_addr = int(e.disasm(main_addr + offset, 7).split('# ')[1], 16)
>>> len2_addr  = int(e.disasm(main_addr + offset + 0x10, 6).split('# ')[1], 16)
>>> data2_addr = int(e.disasm(main_addr + offset + 0x21, 7).split('# ')[1], 16)
>>> len1_addr  = int(e.disasm(main_addr + offset + 0x53, 6).split('# ')[1], 16)
>>> print(hex(data1_addr), hex(len2_addr), hex(data2_addr), hex(len1_addr))
0x4060 0x18f2fc 0x18eee0 0x18eec8
>>>
```

Finally we can read/dump both byte array data and their respective size at these addresses:
```console
>>> len1  = unpack(e.read(len1_addr, 4))
>>> len2  = unpack(e.read(len2_addr, 4))
>>> data1 = e.read(data1_addr, len1)
>>> data2 = e.read(data2_addr, len2)
>>> print(hex(len1), hex(len2))
0x18ae68 0x41c
```

We peace this together in python's function `extract()`. See the full code in [sol.py](./sol.py).

With with, we have all the peaces to mimic the core of the original program like we manually did before. Moreover, since the extracted programs are almost identical (except for the manipulated byte arrays and their respective size), we can automate this process in a loop over and over again:

```python
elf = "introspection"
count = 0
while True:
    count += 1
    extracted = "extracted" + str(count)
    data1, len1, data2, len2 = extract(elf)
    store(extracted, mimic(data1, len1, data2, len2))
    print("Inception level ", count)
    elf = extracted
```

Let's open these `matriochkas` and see how many are embedded in each other!

```console
$ python3 sol.py SILENT
Inception level  1
Inception level  2
Inception level  3
(...)
Inception level  99
Inception level  100
Inception level  101
```

Eventually, the process stops after catching an exception. The last extracted binary indeed is different. Here is its decompiled `main` function from `Ghidra`, showing the expected password, finally!

```c
undefined8 FUN_00101149(int param_1,long param_2)

{
  int iVar1;
  undefined8 uVar2;

  if (param_1 < 2) {
    puts("Usage : ./introspection [MOT DE PASSE]");
    uVar2 = 1;
  }
  else {
    iVar1 = strcmp(*(char **)(param_2 + 8),"5t3althy_f1Le$-4nD_aUt0matIon");
    if (iVar1 == 0) {
      puts(":)");
      uVar2 = 0;
    }
    else {
      puts(":(");
      uVar2 = 0;
    }
  }
  return uVar2;
}
```

## Python code
Complete solution in [sol.py](./sol.py)

## Flag
404CTF{5t3althy_f1Le$-4nD_aUt0matIon}
