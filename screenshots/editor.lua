-- https://neovim.io/doc/user/options.html
local runtime = dofile(vim.env.FMIND_THEME_ROOT .. "/checks/runtime.lua")
for _, lang in ipairs(runtime.languages) do
  vim.treesitter.language.add(lang)
  assert(vim.treesitter.query.get(lang, "highlights"), "Run mise run install: missing " .. lang .. " query")
end
vim.opt.number = true
vim.opt.hlsearch = true
vim.opt.cursorline = true
vim.opt.colorcolumn = "88"
vim.opt.laststatus = 2
vim.opt.showmode = false
vim.opt.swapfile = false
vim.opt.shortmess:append("I")
vim.cmd("syntax enable")
vim.cmd("colorscheme fmind")
vim.opt.conceallevel = 2
vim.api.nvim_create_autocmd("FileType", { callback = function(ev) vim.treesitter.start(ev.buf) end })
vim.opt.statusline = " %{mode() ==# 'n' ? 'NORMAL' : mode() ==# 'V' ? 'VISUAL LINE' : 'VISUAL'}  %f%=%l:%c  UTF-8 "
vim.api.nvim_create_autocmd("VimEnter", { callback = function() vim.api.nvim_win_set_cursor(0, { 14, 4 }) end })
