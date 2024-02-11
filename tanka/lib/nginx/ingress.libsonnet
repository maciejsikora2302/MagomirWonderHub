{
    nginx_ingress: {
        apiVersion: "networking.k8s.io/v1",
        kind: "Ingress",
        metadata: {
            name: $._config.nginx.name + '-ingress',
            namespace: $._config.namespace
        },
        spec: {
            ingressClassName: "nginx",
            rules: [
                {
                    host: "www.magomir.com",
                    http: {
                        paths: [
                            {
                                pathType: "Prefix",
                                backend: {
                                    service: {
                                        name: $.nginx_service.metadata.name,
                                        port: {
                                            number: $._config.nginx.ports.http
                                        }
                                    },
                                },
                                path: "/"
                            }
                        ]
                    }
                }
            ]
        }
    }
}
