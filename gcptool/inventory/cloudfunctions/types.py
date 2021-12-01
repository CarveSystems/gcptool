# generated by datamodel-codegen:
#   filename:  schemas.json
#   timestamp: 2021-11-29T16:43:15+00:00

from __future__ import annotations

from enum import Enum
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class Type(Enum):
    operation_unspecified = 'OPERATION_UNSPECIFIED'
    create_function = 'CREATE_FUNCTION'
    update_function = 'UPDATE_FUNCTION'
    delete_function = 'DELETE_FUNCTION'


class OperationMetadataV1(BaseModel):
    build_id: Optional[str] = Field(
        None,
        alias='buildId',
        description='The Cloud Build ID of the function created or updated by an API call. This field is only populated for Create and Update operations.',
    )
    version_id: Optional[str] = Field(
        None,
        alias='versionId',
        description='Version id of the function created or updated by an API call. This field is only populated for Create and Update operations.',
    )
    build_name: Optional[str] = Field(
        None,
        alias='buildName',
        description='The Cloud Build Name of the function deployment. This field is only populated for Create and Update operations. `projects//locations//builds/`.',
    )
    request: Optional[Dict[str, Dict[str, Any]]] = Field(
        None, description='The original request that started the operation.'
    )
    type: Optional[Type] = Field(None, description='Type of operation.')
    target: Optional[str] = Field(
        None,
        description='Target of the operation - for example `projects/project-1/locations/region-1/functions/function-1`',
    )
    source_token: Optional[str] = Field(
        None,
        alias='sourceToken',
        description='An identifier for Firebase function sources. Disclaimer: This field is only supported for Firebase function deployments.',
    )
    update_time: Optional[str] = Field(
        None,
        alias='updateTime',
        description='The last update timestamp of the operation.',
    )


class Expr(BaseModel):
    title: Optional[str] = Field(
        None,
        description='Optional. Title for the expression, i.e. a short string describing its purpose. This can be used e.g. in UIs which allow to enter the expression.',
    )
    description: Optional[str] = Field(
        None,
        description='Optional. Description of the expression. This is a longer text which describes the expression, e.g. when hovered over it in a UI.',
    )
    location: Optional[str] = Field(
        None,
        description='Optional. String indicating the location of the expression for error reporting, e.g. a file name and a position in the file.',
    )
    expression: Optional[str] = Field(
        None,
        description='Textual representation of an expression in Common Expression Language syntax.',
    )


class Status(BaseModel):
    code: Optional[int] = Field(
        None,
        description='The status code, which should be an enum value of google.rpc.Code.',
    )
    details: Optional[List[Dict[str, Dict[str, Any]]]] = Field(
        None,
        description='A list of messages that carry the error details. There is a common set of message types for APIs to use.',
    )
    message: Optional[str] = Field(
        None,
        description='A developer-facing error message, which should be in English. Any user-facing error message should be localized and sent in the google.rpc.Status.details field, or localized by the client.',
    )


class Retry(BaseModel):
    pass


class TestIamPermissionsResponse(BaseModel):
    permissions: Optional[List[str]] = Field(
        None,
        description='A subset of `TestPermissionsRequest.permissions` that the caller is allowed.',
    )


class Location(BaseModel):
    labels: Optional[Dict[str, str]] = Field(
        None,
        description='Cross-service attributes for the location. For example {"cloud.googleapis.com/region": "us-east1"}',
    )
    metadata: Optional[Dict[str, Dict[str, Any]]] = Field(
        None,
        description='Service-specific metadata. For example the available capacity at the given location.',
    )
    name: Optional[str] = Field(
        None,
        description='Resource name for the location, which may vary between implementations. For example: `"projects/example-project/locations/us-east1"`',
    )
    display_name: Optional[str] = Field(
        None,
        alias='displayName',
        description='The friendly name for this location, typically a nearby city name. For example, "Tokyo".',
    )
    location_id: Optional[str] = Field(
        None,
        alias='locationId',
        description='The canonical id for this location. For example: `"us-east1"`.',
    )


