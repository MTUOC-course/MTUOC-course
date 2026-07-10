## Introduction

This section provides an overview of the essential Unix commands required to execute programs or scripts via the Terminal. It serves as a "survival guide" for navigating Unix-based environments. While the interface of a Linux or macOS Terminal is conceptually similar to the Windows Command Prompt, several instructions and the underlying file structure differ significantly.

Below is a technical introduction to these commands.

### Launching the Terminal

Accessing the Terminal depends on your specific operating system (macOS or Linux distribution). However, in nearly all environments, the application is simply named Terminal and can be located within your standard applications folder or via the system search bar.

### Identifying Your Current Location

Upon launching the Terminal, you will typically encounter a prompt similar to: `user@computer:~$`

* `user`: Represents your current username.
* `computer`: The hostname assigned to your machine (or its IP address if no name is defined).

By default, the Terminal opens in your home directory, which is why no specific path is displayed initially. As you navigate through the file system, the prompt will update to reflect your current location.

To verify your exact path at any time, use the *Print Working Directory* command:

`pwd`

The output will display the full path, for example: `/home/user`

### Navigating the Directory Structure

Unlike Windows, which uses drive letters (e.g., C:\), Unix-based systems (Linux and macOS) utilize a unified hierarchical structure originating from the root directory, symbolized by a forward slash: `/

Users have full read/write permissions within their specific home directory: `/home/user`

To change your current location, use the `cd` (*Change Directory*) command:

To go to a specific path:

`cd /home/user/translations`

To enter a subdirectory within your current location:

`cd economics`

To move up one level in the directory tree:

`cd ..`

(Note: A space is mandatory between cd and ..)

### Listing Directory Content

To inspect the files and subdirectories contained within your current location, execute:

`ls`

### Managing Files and Directories

The following commands allow you to create, copy, and delete data:

**Create a directory**: To create a folder named medicine:

`mkdir medicine`

**Delete a directory**: (Note: The directory must be empty):

`rmdir medicine`

**Copy files**: To copy doc1.txt to a new file named backup.txt:

`cp doc1.txt backup.txt`

**Delete a file**: To permanently remove a file:

`rm backup.txt`

Unix supports wildcards to perform operations on multiple files simultaneously:

* \* (Asterisk): Matches any sequence of characters.

* ? (Question mark): Matches any single character.

Warning: Executing `rm *` will delete the entire contents of the current directory. In Unix, there is no "Recycle Bin"; once a file is removed via Terminal, it is permanently deleted.

Example of a complex command:

`cp doc?.txt /home/user/translations/medicine`

This will copy all `.txt` files starting with "doc" followed by exactly one character into the specified directory.

### Efficiency and Shortcuts

The Terminal includes several features designed to streamline your workflow and reduce manual typing:

* **Up Arrow**: Cycles through your command history, allowing you to repeat previous instructions.
* T**ab Completion**: Pressing the Tab key automatically completes file names or commands. If there are multiple possibilities, press Tab twice to list all available options.
* **Ctrl+R**: Initiates a reverse search through your command history. Start typing a few letters to find a previous command; press Ctrl+R repeatedly to cycle through matches.

### Documentation and Help

If you encounter unfamiliar instructions, Unix provides built-in documentation:

* **man** [command]: Displays the comprehensive manual for a specific command.
* **whatis** [command]: Provides a concise, one-line description of the command's function.
* **apropos** [keyword]: Searches the manual pages for commands related to a specific keyword.