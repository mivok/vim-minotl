" Minimal Outliner Indentation file
" Maintainer:   Mark Harrison <mark@mivok.net>
" License:      MIT - See LICENSE file for details

" Only load this indent file when no other was loaded.
if exists("b:did_indent")
    finish
endif
let b:did_indent = 1

function! MinotlIndent()
    " Match the indent of the previous lines, and if the fold is closed, then
    " match the indent of the closed folded line (i.e. match the indent of the
    " previous visible line.
    return indent(foldclosed(v:lnum-1))
endfunction
set indentexpr=MinotlIndent()
