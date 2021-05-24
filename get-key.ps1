Add-Type -AssemblyName System.Security

$state = ConvertFrom-Json -InputObject (Get-Content -Raw "$env:localappdata\Google\Chrome\User Data\Local State")
$encrypted_key_data = [System.Convert]::FromBase64String($state.os_crypt.encrypted_key)
$encrypted_key = $encrypted_key_data[5 .. ($encrypted_key_data.Length - 1)]

$key = [Security.Cryptography.ProtectedData]::Unprotect($encrypted_key, $null, [Security.Cryptography.DataProtectionScope]::CurrentUser)

($key | ForEach-Object ToString X2) -Join ''