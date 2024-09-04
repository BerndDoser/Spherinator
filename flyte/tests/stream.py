import os

from flytekit import FlyteContextManager, current_context, task, workflow
from flytekit.configuration import Config
from flytekit.core.data_persistence import FileAccessProvider
from flytekit.types.directory import FlyteDirectory
from flytekit.types.file import FlyteFile


@task
def copy_file(ff: FlyteFile) -> FlyteFile:
    new_file = FlyteFile.new_remote_file(ff.remote_path)
    with ff.open("r", cache_type="simplecache", cache_options={}) as r:
        with new_file.open("w") as w:
            w.write(r.read())
    return new_file


@task
def process_folder(fd: FlyteDirectory) -> FlyteDirectory:
    print(f"Remote dir {fd.path}, {fd.remote_directory}, {fd.remote_source}")
    out_fd = FlyteDirectory.new_remote()
    print(f"Writing folder to {out_fd}")
    for base, x in fd.crawl():
        print(f"\t writing {x}")
        src = os.path.join(base, x)
        out_file = out_fd.new_file(x)
        with FlyteFile(src).open("rb") as f:
            with out_file.open("wb") as o:
                print(f"Writing file to {out_file}")
                o.write(f.read())
    return out_fd


@workflow
def wf(fd: FlyteDirectory, ff: FlyteFile):
    copy_file(ff=ff)
    process_folder(fd=fd)


if __name__ == "__main__":
    ctx = FlyteContextManager.current_context()
    print(Config.for_sandbox().data_config)
    new_f = FileAccessProvider(
        local_sandbox_dir=ctx.file_access.local_sandbox_dir,
        raw_output_prefix="s3://my-s3-bucket/stream-test",
        data_config=Config.for_sandbox().data_config,
    )
    with FlyteContextManager.with_context(
        ctx.new_builder().with_file_access(new_f)
    ) as ctx:
        print(ctx)
        print(f"Sample: {ctx.file_access.get_random_remote_path()}")
        wf(
            ff=FlyteFile(path="/tmp/file_a", remote_path=False),
            fd=FlyteDirectory(path="/tmp/test", remote_directory=False),
        )
