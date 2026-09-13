-- https://neovim.io/doc/user/treesitter.html
local runtime = dofile(vim.env.FMIND_THEME_ROOT .. "/checks/runtime.lua")
vim.cmd("syntax enable")
vim.cmd("colorscheme fmind")
local input = vim.json.decode(table.concat(vim.fn.readfile(arg[1]), "\n"))
local result = {}
for _, case in ipairs(input) do
  vim.cmd.edit(vim.fn.fnameescape(runtime.root .. "/checks/samples/" .. case.file))
  local row, col
  for index, line in ipairs(vim.api.nvim_buf_get_lines(0, 0, -1, false)) do
    local start = line:find(case.text, 1, true)
    if start and (not case.line or case.line == index) then
      assert(not row, "Ambiguous sample token: " .. case.text)
      row, col = index - 1, start - 1
    end
  end
  assert(row, "Missing sample token: " .. case.text)
  local actual = {}
  if case.engine == "treesitter" then
    local parser = vim.treesitter.get_parser(0)
    parser:parse(true)
    parser:for_each_tree(function(tree)
      assert(not tree:root():has_error(), "Parse error in " .. case.file)
    end)
    vim.treesitter.start(0)
    for _, capture in ipairs(vim.treesitter.get_captures_at_pos(0, row, col)) do
      if capture.capture == case.capture then
        actual = vim.api.nvim_get_hl(0, { name = "@" .. capture.capture .. "." .. capture.lang, link = false })
      end
    end
    assert(next(actual), "No styled capture " .. case.capture .. " at " .. case.text)
    vim.treesitter.stop(0)
  else
    -- Query the actual syntax item at the token, not a named group chosen by the test.
    -- Tree-sitter disables legacy syntax when it starts; restore it for this case.
    vim.bo.syntax = vim.bo.filetype
    vim.cmd("syntax sync fromstart")
    local id = vim.fn.synIDtrans(vim.fn.synID(row + 1, col + 1, 1))
    actual = vim.api.nvim_get_hl(0, { name = vim.fn.synIDattr(id, "name"), link = false })
  end
  table.insert(result, actual)
  vim.api.nvim_buf_delete(0, { force = true })
end
vim.fn.writefile({ vim.json.encode(result) }, arg[2])
