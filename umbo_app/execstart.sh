#!/bin/dash


curl --unix-socket /var/run/docker.sock -H "Content-Type: application/json" -d '{"Detach": false, "Tty": false}' -X POST http:/v1.37/exec/$2/start
