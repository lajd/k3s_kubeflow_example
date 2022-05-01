# Install KubeFlow (full) on MicroK8s

## System
- Root privileges
- Ubuntu 20.04 (tested)
- Nvidia GPU(s)
- CUDA drivers (tested on 11.4)

# Limitations
- No GPU support
  - Microk8s version 1.21 has an issue identifying GPUs
  - See https://github.com/canonical/microk8s/issues/2634


# Install MicroK8s
See https://microk8s.io/docs/getting-started

```commandline
sudo snap remove microk8s --purge
# Note: We install 1.21 since this is the last version of Kubernetes for which Kubeflow is supported
sudo snap install microk8s --classic --channel=1.21/stable
```

## Join the user group

```commandline
sudo usermod -a -G microk8s $USER
sudo chown -f -R $USER ~/.kube
newgrp microk8s
```

## Wait until the cluster is ready

```commandline
microk8s status --wait-ready
```

## Use MicroK8s by default with kubectl

```commandline
alias kubectl='microk8s kubectl'
# Consider also updating in ~/.bashrc
```

## Save the KubeConfig and expose the KUBECONFIG envar

```commandline
mkdir -p ~/.kube
microk8s config > ~/.kube/microk8s_config.yaml 
export KUBECONFIG=~/.kube/microk8s_config.yaml
# Consider also updating in ~/.bashrc
```

# Install KubeFlow
See https://charmed-kubeflow.io/docs/quickstart and https://www.kubeflow.org/docs/distributions/charmed/install-kubeflow/

## Set permissions

```commandline
sudo chown -R $USER /var/snap/microk8s/current/juju/share/juju/
sudo rm -r /tmp/juju-store-lock*
```


## Enable addons

```commandline
microk8s enable dns storage ingress metallb:10.64.140.43-10.64.140.49
```

Note that installation of `storage` can take a while.

## Remove any existing juj cache

Helpful for clearing things like ca-certs that have been previously generated.
```commandline
sudo rm -r ~/.local/share/juju/
```

## Bootstrap with JuJu

```commandline
juju bootstrap microk8s
```


## Create JuJu KubeFlow model

```commandline
juju add-model kubeflow
```

## Install KubeFlow
```commandline
juju deploy kubeflow-lite --trust
```

## Wait for installation

In a new terminal, run:
```commandline
watch -c juju status --color
```

## Configure



Configure the juju dex-auth and oidc-gatekeeper:
```commandline
juju config dex-auth public-url=http://10.64.140.43.nip.io
juju config oidc-gatekeeper public-url=http://10.64.140.43.nip.io
```


Set development dex-auth:
```commandline
juju config dex-auth static-username=admin
juju config dex-auth static-password=admin
```

## Access the KubeFlow dashboard
Visit http://10.64.140.43.nip.io to access the dashboard

## Version information
JuJu version:
2.9.28-ubuntu-amd64

K8s version:
Client Version: version.Info{Major:"1", Minor:"21+", GitVersion:"v1.21.11-3+2bdf0a81ac1652", GitCommit:"2bdf0a81ac16527b69a7840edf58307f72c82df2", GitTreeState:"clean", BuildDate:"2022-03-18T13:13:14Z", GoVersion:"go1.16.15", Compiler:"gc", Platform:"linux/amd64"}
Server Version: version.Info{Major:"1", Minor:"21+", GitVersion:"v1.21.11-3+2bdf0a81ac1652", GitCommit:"2bdf0a81ac16527b69a7840edf58307f72c82df2", GitTreeState:"clean", BuildDate:"2022-03-18T13:10:46Z", GoVersion:"go1.16.15", Compiler:"gc", Platform:"linux/amd64"}

# Optional next steps

## Enable the Microk8s registry

```commandline
microk8s enable registry
```
