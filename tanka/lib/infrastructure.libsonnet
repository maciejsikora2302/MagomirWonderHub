local tk = import 'tk';
(import 'nginx/deployment.libsonnet') +
(import 'nginx/service.libsonnet') +
(import 'nginx/configmap.libsonnet') +
(import 'nginx/ingress.libsonnet') +
// (import 'debugger/debugger.libsonnet') +
{
    _config+:: {
        namespace: 'magomir',
        nginx: {
            name: 'nginx',
            labels: {
                app: 'nginx'
            },
            ports: {
                http: 8080,
                https: 443
            }
        }
    },
}