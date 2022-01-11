# Legacy SBOM Buildpack

![Version](https://img.shields.io/badge/dynamic/json?url=https://cnb-registry-api.herokuapp.com/api/v1/buildpacks/sam/legacy-sbom-compat-buildpack&label=Version&query=$.latest.version)

This is a [Cloud Native Buildpack](https://buildpacks.io) that is a poc of providing a compat layer for newer buildpack api versions to allow them to output standard sbom formats while delegating to this buildpack for the legacy format. 


## Usage

Set the environment variable `BP_LEGACY_SBOM_FORMAT` to a non-empty value. Have your other buildpacks with API version 0.7+ output the legacy `launch.toml` like file with 
`bom` entries to `/workspace/sbom/bp-id/launch.toml`. This buildpack will collect all such entries and populate them in the old Buildpack API BOM format.

Example buildpack with API 0.7 that does this - 

buildpack.toml

```toml
api = "0.7"

[buildpack]
id = "sam/new-sbom-buildpack"
version = "0.0.1"
```
bin/detect

```bash
#!/bin/bash
exit 0
```

bin/build

```bash
#!/bin/bash


cat >> "$(pwd)/sbom/sam/new-sbom-buildpack/launch.toml" <<EOL
[[bom]]
name = "ruby"
[bom.metadata]
version = "$ruby_version"
EOL

exit 0
```
