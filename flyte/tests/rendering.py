import flytekit
from flytekit import task, workflow
from flytekit.types.file import FlyteFile
from flytekitplugins.deck.renderer import ImageRenderer


@task(enable_deck=True)
def image_renderer(image: FlyteFile) -> None:
    flytekit.Deck("Image Renderer", ImageRenderer().to_html(image_src=image))


@workflow
def image_renderer_wf(
    image: FlyteFile = "https://bit.ly/3KZ95q4",
) -> None:
    image_renderer(image=image)