class SourceRepository(BaseModel):
    deployed_url: Optional[str] = Field(
        None,
        alias='deployedUrl',
        description='Output only. The URL pointing to the hosted repository where the function were defined at the time of deployment. It always points to a specific commit in the format described above.',
    )
    url: Optional[str] = Field(
        None,
        description='The URL pointing to the hosted repository where the function is defined. There are supported Cloud Source Repository URLs in the following formats: To refer to a specific commit: `https://source.developers.google.com/projects/*/repos/*/revisions/*/paths/*` To refer to a moveable alias (branch): `https://source.developers.google.com/projects/*/repos/*/moveable-aliases/*/paths/*` In particular, to refer to HEAD use `master` moveable alias. To refer to a specific fixed alias (tag): `https://source.developers.google.com/projects/*/repos/*/fixed-aliases/*/paths/*` You may omit `paths/*` if you want to use the main directory.',
    )


class SecretVersion(BaseModel):
    version: Optional[str] = Field(
        None,
        description="Version of the secret (version number or the string 'latest'). It is preferrable to use `latest` version with secret volumes as secret value changes are reflected immediately.",
    )
    path: Optional[str] = Field(
        None,
        description="Relative path of the file under the mount path where the secret value for this version will be fetched and made available. For example, setting the mount_path as '/etc/secrets' and path as `/secret_foo` would mount the secret value file at `/etc/secrets/secret_foo`.",
    )


class GenerateUploadUrlRequest(BaseModel):
    pass


class Binding(BaseModel):
    condition: Optional[Expr] = Field(
        None,
        description='The condition that is associated with this binding. If the condition evaluates to `true`, then this binding applies to the current request. If the condition evaluates to `false`, then this binding does not apply to the current request. However, a different role binding might grant the same role to one or more of the principals in this binding. To learn which resources support conditions in their IAM policies, see the [IAM documentation](https://cloud.google.com/iam/help/conditions/resource-policies).',
    )
    role: Optional[str] = Field(
        None,
        description='Role that is assigned to the list of `members`, or principals. For example, `roles/viewer`, `roles/editor`, or `roles/owner`.',
    )
    members: Optional[List[str]] = Field(
        None,
        description='Specifies the principals requesting access for a Cloud Platform resource. `members` can have the following values: * `allUsers`: A special identifier that represents anyone who is on the internet; with or without a Google account. * `allAuthenticatedUsers`: A special identifier that represents anyone who is authenticated with a Google account or a service account. * `user:{emailid}`: An email address that represents a specific Google account. For example, `alice@example.com` . * `serviceAccount:{emailid}`: An email address that represents a service account. For example, `my-other-app@appspot.gserviceaccount.com`. * `group:{emailid}`: An email address that represents a Google group. For example, `admins@example.com`. * `deleted:user:{emailid}?uid={uniqueid}`: An email address (plus unique identifier) representing a user that has been recently deleted. For example, `alice@example.com?uid=123456789012345678901`. If the user is recovered, this value reverts to `user:{emailid}` and the recovered user retains the role in the binding. * `deleted:serviceAccount:{emailid}?uid={uniqueid}`: An email address (plus unique identifier) representing a service account that has been recently deleted. For example, `my-other-app@appspot.gserviceaccount.com?uid=123456789012345678901`. If the service account is undeleted, this value reverts to `serviceAccount:{emailid}` and the undeleted service account retains the role in the binding. * `deleted:group:{emailid}?uid={uniqueid}`: An email address (plus unique identifier) representing a Google group that has been recently deleted. For example, `admins@example.com?uid=123456789012345678901`. If the group is recovered, this value reverts to `group:{emailid}` and the recovered group retains the role in the binding. * `domain:{domain}`: The G Suite domain (primary) that represents all the users of that domain. For example, `google.com` or `example.com`. ',
    )


class LogType(Enum):
    log_type_unspecified = 'LOG_TYPE_UNSPECIFIED'
    admin_read = 'ADMIN_READ'
    data_write = 'DATA_WRITE'
    data_read = 'DATA_READ'


class AuditLogConfig(BaseModel):
    log_type: Optional[LogType] = Field(
        None, alias='logType', description='The log type that this config enables.'
    )
    exempted_members: Optional[List[str]] = Field(
        None,
        alias='exemptedMembers',
        description='Specifies the identities that do not cause logging for this type of permission. Follows the same format of Binding.members.',
    )


