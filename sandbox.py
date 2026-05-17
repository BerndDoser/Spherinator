from wandb.sandbox import Sandbox

with Sandbox.run() as sandbox:
    result = sandbox.exec(["echo", "Hello!"]).result()
    print(result.stdout)
