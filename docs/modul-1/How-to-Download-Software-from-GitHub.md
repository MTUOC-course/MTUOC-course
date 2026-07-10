## What is GitHub?

GitHub is a cloud-based platform used by developers to store, manage, and share their software code. It uses a system called Git, which tracks every change made to the files. For this course, GitHub acts as our central repository where all the tools and scripts for the MTUOC-server are hosted.

There are three main ways to get the software from a GitHub repository to your local machine:

### 1. Downloading as a ZIP File

This is the simplest method if you just want a one-time copy of the files and do not plan to update them using Git.

* Navigate to the main page of the repository.
* Click the green Code button located at the top right of the file list.
* Select Download ZIP.

Once downloaded, extract the ZIP file to a folder on your computer.

## 2. Cloning the Repository

Cloning creates a linked copy of the repository on your computer. This allows you to easily update the software if the instructor makes changes. To use this method, you need to have [Git installed](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git). Open your terminal or command prompt and type:

```
git clone https://github.com/mtuoc/MTUOC-server
```

Note: Replace the URL with the actual repository address found under the green "Code" button.

### 3. Using Releases

Sometimes, developers package specific versions of their software that are stable and ready for production. These are called Releases.

**Where to find them**: On the right-hand sidebar of the main repository page, look for the Releases section.

**Why use them**: While the main code might be under development, a Release is a "snapshot" that is guaranteed to work.

**How to download**: Click on the latest release version and download the "Source code (zip)" or the specific executable files (assets) provided for your operating system.