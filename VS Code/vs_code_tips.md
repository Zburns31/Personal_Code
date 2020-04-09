# VS Code Features and Tips

## Command Palette:
One of the most useful features in VS Code is the quick access command palette. Use ⇧⌘P to access many of the VS Code features with your keyboard

## How to edit your settings:
Settings that you apply to VS Code can either be done globally (User settings) or inside of a workspace (a directory containing multiple root directories). To edit your user settings, press ⇧⌘P and enter the command **Open Settings JSON** for editing the actual file and **Open Settings UI** for the user-friendly UI.

## Setting up your linter:
In VS Code, you have the option for setting your preferred linter. Some linters will be installed by default when you install the language support extension (Python default is pep8). To change this, you can press ⇧⌘P and enter **language: Select Linter**

## VS Code CLI Tool:
An incredibly helpful feature in VS Code is the CLI.  After pressing ⇧⌘P, type in **shell command** and select `Install code command in Path`. Using this, we can now open VS Code from the command line. For example:

* code ~/Documents/Code/path_to_directory

After this is installed, you can launch VS Code from the command line for a bunch of different use cases. For example, a few helpful commands are:
* **open code with current directory**
    * `code .`
* **open the current directory in the most recently used code window**
    * `code -r .`
* **create a new window**
    * `code -n`
* **open the diff editor**
    * code --diff `file1` `file2`
* **create a new window**
    * code -n

## Integrated Terminal
TODO

# Helpful Extensions

## Git Integration & GitLens:
Git ships with a Git Source Control Manager (SCM) which allows you to use the UI inside of VS Code for git. **Note**, it depends on your computers version of Git, so you will need to install it before you can use this feature. Inside of VS Code on the left hand side access bar, look for the `Source Control` icon. Using this feature, you can:

* add, stage and commit files
* Clone repositories
* Checkout and create branches and tags
* Merge conflicts
* View differences between files
* Search for specific commits or view commit history using Timeline View

See more here: https://code.visualstudio.com/docs/editor/versioncontrol

In addition to this, a helpful extension is GitLens, which allows you to see which code was written by who and when

## Markdown Viewer:
VS Code has a built in markdown document viewer. Press ⇧⌘V when you are working on a markdown document, to see the rendered output in a new tab

## Jupyter Notebook support:
https://code.visualstudio.com/docs/python/jupyter-support-py

## Time Saving Tips:
Add the below commands to your settings.json file to help save you time as you're writing code
1. **Format pasted code:** add "editor.formatOnPaste": true
1. **Format code on saving:** "editor.formatOnSave": true
1. **Trim extra newlines on save:** "files.trimFinalNewlines": true
1. **Trim trailing whitespace on save:** "files.trimTrailingWhitespace": true
1. **Set autowrap length for code:** "editor.wordWrapColumn": 100