import os, sys, time

directory = os.getcwd() #Get current working directory 
while 1:
    command = input(directory+'$') #Ask user for command input 

    rc = os.fork() #create a child process

    if rc < 0: #if rc is less than 0 fork failed
        os.write(2,("Fork failed, returning %d\n" % rc).encode())
        sys.exit(1)
    elif rc == 0: #if rc is equal to 0 run child process
        os.system(command)
        time.sleep(1)
        sys.exit(0)
    else:   #wait for child process to end before continuing.
        child = os.wait()

        
