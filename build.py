import os
import platform
import shutil
import sys
import urllib.request
import zipfile


DOWNLOAD_URL = "https://github.com/BtbN/FFmpeg-Builds/releases/download/latest/{filename}"

FILE_NAME = "ffmpeg-n7.0-latest-win64-gpl-{MAJOR}.{MINOR}.{ext}"

DOWNLOAD_TYPES = {"windows": "zip"}


def get_os_information():
    """Get the os name and the architecture.

    Returns:
        tuple: OS name and architecture.
    """
    os_names = {
        "Windows": "windows",
        "Darwin": "macos",
    }
    architectures = {"AMD64": "x64", "arm64": "arm64"}
    os_platform = platform.system()
    os_architecture = platform.machine()

    return (
        os_names.get(os_platform, "linux"),
        architectures.get(os_architecture, "x64"),
    )


def build(source_path, build_path, install_path, targets):
    """Build/Install function.

    Args:
        source_path (str): Path to the rez package root.
        build_path (str): Path to the rez build directory.
        install_path (str): Path to the rez install directory.
        targets (str): Target run by the command, i.e. `build`, `install`...

    Raises:
        RuntimeError: Your current OS is not supported.
    """
    os_name, _ = get_os_information()
    package_major, package_minor, _ = os.environ.get(
        "REZ_BUILD_PROJECT_VERSION", "0.0.0"
    ).split(".")

    if os_name in ["macos", "linux"]:
        raise RuntimeError(f"Your current OS is not supported ({os_name}).")

    ffmpeg_archive = FILE_NAME.format(
        MAJOR=package_major,
        MINOR=package_minor,
        ext=DOWNLOAD_TYPES.get(os_name),
    )
    download_url = DOWNLOAD_URL.format(filename=ffmpeg_archive)

    def _build():
        """Build the package locally."""
        archive_path = os.path.join(build_path, ffmpeg_archive)

        if not os.path.isfile(archive_path):
            print(f"Downloading FFMPEG archive from: {download_url}")
            
            download_request = urllib.request.Request(
                url=download_url,
                headers={'User-Agent': 'Mozilla/5.0'},
            )

            with open(archive_path, "wb") as file:
                with urllib.request.urlopen(download_request) as request:
                    file.write(request.read())

        print("Extracting the archive.")
        match os_name:
            case "windows":
                with zipfile.ZipFile(archive_path) as archive_file:
                    archive_file.extractall(build_path)
            case _:
                pass

    def _install():
        """Install the package."""
        print("Installing the package.")
        extracted_archive_path = os.path.join(
            build_path, os.path.splitext(ffmpeg_archive)[0]
        )

        match os_name:
            case "windows":
                for element in os.listdir(extracted_archive_path):
                    element_path = os.path.join(extracted_archive_path, element)
                    shutil.move(element_path, install_path)
            case _:
                pass

    _build()

    if "install" in (targets or []):
        _install()


if __name__ == "__main__":
    build(
        source_path=os.environ["REZ_BUILD_SOURCE_PATH"],
        build_path=os.environ["REZ_BUILD_PATH"],
        install_path=os.environ["REZ_BUILD_INSTALL_PATH"],
        targets=sys.argv[1:],
    )
