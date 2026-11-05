param(
    [Parameter(Mandatory=$true)][string]$TextFile,
    [Parameter(Mandatory=$true)][string]$OutputWave
)
$ErrorActionPreference = 'Stop'
$text = Get-Content -LiteralPath $TextFile -Raw -Encoding UTF8
if ($text -match '\[(LIVE|ALL|FALL|MATCH|COMPARATOR|VERIFIED|TEAM-OWNED)|PENDING|TO COMPLETE') {
    throw 'Replace unverified narration placeholders before generating release audio.'
}
$destination = [System.IO.Path]::GetFullPath($OutputWave)
if ([System.IO.Path]::GetExtension($destination) -ne '.wav') { throw 'Output must be a new .wav file.' }
if (Test-Path -LiteralPath $destination) { throw 'Refusing to overwrite existing audio.' }
$voice = New-Object -ComObject SAPI.SpVoice
$stream = New-Object -ComObject SAPI.SpFileStream
try {
    $stream.Open($destination,3,$false)
    $voice.AudioOutputStream = $stream
    $voice.Rate = -1
    $voice.Speak($text) | Out-Null
} finally { $stream.Close() }
Write-Output "Narration created: $destination"
