
Function f_WaitForIt {
	Param ([Parameter(Mandatory=$False)] [string]$WaitText = 'Press any key to continue...')
	Write-Host -NoNewLine $WaitText;
	$null = $Host.UI.RawUI.ReadKey('NoEcho,IncludeKeyDown');
}

Function f_WriteEvent {
	Param (
		[Parameter(Mandatory=$False)] [string]$Message,
		[Parameter(Mandatory=$False)] [string]$LogPath = "E:Debug\",
		[Parameter(Mandatory=$False)] [string]$error = 'No Error'
	)
	$timestamp = Get-Date
	$CallStackFrame = Get-PSCallStack
	"$CallStackFrame.InvocationInfo.MyCommand[1].Name - $timestamp`: $Message" |Out-File -Append -FilePath "$LogPath"
	if ($error -ne 'No Error'){"	$error" |Out-File -Append -FilePath "$LogPath"}
}

Function f_VariableCheck {
	$var = "test1`ttest2"
	$var | Out-Host
}

Function f_CallFromElevated {
	Param (
		[Parameter(Mandatory=$False)] [string]$script = "CallParent"
	)
	if ($script -eq "CallParent"){
		$CallStackFrame = Get-PSCallStack
		$script = $CallStackFrame.InvocationInfo.MyCommand[1].Source
	}
	
	# Get the ID and security principal of the current user account
	$myWindowsID=[System.Security.Principal.WindowsIdentity]::GetCurrent()
	$myWindowsPrincipal=new-object System.Security.Principal.WindowsPrincipal($myWindowsID)
	 
	# Get the security principal for the Administrator role
	$adminRole=[System.Security.Principal.WindowsBuiltInRole]::Administrator
	 
	# Check to see if we are currently running "as Administrator"
	if ($myWindowsPrincipal.IsInRole($adminRole)){
	   # We are running "as Administrator" - so change the title and background color to indicate this
	   $Host.UI.RawUI.WindowTitle = $myInvocation.MyCommand.Definition + "(Elevated)"
	   $Host.UI.RawUI.BackgroundColor = "DarkBlue"
	   clear-host
	}
	else{
	   # We are not running "as Administrator" - so relaunch as administrator
	   # Create a new process object that starts PowerShell
	   $newProcess = new-object System.Diagnostics.ProcessStartInfo "PowerShell";
	   # Specify the current script path and name as a parameter
	   $newProcess.Arguments = $script;
	   # Indicate that the process should be elevated
	   $newProcess.Verb = "runas";
	   # Start the new process
	   [System.Diagnostics.Process]::Start($newProcess);
	   # Exit from the current, unelevated, process
	   exit
	}
	
}

Function f_DeleteSubItems {
    Param ([Parameter(Mandatory=$False)][string]$Path)
    Get-ChildItem $Path | %($_){$Loc=$_.FullName; Remove-Item -Path "$Loc\*"}
}

Function f_CompareFolders {
	Param (
		[Parameter(Mandatory=$True,position=1)] [string]$Folder1,
		[Parameter(Mandatory=$False)] [string]$Folder2,
		[Parameter(Mandatory=$False)] [string]$LogPath
	)
	$Hashes=""	
	$DNEitems=""
	#Recieve 2 folders
	function ff_CompareFolders($F1 = $Folder1, $F2 = $Folder2) {
		foreach ($item in Get-ChildItem $F1){
			#check if item name exists in folder2
			"$F2\$item.Name"
			If (Test-Path "$F2\$item.Name"){
				$message = "$Item.Name found in both locations"			
				#check if item is leaf
				If (Test-Path $item.FullName -PathType Leaf){
					$F1_Hash = Get-FileHash $item.FullName
					$F2_Hash = Get-FileHash $F2\$item.Name
					$Hashes = $Hashes, "$F1_Hash.Hash"
					If ($F1_Hash.Hash -eq $F2_Hash.Hash){$message = $message + " and the Hashes match"
					} else {$message = $message + ", but the Hashes don't match"}
				}
				else{
					ff_CompareFolders -Folder1 $item.FullName -Folder1 $F2\$item.Name
				}
			}
			else {
				$message = "$Item.Name not found in $F2"
				$DNEitems = $DNEitems, "$Item.FullName"
			}
		$message
		}
	}
	If (!$LogPath) {ff_CompareFolders | Out-File $LogPath} else {ff_CompareFolders | Out-Host}
	$temp=$Folder1; $Folder1=$Folder2; $Folder2=$temp
	If (!$LogPath) {ff_CompareFolders | Out-File $LogPath} else {ff_CompareFolders | Out-Host}
}
<#

passing arrays to next function (reset scope?)
adding in check for duplicate hashes
adding in reverse function call for files existing in folder 2 but not in folder 1. call at the end again

#>

Function f_NewOpen {
	Param (
		[Parameter(Mandatory=$False)][string]$Path=".\",
		[Parameter(Mandatory=$True,position=1)][string]$Name,
		[Parameter(Mandatory=$False)][string]$Value=""
	)
	If (-Not (Test-Path "$Path\$Name")){
		New-Item -Path $Path -Name "$Name" -Value $Value -ItemType file -force
	}
	start notepad++ "$Path\$Name"
}

Function f_DriveLetter {
	Param ([Parameter(Mandatory=$False)][string]$DriveName)
	$disks = get-disk | where BusType -eq USB | get-partition | get-volume
	if ($disks[1]){
		ForEach ($disk in $disks) {If ($disk.FileSystemLabel.ToUpper() -like "*$($DriveName.ToUpper())*") {$PickedDrive = $disk.DriveLetter}}
	} else {$PickedDrive = $disks.DriveLetter}
	return $PickedDrive
}