class SecretEnvVar(BaseModel):
    key: Optional[str] = Field(None, description='Name of the environment variable.')
    secret: Optional[str] = Field(
        None,
        description='Name of the secret in secret manager (not the full resource name).',
    )
    project_id: Optional[str] = Field(
        None,
        alias='projectId',
        description="Project identifier (preferrably project number but can also be the project ID) of the project that contains the secret. If not set, it will be populated with the function's project assuming that the secret exists in the same project as of the function.",
    )
    version: Optional[str] = Field(
        None,
        description="Version of the secret (version number or the string 'latest'). It is recommended to use a numeric version for secret environment variables as any updates to the secret value is not reflected until new clones start.",
    )


class IngressSettings(Enum):
    ingress_settings_unspecified = 'INGRESS_SETTINGS_UNSPECIFIED'
    allow_all = 'ALLOW_ALL'
    allow_internal_only = 'ALLOW_INTERNAL_ONLY'
    allow_internal_and_gclb = 'ALLOW_INTERNAL_AND_GCLB'


class VpcConnectorEgressSettings(Enum):
    vpc_connector_egress_settings_unspecified = (
        'VPC_CONNECTOR_EGRESS_SETTINGS_UNSPECIFIED'
    )
    private_ranges_only = 'PRIVATE_RANGES_ONLY'
    all_traffic = 'ALL_TRAFFIC'


class Status1(Enum):
    cloud_function_status_unspecified = 'CLOUD_FUNCTION_STATUS_UNSPECIFIED'
    active = 'ACTIVE'
    offline = 'OFFLINE'
    deploy_in_progress = 'DEPLOY_IN_PROGRESS'
    delete_in_progress = 'DELETE_IN_PROGRESS'
    unknown = 'UNKNOWN'


class FailurePolicy(BaseModel):
    retry: Optional[Retry] = Field(
        None,
        description='If specified, then the function will be retried in case of a failure.',
    )


class SecurityLevel(Enum):
    security_level_unspecified = 'SECURITY_LEVEL_UNSPECIFIED'
    secure_always = 'SECURE_ALWAYS'
    secure_optional = 'SECURE_OPTIONAL'


class HttpsTrigger(BaseModel):
    url: Optional[str] = Field(
        None, description='Output only. The deployed url for the function.'
    )
    security_level: Optional[SecurityLevel] = Field(
        None, alias='securityLevel', description='The security level for the function.'
    )


class GenerateDownloadUrlResponse(BaseModel):
    download_url: Optional[str] = Field(
        None,
        alias='downloadUrl',
        description='The generated Google Cloud Storage signed URL that should be used for function source code download.',
    )


class GenerateDownloadUrlRequest(BaseModel):
    version_id: Optional[str] = Field(
        None,
        alias='versionId',
        description='The optional version of function. If not set, default, current version is used.',
    )


class TestIamPermissionsRequest(BaseModel):
    permissions: Optional[List[str]] = Field(
        None,
        description="The set of permissions to check for the `resource`. Permissions with wildcards (such as '*' or 'storage.*') are not allowed. For more information see [IAM Overview](https://cloud.google.com/iam/docs/overview#permissions).",
    )


class CallFunctionRequest(BaseModel):
    data: Optional[str] = Field(
        None, description='Required. Input to be passed to the function.'
    )


class CallFunctionResponse(BaseModel):
    execution_id: Optional[str] = Field(
        None, alias='executionId', description='Execution id of function invocation.'
    )
    result: Optional[str] = Field(
        None,
        description='Result populated for successful execution of synchronous function. Will not be populated if function does not return a result through context.',
    )
    error: Optional[str] = Field(
        None,
        description='Either system or user-function generated error. Set if execution was not successful.',
    )


class GenerateUploadUrlResponse(BaseModel):
    upload_url: Optional[str] = Field(
        None,
        alias='uploadUrl',
        description='The generated Google Cloud Storage signed URL that should be used for a function source code upload. The uploaded file should be a zip archive which contains a function.',
    )


