#!/bin/dash

curl --unix-socket /var/run/docker.sock -H "Content-Type: application/json" -d '{"AttachStdin": false, "AttachStdout": true, "AttachStderr": true, "DetachKeys": "ctrl-p,ctrl-q", "Tty": false, "Cmd": ["/bin/sh","-c","bash /code/predict.sh"], "Env": ["FOO=bar", "BAZ=quux"]}' -X POST http:/v1.37/containers/umbo_app_classifier_1/exec 
