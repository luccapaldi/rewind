# rewind

For moments when you wish time ran backwards...

A convenient alternative to the rm command for UNIX systems with a built-in undelete interface.

### Did you write this after accidentally deleting something important?

Yes.

### Requirements

You will need to verify Python 3 is installed on your computer, along with the following packages:
* os
* sys
* subprocess

### Installation

These steps are intended for a Linux user running Bash. This script should run correctly on all UNIX systems, but the 'installation' may vary for each.

Begin by placing this file in a convenient location on your system and modifying the 'Options' section at the top of the script file. Note that if the number of files and directories in your bin folder exceeds the max_storage variable, the oldest contents will be deleted for good to keep the total number within check.

If you want to entirely replace the use of rm, add the following line to your .bashrc.

```
alias rm='python3 path_to_script'
```

Alternatively, you may choose to alias this script to another command if you want to retain use of the rm command.

### Usage

This script automatically generates a .recycling_bin folder in the home directory specified in the settings along with a index file. You can delete files or directories (but not both at once) in the same way as you would with the rm command. Note that no flags are necessary.

```
python3 rewind.py file.txt
python3 rewind.py file*
python3 rewind.py folder/
```

To restore the last deleted file or folder to its original directory, call the script with the '-u' flag:

```
python3 rewind.py -u
```

If you need to restore several files or directories at once, or ones deleted previously, call the script with the '-U' flag. This opens the index file in your terminal text editor of choice.

```
python3 rewind.py -U
```

Place an asterisk in front of any files or folders you want to restore.

```
*trash3/               |  /home/lcapaldi/files/scripts_personal/trash3/
trash5/               |  /home/lcapaldi/files/scripts_personal/trash5/
```

### Contributing

Feel free to modify, improve, or extend this script for personal use. If you want to contribute, please follow PEP8 guidelines and adhere to the programming style already present.

### License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.
