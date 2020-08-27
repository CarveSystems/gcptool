from typing import List, Any

from gcptool.scanner.finding import Finding, Severity
from gcptool.scanner.scan import Scan, ScanMetadata, scan
from gcptool.scanner.context import Context

from gcptool.inventory.storage import buckets


@scan
class PubliclyAccessibleBuckets(Scan):
    """
    This scan returns a list of buckets that have been assigned public IAM roles or ACLs.
    """

    @staticmethod
    def meta():
        # TODO - note the permissions for this
        return ScanMetadata("gcs", "public-buckets", [])

    def run(self, context: Context) -> List[Finding]:
        # TODO - make Cloud Storage respect the cache/context
        project = context.projects[0]

        all_buckets = buckets.all(project.id)

        readable_buckets: List[str] = []
        writable_buckets: List[str] = []

        # These entities represent the public.
        # 'allUsers' represents... anyone.
        # 'allAuthenticatedUsers' requires the user to be logged into a Google account.
        public_entities = {"allUsers", "allAuthenticatedUsers"}

        # Which roles grant us read or write access to the storage bucket?
        write_roles = {
            "roles/storage.legacyBucketWriter",
            "roles/storage.legacyBucketOwner",
            "roles/storage.objectCreator",
            "roles/storage.objectAdmin",
            "roles/storage.admin",
        }
        read_roles = {"roles/storage.legacyBucketReader", "roles/storage.objectViewer"}

        for bucket in all_buckets:
            readable = False
            writable = False

            acl = bucket.acl
            iam = bucket.iam_configuration

            # If uniform access is enabled for this bucket, then all control is bucket-level.
            # No fine-grained (per-object controls) in that case.
            uniform_access = iam["uniformBucketLevelAccess"]["enabled"]

            if not uniform_access:
                # If "legacy" ACL are still enabled, we can look through the granted policies separately.
                # TODO - is this even necessary? The API will generate us a legacy role binding that will be found below.

                granted_entities = acl.get_entities()

                for entity in granted_entities:
                    if entity.type in public_entities:
                        print(
                            f"!! found ACL granting {entity.roles} of type {entity.type} on {bucket.id}"
                        )

                        if "WRITER" in entity.roles:
                            writable = True
                            readable = True
                        elif "READER" in entity.roles:
                            readable = True

            iam_policy = bucket.get_iam_policy()

            for binding in iam_policy.bindings:
                public_policy = len(binding["members"] & public_entities) > 0

                if public_policy:
                    print(f"! found public IAM policy {binding} for bucket {bucket.id}")

                    # Check to see what this role gives us...
                    # TODO - we should check to see what permissions this role actually gives us.
                    if binding["role"] in write_roles:
                        writable = True
                        readable = True
                    elif binding["role"] in read_roles:
                        readable = True

            if writable:
                writable_buckets.append(bucket.id)
            if readable:
                readable_buckets.append(bucket.id)

        if len(writable_buckets) or len(readable_buckets):
            if len(writable_buckets):
                title = "World-writable buckets"
                severity = Severity.HIGH
            else:
                title = "World-readable buckets"
                severity = Severity.LOW
            return [
                Finding(
                    "public_buckets.md",
                    title,
                    severity,
                    readable_buckets=readable_buckets,
                    writable_buckets=writable_buckets,
                )
            ]

        return []
