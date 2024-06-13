#!/usr/bin/env cwl-runner

cwlVersion: v1.2
class: CommandLineTool

label: "Generate HiPS tilings"

baseCommand: hipster
arguments: [ --task, hips ]

inputs:
  config:
    type: File
    inputBinding:
      prefix: --config
  output_path:
    type: string?
    default: "HiPSter"
    inputBinding:
      prefix: --output_folder

outputs:
  hips:
    type: Directory
    outputBinding:
      glob: $(inputs.output_name)
