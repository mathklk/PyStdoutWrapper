from stdoutWrapper import StdoutWrapper
from time import sleep

# put the process output into a buffer array
buff_size = 10
buff = []
def callback(stdout_line: str):
    global buff
    buff.append(int(stdout_line))
    buff = buff[-buff_size:]


def main():
    # create a StdoutWrapper instance, when count_up.exe outputs a new line on stdout, the callback will be called
    stw = StdoutWrapper('./count_up.exe', callback_output=callback)
    # start the execution, this will be done in a new thread, not blocking the current thread.
    stw.start()
    while True:
        try:
            sleep(1)
            print(buff)
        except KeyboardInterrupt:
            break
    stw.stop()


if __name__ == '__main__':
    main()
