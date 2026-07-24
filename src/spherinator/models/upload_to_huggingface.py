from huggingface_hub import HfApi


def upload_to_huggingface(
    local_path: str,
    repo_id: str,
    path_in_repo: str = "",
    repo_type: str = "model",
    token: str | None = None,
):
    """Upload a folder to a HuggingFace repository.

    Args:
        local_path (str): Local directory containing files to upload.
        repo_id (str): HuggingFace repository ID.
        path_in_repo (str): Destination folder path inside the repository. Defaults to "".
        repo_type (str): Repository type ('model', 'dataset', or 'space').
        token (str): HuggingFace API token. Falls back to the cached login token if None.
    """
    api = HfApi(token=token)
    api.create_repo(repo_id=repo_id, repo_type=repo_type, exist_ok=True)
    api.upload_folder(
        folder_path=local_path,
        repo_id=repo_id,
        path_in_repo=path_in_repo,
        repo_type=repo_type,
    )
    print(f"Uploaded {local_path} to {repo_id}/{path_in_repo}")
