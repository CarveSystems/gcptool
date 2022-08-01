import argparse
import logging
import os
from pathlib import Path

from .inventory.cache import Cache
from .inventory.resourcemanager import projects
from .scanner import Scanner
from .scanner.context import Context
from .scanner.finding import Severity
from .scanner.output import write_findings


def scan(args):
    print(f"Using cache at {args.cache}...")
    cache = Cache(args.cache, args.cache_only)

    # Take the list of projects to scan from the command line as a comma-separated list of project IDs.
    to_scan = [projects.get(cache, project_id) for project_id in args.project.split(",")]

    # Let's just make sure we're able to output first...
    out: Path = args.output
    if not out.exists():
        out.mkdir()

    print(f"Scanning {len(to_scan)} project(s)...")

    context = Context(to_scan, cache)

    scanner = Scanner(context)
    findings = scanner.scan()

    num_high_findings = sum(1 for finding in findings if finding.severity >= Severity.HIGH)

    print(f"Scan complete... found {len(findings)} findings.  ")
    print(f"{num_high_findings} are HIGH or CRITICAL severity.")
    print("---------------------------------------------------")

    for finding in findings:
        print(f"Title: {finding.title}")
        print(f"Severity: {finding.severity.name}")
        print("-" * 40)

    print(f"Writing findings to {args.output}...")
    write_findings(out, findings)
    print("Done!")


def permissions_check(args):
    print(f"Using cache at {args.cache}...")
    cache = Cache(args.cache)

    # Take the list of projects to scan from the command line as a comma-separated list of project IDs.
    to_scan = [projects.get(cache, project_id) for project_id in args.project.split(",")]

    context = Context(to_scan, cache)
    scanner = Scanner(context)

    scanner.test_permissions()


def list_projects(_args):
    print("Listing of all projects.\n")

    for project in projects.all():
        print(f"|{project.id}|{project.name}|{project.number}|")


parser = argparse.ArgumentParser(prog="gcptool")

subparsers = parser.add_subparsers(dest="command", required=True)
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
parser_scan.add_argument(
    "--cache-only",
    help="If enabled, do not make any outbound API requests. Only analyze existing, cached data.",
    type=bool,
    default=False,
)
parser_scan.set_defaults(func=scan)

parser_check = subparsers.add_parser(
    "check", help="Check to see if adequate permissions have been granted to run a scan."
)
parser_check.add_argument("project", help="Project to scan.")
parser_check.add_argument(
    "--cache",
    help="File to write cached API data to.",
    type=Path,
    default=Path(os.getcwd()) / "gcptool_cache.json",
)
parser_check.set_defaults(func=permissions_check)


def main():
    logging.basicConfig(filename="gcptool.log")

    args = parser.parse_args()

    args.func(args)


if __name__ == "__main__":
    main()
