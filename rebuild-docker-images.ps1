#add parameters to start docker compose up if flag -y has been provided
param(
    [switch]$y
)

Write-Output "Rebuilding docker images"

Write-Output "Rebuilding docker magomirwonderhub"
docker build -f ./docker/webserver/dockerfile --tag magomirwonderhub .

if ($y) {
    Write-Output "Starting docker compose up"
    docker-compose up -d
}
