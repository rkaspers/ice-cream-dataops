"""Check the capabilities of the icapi_extractors group in CDF"""
from cognite.client import CogniteClient
from cognite.client.credentials import OAuthClientCredentials
from dotenv import load_dotenv
import json
import os

# Load environment variables from .env file
load_dotenv()

# Get credentials from environment
client_id = os.getenv("IDP_CLIENT_ID")
client_secret = os.getenv("IDP_CLIENT_SECRET")
tenant_id = os.getenv("IDP_TENANT_ID")
project = os.getenv("CDF_PROJECT")
cluster = os.getenv("CDF_CLUSTER", "westeurope-1")

if not all([client_id, client_secret, tenant_id, project]):
    print("ERROR: Missing required environment variables!")
    print(f"IDP_CLIENT_ID: {'✓' if client_id else '✗'}")
    print(f"IDP_CLIENT_SECRET: {'✓' if client_secret else '✗'}")
    print(f"IDP_TENANT_ID: {'✓' if tenant_id else '✗'}")
    print(f"CDF_PROJECT: {'✓' if project else '✗'}")
    exit(1)

print(f"Connecting to CDF project: {project}")
print(f"Using cluster: {cluster}")
print("-" * 80)

# Create the client
try:
    client = CogniteClient.default_oauth_client_credentials(
        project=project,
        tenant_id=tenant_id,
        client_id=client_id,
        client_secret=client_secret,
        cdf_cluster=cluster
    )
    print("✓ Successfully authenticated\n")
except Exception as e:
    print(f"✗ Authentication failed: {e}")
    exit(1)

# Find the icapi_extractors group
print("Fetching groups...")
groups = client.iam.groups.list(all=True)

# Find our specific group
target_group = None
for group in groups:
    if group.name == "icapi_extractors":
        target_group = group
        break

if not target_group:
    print("✗ Group 'icapi_extractors' not found!")
    print("\nAvailable groups:")
    for group in groups:
        print(f"  - {group.name}")
    exit(1)

print(f"✓ Found group: {target_group.name}")
print(f"  Source ID: {target_group.source_id}")
print("\n" + "=" * 80)
print("CAPABILITIES:")
print("=" * 80)

# Display each capability in a readable format
for i, capability in enumerate(target_group.capabilities, 1):
    cap_dict = capability.dump(camel_case=False)
    cap_name = list(cap_dict.keys())[0]
    cap_details = cap_dict[cap_name]
    
    print(f"\n{i}. {cap_name}")
    print(f"   Actions: {', '.join(cap_details.get('actions', []))}")
    
    scope = cap_details.get('scope', {})
    if 'all' in scope:
        print(f"   Scope: ALL")
    elif 'dataset_scope' in scope or 'datasetScope' in scope:
        dataset_scope = scope.get('dataset_scope') or scope.get('datasetScope', {})
        ids = dataset_scope.get('ids', [])
        print(f"   Scope: Dataset - {ids}")
    elif 'space_id_scope' in scope or 'spaceIdScope' in scope:
        space_scope = scope.get('space_id_scope') or scope.get('spaceIdScope', {})
        space_ids = space_scope.get('space_ids') or space_scope.get('spaceIds', [])
        print(f"   Scope: Spaces - {space_ids}")
    elif 'id_scope' in scope or 'idScope' in scope:
        id_scope = scope.get('id_scope') or scope.get('idScope', {})
        ids = id_scope.get('ids', [])
        print(f"   Scope: IDs - {ids}")
    elif 'table_scope' in scope or 'tableScope' in scope:
        table_scope = scope.get('table_scope') or scope.get('tableScope', {})
        dbs = table_scope.get('dbs_to_tables') or table_scope.get('dbsToTables', {})
        print(f"   Scope: Tables - {dbs}")
    elif 'currentuserscope' in scope or 'current_user_scope' in scope:
        print(f"   Scope: Current User")
    else:
        print(f"   Scope: {scope}")

print("\n" + "=" * 80)
print("\nKEY CHECKS FOR EXTRACTOR:")
print("=" * 80)

# Check for specific required capabilities
has_dm_instances = False
dm_instances_scope = None
has_datasets_owner = False

for capability in target_group.capabilities:
    cap_dict = capability.dump(camel_case=False)
    
    if 'data_model_instances_acl' in cap_dict:
        cap = cap_dict['data_model_instances_acl']
        has_dm_instances = 'WRITE' in cap.get('actions', [])
        dm_instances_scope = cap.get('scope', {})
    
    if 'datasets_acl' in cap_dict:
        cap = cap_dict['datasets_acl']
        has_datasets_owner = 'OWNER' in cap.get('actions', [])

print(f"\n✓ dataModelInstancesAcl with WRITE: {'YES ✓' if has_dm_instances else 'NO ✗'}")
if has_dm_instances:
    if 'all' in dm_instances_scope:
        print(f"  └─ Scope: ALL ✓")
    else:
        print(f"  └─ Scope: {dm_instances_scope} (may need to be 'all')")

print(f"✓ datasetsAcl with OWNER: {'YES ✓' if has_datasets_owner else 'NO ✗'}")

if has_dm_instances and has_datasets_owner:
    print("\n✓ Group has the required permissions for writing data model instances!")
else:
    print("\n✗ Group is missing required permissions.")

