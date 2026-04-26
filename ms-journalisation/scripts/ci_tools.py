#!/usr/bin/env python3
"""CI helper for build, test and deployment tasks."""

import argparse
import os
import subprocess
import sys

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))


def run_command(command, cwd=ROOT_DIR):
    print(f"$ {' '.join(command)}")
    result = subprocess.run(command, cwd=cwd)
    if result.returncode != 0:
        raise SystemExit(result.returncode)


def build(args):
    os.chdir(ROOT_DIR)
    run_command([sys.executable, "-m", "pip", "install", "--upgrade", "pip"])
    run_command([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
    image_name = args.image or "ms-journalisation:ci"
    command = ["docker", "build", "-t", image_name, "."]
    if args.no_cache:
        command.insert(3, "--no-cache")
    run_command(command)
    print(f"Built Docker image: {image_name}")


def test(args):
    os.chdir(ROOT_DIR)
    run_command([sys.executable, "-m", "pip", "install", "--upgrade", "pip"])
    run_command([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
    run_command([
        "pytest",
        "--cov=src",
        "--cov-report=xml",
        "--cov-report=term-missing",
    ])
    print("Tests passed successfully.")


def report(args):
    os.chdir(ROOT_DIR)
    run_command([sys.executable, "-m", "pip", "install", "--upgrade", "pip"])
    run_command([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
    command = [
        "pytest",
        "--junitxml=rapport_tests.xml",
        "--cov=src",
        "--cov-report=xml",
        "--cov-report=html:coverage_html",
        "--cov-report=term-missing",
    ]
    print(f"$ {' '.join(command)}")
    result = subprocess.run(command, cwd=ROOT_DIR, text=True, capture_output=True)
    with open(os.path.join(ROOT_DIR, "rapport_tests.txt"), "w", encoding="utf-8") as output_file:
        output_file.write(result.stdout)
        if result.stderr:
            output_file.write("\n--- STDERR ---\n")
            output_file.write(result.stderr)
    print(result.stdout, end="")
    if result.stderr:
        print(result.stderr, file=sys.stderr)
    if result.returncode != 0:
        raise SystemExit(result.returncode)
    print("Generated rapport_tests.txt, rapport_tests.xml, coverage.xml and coverage_html/")


def deploy(args):
    os.chdir(ROOT_DIR)
    registry = args.registry or os.environ.get("REGISTRY")
    if not registry:
        print("ERROR: registry is required. Set REGISTRY env or use --registry.")
        raise SystemExit(1)

    image_name = args.image or "ms-journalisation:ci"
    target_image = f"{registry}/{image_name}" if "/" not in image_name else image_name
    run_command(["docker", "tag", image_name, target_image])
    run_command(["docker", "push", target_image])
    print(f"Deployed image: {target_image}")


def main():
    parser = argparse.ArgumentParser(description="CI helper for ms-journalisation")
    subparsers = parser.add_subparsers(dest="command", required=True)

    build_parser = subparsers.add_parser("build", help="Build the Docker image")
    build_parser.add_argument("--image", help="Docker image name", default="ms-journalisation:ci")
    build_parser.add_argument("--no-cache", action="store_true", help="Build without cache")

    test_parser = subparsers.add_parser("test", help="Run unit tests with coverage")
    report_parser = subparsers.add_parser("report", help="Generate test and coverage reports")

    deploy_parser = subparsers.add_parser("deploy", help="Tag and push Docker image")
    deploy_parser.add_argument("--registry", help="Docker registry to push image")
    deploy_parser.add_argument("--image", help="Docker image name", default="ms-journalisation:ci")

    args = parser.parse_args()
    if args.command == "build":
        build(args)
    elif args.command == "test":
        test(args)
    elif args.command == "report":
        report(args)
    elif args.command == "deploy":
        deploy(args)


if __name__ == "__main__":
    main()
