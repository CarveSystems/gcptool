from typing import List

import gcptool.scanner.scans
from .finding import Finding
from .scan import all_scans
from .context import Context


class Scanner:
    def __init__(self):
        self.findings: List[Finding] = []

    def scan(self, context: Context) -> List[Finding]:
        print(f"Scanner: Beginning scan")

        all_findings: List[Finding] = []

        for scanner in all_scans:
            meta = scanner.meta()

            print(f"Running scanner {meta.name} for {meta.service}")

            scan = scanner()
            findings = scan.run(context)

            all_findings.extend(findings)

        print(f"Writing data to cache...")
        context.cache.save()

        return all_findings