class Operation(BaseModel):
    metadata: Optional[Dict[str, Dict[str, Any]]] = Field(
        None,
        description='Service-specific metadata associated with the operation. It typically contains progress information and common metadata such as create time. Some services might not provide such metadata. Any method that returns a long-running operation should document the metadata type, if any.',
    )
    done: Optional[bool] = Field(
        None,
        description='If the value is `false`, it means the operation is still in progress. If `true`, the operation is completed, and either `error` or `response` is available.',
    )
    error: Optional[Status] = Field(
        None,
        description='The error result of the operation in case of failure or cancellation.',
    )
    name: Optional[str] = Field(
        None,
        description='The server-assigned name, which is only unique within the same service that originally returns it. If you use the default HTTP mapping, the `name` should be a resource name ending with `operations/{unique_id}`.',
    )
    response: Optional[Dict[str, Dict[str, Any]]] = Field(
        None,
        description='The normal response of the operation in case of success. If the original method returns no data on success, such as `Delete`, the response is `google.protobuf.Empty`. If the original method is standard `Get`/`Create`/`Update`, the response should be the resource. For other methods, the response should have the type `XxxResponse`, where `Xxx` is the original method name. For example, if the original method name is `TakeSnapshot()`, the inferred response type is `TakeSnapshotResponse`.',
    )


class ListLocationsResponse(BaseModel):
    locations: Optional[List[Location]] = Field(
        None,
        description='A list of locations that matches the specified filter in the request.',
    )
    next_page_token: Optional[str] = Field(
        None, alias='nextPageToken', description='The standard List next-page token.'
    )


class SecretVolume(BaseModel):
    secret: Optional[str] = Field(
        None,
        description='Name of the secret in secret manager (not the full resource name).',
    )
    mount_path: Optional[str] = Field(
        None,
        alias='mountPath',
        description='The path within the container to mount the secret volume. For example, setting the mount_path as `/etc/secrets` would mount the secret value files under the `/etc/secrets` directory. This directory will also be completely shadowed and unavailable to mount any other secrets. Recommended mount paths: /etc/secrets Restricted mount paths: /cloudsql, /dev/log, /pod, /proc, /var/log',
    )
    project_id: Optional[str] = Field(
        None,
        alias='projectId',
        description="Project identifier (preferrably project number but can also be the project ID) of the project that contains the secret. If not set, it will be populated with the function's project assuming that the secret exists in the same project as of the function.",
    )
    versions: Optional[List[SecretVersion]] = Field(
        None,
        description='List of secret versions to mount for this secret. If empty, the `latest` version of the secret will be made available in a file named after the secret under the mount point.',
    )


class AuditConfig(BaseModel):
    audit_log_configs: Optional[List[AuditLogConfig]] = Field(
        None,
        alias='auditLogConfigs',
        description='The configuration for logging of each type of permission.',
    )
    service: Optional[str] = Field(
        None,
        description='Specifies a service that will be enabled for audit logging. For example, `storage.googleapis.com`, `cloudsql.googleapis.com`. `allServices` is a special value that covers all services.',
    )


class EventTrigger(BaseModel):
    service: Optional[str] = Field(
        None,
        description='The hostname of the service that should be observed. If no string is provided, the default service implementing the API will be used. For example, `storage.googleapis.com` is the default for all event types in the `google.storage` namespace.',
    )
    event_type: Optional[str] = Field(
        None,
        alias='eventType',
        description="Required. The type of event to observe. For example: `providers/cloud.storage/eventTypes/object.change` and `providers/cloud.pubsub/eventTypes/topic.publish`. Event types match pattern `providers/*/eventTypes/*.*`. The pattern contains: 1. namespace: For example, `cloud.storage` and `google.firebase.analytics`. 2. resource type: The type of resource on which event occurs. For example, the Google Cloud Storage API includes the type `object`. 3. action: The action that generates the event. For example, action for a Google Cloud Storage Object is 'change'. These parts are lower case.",
    )
    resource: Optional[str] = Field(
        None,
        description='Required. The resource(s) from which to observe events, for example, `projects/_/buckets/myBucket`. Not all syntactically correct values are accepted by all services. For example: 1. The authorization model must support it. Google Cloud Functions only allows EventTriggers to be deployed that observe resources in the same project as the `CloudFunction`. 2. The resource type must match the pattern expected for an `event_type`. For example, an `EventTrigger` that has an `event_type` of "google.pubsub.topic.publish" should have a resource that matches Google Cloud Pub/Sub topics. Additionally, some services may support short names when creating an `EventTrigger`. These will always be returned in the normalized "long" format. See each *service\'s* documentation for supported formats.',
    )
    failure_policy: Optional[FailurePolicy] = Field(
        None,
        alias='failurePolicy',
        description='Specifies policy for failed executions.',
    )


