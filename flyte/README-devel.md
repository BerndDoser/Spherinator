## flytectl

See https://docs.flyte.org/en/latest/flytectl/overview.html#installation

```
curl -sL https://ctl.flyte.org/install | bash
```

Install flytectl in $HOME/bin which is not in PATH
Copy bin to $HOME/.flyte/bin and add it to PATH for convenience


## Sandbox

https://docs.flyte.org/en/latest/deployment/deployment/sandbox.html

```
flytectl demo start
export FLYTECTL_CONFIG=~/.flyte/config-sandbox.yaml
```
- [MinIO](http://localhost:30080/minio/login)
- [Flyte console](http://localhost:30080/console)


## Kubernetes

### Install kubectl

```bash
curl -LO "https://dl.k8s.io/release/v1.29.4/bin/linux/amd64/kubectl"
curl -LO "https://dl.k8s.io/release/v1.29.4/bin/linux/amd64/kubectl.sha256"
echo "$(cat kubectl.sha256)  kubectl" | sha256sum --check
chmod u+x kubectl
mv kubectl* .local/bin/
```

### List pods

```bash
kubectl get pod -A -o wide
kubectl get pod --namespace=spherinator-development -o wide
```

### Print logs

```bash
kubectl logs --namespace=spherinator-development < pod_name >
```

### Enter running pod

```bash
kubectl exec --stdin --tty --namespace=spherinator-development < pod_name > -- /bin/bash
```


## Flyte using SLURM Rest API

- https://docs.flyte.org/en/latest/flyte_agents/index.html
- https://discuss.flyte.org/t/8281866/hi-all-i-am-currently-evaluating-if-flyte-could-be-used-as-a


## Add registry

[Flyte docu](https://docs.flyte.org/en/latest/user_guide/environment_setup.html#local-registry)


```bash
envd context create --name flyte2 --builder tcp --builder-address registry.h-its.org --use
envd context ls
```
