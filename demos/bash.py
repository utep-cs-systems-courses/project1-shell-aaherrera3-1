import os, sys, time, shlex, re 
from bashFunc import *


def main():
    while True:
        directory = os.getcwd() # Get current working directory
        args = input(directory+'$') # user input

        if args == "exit": # check if user wants to exit progrma
            sys.exit(1)
        
        args = shlex.split(args) # slit input to shell keys 

        rc = os.fork() # creat new child process

        if rc < 0: # If fork fails 
            os.write(2,("fork failed, returning %d\n" % rc).encode)
            sys.exit(1)
        elif rc == 0: # If fork works
            runExec(args) # Run simple command
        else:
            os.wait() # wait for child process to 

if __name__ == "__main__":
    main()