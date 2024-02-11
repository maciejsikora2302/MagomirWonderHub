{
    nginx_service: {
        apiVersion: "v1",
        kind: "Service",
        metadata: {
            name: $._config.nginx.name + "-service"
        },
        spec: {
            selector: {
                app: $._config.nginx.name
            },
            ports: [
                {
                    protocol: "TCP",
                    port: $._config.nginx.ports.http,
                    targetPort: $._config.nginx.ports.http
                }
            ],
            type: "ClusterIP"
        }
    }
}