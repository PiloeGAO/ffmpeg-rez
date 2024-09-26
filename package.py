name = "ffmpeg"

version = "7.0.2"

authors = ["ffmpeg contributors", "Leo Depoix (@piloegao)"]

description = """
    FFmpeg is the leading multimedia framework, able to decode, encode, transcode, mux, demux, stream, filter and play pretty much anything that humans and machines have created.
    """

requires = ["python"]

uuid = "ffmpeg.ffmpeg"

build_command = "python {root}/build.py {install}"


def commands():
    executables = {
        "windows": {
            "ffmpeg": "ffmpeg.exe",
            "ffplay": "ffplay.exe",
            "ffprobe": "ffprobe.exe",
        },
        "osx": {},
        "linux": {},
    }
    
    for exec_command, executable_file in executables.get(system.platform).items():
        alias(exec_command, "{root}/bin/%s" % executable_file)
    
    env.PATH.append("{root}/bin")
