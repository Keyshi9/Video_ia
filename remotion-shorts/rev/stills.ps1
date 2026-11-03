param([string]$frames)
cd C:\Users\pu99cle\remotion-shorts
$env:REMOTION_TMP='C:\Users\pu99cle\remotion-tmp'
foreach($f in $frames.Split(',')){ npx remotion still Revolution out/r$f.png --frame=$f --gl=angle --scale=0.5 --timeout=180000 2>&1 | Select-String "rror|Rendered 1/1" | Select-Object -First 4 }
