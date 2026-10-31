# Fmind for Evidence

Light theme for [Evidence](https://evidence.dev/) projects, in the current [`theme.yaml` format](https://docs.evidence.dev/features/themes). The legacy Evidence framework, which read themes from `evidence.config.yaml`, is not supported.

Format: [Evidence themes](https://docs.evidence.dev/features/themes) · [theme schema](https://github.com/evidence-dev/evidence/blob/main/core/src/types/theme.ts)

## Installation

Merge the keys of [fmind.yaml](fmind.yaml) into `theme.yaml` at your project root, next to `evidence.config.yaml`; Evidence reads only that file name. If the project has no `theme.yaml`, copy `fmind.yaml` there as `theme.yaml`. Fmind sets light-mode colors only; dark mode keeps the Evidence defaults.
