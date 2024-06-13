#!/usr/bin/env cwl-runner

cwlVersion: v1.2
class: Workflow

inputs:
  config:
    type: File?
    default:
      class: File
      location: ./shapes.yml

outputs:
  outdir:
    type: Directory
    outputSource: create_images/hipster

steps:
  create_images:
    run: tasks/create_images.cwl
    in:
      config: config
    out:
      - hipster
