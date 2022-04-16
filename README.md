# StdoutWrapper

A simple Python wrapper for running programs as subprocesses in a new thread while convieniently accessing their stdout.

This is intended for accessing the stdout of a program while the program is still executing.
For example, when a program outputs live/realtime data that you want to handle in a Python script.

# Example

As an example theres the pre-compiled program `count_up.exe` included in this repository.
`count_up.exe` starts at 0 and outputs the next integer with a one second delay.

```
> count_up.exe
0
1
2
3
...
```

To capture this programs output, the following example code can be used.

```py
from stdoutWrapper import StdoutWrapper
from time import sleep

# callback method, put the process output into a buffer array
buff_size = 10
buff = []
def callback(stdout_line: str):
    global buff
    buff.append(int(stdout_line))
    buff = buff[-buff_size:]


# create a StdoutWrapper instance, when count_up.exe outputs a new line on stdout, the callback will be called
stw = StdoutWrapper('./count_up.exe', callback_output=callback)
# start the execution, this will be done in a new thread, not blocking the current thread
stw.start()
while True:
    try:
        sleep(1)
        print(buff)
    except KeyboardInterrupt:
        break
stw.stop()
```