class ListOperationsResponse(BaseModel):
    operations: Optional[List[Operation]] = Field(
        None,
        description='A list of operations that matches the specified filter in the request.',
    )
    next_page_token: Optional[str] = Field(
        None, alias='nextPageToken', description='The standard List next-page token.'
    )


class Policy(BaseModel):
    bindings: Optional[List[Binding]] = Field(
        None,
        description='Associates a list of `members`, or principals, with a `role`. Optionally, may specify a `condition` that determines how and when the `bindings` are applied. Each of the `bindings` must contain at least one principal. The `bindings` in a `Policy` can refer to up to 1,500 principals; up to 250 of these principals can be Google groups. Each occurrence of a principal counts towards these limits. For example, if the `bindings` grant 50 different roles to `user:alice@example.com`, and not to any other principal, then you can add another 1,450 principals to the `bindings` in the `Policy`.',
    )
    etag: Optional[str] = Field(
        None,
        description='`etag` is used for optimistic concurrency control as a way to help prevent simultaneous updates of a policy from overwriting each other. It is strongly suggested that systems make use of the `etag` in the read-modify-write cycle to perform policy updates in order to avoid race conditions: An `etag` is returned in the response to `getIamPolicy`, and systems are expected to put that etag in the request to `setIamPolicy` to ensure that their change will be applied to the same version of the policy. **Important:** If you use IAM Conditions, you must include the `etag` field whenever you call `setIamPolicy`. If you omit this field, then IAM allows you to overwrite a version `3` policy with a version `1` policy, and all of the conditions in the version `3` policy are lost.',
    )
    audit_configs: Optional[List[AuditConfig]] = Field(
        None,
        alias='auditConfigs',
        description='Specifies cloud audit logging configuration for this policy.',
    )
    version: Optional[int] = Field(
        None,
        description='Specifies the format of the policy. Valid values are `0`, `1`, and `3`. Requests that specify an invalid value are rejected. Any operation that affects conditional role bindings must specify version `3`. This requirement applies to the following operations: * Getting a policy that includes a conditional role binding * Adding a conditional role binding to a policy * Changing a conditional role binding in a policy * Removing any role binding, with or without a condition, from a policy that includes conditions **Important:** If you use IAM Conditions, you must include the `etag` field whenever you call `setIamPolicy`. If you omit this field, then IAM allows you to overwrite a version `3` policy with a version `1` policy, and all of the conditions in the version `3` policy are lost. If a policy does not include any conditions, operations on that policy may specify any valid version or leave the field unset. To learn which resources support conditions in their IAM policies, see the [IAM documentation](https://cloud.google.com/iam/help/conditions/resource-policies).',
    )


