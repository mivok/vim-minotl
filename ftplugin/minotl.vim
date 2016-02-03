" Minimal Outliner
" Maintainer:   Mark Harrison <mark@mivok.net>
" License:      MIT - See LICENSE file for details

" Only load if we haven't already
if exists("b:did_ftplugin")
    finish
endif
let b:did_ftplugin = 1

" One line == one item, wrapping is all visual
setlocal textwidth=0
setlocal breakindent " Needs vim 7.4.354 or higher
setlocal linebreak
"set breakindentopt=min:20,shift:0,sbr
set showbreak=\|\ 

"" Folding/indentation

" Indent folding done right
function! GetOutlineFold(line)
    if getline(a:line) =~? '\v^\s*$'
        return '-1'
    endif
    let curr_indent = indent(a:line) / &shiftwidth
    let next_indent = indent(a:line + 1) / &shiftwidth
    if next_indent > curr_indent
        return ">" . next_indent
    else
        return curr_indent
    end
endfunction

function! GetFoldText()
    " Sets the fold text to a full line of text plus '...'
    " Works out the visible part of the window for the width of the line
    let linewidth = winwidth(0) - &foldcolumn
        \- (&number || &relativenumber ? &numberwidth : 0)
    return getline(v:foldstart)[:linewidth-4]."..."
endfunction

setlocal foldmethod=expr
setlocal foldexpr=GetOutlineFold(v:lnum)
setlocal foldtext=GetFoldText()
setlocal fillchars=fold:\ 
setlocal autoindent
setlocal foldcolumn=1

" Mappings for folding
map <buffer> <LocalLeader>0 :set foldlevel=0<CR>
map <buffer> <LocalLeader>1 :set foldlevel=1<CR>
map <buffer> <LocalLeader>2 :set foldlevel=2<CR>
map <buffer> <LocalLeader>3 :set foldlevel=3<CR>
map <buffer> <LocalLeader>4 :set foldlevel=4<CR>
map <buffer> <LocalLeader>5 :set foldlevel=5<CR>
map <buffer> <LocalLeader>6 :set foldlevel=6<CR>
map <buffer> <LocalLeader>7 :set foldlevel=7<CR>
map <buffer> <LocalLeader>8 :set foldlevel=8<CR>
map <buffer> <LocalLeader>9 :set foldlevel=9<CR>

" Some other mappings
"" TODO - do we actually want tab to indent/unindent?
"" It doesn't work quite as expected when folded
nnoremap <buffer> <Tab> >>
nnoremap <buffer> <S-Tab> <<
" From TVO - it seems like a good idea
nnoremap <buffer> = zo
nnoremap <buffer> - zc
" Jump to next/previous entry at the same level as the current one
nnoremap <buffer> <silent> { :call search('^'. matchstr(getline('.'),
    \'\(^\s*\)') . '\%<' . line('.') . 'l\S', 'be')<CR>
nnoremap <buffer> <silent> } :call search('^'. matchstr(getline('.'),
    \'\(^\s*\)') . '\%>' . line('.') . 'l\S', 'e')<CR>

" Don't close folds when inserting nested text right after a title
" (Taken From
" http://vim.wikia.com/wiki/Keep_folds_closed_while_inserting_text)
autocmd InsertEnter * if !exists('w:last_fdm') |
    \ let w:last_fdm=&foldmethod | setlocal foldmethod=manual | endif
autocmd InsertLeave,WinLeave * if exists('w:last_fdm') |
    \ let &l:foldmethod=w:last_fdm | unlet w:last_fdm | foldopen | endif
