# SPDX-License-Identifier: MPL-2.0
<#
  run_service.ps1 — PowerShell twin of run_service.py.

  Start/stop/status a dev server by tracked PID+port.

  Why this twin matters more than most: the rule it enforces is "never bulk-kill
  by image name". `Get-Process node | Stop-Process` also kills the MCP servers the
  agent itself depends on. A PowerShell-only machine with no twin here has no tool
  that does it safely, so the temptation is exactly the command that breaks things.

  Ownership: a PID alone does not identify a process. The OS-reported start time is
  recorded alongside it and compared before anything is signalled, so a reused PID
  gets a refusal instead of a kill.

  Windows PowerShell 5.1 compatible: no &&, no ??, no ternary, no -Parallel.

  Exit codes: 0 ok; 1 usage/IO error; 2 stop could not confirm the port is free.
#>
param(
    [Parameter(Mandatory = $true, Position = 0)][string]$Command,
    [string]$Name = "",
    [int]$Port = 0,
    [string]$Cwd = "",
    # The command to start, as ONE comma-separated string:
    #     -CommandArgs "dotnet,run,--project,src/App"
    #
    # A single string, and split here rather than by PowerShell. Two reasons, both
    # found by testing rather than by reading:
    #
    # PowerShell's binder claims any token that looks like a parameter before this
    # script sees it. `-- python -c ...` does not survive `pwsh -File`: the `--` is
    # consumed, then `-c` is matched against -Command/-Cwd and rejected as
    # ambiguous. `dotnet run --project x` hits the same wall, so this is not an
    # artefact of one test.
    #
    # And declaring [string[]] does not help, because comma splitting is done by
    # PowerShell's *command-line parser*. Arguments arriving from an external argv
    # -- which is how a hook, a CI job or another script invokes this -- are passed
    # through literally, commas and all. So the split has to happen in here.
    #
    # A command argument containing a literal comma cannot be expressed this way;
    # pass it through the trailing arguments instead, which works whenever no
    # argument starts with a dash. The .py twin keeps its idiomatic `-- <command>`.
    # tools/run-managed-service/README.md states both.
    [string]$CommandArgs = "",
    [Parameter(ValueFromRemainingArguments = $true)][string[]]$Rest = @()
)

$ErrorActionPreference = "Stop"

$StatePath = ".agent-state/services.json"

# ---------------------------------------------------------------------------
function Get-State {
    if (-not (Test-Path -LiteralPath $StatePath -PathType Leaf)) { return @{} }
    try {
        $parsed = [System.IO.File]::ReadAllText($StatePath) | ConvertFrom-Json
    } catch {
        return @{}
    }
    if ($null -eq $parsed) { return @{} }
    # ConvertFrom-Json yields a PSCustomObject; an ordered hashtable keeps the
    # insertion order the Python dict has, so `stop` with no name visits the
    # services in the same sequence.
    $data = [ordered]@{}
    foreach ($property in $parsed.PSObject.Properties) { $data[$property.Name] = $property.Value }
    return $data
}

function Save-State {
    param($Data)
    $directory = [System.IO.Path]::GetDirectoryName(
        [System.IO.Path]::GetFullPath([System.IO.Path]::Combine((Get-Location).Path, $StatePath)))
    if ($directory -and -not (Test-Path -LiteralPath $directory)) {
        # [System.IO.Directory]::CreateDirectory, not New-Item: New-Item has no
        # -LiteralPath parameter at all (only -Path, which expands wildcards), so a
        # path containing [ ] * ? cannot be created safely through it. The .NET call
        # is literal by definition and creates intermediate directories.
        [void][System.IO.Directory]::CreateDirectory($directory)
    }
    if ($Data.Count -eq 0) {
        [System.IO.File]::WriteAllText($StatePath, "{}`n")
        return
    }
    [System.IO.File]::WriteAllText($StatePath, (ConvertTo-Json $Data -Depth 6) + "`n")
}

