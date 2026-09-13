-- https://neovim.io/doc/user/treesitter.html
-- Shared by the syntax tests and captures; no personal configuration is loaded.
local root = assert(vim.env.FMIND_THEME_ROOT, "Set FMIND_THEME_ROOT to this checkout")
local cache = root .. "/.cache/syntax"
assert(vim.fn.isdirectory(cache .. "/nvim-treesitter") == 1, "Run mise run install to prepare syntax checks")
vim.opt.runtimepath:prepend(root .. "/nvim")
vim.opt.runtimepath:append(cache .. "/nvim-treesitter/runtime")
vim.opt.runtimepath:append(cache .. "/nvim-treesitter")
vim.opt.runtimepath:append(cache .. "/site")
vim.treesitter.language.register("bash", "sh")
return { root = root, cache = cache, languages = {
  "python", "yaml", "markdown", "markdown_inline", "json", "toml", "bash", "html", "css", "lua",
} }
