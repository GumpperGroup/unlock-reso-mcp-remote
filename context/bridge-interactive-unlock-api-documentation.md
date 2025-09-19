# Bridge Documentation

Bridge is a data distribution platform that allows MLSs and other data providers to manage licensing, billing and data access using APIs built on modern industry standards.

For software developers, the platform standardizes how you access MLS datasets and other real estate data in the United States and Canada. MLS data is normalized to RESO Data Dictionary standards and made available through a variety of transports, including RESO Web API and RETS.

## Support and Updates

Recent updates to the platform and functionality can be found here: https://www.bridgeinteractive.com/bridge-platform-updates/

If you have any questions about using the APIs available on the platform, contact support at api@bridgeinteractive.com.

For questions related to MLS licensing agreements and listing data, it's usually best to talk to the MLS directly, as all access is at their discretion.

At this time support is only offered in English.

## Getting started with the Bridge Platform

The Bridge platform is comprised of two components:

- The platform dashboard: for managing data access, API tokens and documentation.
- The data transports: RESO Web API, RETS and Bridge Web API.

Access to the Bridge platform is typically initiated by the MLS. If you are looking to access MLS data, first contact the relevant MLS to request an invite to the platform.

### Step 1: Registering on the Bridge platform

If you are invited directly by a data provider to the Bridge platform, click the link in the email invitation and follow the prompts to complete the registration process.

Once registered, you will be able to log into the dashboard to manage various aspects of your applications, including getting API tokens and data. If the data provider has included data licenses in your invitation, you'll be able to execute the agreements and manage your billing if applicable.

#### What is an application?

An application represents a product that consumes data using the API and requires a distinct API token. Elements linked to an application include:

- The application profile
- API tokens
- Data access approvals for various datasets
- API traffic logs

When registering your account, your first application is automatically generated. While most users will only need a single application, you may create as many as you need. Typically you'll only need more than one if you are receiving multiple feeds from a single MLS.

For example, if you are receiving an IDX feed and a VOW feed from a single MLS, then you will need to create an additional application for the second feed. This can then be re-used for other MLSs that also want to give multiple feeds. Note that you will now have two sets of API access tokens - one for each type of feed.

#### Your Primary application

By default, your first application is set as the Primary application. Any data access that is shared with you (either from an MLS invite or by a Broker) is provisioned against your Primary application. You can specify which application is Primary under Application Settings on the dashboard.

#### Application Profile

Your application profile is shown to data providers during the approval process, and allows you to add details that will help them decide whether or not to grant access and what type of data feed you should get.

If you are a vendor working with a specific brokerage, be sure to include the brokerage name and contact details.

Including details about what data you need, as well as how and where the data will be used, will speed up the approval process. Consider adding a link to your application or website, as well as screenshots to help provide context for your request.

> **Note:** Each application will have its own profile, and they can be updated at any time.

#### Merging Accounts

If you have more than one account on the platform, you may use the tool in your account settings to merge them together. By doing so, you will combine all the applications, users, agreements and payment profiles into a single account. You will require the platform credentials for the account you wish to merge.

Since all the users will still be active, you are able to sign into the platform with any of the credentials. You may de-activate a user by adjusting your account settings.

Accounts can only be merged if they have the same role (broker, agent or vendor). If you require the account role to be updated, please reach out to support.

Account merges cannot be undone.

### Step 2: Data Access

The Bridge platform allows you to request data access from any of our customer data providers. All datasets available through the platform require approval from the data provider. Whether they approve your request, or what is required to get that approval, is at their discretion. In some cases, data providers may require you to execute data license agreements, pay fees or do compliance testing.

A list of available datasets you can apply for can be found in your dashboard. Not all available MLSs are listed here; some have additional requirements you must fulfil in order to apply for the dataset.

If you are a member of an MLS that you want to work with, and you do not see that MLS on the dashboard, please reach out to support to see if we are able to facilitate access.

If you have been invited onto the platform by an MLS, your Primary application will automatically have data access to that MLS in a pending state. Once the MLS makes final approval, that status will change to "Approved", and you will be able to retrieve data via the API.

#### Data Access Statuses

