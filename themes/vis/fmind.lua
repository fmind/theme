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
lexers.STYLE_COMMENT = "fore:" .. lexers.colors.dark_gray
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

-- vis loads base-16 first and keeps every style a theme omits, including the derived ones.
local c = lexers.colors
lexers.STYLE_ATTRIBUTE = "fore:" .. c.purple
lexers.STYLE_HEADING = "fore:" .. c.dark_blue .. ",bold"
lexers.STYLE_LABEL = "fore:" .. c.dark_blue
lexers.STYLE_PREPROCESSOR = "fore:" .. c.purple
lexers.STYLE_TAG = "fore:" .. c.dark_blue .. ",bold"
lexers.STYLE_EMBEDDED = "back:" .. c.panel
lexers.STYLE_LINENUMBER_CURSOR = "fore:" .. c.black .. ",back:" .. c.white .. ",bold"
lexers.STYLE_COLOR_COLUMN = "back:" .. c.panel
lexers.STYLE_SEPARATOR = lexers.STYLE_DEFAULT
lexers.STYLE_INFO = "fore:" .. c.dark_blue .. ",bold"
lexers.STYLE_EOF = "fore:" .. c.dark_gray
lexers.STYLE_ADDITION = "fore:" .. c.dark_green .. ",back:" .. c.pale_green
lexers.STYLE_DELETION = "fore:" .. c.dark_red .. ",back:" .. c.pale_red
lexers.STYLE_CHANGE = "fore:" .. c.dark_orange .. ",back:" .. c.pale_yellow
lexers.STYLE_PROPERTY = lexers.STYLE_ATTRIBUTE
lexers.STYLE_TAG_UNKNOWN = lexers.STYLE_TAG .. ",italics"
lexers.STYLE_TAG_SINGLE = lexers.STYLE_TAG
lexers.STYLE_TAG_DOCTYPE = lexers.STYLE_TAG
lexers.STYLE_ATTRIBUTE_UNKNOWN = lexers.STYLE_ATTRIBUTE .. ",italics"
lexers.STYLE_COMMAND = lexers.STYLE_KEYWORD
lexers.STYLE_COMMAND_SECTION = lexers.STYLE_CLASS
lexers.STYLE_ENVIRONMENT = lexers.STYLE_TYPE
lexers.STYLE_ENVIRONMENT_MATH = lexers.STYLE_NUMBER
for i = 1, 6 do
	lexers["STYLE_HEADING_H" .. i] = lexers.STYLE_HEADING
end
lexers.STYLE_LIST = lexers.STYLE_KEYWORD
lexers.STYLE_LINK = "fore:" .. c.dark_blue .. ",underlined"
lexers.STYLE_REFERENCE = lexers.STYLE_LINK
lexers.STYLE_CODE = "fore:" .. c.black .. ",back:" .. c.panel
