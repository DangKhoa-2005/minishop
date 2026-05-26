#!/usr/bin/env python3
import argparse
import os
import shutil
import subprocess
import sys
import time
from urllib.request import urlopen
from urllib.error import URLError, HTTPError


def log(message):
    print(f"[mini-shop] {message}")


def run(cmd, cwd=None, env=None):
    log(f"Running: {' '.join(cmd)}")
    subprocess.check_call(cmd, cwd=cwd, env=env)


def docker_compose_command():
    if shutil.which("docker-compose"):
        return ["docker-compose"]
    return ["docker", "compose"]


def docker_ready():
    try:
        subprocess.check_output(["docker", "info"], stderr=subprocess.STDOUT)
        return True
    except Exception:
        return False


def wait_http(url, timeout_sec):
    deadline = time.time() + timeout_sec
    while time.time() < deadline:
        try:
            with urlopen(url, timeout=5) as resp:
                if 200 <= resp.status < 500:
                    return
        except (URLError, HTTPError):
            time.sleep(3)
    raise RuntimeError(f"Timeout waiting for {url}")


def main():
    parser = argparse.ArgumentParser(description="Run full Docker + E2E automation")
    parser.add_argument("--compose-file", default="docker-compose.yml")
    parser.add_argument("--frontend-url", default="http://localhost:8081")
    parser.add_argument("--backend-url", default="http://localhost:5002")
    parser.add_argument("--timeout", type=int, default=240)
    parser.add_argument("--keep-containers", action="store_true")
    parser.add_argument("--headed", action="store_true")
    args = parser.parse_args()

    if not shutil.which("docker"):
        raise RuntimeError("Docker CLI not found. Please install Docker Desktop first.")

    if not docker_ready():
        raise RuntimeError(
            "Docker is not ready. Please start Docker Desktop and wait until it is running."
        )

    repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    e2e_dir = os.path.join(repo_root, "tests", "e2e")

    compose_cmd = docker_compose_command()
    run(compose_cmd + ["-f", args.compose_file, "up", "-d", "--build"], cwd=repo_root)

    log("Waiting for backend...")
    wait_http(f"{args.backend_url}/api/health", args.timeout)
    log("Waiting for frontend...")
    wait_http(args.frontend_url, args.timeout)

    if not os.path.isdir(os.path.join(e2e_dir, "node_modules")):
        run(["npm", "install"], cwd=e2e_dir)

    run(["npx", "playwright", "install"], cwd=e2e_dir)

    env = os.environ.copy()
    env["BASE_URL"] = args.frontend_url

    test_cmd = [
        "npx",
        "playwright",
        "test",
        "full-flow.spec.js",
        "--project=chromium",
        "--reporter=list",
    ]
    if args.headed:
        test_cmd.append("--headed")
    run(test_cmd, cwd=e2e_dir, env=env)

    if not args.keep_containers:
        run(compose_cmd + ["-f", args.compose_file, "down"], cwd=repo_root)


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        log(str(exc))
        sys.exit(1)
