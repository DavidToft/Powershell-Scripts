$Depth=255
$FileTypes = @(".log", ".txt")
$Paths = @{
	'Full Directory Path' = "Description"; 
	'D:\VMs'="Development VMs"; 
}
Function FolderSearch($Path, [Byte]$ToDepth = $Depth, [Byte]$CurrentDepth = 0){
	$CurrentDepth++
	If ($CurrentDepth -le $ToDepth) {
		foreach ($item in Get-ChildItem $Path){
			if (Test-Path $item.FullName -PathType Container){
				FolderSearch $item.FullName -ToDepth $ToDepth -CurrentDepth $CurrentDepth
			} Else {
				ForEach ($Ext in $FileTypes){
					If ($item.Extension -like $Ext -and $item.LastWriteTime -gt $(get-date).AddDays(-1)){
						"Recently updated log file found:`n$($item.Name)"|out-host
					}
				}
			}
		}
	}
}
ForEach ($Path in $Paths.Keys){
	$Paths.$Path | Out-Host
	FolderSearch($Path) | Out-Host
}