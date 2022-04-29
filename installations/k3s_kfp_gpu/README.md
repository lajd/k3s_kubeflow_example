# KubeFlow Pipelines Example on K3s with GPU support 
Minimal example running KubeFlow locally with GPU support using K3s.

This tutorial covers the following:
- Installation of prerequisites
  - K3s
  - Containerd
  - Nvidia drivers
  - Configuring K3s to use Nvidia GPUs
  - Installing the nvidia-device-plugin
- Installation of KubeFlow

# Limitations
- Only Kubeflow pipelines is installed

# Prerequisites

## System
- Root privileges
- Ubuntu 20.04 (tested)
- Nvidia GPU(s)
- CUDA drivers (tested on 11.4)

## Install K3
https://rancher.com/docs/k3s/latest/en/installation/install-options/

```bash
# Tested on version INSTALL_K3S_VERSION=v1.23.5+k3s1
curl -sfL https://get.k3s.io | INSTALL_K3S_VERSION=v1.21.11+k3s1  sh -
```

Example output:

```bash
[INFO]  Using v1.21.11+k3s1 as release
[INFO]  Downloading hash https://github.com/k3s-io/k3s/releases/download/v1.21.11+k3s1/sha256sum-amd64.txt
[INFO]  Downloading binary https://github.com/k3s-io/k3s/releases/download/v1.21.11+k3s1/k3s
[INFO]  Verifying binary download
[INFO]  Installing k3s to /usr/local/bin/k3s
[INFO]  Skipping installation of SELinux RPM
[INFO]  Skipping /usr/local/bin/kubectl symlink to k3s, already exists
[INFO]  Creating /usr/local/bin/crictl symlink to k3s
[INFO]  Skipping /usr/local/bin/ctr symlink to k3s, command exists in PATH at /usr/bin/ctr
[INFO]  Creating killall script /usr/local/bin/k3s-killall.sh
[INFO]  Creating uninstall script /usr/local/bin/k3s-uninstall.sh
[INFO]  env: Creating environment file /etc/systemd/system/k3s.service.env
[INFO]  systemd: Creating service file /etc/systemd/system/k3s.service
[INFO]  systemd: Enabling k3s unit
Created symlink /etc/systemd/system/multi-user.target.wants/k3s.service → /etc/systemd/system/k3s.service.
[INFO]  systemd: Starting k3s

```

Check that the K3s CLI is working:
```commandline
k3s
```

Example output:

```bash
NAME:
   k3s - Kubernetes, but small and simple

USAGE:
   k3s [global options] command [command options] [arguments...]

VERSION:
   v1.22.7+k3s1 (8432d7f2)

COMMANDS:
   server           Run management server
   agent            Run node agent
   kubectl          Run kubectl
   crictl           Run crictl
   ctr              Run ctr
   check-config     Run config check
   etcd-snapshot    Trigger an immediate etcd snapshot
   secrets-encrypt  Control secrets encryption and keys rotation
   certificate      Certificates management
   help, h          Shows a list of commands or help for one command

GLOBAL OPTIONS:
   --debug                     (logging) Turn on debug logs [$K3S_DEBUG]
   --data-dir value, -d value  (data) Folder to hold state default /var/lib/rancher/k3s or ${HOME}/.rancher/k3s if not root
   --help, -h                  show help
   --version, -v               print the version
```


## Install ContainerD
See https://containerd.io/ for details.


After, verify containerd is working with `ctr`:
```commandline
ctr
```


