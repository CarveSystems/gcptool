import argparse
import os
from pathlib import Path
import sys

from .inventory.compute.addresses import addresses
from .inventory.compute.compute import instances
from .inventory.resourcemanager import projects
from .inventory.cache import Cache

from .scanner import Scanner
from .scanner.context import Context
from .scanner.finding import Severity
from .scanner.output import write_findings

from .creds import project as default_project


def scan(args):

    print(f"Using cache at {args.cache}...")
    cache = Cache(args.cache)

    # Take the list of projects to scan from the command line as a comma-separated list of project IDs.
    to_scan = [projects.get(project_id) for project_id in args.project.split(",")]

    # Let's just make sure we're able to output first...
    out: Path = args.output
    if not out.exists():
        out.mkdir()

    print(f"Scanning {len(to_scan)} project(s)...")

    context = Context(to_scan, cache)

    scanner = Scanner()
    findings = scanner.scan(context)

    num_high_findings = sum(1 for finding in findings if finding.severity >= Severity.HIGH)

    print(f"Scan complete... found {len(findings)} findings.  ")
    print(f"{num_high_findings} are HIGH or CRITICAL severity.")
    print("---------------------------------------------------")

    for finding in findings:
        print(f"Title: {finding.title}")
        print(f"Severity: {finding.severity.name}")
        print("-" * 40)

    print(f"Writing findings to {args.output}...")
    write_findings(out, project.id, findings)
    print("Done!")


def list_projects(args):
    print("Listing of all projects.\n")

    for project in projects.all():
        print(f"{project.id}:\t{project.name}")


parser = argparse.ArgumentParser(prog="gcptool")

subparsers = parser.add_subparsers(required=True)
parser_projects = subparsers.add_parser(
    "list-projects", help="List process accessible to this user"
)
parser_projects.set_defaults(func=list_projects)

parser_scan = subparsers.add_parser("scan", help="Scan a given project")
parser_scan.add_argument("project", help="Project to scan.")
parser_scan.add_argument("output", help="Folder to write generated findings to.", type=Path)
parser_scan.add_argument(
    "--cache",
    help="File to write cached API data to.",
    type=Path,
    default=Path(os.getcwd()) / "gcptool_cache.json",
)
parser_scan.set_defaults(func=scan)


def main():
    args = parser.parse_args()

    args.func(args)


if __name__ == "__main__":
    main()
