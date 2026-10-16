from massive import RESTClient

# docs
# https://massive.com/docs/indices/get_v3_snapshot_indices
# https://github.com/massive-com/client-python/blob/master/massive/rest/snapshot.py#

# client = RESTClient("XXXXXX") # hardcoded api_key is used
client = RESTClient()  # MASSIVE_API_KEY environment variable is used

# list_snapshot_indices follows pagination, so this iterates over every index
snapshots = []
for s in client.list_snapshot_indices(limit=250):
    snapshots.append(s)

print(len(snapshots))
print(snapshots[0])
