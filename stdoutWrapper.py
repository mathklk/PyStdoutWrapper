import subprocess
import sys
from typing import *
from threading import Thread


class StdoutWrapper:
    def __init__(self, command: str,
                 callback_output: Callable[[str], Any],
                 callback_command_exit: Callable[[], Any] = None,
                 encoding: str = 'ascii'):
        """
        command: shell command to be executed, forwarded to subprocess.Popen
        callbackOut: When the command outputs a new line of text on stdout, this function will be called
        callbackExit: When the command finishes (by itself, not via stop()), this function will be called
        """
        self.__encoding = encoding
        self.__process = None
        self.__thread = None
        self.__command = command
        self.__callbackOut = callback_output
        self.__callbackExit = callback_command_exit
        self.__signalStopThread = False

    def start(self):
        """
        Starts the execution as a new process in in a new thread
        """
        if self.__thread is not None:
            return
        self.__signalStopThread = False
        self.__thread = Thread(target=self.__run)
        self.__thread.start()

    def stop(self):
        """
        Kills the process and then signals to stop the thread.
        """
        if self.__process is not None:
            self.__process.kill()
        self.__signalStopThread = True  # most likely redundant, killing the process also does the job

    def __run(self):
        self.__process = subprocess.Popen(
            self.__command,
            stdout=subprocess.PIPE,
            stderr=sys.stderr,
            shell=False,
            encoding=self.__encoding
        )
        while True:
            pOut = self.__process.stdout.readline()
            if pOut == '' and self.__process.poll() is not None:
                self.__callbackExit()
                break
            if self.__signalStopThread:
                break
            if pOut:
                self.__callbackOut(pOut.strip())

    def __callbackExit(self):
        if self.__callbackExit is not None:
            self.__callbackExit()
        self.stop()
