# Fmind PowerShell ISE theme
# https://learn.microsoft.com/powershell/scripting/windows-powershell/ise/object-model/the-iseoptions-object
$psISE.Options.ConsolePaneBackgroundColor = '#ffffff'
$psISE.Options.ConsolePaneTextBackgroundColor = '#ffffff'
$psISE.Options.ConsolePaneForegroundColor = '#202124'
$psISE.Options.ScriptPaneBackgroundColor = '#ffffff'
$psISE.Options.ScriptPaneForegroundColor = '#202124'
$psISE.Options.ErrorForegroundColor = '#a50e0e'
$psISE.Options.WarningForegroundColor = '#934900'
$psISE.Options.VerboseForegroundColor = '#00636d'
$psISE.Options.DebugForegroundColor = '#595d62'

# Set every token type in both panes: the console defaults are pale colors meant for a navy background.
# Run in a child scope so dot-sourcing from the profile leaves no variables behind.
& {
    $tokenColors = [ordered]@{
        Attribute          = '#681da8'
        Command            = '#174ea6'
        CommandArgument    = '#202124'
        CommandParameter   = '#934900'
        Comment            = '#595d62'
        GroupEnd           = '#202124'
        GroupStart         = '#202124'
        Keyword            = '#174ea6'
        LineContinuation   = '#202124'
        LoopLabel          = '#202124'
        Member             = '#202124'
        NewLine            = '#202124'
        Number             = '#934900'
        Operator           = '#202124'
        Position           = '#202124'
        StatementSeparator = '#202124'
        String             = '#0d652d'
        Type               = '#681da8'
        Unknown            = '#202124'
        Variable           = '#202124'
    }
    foreach ($token in $tokenColors.GetEnumerator()) {
        $psISE.Options.TokenColors[$token.Key] = $token.Value
        $psISE.Options.ConsoleTokenColors[$token.Key] = $token.Value
    }
}