- **Pending:** Your application has been submitted to the data provider and is pending approval.
- **Approved:** Your application has been approved by the data provider, and the data is available through the Bridge.
- **Denied:** Your application has been denied for a data license. A reason will be supplied when you are notified of this status change. You may apply again if desired.
- **Suspended:** Your application has been temporarily suspended.
- **Revoked:** The data provider has revoked your access to their data. The data feed for this resource is no longer available. You will need to reapply to regain access.

#### Combined Feed Types

MLSs may approve a single application for multiple feed types. This is done to create efficiencies for data consumers, who may have multiple data licenses with an MLS.

By combining multiple feed types within a single approval, instead of maintaining two or more feeds with similar data, all the data available to you from the MLS is accessible in one.

The API response will include a superset of all available listings, while still respecting the underlying rules for each type.

##### Managing Combined Feed Types

Each record in an API response contains the field "FeedTypes". This automatically-generated field indicates which feed type(s) the record is sourced from - and therefore what license rules would be applicable.

##### Splitting combined feeds

While the FeedTypes field itself not queryable, you are able to split a combined feed into its individual components by adding the feed type metadata tag into the API path:

| Example | Query |
|---------|-------|
| **Return only IDX properties from a combined feed** | `https://api.bridgedataoutput.com/api/v2/OData/{dataset_id}/idx/Properties` |

##### Field level rules

In addition to knowing which license type governs a listing, you are also able to use the API to determine the licenses type for each field. This is important for the scenario where a listing is sourced from multiple feed types that have different field payloads.

Since the payloads are combined, this functionality makes it easier to determine which fields are allowed to be used for each feed type. This information is available using the "FieldRules" resource. This resource allows you to answer the following two questions:

- "What data licenses back this field?"
- "What fields can be used as part of this data license"

The values returned in this resource are automatically derived from the field payloads available as part of the underlying feed types that make up your combined feeds.

Note that fields in this resource are not queryable. If you'd like to see only the relevant fields for a specific subset of a combined feed you may include the feed type metadata tag into the URL path:

| Example | Query |
|---------|-------|
| **Return only IDX fields** | `https://api.bridgedataoutput.com/api/v2/OData/{dataset_id}/idx/Field` |

#### Test datasets

Every application is automatically approved for access a Test dataset. This is machine-generated and useful when trying an initial integration with the platform using generic, static data. Note that test data may not accurately match real data that will be provisioned, which will vary between MLSs.

This dataset should not be used for building production integration tests, as it is subject to change.

### Step 3: Using the APIs

The platform offers various transport mechanisms to choose from when accessing MLS data:

- RESO Web API
- RETS
- Our proprietary Bridge Web API

All APIs make the same data available (ie whatever the specific data provider has allowed you access to). For MLS data, we recommend using the RESO Web API, as it conforms to the latest industry standards and will provide the most interoperability with other MLS data distribution platforms.

MLS data is normalized to RESO Data Dictionary standards. Any fields that are not able to be normalized to the RESO Data Dictionary are name-spaced with a prefix corresponding to the dataset.

Each API request should contain the dataset code of the MLS, the resource you are querying, your access token, and any parameters you'd like to use to constrain the result set. HTTPS is required, as the Bridge only respond to encrypted traffic.

> **Note:** Program defensively! MLS data is prone to change as data providers have the ability to update restrictions and field payloads at their discretion. To avoid disruption, we recommend that you program with this expectation in mind.

#### Dataset Codes

All API requests need to include a dataset code. This indicates which dataset you wish to query and either represents a specific data provider or a virtual dataset consisting of multiple MLS datasets.

#### Resources

Records are organized into standardized resources: typically Properties, Members, and Offices. Most MLSs will also have Open Houses available and possibly other resources like Rooms and UnitTypes.

#### API Access Tokens

All data access for an application is authorized and authenticated using API tokens. Your Client ID, Client Secret, Browser and Server tokens can be found on your dashboard.

For Web API we recommend using the Server token to implement server-to-server API requests. Including your token in user-accessible client code may allow unauthorized access to your data feeds.

| Token | Description |
|-------|-------------|
| **Client ID** | Use as your username for the RETS API |
| **Client Secret** | Use as your password for the RETS API |
| **Server Token** | Use as the bearer token for API requests |
| **Browser Token** | Used for websites that may query the API directly from the browser; be sure to set the Referrer Domain if you use this approach |