Example output:
```bash
NAME:
   ctr - 
        __
  _____/ /______
 / ___/ __/ ___/
/ /__/ /_/ /
\___/\__/_/

containerd CLI


USAGE:
   ctr [global options] command [command options] [arguments...]

VERSION:
   1.4.12

DESCRIPTION:
   
ctr is an unsupported debug and administrative client for interacting
with the containerd daemon. Because it is unsupported, the commands,
options, and operations are not guaranteed to be backward compatible or
stable from release to release of the containerd project.

COMMANDS:
   plugins, plugin            provides information about containerd plugins
   version                    print the client and server versions
   containers, c, container   manage containers
   content                    manage content
   events, event              display containerd events
   images, image, i           manage images
   leases                     manage leases
   namespaces, namespace, ns  manage namespaces
   pprof                      provide golang pprof outputs for containerd
   run                        run a container
   snapshots, snapshot        manage snapshots
   tasks, t, task             manage tasks
   install                    install a new package
   oci                        OCI tools
   shim                       interact with a shim directly
   help, h                    Shows a list of commands or help for one command

GLOBAL OPTIONS:
   --debug                      enable debug output in logs
   --address value, -a value    address for containerd's GRPC server (default: "/run/containerd/containerd.sock") [$CONTAINERD_ADDRESS]
   --timeout value              total timeout for ctr commands (default: 0s)
   --connect-timeout value      timeout for connecting to containerd (default: 0s)
   --namespace value, -n value  namespace to use with commands (default: "default") [$CONTAINERD_NAMESPACE]
   --help, -h                   show help
   --version, -v                print the version
```

## Install Nvidia drivers on local system
Confirm nvidia is configured locally with:

```commandline
nvidia-smi
```

Example output:
```bash
+-----------------------------------------------------------------------------+
| NVIDIA-SMI 470.103.01   Driver Version: 470.103.01   CUDA Version: 11.4     |
|-------------------------------+----------------------+----------------------+
| GPU  Name        Persistence-M| Bus-Id        Disp.A | Volatile Uncorr. ECC |
| Fan  Temp  Perf  Pwr:Usage/Cap|         Memory-Usage | GPU-Util  Compute M. |
|                               |                      |               MIG M. |
|===============================+======================+======================|
|   0  NVIDIA GeForce ...  On   | 00000000:0B:00.0  On |                  N/A |
|  0%   32C    P8    34W / 300W |    528MiB / 11011MiB |     11%      Default |
|                               |                      |                  N/A |
+-------------------------------+----------------------+----------------------+
                                                                               
+-----------------------------------------------------------------------------+
| Processes:                                                                  |
|  GPU   GI   CI        PID   Type   Process name                  GPU Memory |
|        ID   ID                                                   Usage      |
|=============================================================================|
|    0   N/A  N/A      1361      G   /usr/lib/xorg/Xorg                 78MiB |
|    0   N/A  N/A      5647      G   /usr/lib/xorg/Xorg                205MiB |
|    0   N/A  N/A      5789      G   /usr/bin/gnome-shell              113MiB |
|    0   N/A  N/A     12364      G   ...007793464990344240,131072       77MiB |
|    0   N/A  N/A     14013      G   ..._13195.log --shared-files       37MiB |
+-----------------------------------------------------------------------------+

```

## Install Nvidia container toolkit
See https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/install-guide.html#install-guide
for installation of the NVIDIA Container Toolkit.

In addition, install the nvidia-container-runtime package.
```commandline
sudo apt-get update && sudo apt-get install -y nvidia-container-runtime
```

Validate the installation by running a container and passing GPUs from the host to the container:
```commandline
sudo ctr image pull docker.io/nvidia/cuda:11.0-base
sudo ctr run --rm --gpus 0 -t docker.io/nvidia/cuda:11.0-base cuda-11.0-base nvidia-smi
```

Example output:

```bash
11.0-base cuda-11.0-base nvidia-smi
Tue Apr 26 03:51:24 2022       
+-----------------------------------------------------------------------------+
| NVIDIA-SMI 470.103.01   Driver Version: 470.103.01   CUDA Version: 11.4     |
|-------------------------------+----------------------+----------------------+
| GPU  Name        Persistence-M| Bus-Id        Disp.A | Volatile Uncorr. ECC |
| Fan  Temp  Perf  Pwr:Usage/Cap|         Memory-Usage | GPU-Util  Compute M. |
|                               |                      |               MIG M. |
|===============================+======================+======================|
|   0  NVIDIA GeForce ...  On   | 00000000:0B:00.0  On |                  N/A |
|  0%   58C    P3    72W / 300W |    472MiB / 11011MiB |     11%      Default |
|                               |                      |                  N/A |
+-------------------------------+----------------------+----------------------+
                                                                               
+-----------------------------------------------------------------------------+
| Processes:                                                                  |
|  GPU   GI   CI        PID   Type   Process name                  GPU Memory |
|        ID   ID                                                   Usage      |
|=============================================================================|
+-----------------------------------------------------------------------------+
```