function Test-PortListening {
    param([int]$PortNumber)
    $client = New-Object System.Net.Sockets.TcpClient
    try {
        $async = $client.BeginConnect("127.0.0.1", $PortNumber, $null, $null)
        if (-not $async.AsyncWaitHandle.WaitOne(400)) { return $false }
        $client.EndConnect($async)
        return $true
    } catch {
        return $false
    } finally {
        $client.Close()
    }
}


function Get-ProcessStartToken {
    # An OS-reported identity for a running process, or "" if it is gone.
    #
    # Liveness alone is not enough: PIDs are reused, so a stale record plus an
    # unlucky reuse means this tool signals something it never started -- the exact
    # collateral damage it exists to prevent, just smaller and harder to notice
    # than a bulk kill.
    #
    # The token is the kernel's own start time, never a timestamp this tool took.
    # A local timestamp would drift from the kernel's and force a tolerance
    # window, and a tolerance window is a hole.
    #
    # The two twins read the same fact from the same place per platform: on Linux
    # /proc/<pid>/stat field 22, on Windows the process StartTime. Reading /proc
    # here rather than using Get-Process on Linux is deliberate -- Get-Process
    # StartTime is a .NET-computed wall-clock value there, and the .py twin reads
    # the raw tick count, so the two strings would never match.
    param([int]$ProcessId)
    if ($IsWindows -or $env:OS -eq "Windows_NT") {
        try {
            return [string](Get-Process -Id $ProcessId -ErrorAction Stop).StartTime.Ticks
        } catch {
            return ""
        }
    }
    $statPath = "/proc/$ProcessId/stat"
    if (-not (Test-Path -LiteralPath $statPath)) { return "" }
    try {
        $content = [System.IO.File]::ReadAllText($statPath)
    } catch {
        return ""
    }
    # The comm field can contain spaces and parentheses, so split after the last
    # ')' rather than on whitespace from the start.
    $index = $content.LastIndexOf(")")
    if ($index -lt 0) { return "" }
    $tail = @($content.Substring($index + 1).Split(" ", [System.StringSplitOptions]::RemoveEmptyEntries))
    if ($tail.Count -lt 20) { return "" }
    return $tail[19]
}

function Test-Ownership {
    # Returns @{ mine = <bool>; reason = <string> }.
    #
    # A record written before ownership tokens existed has no token to compare.
    # Refusing on that basis would strand anyone upgrading mid-session, so it is
    # accepted with the reason stated -- an explicit, visible gap, not a silent one.
    param($Entry, [int]$ProcessId)
    $recorded = ""
    if ($null -ne $Entry.start_token) { $recorded = [string]$Entry.start_token }
    if (-not $recorded) {
        return @{ mine = $true; reason = "record predates ownership tokens; identity unverified" }
    }
    $current = Get-ProcessStartToken $ProcessId
    if (-not $current) { return @{ mine = $false; reason = "process is gone" } }
    if ($current -ne $recorded) {
        return @{ mine = $false; reason = "start token $current does not match the recorded $recorded" }
    }
    return @{ mine = $true; reason = "" }
}

function Test-PidAlive {
    # Asked by PID, never by image name. A recorded PID whose process is gone must
    # not be signalled: the number may have been reused by something unrelated,
    # and this tool exists precisely so a stale record cannot become collateral
    # damage.
    #
    # Liveness is necessary but not sufficient; Test-Ownership answers identity.
    param([int]$ProcessId)
    try {
        $process = Get-Process -Id $ProcessId -ErrorAction Stop
        return ($null -ne $process)
    } catch {
        return $false
    }
}

