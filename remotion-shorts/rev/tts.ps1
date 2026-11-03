Add-Type -AssemblyName System.Speech
$s = New-Object System.Speech.Synthesis.SpeechSynthesizer
$s.SelectVoice("Microsoft Hortense Desktop")
$s.Rate = 2
$lines = @(
"Le quatorze juillet dix-sept cent quatre-vingt-neuf, la foule de Paris prend la Bastille.",
"Dedans : sept prisonniers. Sept.",
"Mais c'était le symbole du roi.",
"Un mois après, les privilèges sont abolis.",
"Trois ans plus tard, le roi est renversé.",
"Et la France en fait encore sa fête."
)
for ($i=0; $i -lt $lines.Count; $i++) {
  $s.SetOutputToWaveFile("$PWD\v$($i+1).wav")
  $s.Speak($lines[$i])
  $s.SetOutputToNull()
}
