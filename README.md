# PythonShit
These are the collected python shit projects witch may have a usage for anyone.

The install is very easy, just
```
dpkg -i pythonshit.deb
```
## b2fsh
https://github.com/boba2fett/b2fSh
## dcnotify
A deamon configured by /etc/python-shit/discordnotify.json
that sends a push message per the "Schwering Benachrichtigungscenter".
It has no arguments.
## dcshowon
A program to list all the users online on a discord.
It has no arguments.
## fromandto
Binds a key to an action of copying the selected text into a file and pasting contents from another file. Hookline means sth the test copied has to contain. It is designed for assisted browser automation.

```
usage: fromandto [-h] [-s HOOKLINE] [-d] [-v] readfile writefile                                                           
                                                                                                                           
Insert line by line in a file from a GUI by just pressing a key (ESC exits everytime)                                      
                                                                                                                           
positional arguments:                                                                                                      
  readfile                                                                                                                 
  writefile                                                                                                                
                                                                                                                           
optional arguments:                                                                                                        
  -h, --help            show this help message and exit                                                                    
  -s HOOKLINE, --hookline HOOKLINE                                                                                         
                        search for occurence of string                                                                     
  -d, --delay           make a bigger delay before using clipboard                                                         
  -v, --verbose         verbose output
```
## indexsto
A too designed for indexing all contents of a special website.
## insert
Pastes line for line out of a file.
```
usage: insert [-h] [-e] filename                                                                                           
                                                                                                                           
Insert line by line of a file into a GUI by just pressing a key                                                            
                                                                                                                           
positional arguments:                                                                                                      
  filename                                                                                                                 
                                                                                                                           
optional arguments:                                                                                                        
  -h, --help   show this help message and exit                                                                             
  -e, --enter  makes an enter after insert
```