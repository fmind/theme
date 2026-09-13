# https://learn.microsoft.com/powershell/module/psreadline/set-psreadlineoption
# PowerShell 7 and PSReadLine 2.2+; use the matching terminal ANSI palette.
#requires -Version 7.0
#requires -Modules @{ ModuleName = 'PSReadLine'; ModuleVersion = '2.2.0' }
Set-PSReadLineOption -Colors @{
    Default = "`e[38;2;32;33;36m"
    Comment = "`e[38;2;89;93;98m"
    Keyword = "`e[38;2;23;78;166m"
    String = "`e[38;2;13;101;45m"
    Operator = "`e[38;2;32;33;36m"
    Variable = "`e[38;2;32;33;36m"
    Command = "`e[38;2;23;78;166m"
    Parameter = "`e[38;2;147;73;0m"
    Type = "`e[38;2;104;29;168m"
    Number = "`e[38;2;147;73;0m"
    Member = "`e[38;2;32;33;36m"
    Error = "`e[38;2;165;14;14m"
    Emphasis = "`e[38;2;23;78;166m"
    ContinuationPrompt = "`e[38;2;0;99;109m"
    Selection = "`e[38;2;32;33;36;48;2;210;227;252m"
    InlinePrediction = "`e[38;2;89;93;98m"
    ListPrediction = "`e[38;2;89;93;98m"
    ListPredictionSelected = "`e[38;2;32;33;36;48;2;210;227;252m"
}
