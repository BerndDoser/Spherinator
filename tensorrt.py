import torch
import torch_tensorrt
import torchvision.models as models

model = models.resnet18(pretrained=True).eval().to("cuda")
input = torch.randn((1, 3, 224, 224)).to("cuda")
# trt_mod = torch_tensorrt.compile(model, ir="dynamo", inputs=[input])
trt_mod = torch_tensorrt.compile(model, ir="fx", inputs=[input])
trt_mod(input)
