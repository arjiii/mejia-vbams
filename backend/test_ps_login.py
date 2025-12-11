import sys
import subprocess

# Use PowerShell's Invoke-WebRequest
powershell_script = """
$body = '{"email":"driver@test.com","password":"password123"}'
try {
    $response = Invoke-WebRequest -Uri "http://localhost:8000/api/auth/login" -Method POST -Body $body -ContentType "application/json" -UseBasicParsing
    Write-Host "Status:" $response.StatusCode
    Write-Host "Content:" $response.Content
} catch {
    Write-Host "Error Status:" $_.Exception.Response.StatusCode.Value__
    Write-Host "Error:" $_.Exception.Message
    $reader = New-Object System.IO.StreamReader($_.Exception.Response.GetResponseStream())
    Write-Host "Response:" $reader.ReadToEnd()
}
"""

result = subprocess.run(
    ["powershell", "-Command", powershell_script],
    capture_output=True,
    text=True
)

print(result.stdout)
if result.stderr:
    print("STDERR:", result.stderr)
