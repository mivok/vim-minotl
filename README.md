# vim-minotl - A minimal outliner for vim

Vim already works pretty well as an outliner. Vim-minotl provides some useful
default settings, a basic syntax file, and a couple of mappings that help.
Otherwise it tries to get out of your way.

Each outline entry is intended to take up one line, and vim-minotl is set to
visually wrap any long lines while keeping the file contents the same.

## Installation

If you don't use a plugin manager for vim:

* Copy the `ftplugin/` and `syntax/` directories to your `~/.vim` directory.

Vundle:

* Add `Plugin "mivok/vim-minotl"` to your vimrc, then run `:PluginInstall`

Pathogen:

* Clone this repository and place it in ~/.vim/bundle/vimtodo

## Enabling the plugin

* Option 1: Place `# vim: ft=minotl` at the top of your file, then reload the
  file.
* Option 2: Add the following to your `.vimrc` (this will use minotl for all
  files with the `.otl` extension):

        au BufNew,BufRead *.otl set ft=minotl

## Usage

Once the plugin is enabled for your file, simply add your entries to the file,
using Tab to indent while in insert mode, and `<<` and `>>` to (un)indent
while in normal mode.

Each entry should be on a single line. New lines will be treated as separate
entries for the purposes of folding. If a line is longer than your terminal
width, then it will wrap. Note: this feature requires support for the
`breakindent` option in vim 7.4.354 and above.

There are some additional keybindings added to make things easier:

* `<Leader>1`, `<Leader>2` and so on, set the fold level to the number you
  typed.
* `-` and `=` - open and close a fold (same as zc and zo respectively).

<!--
Make sure there are 5 blank lines at the bottom of the file so we don't
accidentally trigger the modeline mentioned in the doc.
.
-->
