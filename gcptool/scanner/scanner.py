from typing import List

import gcptool.scanner.scans
from .finding import Finding
from .scan import all_scans


class Scanner:
    def __init__(self):
        self.findings: List[Finding] = []

    def scan(self, project: str) -> List[Finding]:
        print(f"Scanner: Starting scan of f{project}")

        all_findings: List[Finding] = []

        for scanner in all_scans:
            meta = scanner.meta()

            print(f"Running scanner {meta.name} for {meta.service}")

            scan = scanner()
            findings = scan.run(project)

            all_findings.extend(findings)

        return all_findings
