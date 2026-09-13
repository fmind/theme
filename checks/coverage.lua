-- https://neovim.io/doc/user/treesitter.html
-- Check real resolved defaults, including captures not exercised by sample tokens.
local runtime = dofile(vim.env.FMIND_THEME_ROOT .. "/checks/runtime.lua")
vim.cmd("colorscheme fmind")
local allowed = {}
for _, color in ipairs({ 0x202124, 0x681da8, 0x00636d, 0x0d652d, 0x934900, 0x174ea6, 0xa50e0e, 0x595d62 }) do
  allowed[color] = true
end
local function check(name)
  local style = vim.api.nvim_get_hl(0, { name = name, link = false })
  assert(allowed[style.fg], "Unstyled or foreign foreground: " .. name .. " " .. vim.inspect(style))
  assert(not style.italic, "Unexpected italic: " .. name)
end
local standard = vim.fn.readfile(vim.env.VIMRUNTIME .. "/doc/treesitter.txt")
local seen = {}
for _, line in ipairs(standard) do
  local capture = line:match("^(@[%w_.]+)%s+")
  if capture and not seen[capture] then check(capture); seen[capture] = true end
end
for _, lang in ipairs(runtime.languages) do
  local query = assert(vim.treesitter.query.get(lang, "highlights"))
  for _, capture in ipairs(query.captures) do
    if capture ~= "spell" and capture ~= "nospell" and capture:sub(1, 1) ~= "_" and capture ~= "none" then
      check("@" .. capture .. "." .. lang)
    end
  end
end
local normal = vim.api.nvim_get_hl(0, { name = "Normal" })
local cursorline = vim.api.nvim_get_hl(0, { name = "CursorLine" })
assert(normal.bg ~= cursorline.bg, "Cursor line blends into the background")
assert(vim.api.nvim_get_hl(0, { name = "PmenuThumb" }).bg ~= vim.api.nvim_get_hl(0, { name = "PmenuSbar" }).bg,
  "Scrollbar thumb is invisible")
for token in ("namespace type class enum interface struct typeParameter parameter variable property enumMember event "
  .. "function method macro keyword modifier comment string number regexp operator decorator"):gmatch("%S+") do
  check("@lsp.type." .. token)
end
local lualine = dofile(runtime.root .. "/lualine/fmind.lua")
local function luminance(color)
  local value = type(color) == "number" and color or tonumber(color:sub(2), 16)
  local total = 0
  for i, weight in ipairs({ 0.2126, 0.7152, 0.0722 }) do
    local channel = math.floor(value / 256 ^ (3 - i)) % 256 / 255
    total = total + weight * (channel <= 0.04045 and channel / 12.92 or ((channel + 0.055) / 1.055) ^ 2.4)
  end
  return total
end
local function check_label(name, style)
  local fg, bg = luminance(style.fg), luminance(style.bg)
  assert((math.max(fg, bg) + 0.05) / (math.min(fg, bg) + 0.05) >= 4.5, "Unreadable filled label: " .. name)
end
for _, name in ipairs({ "Search", "IncSearch", "CurSearch", "Substitute", "Cursor", "TabLineSel",
  "Todo", "TodoBgFIX", "TodoBgTODO", "TodoBgHACK", "TodoBgWARN", "TodoBgPERF", "DiffText" }) do
  check_label(name, vim.api.nvim_get_hl(0, { name = name, link = false }))
end
assert(vim.api.nvim_get_hl(0, { name = "DiffText" }).bg ~= vim.api.nvim_get_hl(0, { name = "DiffChange" }).bg,
  "Changed words blend into their diff line")
for _, mode in ipairs({ "normal", "insert", "visual", "replace", "command", "terminal", "inactive" }) do
  assert(lualine[mode] and lualine[mode].a.fg and lualine[mode].a.bg, "Missing statusline mode: " .. mode)
  for section, style in pairs(lualine[mode]) do check_label(mode .. "." .. section, style) end
end

-- Syntax survives selection and diff backgrounds; membership alone cannot prove this.
for _, name in ipairs({ "Normal", "Comment", "String", "Number", "Function", "Keyword", "Type",
  "Error", "LineNr", "DiagnosticError", "DiagnosticWarn", "DiagnosticInfo" }) do
  local foreground = vim.api.nvim_get_hl(0, { name = name, link = false }).fg
  for _, surface in ipairs({ "Normal", "CursorLine", "Visual", "DiffAdd", "DiffDelete", "DiffChange" }) do
    check_label(name .. " on " .. surface, {
      fg = foreground, bg = vim.api.nvim_get_hl(0, { name = surface, link = false }).bg,
    })
  end
end
assert(vim.api.nvim_get_hl(0, { name = "MiniIconsBlue" }).fg == 0x174ea6, "Blue icons lost their hue")
