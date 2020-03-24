import os.path
import sys
import subprocess

#  OPTIONS:
# ----------------------------------------------------------------------------
home = "/home/lcapaldi"  #  path to home directory
max_storage = 100           #  max number of files or directories in bin
bin_path = home + "/.recycling_bin"
index_path = home + "/.recycling_bin/index.txt"
editor = "vi"
# ----------------------------------------------------------------------------

#  Bold text in terminal
start_bold = "\033[1m"
end_bold = "\033[0;0m"

#  Create bin file if nonexistent
if not os.path.isdir(bin_path):
    subprocess.run(["mkdir",bin_path])
# Create index file if nonexistent
if not os.path.isfile(index_path):
    subprocess.run(["touch",index_path])

#  Store command line inputs
args = sys.argv
args.remove("rewind.py")
#  Process inputs and identify flags
undo = False
rewind = False
for i in range(len(args)):
    if args[i] == "-u":
        undo = True
        args.remove("-u")
    elif args[i] == "-U":
        rewind = True
        args.remove("-U")
    #  Append '/' to directories if necessary
    elif len(args[i].split(".")) == 1 and args[i][-1] != "/":
        args[i] = args[i] + "/"

#  Store file or directory info in index
def store_info(arg):
    location = os.getcwd() + "/" + arg
    with open(index_path, 'a') as index:
        arg_formatted = "{:<20}".format(arg)
        index.write(arg_formatted) 
        index.write("  |  " + location + "\n")

#  Physically replace file or directory 
def replace_filedir(fileinfo):
    filename = start_bold + fileinfo[0] + end_bold
    filepath = start_bold + fileinfo[2] + end_bold
    try:
        current_path = bin_path + "/" + fileinfo[0]
        subprocess.run(["mv",current_path,fileinfo[2]])  
        print(filename + " successfully restored to " + filepath + " !")
    except:
        print("Error! File could not be restored!")

#  Restore last deleted file or directory 
def restore_prev():
    if undo == True:
        with open(index_path, "r+") as index:
            #  Store file info
            files = index.readlines()
            #  Reset pointer
            index.seek(0)
            #  Check case where bin is empty
            if len(files) == 0:
                print("Error! Recycling bin is empty")
            else:
                #  Remove last file from index
                for f in files[:-1]:
                    index.write(f)
                index.truncate()
                #  Store file info 
                fileinfo = files[-1].split()    
                replace_filedir(fileinfo)

#  Verify number of files and directories in bin does not exceed limit
def check_count():
    with open(index_path, "r+") as index:
        lines = index.readlines()
        #  Determine if too many files
        if len(lines) > max_storage:
            numdelete = len(lines) - max_storage
            #  Update index file
            index.seek(0)
            for l in lines[numdelete:]:
                index.write(l)
            index.truncate() 
            #  Get paths of files to delete
            todelete = []
            for l in lines[:numdelete]:
                todelete.append(bin_path + "/" + l.split()[0])
            for path in todelete:
                #  Check if directory
                if path[-1] == "/":
                    subprocess.run(["rm",'-r',path])                
                else:
                    subprocess.run(["rm",path])
 
#  Restore selection of previously deleted files or folders
def rewind_time():
    if rewind == True:
        #  Mark files and directories with *
        subprocess.run(["vim",index_path])
        #  Restore files and directories
        with open(index_path, "r+") as index:    
            lines = index.readlines()
            index.seek(0)
            for l in lines:
                if l[0] == "*":
                    #  Format strings 
                    fileinfo = l.split()
                    fileinfo[0] = fileinfo[0][1:]
                    replace_filedir(fileinfo) 
                else:
                    index.write(l)
            index.truncate()

#  Remove files or directories
for a in args:
    subprocess.run(["mv",a,bin_path])    
    store_info(a)
    #print(a)
    #try:
    #    subprocess.run(["mv",a,bin_path])    
    #    store_info(a,bin_path)
    #except:
    #    print("Error! File could not be removed!")

#  Execute script
restore_prev()
check_count()
rewind_time()
