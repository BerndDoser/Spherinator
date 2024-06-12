# Machine learning workflow orchestration

## Common Workflow Language (CWL)

### cwltool and cwl-runner

`cwltool` is a reference implementation of the CWL standard.
 - Supports CWL v1.2
 - Supports Docker and Singularity
 - Good for CWL sanity checks

```bash
cwltool example.cwl
```

`cwl-runner` is an implementation-agnostic runner for CWL. By default, it is a reference to `cwltool`.

### VSCode extension

[benten-cwl](https://marketplace.visualstudio.com/items?itemName=sbg-rabix.benten-cwl)

### Visualization of workflow pipeline

https://view.commonwl.org/



### Hipster workflow

![](../docs/assets/HiPSter_workflow.svg)

```bash
cwltool hipster_images.cwl --config shapes.yml
```

```bash
cwl-runner hipster_images.cwl hipster_input.yml
```


## Streamflow

Python package: https://pypi.org/project/streamflow/

Execute with streamflow:

```bash
streamflow run example_container.yml
streamflow run hipster_images_local.yml    # Single hipster task using default values
streamflow run hipster_wf_local.yml        # Hipster workflow running local
streamflow run hipster_wf_container.yml    # Hipster workflow running container
streamflow run hipster_wf_ssh.yml          # Hipster workflow running ssh
streamflow run hipster_wf_slurm.yml        # Hipster workflow running slurm
```

Create report:

```bash
streamflow report --format html
```
