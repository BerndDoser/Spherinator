cwlVersion: v1.2

class: Workflow

steps:
  generate_hips:
    run:
      class: CommandLineTool
      baseCommand: hipster
