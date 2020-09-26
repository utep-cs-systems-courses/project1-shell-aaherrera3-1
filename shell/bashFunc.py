import os, sys, time, shlex, re 

def runExec(args, flag): # Run simple Command 
    for dir in re.split(":", os.environ['PATH']):
        program = "%s/%s" % (dir,args[0])
        try:
            if not flag:
                os.execve(program, args, os.environ)
            else:
                os.spawnve(os.P_WAIT, program, args, os.environ)
        except FileNotFoundError:
            pass
    sys.exit(0)

def outputRedirect(args, flag):
    index = args.index('>') # get index of redirect symbol 
    os.close(1)  # redirect child's output (stander input)
    os.open(args[index+1], os.O_CREAT | os.O_WRONLY) # open file to write to
    os.set_inheritable(1, True)
    runExec(args[0:index], flag)

def inputRedirect(args, flag):
    index = args.index('<') # get index of redirect symbol
    os.close(0)  # redirect child's input (stander input)
    os.open(args[index+1], os.O_RDONLY) #open file to read
    os.set_inheritable(0,True)
    runExec(args[0:index], flag)

def cd(args):
    if '..' in args[1]: # go back once in directory 
        os.chdir('..')
    else:
        os.chdir(args[1]) # change the directory 

def pipe(args, flag):
    cmd1 = args[0:args.index('|')] # first command 
    cmd2 = args[args.index("|")+1:] # second command
    
    pr, pw = os.pipe() # copy fd for reading and writing 
    for fd in (pr, pw):
        os.set_inheritable(fd, True) # set inheritance true 

    rc = os.fork() # start fork

    if rc < 0:
        print("fork failed, returning %d\n" % rc, file=sys.stderr)
        sys.exit(1)
    elif rc == 0:
        os.close(1)              # redirect child's stdout
        os.dup(pw)  # duplicate stdout into pw
        os.set_inheritable(1,True) # set inheritance true for stdout
        for fd in (pr, pw): #close fd 
            os.close(fd)
        runExec(cmd1, flag) # run first command 
    else:
        os.close(0) # close stdin 
        os.dup(pr) # duplicate stdin
        os.set_inheritable(0,True) #set stdin inheritance true 
        for fd in (pw, pr): # close fd 
            os.close(fd)
        runExec(cmd2, flag) # run second command 