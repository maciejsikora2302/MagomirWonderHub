#print work dir
#check if pwd is in docker dir

if ($pwd -like "*docker*") {
    Write-Host "Running from docker directory"
} else {
    Write-Host "Not running from docker directory"
    cd docker
}

try {
    ./persistent_run_container.ps1 -use_ephemeral_container "true"
} catch {
    Write-Host "Error: $_"
} finally {
    cd ..
}