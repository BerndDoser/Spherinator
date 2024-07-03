from flytekit.configuration import Config
from flytekit.remote import FlyteRemote

remote = FlyteRemote(
    config=Config.auto(),
    default_project="spherinator",
    default_domain="development",
)

flyte_wf = remote.fetch_workflow(name="spherinator_training.wf")
execution = remote.execute(flyte_wf, inputs={"max_epochs": 10})

# Print the execution url
print(f"Execution url: {remote.generate_console_url(execution)}")

# Print the inputs of the execution
synced_execution = remote.sync(execution)
print(synced_execution.inputs)

# Wait for the execution to complete and print the outputs
completed_execution = remote.wait(execution)
print(completed_execution.outputs)
