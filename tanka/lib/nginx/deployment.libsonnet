{
    _nginx_pod :: {
        metadata: {
            name: $._config.nginx.name + "-pod",
            labels: {
                app: $._config.nginx.name
            }
        },
        spec: {
            containers: [
                {
                    name: $._config.nginx.name + "-lb",
                    image: "nginx:latest",
                    ports: [
                        {
                            containerPort: $._config.nginx.ports.http
                        }
                    ],
                }
            ]
        }
    },
    nginx_deployment: {
        apiVersion: "apps/v1",
        kind: "Deployment",
        metadata: {
            name: $._config.nginx.name + "-deployment",
        },
        spec: {
            replicas: 1,
            selector: {
                matchLabels: $._nginx_pod.metadata.labels
            },
            template: $._nginx_pod
        }
    }
}