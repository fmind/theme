-- https://github.com/nvim-lualine/lualine.nvim#customizing-themes
--
-- Drop into lua/lualine/themes/ under the Neovim config directory. lualine's
-- `auto` theme loads this by vim.g.colors_name before it derives anything,
-- so nothing has to be configured for it to take effect.

local ground = {
  panel = "#f1f3f4",
}

return {
  normal = {
    a = { bg = "#4285f4", fg = "#202124", gui = 'bold' },
    b = { bg = ground.panel, fg = "#202124" },
    c = { bg = ground.panel, fg = "#202124" },
  },
  insert = {
    a = { bg = "#34a853", fg = "#202124", gui = 'bold' },
    b = { bg = ground.panel, fg = "#202124" },
    c = { bg = ground.panel, fg = "#202124" },
  },
  visual = {
    a = { bg = "#fbbc04", fg = "#202124", gui = 'bold' },
    b = { bg = ground.panel, fg = "#202124" },
    c = { bg = ground.panel, fg = "#202124" },
  },
  replace = {
    a = { bg = "#a50e0e", fg = "#ffffff", gui = 'bold' },
    b = { bg = ground.panel, fg = "#202124" },
    c = { bg = ground.panel, fg = "#202124" },
  },
  command = {
    a = { bg = "#e37400", fg = "#202124", gui = 'bold' },
    b = { bg = ground.panel, fg = "#202124" },
    c = { bg = ground.panel, fg = "#202124" },
  },
  terminal = {
    a = { bg = "#4285f4", fg = "#202124", gui = 'bold' },
    b = { bg = ground.panel, fg = "#202124" },
    c = { bg = ground.panel, fg = "#202124" },
  },
  inactive = {
    a = { bg = ground.panel, fg = "#202124", gui = 'bold' },
    b = { bg = ground.panel, fg = "#202124" },
    c = { bg = ground.panel, fg = "#202124" },
  },
}
