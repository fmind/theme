-- https://neovim.io/doc/user/diagnostic.html
-- Exercise native editor states with synthetic content and no user configuration.
vim.opt.runtimepath:prepend(assert(vim.env.FMIND_THEME_ROOT) .. "/nvim")
vim.cmd.colorscheme("fmind")
local api = vim.api
api.nvim_buf_set_lines(0, 0, -1, false, { "value = 1", "value = 2", "return value" })
local namespace = api.nvim_create_namespace("fmind-states")
vim.diagnostic.set(namespace, 0, {
  { lnum = 0, col = 0, message = "Synthetic error", severity = vim.diagnostic.severity.ERROR },
  { lnum = 1, col = 0, message = "Synthetic warning", severity = vim.diagnostic.severity.WARN },
})
local floatbuf, floatwin = vim.diagnostic.open_float(0, { scope = "buffer", focusable = false })
assert(floatbuf and api.nvim_win_is_valid(floatwin))
assert(table.concat(api.nvim_buf_get_lines(floatbuf, 0, -1, false), "\n"):find("Synthetic error"))
api.nvim_win_close(floatwin, true)
vim.cmd("vnew")
api.nvim_buf_set_lines(0, 0, -1, false, { "value = 1", "value = 3", "return value" })
vim.cmd("diffthis")
vim.cmd("wincmd p")
vim.cmd("diffthis")
vim.cmd("diffupdate")
assert(vim.fn.diff_hlID(2, 9) > 0, "Changed word must have a native diff highlight")
vim.cmd("diffoff!")
vim.fn.setreg("/", "value")
vim.opt.hlsearch = true
assert(vim.fn.searchcount({ recompute = true }).total == 3)
vim.cmd("normal! ggVj")
assert(vim.fn.mode() == "V")
api.nvim_feedkeys(api.nvim_replace_termcodes("<Esc>", true, false, true), "nx", false)
-- complete() must run in Insert mode. Query its real item list before Escape.
_G.fmind_complete = function()
  vim.fn.complete(1, { "value", "variable", "variant" })
  assert(#vim.fn.complete_info({ "items" }).items == 3)
end
api.nvim_feedkeys(api.nvim_replace_termcodes("i<Cmd>lua fmind_complete()<CR><Esc>", true, false, true), "nx", false)
local result = {}
for _, name in ipairs({
  "Normal", "NormalFloat", "FloatBorder", "DiagnosticFloatingError", "DiagnosticFloatingWarn",
  "Pmenu", "PmenuSel", "PmenuSbar", "PmenuThumb", "Visual", "Search", "CurSearch", "IncSearch",
  "DiffAdd", "DiffDelete", "DiffChange", "DiffText", "Comment", "String", "Number", "Function",
}) do
  result[name] = api.nvim_get_hl(0, { name = name, link = false })
end
vim.fn.writefile({ vim.json.encode(result) }, arg[1])
