import os, sys, time, shlex, re 

def runExec(args): # Run simple Command 
    for dir in re.split(":", os.environ['PATH']):
        program = "%s/%s" % (dir,args[0])
        try:
            os.execve(program, args, os.environ)
        except FileNotFoundError:
            pass
    sys.exit(0)