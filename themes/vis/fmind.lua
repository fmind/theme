-- Fmind light theme for vis

local lexers = vis.lexers

lexers.colors = {
	["black"] = "#202124",
	["white"] = "#ffffff",
	["panel"] = "#f1f3f4",
	["dark_gray"] = "#595d62",
	["dark_blue"] = "#174ea6",
	["pale_blue"] = "#d2e3fc",
	["dark_green"] = "#0d652d",
	["pale_green"] = "#ceead6",
	["dark_red"] = "#a50e0e",
	["pale_red"] = "#fad2cf",
	["dark_orange"] = "#934900",
	["yellow"] = "#fbbc04",
	["pale_yellow"] = "#feefc3",
	["purple"] = "#681da8",
	["teal"] = "#00636d",
}

local fg = "fore:" .. lexers.colors.black .. ","
local bg = "back:" .. lexers.colors.white .. ","

lexers.STYLE_DEFAULT = fg .. bg
lexers.STYLE_NOTHING = ""
lexers.STYLE_CLASS = "fore:" .. lexers.colors.purple
lexers.STYLE_COMMENT = "fore:" .. lexers.colors.dark_gray .. ",italics"
lexers.STYLE_CONSTANT = "fore:" .. lexers.colors.dark_orange
lexers.STYLE_DEFINITION = "fore:" .. lexers.colors.dark_blue .. ",bold"
lexers.STYLE_ERROR = "fore:" .. lexers.colors.dark_red .. ",bold"
lexers.STYLE_FUNCTION = "fore:" .. lexers.colors.dark_blue
lexers.STYLE_KEYWORD = "fore:" .. lexers.colors.dark_blue .. ",bold"
lexers.STYLE_NUMBER = "fore:" .. lexers.colors.dark_orange
lexers.STYLE_OPERATOR = "fore:" .. lexers.colors.black
lexers.STYLE_REGEX = "fore:" .. lexers.colors.dark_orange
lexers.STYLE_STRING = "fore:" .. lexers.colors.dark_green
lexers.STYLE_TYPE = "fore:" .. lexers.colors.purple
lexers.STYLE_VARIABLE = "fore:" .. lexers.colors.black

lexers.STYLE_LINENUMBER = "fore:" .. lexers.colors.dark_gray .. ",back:" .. lexers.colors.white
lexers.STYLE_CURSOR = "fore:" .. lexers.colors.white .. ",back:" .. lexers.colors.dark_blue
lexers.STYLE_CURSOR_PRIMARY = "fore:" .. lexers.colors.white .. ",back:" .. lexers.colors.dark_blue
lexers.STYLE_CURSOR_LINE = "back:" .. lexers.colors.panel
lexers.STYLE_SELECTION = "back:" .. lexers.colors.pale_blue
lexers.STYLE_STATUS = "fore:" .. lexers.colors.black .. ",back:" .. lexers.colors.panel
lexers.STYLE_STATUS_FOCUSED = "fore:" .. lexers.colors.black .. ",back:" .. lexers.colors.pale_blue
