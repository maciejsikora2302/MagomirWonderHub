{
    debugger: {
        # simple busybox pod that sleeps for 10h
        apiVersion: 'v1',
        kind: 'Pod',
        metadata: { name: 'busybox' },
        spec: {
            containers: [{
                name: 'busybox',
                image: 'busybox',
                command: ['sleep', '36000'],
            }]
        }
    }
}