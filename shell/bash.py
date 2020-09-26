import os, sys, time, shlex, re 
from bashFunc import *


def main():
    while True:
        directory = os.getcwd() # Get current working directory
        os.write(1,(directory+' $').encode())
        args = os.read(0,128).decode() # user input
        backFlag = False # false if not in background
        if '&' in args:
            backFlag = True # set it true if background
            args = args.replace('&','').strip() # remove & and trayling spaces

        if 'exit' in args: # check if user wants to exit progrma
            sys.exit(1)
        
        args = shlex.split(args) # slit input to shell keys 

        rc = os.fork() # creat new child process

        if rc < 0: # If fork fails 
            os.write(2,("fork failed, returning %d\n" % rc).encode)
            sys.exit(1)
        elif rc == 0: # If fork works
            if '>' in args:
                outputRedirect(args, backFlag) # run redirect output
            elif '<' in args:
                inputRedirect(args, backFlag) # run redirect intput 
            elif 'cd' in args:
                cd(args) # run change working directory 
            elif '|' in args:
                pipe(args, backFlag) # run pipe function 
            else:
                runExec(args, backFlag) # Run simple command
        else:
            if not backFlag: # if in background dont wait 
                os.wait() # wait for child process to 

if __name__ == "__main__":
    main()