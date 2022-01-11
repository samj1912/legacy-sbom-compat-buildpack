import os
import libcnb
import toml
import shutil

def detector(context: libcnb.DetectContext) -> libcnb.DetectResult:
    return libcnb.DetectResult(
        passed=bool(os.environ.get("BP_LEGACY_SBOM_FORMAT", ""))
    )

def builder(context: libcnb.BuildContext) -> libcnb.BuildResult:
    result = libcnb.BuildResult()
    result.launch_metadata = libcnb.LaunchMetadata()
    for file in context.application_dir.glob("sbom/*/launch.toml"):
        data = toml.load(file)
        for entry in data.get("bom", []):
            result.launch_metadata.bom.append(libcnb.BOMEntry.parse_obj(entry))
    shutil.rmtree(context.application_dir / "sbom")
    return result

if __name__ == "__main__":
    libcnb.run(detector=detector, builder=builder)