## Export default KUBECONFIG

This is helpful for allowing kubectl access without sudo, and pointing kubectl, helm and other
clients to use the kubeconfig from k3s

```commandline
sudo cp /etc/rancher/k3s/k3s.yaml ~/.kube/k3s_config.yaml
sudo setfacl -m u:$USER:rwx ~/.kube/k3s_config.yaml
export KUBECONFIG=~/.kube/k3s_config.yaml
```

## Configure K3S to use your Nvidia GPU
In order for K3s to utilize GPUs when deploying K8s resources to the cluster, we must configure the containerd agent
such that it is aware of the GPUs present on the host.

Copy CUDA config file to containderd directory. See https://k3d.io/v4.4.8/usage/guides/cuda/ for details.
```commandline
sudo cp configs/config.toml.tmpl /var/lib/rancher/k3s/agent/etc/containerd/config.toml.tmpl
```

Restart k3s after the changes:
```commandline
sudo systemctl restart k3s
```

## Install helm
See https://helm.sh/docs/intro/install/ for details.

```commandline
helm version
```

Example output:
```bash
version.BuildInfo{Version:"v3.7.0", GitCommit:"eeac83883cb4014fe60267ec6373570374ce770b", GitTreeState:"clean", GoVersion:"go1.16.8"}
```

## Install Nvidia device plugin for K3s with helm
For Kubernetes to recognize that GPUs are available on the nodes (e.g. when scheduling jobs with resource requests for gpus), 
we must deploy the nvidia-device-plugin daemonset.

```commandline
helm repo add nvdp https://nvidia.github.io/k8s-device-plugin \
   && helm repo update
helm install --generate-name nvdp/nvidia-device-plugin
```

To validate that Kubernetes can see the GPUs, run:
```commandline
kubectl describe nodes
```

Verify that the `nvidia.com/gpu` resource is present on the node:
```bash
Capacity:
  cpu:                24
  ephemeral-storage:  510470752Ki
  hugepages-1Gi:      0
  hugepages-2Mi:      0
  memory:             32853556Ki
  nvidia.com/gpu:     1
```


## Apply a test pod that requires GPU access

```commandline
kubectl apply -f configs/nvidia-smi-test-pod.yaml
```

Verify that the container can be brought up:

```commandline
kubectl describe pod gpu
```

Example output:
```bash
  Type    Reason     Age   From               Message
  ----    ------     ----  ----               -------
  Normal  Scheduled  17h   default-scheduler  Successfully assigned default/gpu to metamorphesis
  Normal  Pulling    17h   kubelet            Pulling image "nvidia/cuda:11.4.1-base-ubuntu20.04"
  Normal  Pulled     17h   kubelet            Successfully pulled image "nvidia/cuda:11.4.1-base-ubuntu20.04" in 5.451902158s
  Normal  Created    17h   kubelet            Created container gpu
  Normal  Started    17h   kubelet            Started container gpu
```

# Installing KubeFlow Pipelines on K3s

See https://www.kubeflow.org/docs/components/pipelines/installation/localcluster-deployment/ for details.

```commandline
export PIPELINE_VERSION=1.8.1
kubectl apply -k "github.com/kubeflow/pipelines/manifests/kustomize/cluster-scoped-resources?ref=$PIPELINE_VERSION"
kubectl wait --for condition=established --timeout=60s crd/applications.app.k8s.io
kubectl apply -k "github.com/kubeflow/pipelines/manifests/kustomize/env/platform-agnostic-pns?ref=$PIPELINE_VERSION"
```

## Verify Kubeflow pipelines UI is accessible

```commandline
kubectl port-forward -n kubeflow svc/ml-pipeline-ui 8080:80
```