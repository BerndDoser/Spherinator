#!/usr/bin/env cwl-runner

cwlVersion: v1.2
class: Workflow

inputs:
  config: File

outputs:
  hipster: Directory

steps:
  create_images:
    run: hipster_images.cwl
    in:
      config: config
    out:
      hipster: hipster