#### Rate limits

There is no usage cap on the total number of API requests or concurrent requests you can make against a token. However, there is a default rate limit of 5,000 requests per hour. If your application has high usage, please reach out to discuss increasing the limit.

In addition to the hourly rate limit, we have introduced a burst rate limit to better manage sudden spikes in traffic. This burst rate limit is set on a per-minute basis and is equal to 1/15 of the hourly rate limit. By default, this means you can make up to 334 requests per minute (since 5,000 / 15 = 333.33, rounded up to 334).

There are six rate limit headers that are included in every response from the Bridge.

| Rate Limit Header | Description |
|-------------------|-------------|
| Application-RateLimit-Limit | The maximum number of API requests that can be made in an hour |
| Application-RateLimit-Remaining | The number of API requests that can still be made. This number will be set to the value of application-ratelimit-limit when the application rate limit resets |
| Application-RateLimit-Reset | The UTC time at which the application rate limit resets |
| Burst-RateLimit-Limit | The maximum number of API requests that can be made in a minute |
| Burst-RateLimit-Remaining | The number of API requests that can still be made. This number will be set to the value of burst-ratelimit-limit when the burst rate limit resets |
| Burst-RateLimit-Reset | The UTC time at which the burst rate limit resets |

#### Error Codes

The Web API may return the following HTTP status codes. For non-200 statuses, we also return an error object in the response body, with a message containing additional specifics about the error.

| HTTP Status Code | Description |
|------------------|-------------|
| 200 | OK |
| 400 | Bad request |
| 401 | Unauthorized |
| 403 | Forbidden |
| 404 | Not found |
| 408 | Request timeout |
| 415 | Unsupported MIME type |
| 429 | Too many requests |
| 500 | Internal server error |
| 503 | Service unavailable |

## RESO Web API

The Bridge platform allows you to query MLS data using the RESO Web API specification, which is based on OData. For more information about the specification, please visit the RESO website. The API has been RESO Platinum Certified to version 1.0.2.

### Authorization

Your application should send an Authorization header with every HTTP request to the API:

| Example | Query |
|---------|-------|
| **Authorization header** | `Authorization: Bearer {token}` |

If you can't set headers, you can send the token in the `access_token` parameter in the query string of your request:

| Example | Query |
|---------|-------|
| **Token in query string** | `GET https://api.bridgedataoutput.com/api/v2/OData/{{dataset_id}}/{resource}?access_token={server_token}` |

### API Response

By default, the RESO Web API will return 10 listings, regardless of the number of total records available. You may use the `$top` parameter to specify your request to return up to 200 listings at a time.

If there are more than 200 records available, you will need to paginate through the results.

If you wish to paginate through more than 10,000 listings you will need to use the dedicated replication endpoint.

All API responses besides metadata are returned in JSON format.

### Paginating through results

If the total number of records that are returned by a query is greater than 200 (the maximum limit of a result set), then you will need to paginate through the results. This is done by incrementing the number of skipped records.

| Example | Query |
|---------|-------|
| **Return the next 200 records, ordered by ListPrice** | `https://api.bridgedataoutput.com/api/v2/OData/{dataset_id}/{resource}?access_token={access_token}&$top=200&$skip=200&$orderby=ListPrice desc` |

### Using Expand

Using the `$expand` operator allow you to include associated data from additional resources. For example, you are able to bring in more detail about the relevant office or member into the response payload for a property, without having to make a second or third API query to the other resources.

