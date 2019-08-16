#Not My Original Source Code!
#Modified by David Toft for use with VMWare OVF Exports

param(
	[Parameter(Mandatory=$true)][string]$path,
	[Parameter(Mandatory=$false)][string]$chunkSize=2147000000
)


function f_split
{
    $fileName = [System.IO.Path]::GetFileNameWithoutExtension($path)
    $directory = [System.IO.Path]::GetDirectoryName($path)
    $extension = [System.IO.Path]::GetExtension($path)

    $file = New-Object System.IO.FileInfo($path)
    $totalChunks = [int]($file.Length / $chunkSize) + 1
    $digitCount = [int][System.Math]::Log10($totalChunks) + 1

    $reader = [System.IO.File]::OpenRead($path)
    $count = 0
    $buffer = New-Object Byte[] $chunkSize
    $hasMore = $true
    while($hasMore)
    {
        $bytesRead = $reader.Read($buffer, 0, $buffer.Length)
        $chunkFileName = "$directory\$fileName$extension.{0:D$digitCount}.part"
        $chunkFileName = $chunkFileName -f $count
        $output = $buffer
        if ($bytesRead -ne $buffer.Length)
        {
            $hasMore = $false
            $output = New-Object Byte[] $bytesRead
            [System.Array]::Copy($buffer, $output, $bytesRead)
        }
        [System.IO.File]::WriteAllBytes($chunkFileName, $output)
        ++$count
    }

    $reader.Close()
}

#split "C:\path\to\file"

function f_join
{
    $files = Get-ChildItem -Path "$path.*.part" | Sort-Object -Property @{Expression={
        $shortName = [System.IO.Path]::GetFileNameWithoutExtension($_.Name)
        $extension = [System.IO.Path]::GetExtension($shortName)
        if ($extension -ne $null -and $extension -ne '')
        {
            $extension = $extension.Substring(1)
        }
        [System.Convert]::ToInt32($extension)
    }}
    $writer = [System.IO.File]::OpenWrite($path)
    foreach ($file in $files)
    {
        $bytes = [System.IO.File]::ReadAllBytes($file)
        $writer.Write($bytes, 0, $bytes.Length)
    }
    $writer.Close()
}

#join "C:\path\to\file"

Function f_deleteQuitLoop ($found){
	$answer = Read-Host "$(split-path $found -leaf) found at: `n$(split-path $found) `nDo you want to delete this file? [Yes/No]"
	If ($answer.ToUpper() -eq "NO") {Exit}
	If ($answer.ToUpper() -eq "YES") {Remove-Item -Path "$found"}
	Else {Return}
}

#Script Start#

If (Test-Path "$path.*.part"){
	While (Test-Path "$path"){f_deleteQuitLoop($path)}
	f_join
}
else {
	f_split
}