#add parameter to pass in the name of the container
param ([string]$use_ephemeral_container = "false")

$container_name = "MagomirWonderHubServer"
if ($use_ephemeral_container -eq "true") {
    $container_name = $container_name + "_ephemeral"
}
$image_name = "magomirwonderhub"

$volume_name = "HubData"
$volume_bind_path = "/app/webpage/data"
$volume_expression = "--mount type=volume,src=$volume_name,dst=$volume_bind_path"
$common_expression = "docker run -it -p 23463:23463 --name $container_name $volume_expression"

if ($use_ephemeral_container -eq "true") {
    ### EPHEMERAL CONTAINER ###
    
    Invoke-Expression "$common_expression --rm $image_name"
} else {
    ### PERSISTENT CONTAINER ###

    #check if container exists
    $container_exists = docker ps -a --format "{{.Names}}" | Select-String -Pattern $container_name
    if ($container_exists -ne $null) {
        #container exists, start it
        docker start -i $container_name
    } else {
        #container does not exist, create it
        Invoke-Expression "$common_expression --restart unless-stopped $image_name"
    }
}