# Fmind for Hyper

Files: [fmind.json](fmind.json).

Format: [Hyper 3 default config](https://github.com/vercel/hyper/blob/v3.4.1/app/config/config-default.js) · [Hyper 4 schema](https://github.com/vercel/hyper/blob/canary/app/config/schema.json)

## Installation

Copy the keys of [fmind.json](fmind.json) into the `config` object of your Hyper configuration: `.hyper.js` in Hyper 3 or `hyper.json` in Hyper 4 canary. Hyper 3 evaluates `.hyper.js` without `require`, so paste the keys rather than importing the file. Use Hyper’s Edit → Preferences to open the config.
