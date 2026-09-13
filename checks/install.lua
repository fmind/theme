-- https://github.com/nvim-treesitter/nvim-treesitter#installation
local runtime = dofile(vim.env.FMIND_THEME_ROOT .. "/checks/runtime.lua")
local ts = require("nvim-treesitter")
ts.setup({ install_dir = runtime.cache .. "/site" })
assert(ts.install(runtime.languages):wait(300000), "Parser installation failed; inspect the installer output")
assert(ts.update(runtime.languages):wait(300000), "Parser revision update failed; inspect the installer output")
-- The installer can log a failed build without raising. Require actual parsers and queries.
for _, lang in ipairs(runtime.languages) do
  -- Load the file just installed; runtime discovery can cache a missing parser directory.
  assert(vim.treesitter.language.add(lang, { path = runtime.cache .. "/site/parser/" .. lang .. ".so" }))
  assert(vim.treesitter.query.get(lang, "highlights"), "Missing highlight query for " .. lang)
end
print("Pinned syntax runtime ready")