> **Note:**
> - You are not able to use all query parameters on data you've expanded into your response.
> - If you are using the `$select` parameter in your query to limit the fields in the response payload, be sure to include the expanded field as well (eg, add the ListOffice field if you're expanding ListOffice)

| Example | Query |
|---------|-------|
| **Expand ListOffice in a Property query** | `https://api.bridgedataoutput.com/api/v2/OData/{dataset_id}/Property?access_token={access_token}&$expand=ListOffice` |

### Dataset Replication

While we encourage the use of the API to query the listing data as needed, there are use-cases where replication of the full dataset may be preferred.

To help with this, you are able to request data with the `/replication` endpoint. Whereas on-demand API requests can have a maximum of 200 results returned at once, with this endpoint the maximum `$top` parameter is 2,000 results.

The header of the response will contain a 'next' link. Results are returned ordered from oldest to newest, so by using the next link you are able to pull down all the available records to seed your data, and then continue using the next link at regular intervals to keep up to date.

| Example | Query |
|---------|-------|
| **Use the replication endpoint** | `https://api.bridgedataoutput.com/api/v2/OData/{dataset_id}/Property/replication?access_token={access_token}` |

> **Note:**
> - If you are trying to replicate anything more than 10,000 records you will need to use the replication endpoint.
> - Because of the potential payload size, this is only suitable for server to server requests.
> - This functionality is only available at the discretion of the MLS that has authorized data access.
> - Certain parameters like 'skip' and 'orderby' are not available with this endpoint.
> - To reduce payload size and improve performance we recommend using the `select` parameter to request only the fields you need.
> - BridgeModificationTimestamp is the best field to use for incremental updates as it represents the last modification in the Bridge system; ModificationTimestamp is ingested directly from the MLS system and is not a consistent proxy for modifications to the listing in the Bridge database.

### Media

Rather than keeping it in a separate resource, Media is returned as an object directly on the Property record. Typically, it is the highest resolution media available from the MLS and is stored on our CDN. You may link directly to the CDN.

### Metadata

You can request metadata that will return the fields and lookup values that have been made available to by the data provider. Metadata is returned in XML, according to the RESO spec.

| Example | Query |
|---------|-------|
| **Request metadata** | `https://api.bridgedataoutput.com/api/v2/OData/{dataset_id}/$metadata?access_token={access_token}` |

### Operators

You can constrain the result set of a resource by passing additional operators with your request. Valid operators include:

| Operator | Description |
|----------|-------------|
| eq | Equal |
| ne | Not equal |
| gt | Greater than |
| lt | Less than |
| ge | Greater than or equal |
| le | Less than or equal |
| and | Logical and |
| or | Logical or |
| not | Logical not |

### Parameters

The following query parameters may be passed to narrow down your results.

| Name | Type | Description | Example |
|------|------|-------------|---------|
| **access_token** | string | Token to identify the application. This is always required. | **return all datasets approved for an application:** `https://api.bridgedataoutput.com/api/v2/OData/DataSystem?access_token={access_token}` |
| **ListingKey** | string | The listing key, available on the /Properties resource. | **return data relating to a listing where the ListingKey "12345":** `https://api.bridgedataoutput.com/api/v2/OData/{dataset_id}/Properties('12345')?access_token={access_token}` |
| **MemberKey** | string | The member key, available on the /Members resource. | **Return data relating to a member where the memberKey is "12345":** `https://api.bridgedataoutput.com/api/v2/OData/{dataset_id}/Members('12345')?access_token={access_token}` |
| **OfficeKey** | string | The office key, available on the /Offices resource. | **Return data relating to an office where the officeKey is "12345":** `https://api.bridgedataoutput.com/api/v2/OData/{dataset_id}/Offices('12345')?access_token={access_token}` |
| **$skip** | number | Skips this number of results | **Skip the first 10 records of a dataset:** `https://api.bridgedataoutput.com/api/v2/OData/{dataset_id}/Properties?access_token={access_token}&$skip=10` |
| **$select** | string | Select the fields to be returned | **Only return the LivingArea field:** `https://api.bridgedataoutput.com/api/v2/OData/{dataset_id}/Properties?access_token={access_token}&$select=LivingArea` |
| **$unselect** | string | Select the fields to be excluded | **Do not return the Media object:** `https://api.bridgedataoutput.com/api/v2/OData/{dataset_id}/Properties?access_token={access_token}&$unselect=Media` |
| **$filter** | string | Filter the results to be returned | **Only return the listings where the ListPrice is greater than $100000:** `https://api.bridgedataoutput.com/api/v2/OData/{dataset_id}/Properties?access_token={access_token}&$filter=ListPrice gt 100000` |
| **$top** | number | Limits the size of the result set. Default is 10, maximum is 200. | **Limit results from the Test dataset to only 2:** `https://api.bridgedataoutput.com/api/v2/OData/{dataset_id}/Properties?access_token={access_token}&$top=2` |
| **$orderby** | string | Response field to sort query by (either "desc" or "asc") | **Sort order by descending price:** `https://api.bridgedataoutput.com/api/v2/OData/{dataset_id}/Properties?access_token={access_token}&$orderby=ListPrice desc` |
| **$expand** | string | Include query specified entities inline with response | **Expand the relevant listing agent for a given property:** `https://api.bridgedataoutput.com/api/v2/OData/{dataset_id}/Properties?access_token={access_token}&$expand=ListAgent` |

### Query Functions

| Function | Description | Example |
|----------|-------------|---------|
| **any** | Search fields where any element of an array is satisfied by a condition | **Return listings where there is an option of electric heating:** `https://api.bridgedataoutput.com/api/v2/OData/{dataset_id}/Properties?access_token={access_token}&$filter=Heating/any(a: a eq 'Electric')` |
| **all** | Search fields where all elements of an array is satisfied by a condition | **Return listings where all of the flooring is hardwood:** `https://api.bridgedataoutput.com/api/v2/OData/{dataset_id}/Properties?access_token={access_token}&$filter=Flooring/all(a: a eq 'Hardwood')` |
| **geo.distance** | Search by coordinates | **Return listings that are near specific co-ordinates, to a radius of 0.5 miles:** `https://api.bridgedataoutput.com/api/v2/OData/{dataset_id}/Properties?access_token={access_token}&$filter=geo.distance(Coordinates, POINT(-118.62 34.22)) lt 0.5` |
| **geo.intersects** | If you know the extents of a polygonal region, you can provide the each point as co-ordinates | **Return listings within a shape:** `https://api.bridgedataoutput.com/api/v2/OData/{dataset_id}/Properties?access_token={access_token}&$filter=geo.intersects(Coordinates, POLYGON((-127.02 45.08,-127.02 45.38,-127.32 45.38,-127.32 45.08,-127.02 45.08)))` |
| **tolower** | Search fields with lowercase queries | **Return listings using a lowercase query:** `https://api.bridgedataoutput.com/api/v2/OData/{dataset_id}/Properties?access_token={access_token}&$filter=tolower(StandardStatus) eq 'active'` |
| **startswith** | Search fields by a string prefix | **Return listings using a city that starts with a specific string:** `https://api.bridgedataoutput.com/api/v2/OData/{dataset_id}/Properties?access_token={access_token}&$filter=startswith(City, 'Spring')` |
| **endswith** | Search fields by string ending | **Return listings using a city that ends with a specific string:** `https://api.bridgedataoutput.com/api/v2/OData/{dataset_id}/Properties?access_token={access_token}&$filter=endswith(City, 'field')` |
| **contains** | Search field by string inclusion | **Return listings using a city that contains a specific string:** `https://api.bridgedataoutput.com/api/v2/OData/{dataset_id}/Properties?access_token={access_token}&$filter=contains(City, 'nge')` |
| **date** | Search fields by date | **Return listings with a specific date:** `https://api.bridgedataoutput.com/api/v2/OData/{dataset_id}/Properties?access_token={access_token}&$filter=date(ModificationTimestamp) eq 2017-08-29` |
| **time** | Search fields by time | **Return listings with a specific time:** `https://api.bridgedataoutput.com/api/v2/OData/{dataset_id}/Properties?access_token={access_token}&$filter=time(ModificationTimestamp) eq 17:03:04` |
| **year** | Search fields by year | **Return listings with a specific year:** `https://api.bridgedataoutput.com/api/v2/OData/{dataset_id}/Properties?access_token={access_token}&$filter=year(ModificationTimestamp) eq 2017` |
| **month** | Search fields by month | **Return listings with a specific month:** `https://api.bridgedataoutput.com/api/v2/OData/{dataset_id}/Properties?access_token={access_token}&$filter=month(ModificationTimestamp) eq 12` |
| **day** | Search fields by day | **Return listings with a specific day:** `https://api.bridgedataoutput.com/api/v2/OData/{dataset_id}/Properties?access_token={access_token}&$filter=day(ModificationTimestamp) eq 23` |
| **hour** | Search fields by hour | **Return listings with a specific hour:** `https://api.bridgedataoutput.com/api/v2/OData/{dataset_id}/Properties?access_token={access_token}&$filter=hour(ModificationTimestamp) eq 17` |
| **now()** | Search fields by current timestamp | **Return listings within the current timestamp:** `https://api.bridgedataoutput.com/api/v2/OData/{dataset_id}/Properties?access_token={access_token}&$filter=ModificationTimestamp eq now()` |

### Examples

| Example | Query |
|---------|-------|
| **Search for a specific property by ListingId** | `https://api.bridgedataoutput.com/api/v2/OData/{dataset_id}/Property?access_token={access_token}&$filter=ListingId eq '123456789'` |
| **Search for a property by address** | `https://api.bridgedataoutput.com/api/v2/OData/{dataset_id}/Property?access_token={access_token}&$filter=UnparsedAddress eq '123 Main'` |
| **Search for a property by address, using 'tolower' to work around API case-sensitivity** | `https://api.bridgedataoutput.com/api/v2/OData/{dataset_id}/Property?access_token={access_token}&$filter=tolower(UnparsedAddress) eq '123 main'` |
| **Search for all residential properties that are on sale** | `https://api.bridgedataoutput.com/api/v2/OData/{dataset_id}/Property?access_token={access_token}&$filter=PropertyType eq 'Residential' and StandardStatus eq 'Active'` |
| **Search for all residential properties that are for rent** | `https://api.bridgedataoutput.com/api/v2/OData/{dataset_id}/Property?access_token={access_token}&$filter=PropertyType eq 'Residential Income' and StandardStatus eq 'Active'` |
| **Search for all residential properties that are for sale and in a specific zip code** | `https://api.bridgedataoutput.com/api/v2/OData/{dataset_id}/Property?access_token={access_token}&$filter=PropertyType eq 'Residential Lease' and PostalCode eq '90210' and StandardStatus eq 'Active'` |
| **Search for all properties that are in one of two zip codes** | `https://api.bridgedataoutput.com/api/v2/OData/{dataset_id}/Property?access_token={access_token}&$filter=PostalCode eq '12345' or PostalCode eq '54321'` |
| **Search using complex nested queries** | `https://api.bridgedataoutput.com/api/v2/OData/{dataset_id}/Property?access_token={access_token}&$filter=((InternetEntireListingDisplayYN ne false) and ((StandardStatus eq 'Closed') and (((YearBuilt eq null) or ((YearBuilt le 1986) and (YearBuilt ge 1976))) and (((LivingArea eq null) or ((LivingArea le 3264) and (LivingArea ge 2412))) and ((CloseDate ge 2019-09-01) and (((BedroomsTotal eq null) or ((BedroomsTotal le 5) and (BedroomsTotal ge 3))) and (((BathroomsTotalDecimal eq null) or ((BathroomsTotalDecimal le 3.5) and (BathroomsTotalDecimal ge 1.5))) and ((SpecialListingConditions ne 'Auction') and ((SpecialListingConditions ne 'Probate') and ((SpecialListingConditions ne 'Short Sale') and ((SpecialListingConditions ne 'REO') and (((ClosePrice eq null) or ((ClosePrice le 472666) and (ClosePrice ge 315110))) and (geo.distance(Coordinates,POINT(-115.10998 36.091513)) lt 0.5))))))))))))))` |

## Glossary of common terminology

| Term | Description |
|------|-------------|
| **Application** | A representation of a single product that consumes data via the API. Each application has a profile, a set of access tokens and a set of data approvals. |
| **API Key** | Also called an API Token, it's an authorization code sent with an API request that identifies the user, and also what data they are allowed to see. |
| **API Platform** | The system that an MLS will leverage to manage and monitor data distribution, and provide software developers with various APIs to get data. |
| **Authentication** | Identifying the user of the API. Common techniques include API Keys and OAuth Tokens. |
| **Authorization** | The data an authenticated user of the API is allowed to access and query. |
| **CDN** | Content Delivery Network - a network of servers used to store data to provide high availability and performance. |
| **Data License** | A legal agreement between a data provider and a data consumer to allow access to content. |
| **Dataset** | A representation of either a single MLS on the platform, or an aggregation of multiple MLSs available through a single endpoint. |
| **Endpoint** | A web address that specifies the data or service the user is requesting. For example, going to the "/Offices" address in the Web API will return office data. |
| **JSON** | Similar to XML or CSV, JSON is a simple way to represent data, but it's easy for both humans and machines to interpret. By default, the RESO Web API returns data in JSON. |
| **Latency** | The amount of time it takes to get data back. This may include how long it took the server to find the right data and how long data took to travel back to the recipient. |
| **OAuth** | A specification for token-based authentication and authorization. The RESO Web API can use this to determine who is allowed to get data and what data they are allowed to see. |
| **OData** | A standard specification for APIs that defines how the data should be organized and how it can be queried. The RESO Web API is based on this specification. |
| **Metadata** | Information about the data the user has access to, usually accessible from a dedicated API endpoint. May include things like the available fields and their possible values. |
| **MLS** | Multiple Listing Service. An MLS is a network for agents and brokers that grants them access to exchange property listing information and share compensation for a sale. |
| **Payload** | A bundle of data that is returned by an API. |
| **Query** | The request a user makes to an API endpoint, which usually contains their API key, what data they want, and any additional parameters, like filters. |
| **Rate Limit** | Limits on how many requests to an API can be made within a specific time frame. There may be multiple rate limits in place specific to the user or the data they are requesting. |
| **Replication** | The process of recreating and storing your own version of the original database and continuously updating to keep the two copies in sync. |
| **Resource** | A collection of data within a dataset, e.g. Properties, Members, Offices, or Open Houses. |

## Frequently Asked Questions

### How do I set up a Bridge account?
Typically an invitation for access to the Bridge platform is initiated by the data providers (MLSs).

### How long does it take for an MLS to approve my data access?
Any data access is entirely at the discretion of the MLS, and each will have their own processes and criteria for approval.

### What MLSs do you currently have API integrations for?
Currently available datasets can be seen on the dashboard after you have created an account. We are always in the process of adding more datasets. If you are a brokerage and a member of an MLS that you do not see on the dashboard, please reach out to us to discuss further options.

### Is the RESO Web API and Data Dictionary RESO certified?
Yes, our RESO Web API is Platinum compliant and certified. MLS data is normalized to RESO Data Dictionary standards.

### How does the MLS data get returned?
MLS data is normalized to the RESO Data Dictionary and returned in JSON format (from the Web API), XML or CSV (from RETS). Any fields that are not able to be normalized (e.g. 'custom' or 'native' fields) are made available as well, at the MLS's discretion.

### I am a broker and a member of multiple MLSs - can I get all my data with a single feed?
Yes, you may create a virtual dataset that will allow you to retrieve listing data across all of your datasets.

### How often do you refresh the MLS listing data?
Typically we refresh listing data every 10 minutes or less, depending on the resource and the MLS.

### What MLS listing data will I have access to after access has been approved?
The API can serve all data from all resources (including Properties, Members, Offices, Open Houses and any others like Rooms and UnitTypes), as well as off-market data. However, the MLS has full control of what data is served through the API on a per application basis, and access is at their discretion.

### Can I use the Bridge to replicate an entire MLS dataset?
Yes, we have tools that make replication easy, although this is only available at the discretion of the MLS that has approved your data access. See the documentation for more information.

### Can I get access to all MLS listing data nationwide?
No - the Bridge is available on an MLS by MLS basis, and each of them individually control the data they distribute.

### How can I access non-MLS datasets?
The process is essentially the same as for MLS data access. After registering an account, apply for access to any available dataset you are interested in. Access will be granted depending on your specific use-case.

### How much does using the Bridge API cost?
Bridge Interactive does not charge vendors and brokerages any additional service fees when integrating with our partner MLSs. Note that MLSs may charge their own licensing fees, at their discretion.

### There are three data transports available, which should I use?
For MLS data you may choose between the Bridge Web API, the RESO Web API, or RETS. We recommend using the RESO Web API for accessing MLS data as it uses the latest industry standard and has the best interoperability with other real estate API platforms. RETS can be used if you wish to leverage your existing data ingestion pipeline. The Bridge Web API is best for simple API queries and is required for any non-MLS datasets.