function Stop-PidTree {
    # Terminate only this PID and its children — never by image name.
    param([int]$ProcessId)
    $previous = $ErrorActionPreference
    $ErrorActionPreference = "Continue"
    if ($IsWindows -or $env:OS -eq "Windows_NT") {
        & taskkill /PID $ProcessId /T /F 2>$null | Out-Null
    } else {
        # Children first, so a parent cannot re-parent them away mid-kill.
        $children = @()
        try {
            $children = @(& pgrep -P $ProcessId 2>$null)
        } catch {
            $children = @()
        }
        foreach ($child in $children) {
            if ($child -match '^\d+$') { & kill -TERM $child 2>$null | Out-Null }
        }
        & kill -TERM $ProcessId 2>$null | Out-Null
        Start-Sleep -Milliseconds 1000
        foreach ($child in $children) {
            if ($child -match '^\d+$') { & kill -KILL $child 2>$null | Out-Null }
        }
        & kill -KILL $ProcessId 2>$null | Out-Null
    }
    $ErrorActionPreference = $previous
}

function Stop-One {
    # Every message here goes to the console directly, never through Write-Output.
    # A PowerShell function returns its whole pipeline, so `Write-Output` inside a
    # function that also returns an exit code makes the message *part of the
    # return value*: the caller receives @("...", 0), the text never reaches the
    # console, and the identifier vanishes from the output. That is how the one
    # invariant this tool exists to hold -- "an untracked name is refused, not
    # widened into an image-name sweep" -- became unobservable from outside.
    param($Data, [string]$ServiceName)
    if (-not $Data.Contains($ServiceName)) {
        # The refusal is the feature. There is no fallback that widens this into
        # an image-name sweep, and there must never be one.
        [Console]::Out.WriteLine("[run-managed-service:untracked-service] no tracked service '" +
                      $ServiceName + "'; not widening the search")
        return 0
    }
    $entry = $Data[$ServiceName]
    $processId = [int]$entry.pid
    if (-not (Test-PidAlive $processId)) {
        [Console]::Out.WriteLine("[run-managed-service:pid-not-alive] tracked pid " + $processId +
                      " for '" + $ServiceName + "' is gone; nothing signalled")
    } else {
        $ownership = Test-Ownership $entry $processId
        if (-not $ownership.mine) {
            # Refuse, and keep the record. Dropping it would make the next run
            # report "not tracked" and look clean, hiding the fact that something
            # was never stopped. Exit 2 for the same reason the port check uses it:
            # this tool could not confirm it did its job.
            [Console]::Error.WriteLine("[run-managed-service:pid-owner-mismatch] pid " + $processId +
                " recorded for '" + $ServiceName + "' is not the process this tool started (" +
                $ownership.reason + "); refusing to signal it. Stop it yourself, or remove the " +
                "entry from .agent-state/services.json.")
            return 2
        }
        if ($ownership.reason) {
            [Console]::Out.WriteLine("[run-managed-service:ownership-unverified] " + $ServiceName +
                ": " + $ownership.reason)
        }
        Stop-PidTree $processId
    }

    $portNumber = 0
    if ($null -ne $entry.port) { $portNumber = [int]$entry.port }
    $ok = $true
    if ($portNumber -ne 0) {
        $ok = $false
        for ($attempt = 0; $attempt -lt 10; $attempt++) {
            if (-not (Test-PortListening $portNumber)) { $ok = $true; break }
            Start-Sleep -Milliseconds 300
        }
    }
    $Data.Remove($ServiceName)
    Save-State $Data
    if ($portNumber -ne 0 -and -not $ok) {
        [Console]::Error.WriteLine("[run-managed-service:port-still-listening] stopped pid " +
            $processId + " but port " + $portNumber + " still LISTENING - check manually")
        return 2
    }
    $suffix = ""
    if ($portNumber -ne 0) { $suffix = "; port " + $portNumber + " free (confirmed)" }
    [Console]::Out.WriteLine("stopped '" + $ServiceName + "' (pid " + $processId + ")" + $suffix)
    return 0
}

