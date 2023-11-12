# Author:   Tyler Santos
# Date:     9/9/2023
# Version:  2.0
# Repo:     https://github.com/santost12/uf-abe-scripts/
# About:    This script is for Windows 11 computers to default to left aligned start menu


##
# Returns true or false if computer is running Windows 11
##
function is_win11 {
    return (Get-WmiObject Win32_OperatingSystem).Caption -match "Windows 11"
}

##
# Returns true or false if a registry value exists
##
function Test-RegistryValue {
    [CmdletBinding()]
    param (
        [Parameter(Mandatory=$true)]
        [ValidateNotNullOrEmpty()]
        $Path,

        [Parameter(Mandatory=$true)]
        [ValidateNotNullOrEmpty()]
        $Value
    )

    try {
        $registryValue = Get-ItemProperty -Path $Path -ErrorAction Stop
        if ($registryValue.PSObject.Properties.Name -contains $Value) {
            return $true
        } else {
            return $false
        }
    }
    catch {
        return $false
    }
}

##
# Create registry value with taskbar aligned left
##
function set_leftaligned_startmenu {
    $path = 'HKCU:\Software\Microsoft\Windows\CurrentVersion\Explorer\Advanced'
    
    New-Item -Path $path -Force
    New-ItemProperty -Path $path -Name 'TaskbarAl' -Value 0 -PropertyType DWord
}

if (is_win11) {
    $reg_exists = Test-RegistryValue -Path 'HKCU:\Software\Microsoft\Windows\CurrentVersion\Explorer\Advanced' -Value 'TaskbarAl'

    if ($reg_exists -eq $false) {
        set_leftaligned_startmenu
    }
}
