" Minimal outliner syntax file
" Maintainer:   Mark Harrison <mark@mivok.net>
" License:      MIT - See LICENSE file for details

" Quit when a (custom) syntax file was already loaded
if exists("b:current_syntax")
  finish
endif

syn match otlComment /^#.*$/

function! s:HighlightIndent(level)
    exe "syn match level" . a:level . " /^" .
                \repeat(" ",  &shiftwidth * (a:level - 1)) . "\\S.*$/"
endfunction

call s:HighlightIndent(1)
call s:HighlightIndent(2)
call s:HighlightIndent(3)
call s:HighlightIndent(4)
call s:HighlightIndent(5)

hi def link level1 Statement
hi def link level2 Identifier
hi def link level3 Preproc
hi def link level4 Constant
hi def link level5 Type

hi def link otlComment Comment

let b:current_syntax = "minotl"
