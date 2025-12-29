import os
import subprocess
from fastmcp import FastMCP

mcp = FastMCP("httpx-mcp", version="1.0.0", allow_server_logs=True)

@mcp.tool()
def httpx(
    target: list[str],
    ports: list[int] | None = None,
    probes: list[str] | None = None,
) -> str:
    """
    Scans the given target domains and detects active HTTP/HTTPS services on ports like 80 and 443.

    target: List of domain names to scan (e.g., example.com)
    ports: Optional list of port numbers to scan (e.g., [80,443,8080])
    probes: Optional list of probe flags (e.g., ["status-code", "title", "tech-detect"]).
    """

    if not target:
        raise ValueError("'target' must contain at least one domain")

    args = ["httpx", "-u", ",".join(target), "-silent"]

    if ports:
        args += ["-p", ",".join(str(p) for p in ports)]

    if probes:
        for probe in probes:
            probe_flag = probe if probe.startswith("-") else f"-{probe}"
            args.append(probe_flag)

    try:
        result = subprocess.run(
            args,
            capture_output=True,
            text=True,
            timeout=300,
            check=False,
        )
    except FileNotFoundError:
        raise RuntimeError("httpx binary not found on server PATH")

    if result.returncode not in (0,):
        raise RuntimeError(
            f"httpx exited with code {result.returncode}: {result.stderr.strip()}"
        )

    output = result.stdout.strip()
    return output or "(no output from httpx)"


if __name__ == "__main__":
    host = os.environ.get("HOST", "0.0.0.0")
    port = int(os.environ.get("PORT", "8000"))
    mcp.run(transport="http", host=host, port=port, path="/mcp")
