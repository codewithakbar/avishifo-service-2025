# Fix PowerShell Execution Policy to allow virtual environment activation
# Run this script as Administrator or it will set for CurrentUser only

Write-Host "Setting PowerShell execution policy..." -ForegroundColor Yellow

# Set execution policy for current user (doesn't require admin)
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser -Force

Write-Host "Execution policy updated successfully!" -ForegroundColor Green
Write-Host ""
Write-Host "You can now activate your virtual environment using:" -ForegroundColor Cyan
Write-Host "  .\venv\Scripts\activate" -ForegroundColor White
Write-Host ""
Write-Host "Or verify the policy was set:" -ForegroundColor Cyan
Write-Host "  Get-ExecutionPolicy -List" -ForegroundColor White




