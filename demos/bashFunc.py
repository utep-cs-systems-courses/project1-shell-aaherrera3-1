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
    os.close(1)  # redirect child's output (stander input)
    os.open(args[index+1], os.O_CREAT | os.O_WRONLY) # open file to write to
    os.set_inheritable(1, True)
    runExec(args[0:index])

def inputRedirect(args):
    index = args.index('<') # get index of redirect symbol
    os.close(0)  # redirect child's input (stander input)
    os.open(args[index+1], os.O_RDONLY) #open file to read
    os.set_inheritable(0,True)
    runExec(args[0:index])

def cd(args):
    if '..' in args[1]:
        os.chdir('..')
    else:
        os.chdir(args[1])

def pipe(args):
    cmd1 = args[0:args.index('|')]
    cmd2 = args[args.index("|")+1:]
    
    pr, pw = os.pipe()
    for fd in (pr, pw):
        os.set_inheritable(fd, True)

    rc = os.fork()

    if rc < 0:
        print("fork failed, returning %d\n" % rc, file=sys.stderr)
        sys.exit(1)
    elif rc == 0:
        os.close(1)              # redirect child's stdout
        os.dup(pw)
        os.set_inheritable(1,True)
        for fd in (pr, pw):
            os.close(fd)
        runExec(cmd1)
    else:
        os.close(0)
        os.dup(pr)
        os.set_inheritable(0,True)
        for fd in (pw, pr):
            os.close(fd)
        runExec(cmd2)