class CloudFunction(BaseModel):
    min_instances: Optional[int] = Field(
        None,
        alias='minInstances',
        description='A lower bound for the number function instances that may coexist at a given time.',
    )
    update_time: Optional[str] = Field(
        None,
        alias='updateTime',
        description='Output only. The last update timestamp of a Cloud Function.',
    )
    labels: Optional[Dict[str, str]] = Field(
        None, description='Labels associated with this Cloud Function.'
    )
    source_token: Optional[str] = Field(
        None,
        alias='sourceToken',
        description='Input only. An identifier for Firebase function sources. Disclaimer: This field is only supported for Firebase function deployments.',
    )
    build_name: Optional[str] = Field(
        None,
        alias='buildName',
        description='Output only. The Cloud Build Name of the function deployment. `projects//locations//builds/`.',
    )
    source_archive_url: Optional[str] = Field(
        None,
        alias='sourceArchiveUrl',
        description='The Google Cloud Storage URL, starting with `gs://`, pointing to the zip archive which contains the function.',
    )
    kms_key_name: Optional[str] = Field(
        None,
        alias='kmsKeyName',
        description="Resource name of a KMS crypto key (managed by the user) used to encrypt/decrypt function resources. It must match the pattern `projects/{project}/locations/{location}/keyRings/{key_ring}/cryptoKeys/{crypto_key}`. If specified, you must also provide an artifact registry repository using the `docker_repository` field that was created with the same KMS crypto key. The following service accounts need to be granted the role 'Cloud KMS CryptoKey Encrypter/Decrypter (roles/cloudkms.cryptoKeyEncrypterDecrypter)' on the Key/KeyRing/Project/Organization (least access preferred). 1. Google Cloud Functions service account (service-{project_number}@gcf-admin-robot.iam.gserviceaccount.com) - Required to protect the function's image. 2. Google Storage service account (service-{project_number}@gs-project-accounts.iam.gserviceaccount.com) - Required to protect the function's source code. If this service account does not exist, deploying a function without a KMS key or retrieving the service agent name provisions it. For more information, see https://cloud.google.com/storage/docs/projects#service-agents and https://cloud.google.com/storage/docs/getting-service-agent#gsutil. Google Cloud Functions delegates access to service agents to protect function resources in internal projects that are not accessible by the end user.",
    )
    ingress_settings: Optional[IngressSettings] = Field(
        None,
        alias='ingressSettings',
        description='The ingress settings for the function, controlling what traffic can reach it.',
    )
    build_worker_pool: Optional[str] = Field(
        None,
        alias='buildWorkerPool',
        description='Name of the Cloud Build Custom Worker Pool that should be used to build the function. The format of this field is `projects/{project}/locations/{region}/workerPools/{workerPool}` where `{project}` and `{region}` are the project id and region respectively where the worker pool is defined and `{workerPool}` is the short name of the worker pool. If the project id is not the same as the function, then the Cloud Functions Service Agent (`service-@gcf-admin-robot.iam.gserviceaccount.com`) must be granted the role Cloud Build Custom Workers Builder (`roles/cloudbuild.customworkers.builder`) in the project.',
    )
    environment_variables: Optional[Dict[str, str]] = Field(
        None,
        alias='environmentVariables',
        description='Environment variables that shall be available during function execution.',
    )
    available_memory_mb: Optional[int] = Field(
        None,
        alias='availableMemoryMb',
        description='The amount of memory in MB available for a function. Defaults to 256MB.',
    )
    event_trigger: Optional[EventTrigger] = Field(
        None,
        alias='eventTrigger',
        description='A source that fires events in response to a condition in another service.',
    )
    build_id: Optional[str] = Field(
        None,
        alias='buildId',
        description='Output only. The Cloud Build ID of the latest successful deployment of the function.',
    )
    vpc_connector_egress_settings: Optional[VpcConnectorEgressSettings] = Field(
        None,
        alias='vpcConnectorEgressSettings',
        description='The egress settings for the connector, controlling what traffic is diverted through it.',
    )
    network: Optional[str] = Field(
        None,
        description='The VPC Network that this cloud function can connect to. It can be either the fully-qualified URI, or the short name of the network resource. If the short network name is used, the network must belong to the same project. Otherwise, it must belong to a project within the same organization. The format of this field is either `projects/{project}/global/networks/{network}` or `{network}`, where `{project}` is a project id where the network is defined, and `{network}` is the short name of the network. This field is mutually exclusive with `vpc_connector` and will be replaced by it. See [the VPC documentation](https://cloud.google.com/compute/docs/vpc) for more information on connecting Cloud projects.',
    )
    timeout: Optional[str] = Field(
        None,
        description='The function execution timeout. Execution is considered failed and can be terminated if the function is not completed at the end of the timeout period. Defaults to 60 seconds.',
    )
    secret_environment_variables: Optional[List[SecretEnvVar]] = Field(
        None,
        alias='secretEnvironmentVariables',
        description='Secret environment variables configuration.',
    )
    version_id: Optional[str] = Field(
        None,
        alias='versionId',
        description='Output only. The version identifier of the Cloud Function. Each deployment attempt results in a new version of a function being created.',
    )
    https_trigger: Optional[HttpsTrigger] = Field(
        None,
        alias='httpsTrigger',
        description='An HTTPS endpoint type of source that can be triggered via URL.',
    )
    max_instances: Optional[int] = Field(
        None,
        alias='maxInstances',
        description='The limit on the maximum number of function instances that may coexist at a given time. In some cases, such as rapid traffic surges, Cloud Functions may, for a short period of time, create more instances than the specified max instances limit. If your function cannot tolerate this temporary behavior, you may want to factor in a safety margin and set a lower max instances value than your function can tolerate. See the [Max Instances](https://cloud.google.com/functions/docs/max-instances) Guide for more details.',
    )
    entry_point: Optional[str] = Field(
        None,
        alias='entryPoint',
        description='The name of the function (as defined in source code) that will be executed. Defaults to the resource name suffix, if not specified. For backward compatibility, if function with given name is not found, then the system will try to use function named "function". For Node.js this is name of a function exported by the module specified in `source_location`.',
    )
    vpc_connector: Optional[str] = Field(
        None,
        alias='vpcConnector',
        description='The VPC Network Connector that this cloud function can connect to. It can be either the fully-qualified URI, or the short name of the network connector resource. The format of this field is `projects/*/locations/*/connectors/*` This field is mutually exclusive with `network` field and will eventually replace it. See [the VPC documentation](https://cloud.google.com/compute/docs/vpc) for more information on connecting Cloud projects.',
    )
    build_environment_variables: Optional[Dict[str, str]] = Field(
        None,
        alias='buildEnvironmentVariables',
        description='Build environment variables that shall be available during build time.',
    )
    runtime: Optional[str] = Field(
        None,
        description='The runtime in which to run the function. Required when deploying a new function, optional when updating an existing function. For a complete list of possible choices, see the [`gcloud` command reference](https://cloud.google.com/sdk/gcloud/reference/functions/deploy#--runtime).',
    )
    docker_repository: Optional[str] = Field(
        None,
        alias='dockerRepository',
        description="User managed repository created in Artifact Registry optionally with a customer managed encryption key. If specified, deployments will use Artifact Registry. If unspecified and the deployment is eligible to use Artifact Registry, GCF will create and use a repository named 'gcf-artifacts' for every deployed region. This is the repository to which the function docker image will be pushed after it is built by Cloud Build. It must match the pattern `projects/{project}/locations/{location}/repositories/{repository}`. Cross-project repositories are not supported. Cross-location repositories are not supported. Repository format must be 'DOCKER'.",
    )
    service_account_email: Optional[str] = Field(
        None,
        alias='serviceAccountEmail',
        description="The email of the function's service account. If empty, defaults to `{project_id}@appspot.gserviceaccount.com`.",
    )
    secret_volumes: Optional[List[SecretVolume]] = Field(
        None, alias='secretVolumes', description='Secret volumes configuration.'
    )
    status: Optional[Status1] = Field(
        None, description='Output only. Status of the function deployment.'
    )
    description: Optional[str] = Field(
        None, description='User-provided description of a function.'
    )
    source_upload_url: Optional[str] = Field(
        None,
        alias='sourceUploadUrl',
        description='The Google Cloud Storage signed URL used for source uploading, generated by calling [google.cloud.functions.v1.GenerateUploadUrl]. The signature is validated on write methods (Create, Update) The signature is stripped from the Function object on read methods (Get, List)',
    )
    name: Optional[str] = Field(
        None,
        description='A user-defined name of the function. Function names must be unique globally and match pattern `projects/*/locations/*/functions/*`',
    )
    source_repository: Optional[SourceRepository] = Field(
        None,
        alias='sourceRepository',
        description='**Beta Feature** The source repository where a function is hosted.',
    )


