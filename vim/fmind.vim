" https://vimhelp.org/syntax.txt.html#highlight
" GUI or a truecolor terminal with :set termguicolors.
set background=light
highlight clear
if exists("syntax_on")
  syntax reset
endif
let g:colors_name = "fmind"

highlight Normal guifg=#202124 guibg=#ffffff gui=NONE cterm=NONE
highlight NormalNC guifg=#202124 guibg=#ffffff gui=NONE cterm=NONE
highlight Comment guifg=#595d62 guibg=NONE gui=NONE cterm=NONE
highlight Constant guifg=#934900 guibg=NONE gui=NONE cterm=NONE
highlight String guifg=#0d652d guibg=NONE gui=NONE cterm=NONE
highlight Character guifg=#0d652d guibg=NONE gui=NONE cterm=NONE
highlight Number guifg=#934900 guibg=NONE gui=NONE cterm=NONE
highlight Boolean guifg=#934900 guibg=NONE gui=NONE cterm=NONE
highlight Float guifg=#934900 guibg=NONE gui=NONE cterm=NONE
highlight Identifier guifg=#202124 guibg=NONE gui=NONE cterm=NONE
highlight Function guifg=#174ea6 guibg=NONE gui=NONE cterm=NONE
highlight Statement guifg=#174ea6 guibg=NONE gui=bold cterm=bold
highlight Conditional guifg=#174ea6 guibg=NONE gui=NONE cterm=NONE
highlight Repeat guifg=#174ea6 guibg=NONE gui=NONE cterm=NONE
highlight Label guifg=#174ea6 guibg=NONE gui=NONE cterm=NONE
highlight Operator guifg=#202124 guibg=NONE gui=NONE cterm=NONE
highlight Keyword guifg=#174ea6 guibg=NONE gui=bold cterm=bold
highlight Exception guifg=#174ea6 guibg=NONE gui=NONE cterm=NONE
highlight PreProc guifg=#681da8 guibg=NONE gui=NONE cterm=NONE
highlight Type guifg=#681da8 guibg=NONE gui=NONE cterm=NONE
highlight Special guifg=#174ea6 guibg=NONE gui=NONE cterm=NONE
highlight Delimiter guifg=#202124 guibg=NONE gui=NONE cterm=NONE
highlight Underlined guifg=#174ea6 guibg=NONE gui=underline cterm=underline
highlight Ignore guifg=#595d62 guibg=NONE gui=NONE cterm=NONE
highlight Error guifg=#a50e0e guibg=#fad2cf gui=NONE cterm=NONE
highlight Todo guifg=#934900 guibg=#feefc3 gui=NONE cterm=NONE
highlight Cursor guifg=#202124 guibg=#4285f4 gui=NONE cterm=NONE
highlight lCursor guifg=#202124 guibg=#4285f4 gui=NONE cterm=NONE
highlight CursorLine guifg=NONE guibg=#f1f3f4 gui=NONE cterm=NONE
highlight CursorColumn guifg=NONE guibg=#f1f3f4 gui=NONE cterm=NONE
highlight ColorColumn guifg=NONE guibg=#f1f3f4 gui=NONE cterm=NONE
highlight LineNr guifg=#595d62 guibg=#ffffff gui=NONE cterm=NONE
highlight CursorLineNr guifg=#174ea6 guibg=#f1f3f4 gui=bold cterm=bold
highlight SignColumn guifg=#595d62 guibg=#ffffff gui=NONE cterm=NONE
highlight FoldColumn guifg=#595d62 guibg=#ffffff gui=NONE cterm=NONE
highlight Folded guifg=#595d62 guibg=#f1f3f4 gui=NONE cterm=NONE
highlight NonText guifg=#9aa0a6 guibg=NONE gui=NONE cterm=NONE
highlight SpecialKey guifg=#9aa0a6 guibg=NONE gui=NONE cterm=NONE
highlight EndOfBuffer guifg=#595d62 guibg=#ffffff gui=NONE cterm=NONE
highlight Visual guifg=NONE guibg=#d2e3fc gui=NONE cterm=NONE
highlight VisualNOS guifg=NONE guibg=#d2e3fc gui=NONE cterm=NONE
highlight Search guifg=#202124 guibg=#feefc3 gui=NONE cterm=NONE
highlight IncSearch guifg=#202124 guibg=#fbbc04 gui=NONE cterm=NONE
highlight CurSearch guifg=#202124 guibg=#fbbc04 gui=NONE cterm=NONE
highlight MatchParen guifg=#202124 guibg=#feefc3 gui=NONE cterm=NONE
highlight Pmenu guifg=#202124 guibg=#f1f3f4 gui=NONE cterm=NONE
highlight PmenuSel guifg=#202124 guibg=#d2e3fc gui=NONE cterm=NONE
highlight PmenuSbar guifg=NONE guibg=#f1f3f4 gui=NONE cterm=NONE
highlight PmenuThumb guifg=NONE guibg=#9aa0a6 gui=NONE cterm=NONE
highlight StatusLine guifg=#202124 guibg=#d2e3fc gui=bold cterm=bold
highlight StatusLineNC guifg=#595d62 guibg=#f1f3f4 gui=NONE cterm=NONE
highlight StatusLineTerm guifg=#202124 guibg=#d2e3fc gui=NONE cterm=NONE
highlight StatusLineTermNC guifg=#595d62 guibg=#f1f3f4 gui=NONE cterm=NONE
highlight VertSplit guifg=#9aa0a6 guibg=#f1f3f4 gui=NONE cterm=NONE
highlight TabLine guifg=#595d62 guibg=#f1f3f4 gui=NONE cterm=NONE
highlight TabLineSel guifg=#202124 guibg=#fbbc04 gui=bold cterm=bold
highlight TabLineFill guifg=#595d62 guibg=#f1f3f4 gui=NONE cterm=NONE
highlight WildMenu guifg=#202124 guibg=#d2e3fc gui=NONE cterm=NONE
highlight Title guifg=#174ea6 guibg=NONE gui=bold cterm=bold
highlight Directory guifg=#174ea6 guibg=NONE gui=NONE cterm=NONE
highlight ErrorMsg guifg=#a50e0e guibg=#ffffff gui=NONE cterm=NONE
highlight WarningMsg guifg=#934900 guibg=#ffffff gui=NONE cterm=NONE
highlight MoreMsg guifg=#0d652d guibg=#ffffff gui=NONE cterm=NONE
highlight Question guifg=#00636d guibg=#ffffff gui=NONE cterm=NONE
highlight ModeMsg guifg=#174ea6 guibg=#ffffff gui=NONE cterm=NONE
highlight DiffAdd guifg=NONE guibg=#ceead6 gui=NONE cterm=NONE
highlight DiffDelete guifg=#a50e0e guibg=#fad2cf gui=NONE cterm=NONE
highlight DiffChange guifg=NONE guibg=#feefc3 gui=NONE cterm=NONE
highlight DiffText guifg=#202124 guibg=#fbbc04 gui=NONE cterm=NONE
highlight SpellBad guifg=NONE guibg=NONE gui=undercurl cterm=undercurl
highlight SpellCap guifg=NONE guibg=NONE gui=undercurl cterm=undercurl
highlight SpellRare guifg=NONE guibg=NONE gui=undercurl cterm=undercurl
highlight SpellLocal guifg=NONE guibg=NONE gui=undercurl cterm=undercurl
highlight debugPC guifg=NONE guibg=#feefc3 gui=NONE cterm=NONE
highlight debugBreakpoint guifg=#a50e0e guibg=NONE gui=NONE cterm=NONE
highlight SpellBad guisp=#a50e0e
highlight SpellCap guisp=#934900
highlight SpellRare guisp=#681da8
highlight SpellLocal guisp=#00636d

let g:terminal_ansi_colors = [
      \ "#202124", "#a50e0e", "#0d652d", "#934900",
      \ "#174ea6", "#681da8", "#00636d", "#202124",
      \ "#595d62", "#a50e0e", "#0d652d", "#934900",
      \ "#174ea6", "#681da8", "#00636d", "#202124"
      \ ]
