$ErrorActionPreference = "Stop"
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
python (Join-Path $ScriptDir "install.py") --uninstall @args
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
