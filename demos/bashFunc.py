import os, sys, time, shlex, re 

def runExec(args): # Run simple Command 
    for dir in re.split(":", os.environ['PATH']):
        program = "%s/%s" % (dir,args[0])
        try:
            os.execve(program, args, os.environ)
        except FileNotFoundError:
            pass
    sys.exit(0)

def outputRedirect(args):
    index = args.index('>') # get index of redirect symbol 
    os.close(1)  # redirect child's output
    os.open(args[index+1], os.O_CREAT | os.O_WRONLY) # open file to write to
    os.set_inheritable(1, True)
    runExec(args[0:index])

def inputRedirect(args):
    index = args.index('<') # get index of redirect symbol
    os.close(0)  # redirect child's output
    os.open(args[index+1], os.O_RDONLY) #open file to read
    os.set_inheritable(0,True)
    runExec(args[0:index])