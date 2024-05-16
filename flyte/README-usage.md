# How to use Flyte

Flyte is a platform for orchestrating machine learning and data processing workflows. It is designed to be scalable, reliable, and easy to use. Flyte is built on top of Kubernetes and is designed to be cloud-native.

## Quick Start

Create a new Flyte project:
```bash
flytectl create project spherinator
flytectl create project --name spherinator --id spherinator --description "test workflows"
```

Run example workflow:
```bash
pyflyte run --remote -p spherinator -d development example.py say_hello --name Ada
```