# ---------------------------------------------------------------------------
try {
    $data = Get-State

    if ($Command -eq "start") {
        # -CommandArgs when given; otherwise the trailing arguments, which work
        # for any command with no dash-prefixed token in it.
        if ($CommandArgs) {
            $commandParts = @($CommandArgs.Split(",", [System.StringSplitOptions]::RemoveEmptyEntries))
        } else {
            $commandParts = @($Rest)
        }
        # A leading `--` separator is accepted and dropped, matching the .py twin.
        if ($commandParts.Count -gt 0 -and $commandParts[0] -eq "--") {
            $commandParts = @($commandParts[1..($commandParts.Count - 1)])
        }
        if ($commandParts.Count -eq 0) {
            [Console]::Error.WriteLine("[run-managed-service:command-missing] start requires a command: -CommandArgs npm,run,dev")
            exit 1
        }
        if ($data.Contains($Name)) { [void](Stop-One $data $Name) ; $data = Get-State }

        $startInfo = New-Object System.Diagnostics.ProcessStartInfo
        $startInfo.FileName = $commandParts[0]
        if ($commandParts.Count -gt 1) {
            foreach ($argument in $commandParts[1..($commandParts.Count - 1)]) {
                [void]$startInfo.ArgumentList.Add($argument)
            }
        }
        if ($Cwd) { $startInfo.WorkingDirectory = $Cwd }
        $startInfo.UseShellExecute = $false
        $process = [System.Diagnostics.Process]::Start($startInfo)

        $epoch = [System.DateTime]::UtcNow.Subtract([datetime]"1970-01-01T00:00:00Z").TotalSeconds
        # Ask the OS for the child's start time immediately, rather than storing
        # the local clock: the comparison at stop time is then exact, with no
        # tolerance window to be wrong about.
        $data[$Name] = [ordered]@{
            pid = $process.Id
            port = $Port
            cmd = $commandParts
            cwd = $Cwd
            started = $epoch
            start_token = (Get-ProcessStartToken $process.Id)
        }
        Save-State $data
        Write-Output ("started '" + $Name + "' pid=" + $process.Id + " port=" + $Port +
                      " :: " + ($commandParts -join " "))
        exit 0
    }

    if ($Command -eq "stop") {
        if ($Name) { exit (Stop-One $data $Name) }
        $code = 0
        foreach ($serviceName in @($data.Keys)) {
            $result = Stop-One $data $serviceName
            if ($result -ne 0) { $code = $result }
        }
        exit $code
    }

    if ($Command -eq "status") {
        $names = @()
        if ($Name) { $names = @($Name) } else { $names = @($data.Keys) }
        if ($names.Count -eq 0) {
            Write-Output "no tracked services"
            exit 0
        }
        foreach ($serviceName in $names) {
            if (-not $data.Contains($serviceName)) {
                Write-Output ("[run-managed-service:untracked-service] " + $serviceName + ": not tracked")
                continue
            }
            $entry = $data[$serviceName]
            $portNumber = 0
            if ($null -ne $entry.port) { $portNumber = [int]$entry.port }
            $state = "free/unknown"
            if ($portNumber -ne 0 -and (Test-PortListening $portNumber)) { $state = "LISTENING" }
            $portLabel = "-"
            if ($portNumber -ne 0) { $portLabel = [string]$portNumber }
            Write-Output ($serviceName + ": pid=" + $entry.pid + " port=" + $portLabel + " -> " + $state)
        }
        exit 0
    }

    # Exit 1 and no identifier, matching the .py twin. argparse used to exit 2 on
    # a usage error, which under this kit's convention means "validation failure"
    # and made a typo on the command line indistinguishable from a real finding;
    # tools/_lib/kit_cli.py remaps it to 1 kit-wide. PowerShell's own binder
    # already exits 1 when a parameter does not bind, so the two now agree here
    # without either side pretending.
    [Console]::Error.WriteLine("usage: run_service.ps1 {start,stop,status} [-Name n] [-Port p] [-Cwd d] [-CommandArgs a,b,c]")
    [Console]::Error.WriteLine("run_service.ps1: error: invalid choice: '$Command'")
    exit 1
}
catch {
    [Console]::Error.WriteLine("ERROR: $($_.Exception.Message)")
    exit 1
}
