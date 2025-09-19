# Lookup API Endpoint Information

## Request Lookup Information for a List of Lookups

Returns a list of Lookups of the MLS from the UNLOCK MLS based on the filter parameters included in the request.

## Example Code

### Example URL Request
```markdown
https://api.bridgedataoutput.com/api/v2/OData/{dataset_id}/Lookup?access_token={access_token}
```
### Example Response
```json
{
success: true,
status: 200,
bundle: [
{
LookupKey: "13b63d2d49008f19e865c30bafca238b",
ResourceName: "Office",
LookupName: "OfficeStateOrProvince",
LookupValue: "AL",
StandardLookupValue: "AL",
LegacyODataValue: "",
ModificationTimestamp: "2022-07-05T12:32:48.747Z",
BridgeModificationTimestamp: "2022-07-05T12:32:48.747Z",
FeedTypes: [
]
}
],
total: 1
}
```
### Request Parameters for the URL

| Name | Type | Description |
|------|------|-------------|
| `access_token` | string | Token to identify the user or application. |
| `dataset` | string | Dataset to get the listings from. |
| `$skip` | integer | Skip the first n items |
| `$select` | string | Select properties that are explicitly specified e.g. OfficeType |
| `$unselect` | string | Filter record properties that are explicitly specified e.g. OfficeFax |
| `$top` | integer | Show only the first n items |
| `$orderby` | string | Order items by specified property value, e.g. ModificationTimestamp asc |
| `$filter` | string | Filter items by certain values |
| `$expand` | array | Expand related entities |

### Response Data Dictionary
| Name | Type | Description |
|------|------|-------------|
| `Name` | Type | Description |
| `@odata.context` | string | Link to the metadata context. |
| `@odata.id` | string | Link to the OData endpoint for the specific record. |
| `BridgeModificationTimestamp` | string | A timestamp representing when last this record was modified |
| `LegacyODataValue` | string | LegacyODataValue |
| `LookupKey` | string | LookupKey |
| `LookupName` | string | LookupName |
| `LookupValue` | string | LookupValue |
| `ModificationTimestamp` | string | ModificationTimestamp |
| `ResourceName` | string | ResourceName |
| `StandardLookupValue` | string | StandardLookupValue |