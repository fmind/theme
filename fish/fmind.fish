# https://fishshell.com/docs/current/interactive.html#syntax-highlighting
# Syntax highlighting and prompt identity
set -g fish_color_normal 202124  # variable
set -g fish_color_command 174ea6  # function
set -g fish_color_param 202124  # parameter
set -g fish_color_option 681da8  # builtin
set -g fish_color_keyword 174ea6 --bold  # keyword
set -g fish_color_quote 0d652d  # string
set -g fish_color_escape 174ea6  # escape
set -g fish_color_redirection 681da8  # type
set -g fish_color_operator 202124  # property
set -g fish_color_end 934900 --bold  # constant
set -g fish_color_error a50e0e --bold  # error
set -g fish_color_comment 595d62  # comment
set -g fish_color_autosuggestion 595d62  # comment
set -g fish_color_cancel 934900  # warning
set -g fish_color_cwd 202124  # variable
set -g fish_color_cwd_root a50e0e --bold  # error
set -g fish_color_user 202124  # property
set -g fish_color_host 681da8  # type
set -g fish_color_host_remote 934900  # number
set -g fish_color_selection --background=d2e3fc
set -g fish_color_search_match --background=d2e3fc
set -g fish_color_valid_path --underline

# Completion pager
set -g fish_pager_color_progress 595d62
set -g fish_pager_color_prefix 681da8 --bold
set -g fish_pager_color_completion 202124
set -g fish_pager_color_description 595d62
set -g fish_pager_color_selected_background --background=d2e3fc
set -g fish_pager_color_background --background=ffffff
set -g fish_pager_color_selected_prefix 681da8 --bold
set -g fish_pager_color_selected_completion 202124
set -g fish_pager_color_selected_description 595d62
set -g fish_pager_color_secondary_background --background=f1f3f4
set -g fish_pager_color_secondary_prefix 681da8 --bold
set -g fish_pager_color_secondary_completion 202124
set -g fish_pager_color_secondary_description 595d62