class SetIamPolicyRequest(BaseModel):
    update_mask: Optional[str] = Field(
        None,
        alias='updateMask',
        description='OPTIONAL: A FieldMask specifying which fields of the policy to modify. Only the fields in the mask will be modified. If no mask is provided, the following default mask is used: `paths: "bindings, etag"`',
    )
    policy: Optional[Policy] = Field(
        None,
        description='REQUIRED: The complete policy to be applied to the `resource`. The size of the policy is limited to a few 10s of KB. An empty policy is a valid policy but certain Cloud Platform services (such as Projects) might reject them.',
    )


class ListFunctionsResponse(BaseModel):
    functions: Optional[List[CloudFunction]] = Field(
        None, description='The functions that match the request.'
    )
    unreachable: Optional[List[str]] = Field(
        None,
        description='Locations that could not be reached. The response does not include any functions from these locations.',
    )
    next_page_token: Optional[str] = Field(
        None,
        alias='nextPageToken',
        description='If not empty, indicates that there may be more functions that match the request; this value should be passed in a new google.cloud.functions.v1.ListFunctionsRequest to get more functions.',
    )


class Model(BaseModel):
    operation_metadata_v1: Optional[OperationMetadataV1] = Field(
        None, alias='OperationMetadataV1'
    )
    expr: Optional[Expr] = Field(None, alias='Expr')
    list_operations_response: Optional[ListOperationsResponse] = Field(
        None, alias='ListOperationsResponse'
    )
    retry: Optional[Retry] = Field(None, alias='Retry')
    test_iam_permissions_response: Optional[TestIamPermissionsResponse] = Field(
        None, alias='TestIamPermissionsResponse'
    )
    list_locations_response: Optional[ListLocationsResponse] = Field(
        None, alias='ListLocationsResponse'
    )
    source_repository: Optional[SourceRepository] = Field(
        None, alias='SourceRepository'
    )
    status: Optional[Status] = Field(None, alias='Status')
    secret_volume: Optional[SecretVolume] = Field(None, alias='SecretVolume')
    generate_upload_url_request: Optional[GenerateUploadUrlRequest] = Field(
        None, alias='GenerateUploadUrlRequest'
    )
    policy: Optional[Policy] = Field(None, alias='Policy')
    secret_env_var: Optional[SecretEnvVar] = Field(None, alias='SecretEnvVar')
    binding: Optional[Binding] = Field(None, alias='Binding')
    cloud_function: Optional[CloudFunction] = Field(None, alias='CloudFunction')
    secret_version: Optional[SecretVersion] = Field(None, alias='SecretVersion')
    event_trigger: Optional[EventTrigger] = Field(None, alias='EventTrigger')
    audit_config: Optional[AuditConfig] = Field(None, alias='AuditConfig')
    failure_policy: Optional[FailurePolicy] = Field(None, alias='FailurePolicy')
    set_iam_policy_request: Optional[SetIamPolicyRequest] = Field(
        None, alias='SetIamPolicyRequest'
    )
    generate_download_url_response: Optional[GenerateDownloadUrlResponse] = Field(
        None, alias='GenerateDownloadUrlResponse'
    )
    generate_download_url_request: Optional[GenerateDownloadUrlRequest] = Field(
        None, alias='GenerateDownloadUrlRequest'
    )
    location: Optional[Location] = Field(None, alias='Location')
    test_iam_permissions_request: Optional[TestIamPermissionsRequest] = Field(
        None, alias='TestIamPermissionsRequest'
    )
    call_function_request: Optional[CallFunctionRequest] = Field(
        None, alias='CallFunctionRequest'
    )
    list_functions_response: Optional[ListFunctionsResponse] = Field(
        None, alias='ListFunctionsResponse'
    )
    audit_log_config: Optional[AuditLogConfig] = Field(None, alias='AuditLogConfig')
    https_trigger: Optional[HttpsTrigger] = Field(None, alias='HttpsTrigger')
    call_function_response: Optional[CallFunctionResponse] = Field(
        None, alias='CallFunctionResponse'
    )
    operation: Optional[Operation] = Field(None, alias='Operation')
    generate_upload_url_response: Optional[GenerateUploadUrlResponse] = Field(
        None, alias='GenerateUploadUrlResponse'
    )
