# Office API Endpoint Information

## Request Office Information for a List of Offices

Returns a list of Offices of the MLS from the UNLOCK MLS based on the filter parameters included in the request.

## Example Code

### Example URL Request
```markdown
https://api.bridgedataoutput.com/api/v2/OData/{dataset_id}/Office?access_token={access_token}
```
### Example Response
```json
{
@odata.context: "https://api.bridgedataoutput.com/api/v2/OData/{dataset_id}/$metadata#Office",
@odata.nextLink: "https://api.bridgedataoutput.com/api/v2/OData/{dataset_id}/",
value: [
{
@odata.context: "https://api.bridgedataoutput.com/api/v2/OData/{dataset_id}/$metadata#Office",
@odata.id: "https://api.bridgedataoutput.com/api/v2/OData/{dataset_id}/Office('O_5af6019c75f1043ad481d98b')",
OfficeName: "Stoltenberg Inc Realty",
OfficeEmail: "stoltenbergincrealty@hotmail.com",
OfficeFax: "(319) 765-6009",
OfficePhone: "1-309-219-4655",
OfficeAddress1: "9636 Lexi Springs",
OfficePostalCode: "30686",
OfficeCity: "VonRuedenport",
OfficeStateOrProvince: "Connecticut",
OfficeStatus: "Active",
OfficeType: "Appraiser",
OfficeKey: "O_5af6019c75f1043ad481d98b",
OfficeMlsId: "5af6019c75f1043ad481d98c",
OfficeCorporateLicense: "5af6019c75f1043ad481d98d",
OriginalEntryTimestamp: "2018-02-27T06:57:09.322Z",
ModificationTimestamp: "2017-05-12T09:21:36.947Z",
IDXOfficeParticipationYN: false,
SyndicateTo: [
"Zillow",
"Trulia"
],
SyndicateAgentOption: "Allow Agent",
OfficeCountOrParish: "Muellertown",
OfficeBranchType: "Stand Alone",
OfficeAssociationComments: "Aspernatur et amet aliquam.",
FranchiseAffiliation: "Jacobs, Hansen and Wunsch",
OriginatingSystemID: "{dataset_id}",
OriginatingSystemName: "{dataset_id}",
OriginatingSystemOfficeKey: "{dataset_id}"
}
],
@odata.count: 1
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

|------|------|-------------|
| `BillingOfficeKey` | string | The office that will be billed (e.g., corporate headquarters). |
| `BridgeModificationTimestamp` | string | A timestamp representing when last this record was modified in the Bridge system. |
| `BrokerageKey` | string | Brokerage foreign key |
| `FranchiseAffiliation` | string | The name of the franchise to which the broker/office is contracted. |
| `FranchiseNationalAssociationId` | string | The national association ID of the franchise (i.e., the NRDS number in the U.S.). |
| `FranchiseNationalAssociationID` | string | The national association ID of the franchise (i.e., the NRDS number in the U.S.). |
| `IDXOfficeParticipationYN` | boolean | Does the Office/Broker participate in IDX. |
| `MainOfficeKey` | string | OfficeKey of the Main Office in a firm/company of offices. This is a self referencing foreign key relating to this resource's OfficeKey. This key may be the same value as the OfficeKey for a given record if the given office is the Main Office. |
| `MainOfficeKeyNumeric` | number | OfficeKey of the Main Office in a firm/company of offices. This is a self referencing foreign key relating to this resource's OfficeKey. This key may be the same value as the OfficeKey for a given record if the given office is the Main Office. This is the numeric only key and used as an alternative to the MainOfficeKey field. |
| `MainOfficeMlsId` | string | OfficeMlsId of the Main Office in a firm/company of offices. |
| `Media` | array | An object containing media information such as id, url and type. |
| `Media.APIModificationTimestamp` | string | A timestamp representing when last this listing was modified in our system. |
| `Media.BridgeModificationTimestamp` | string | A timestamp representing when last this record was modified in the Bridge system. |
| `Media.ChangedByMemberID` | string | ID of the user, agent, member, etc., that uploaded the media this record refers to. |
| `Media.ChangedByMemberKey` | string | The primary key of the member who uploaded the media this record refers to. This is a foreign key relating to the Member resource's MemberKey. |
| `Media.ChangedByMemberKeyNumeric` | number | The primary key of the member who uploaded the media this record refers to. This is a foreign key relating to the Member resource's MemberKey. This is the numeric only key and used as an alternative to the ChangedByMemberKey field. |
| `Media.ClassName` | string | The class or table of the listing or other record the media. Residential, Lease, Agent, Office, Contact, etc. |
| `Media.Group` | string | A placeholder for media classification such as elevation, exterior, interior, community, view, plan, plat. The purpose is to allow media items to be grouped. |
| `Media.id` | string | The unique media ID |
| `Media.ImageHeight` | number | The height of the image expressed in pixels. |
| `Media.ImageOf` | string | When the media is an image, a list of possible matches such as kitchen, bathroom, front of structure, etc. This field may be used to identify a required image under association or MLS rules. |
| `Media.ImageSizeDescription` | string | A text description of the size of the image. i.e. Small, Thumbnail, Medium, Large, X-Large. The largest image must be described as "Largest". Thumbnail must also be included. Pick List will remain open/extendable. |
| `Media.ImageWidth` | number | The width of the image expressed in pixels. |
| `Media.LongDescription` | string | The full robust description of the object. |
| `Media.MediaCategory` | string | Category describing the , Photos, Documents, Video, Unbranded Virtual Tour, Branded Virtual Tour, Floor Plan, Logo |
| `Media.MediaHTML` | string | The JavaScript or other method to embed a video, image, virtual tour or other media. |
| `Media.MediaKey` | string | A unique identifier for this record from the immediate source. This may be a number, or string that can include URI or other forms. This is the system you are connecting to and not necessarily the original source of the record. |
| `Media.MediaKeyNumeric` | number | A unique identifier for this record from the immediate source. This may be a number, or string that can include URI or other forms. This is the system you are connecting to and not necessarily the original source of the record. This is the numeric only key and used as an alternative to the MediaKey field. |
| `Media.MediaModificationTimestamp` | string | This timestamp is updated when a change to the object has been made, which may differ from a change to the Media Resource. |
| `Media.MediaObjectID` | string | ID of the image, supplement or other object specified by the given media record. |
| `Media.MediaStatus` | string | The status of the media item referenced by this record. (Updated, Deleted, etc.,_ |
| `Media.MediaType` | string | Media Types as defined by IANA. http://www.iana.org/assignments/media-types/index.html |
| `Media.MediaURL` | string | The URI to the media file referenced by this record. |
| `Media.MimeType` | string | Media Types as defined by IANA. http://www.iana.org/assignments/media-types/index.html |
| `Media.ModificationTimestamp` | string | The transactional timestamp automatically recorded by the MLS system representing the date/time the media record was last modified. |
| `Media.Order` | number | Only a positive integer including zero. Element zero is the primary photo per RETS convention. |
| `Media.OriginatingSystemID` | string | The RESO OUID's OrganizationUniqueId of the Originating record provider. The Originating system is the system with authoritative control over the record. For example; the name of the MLS where the listing was input. In cases where the Originating system was not where the record originated (the authoritative system), see the Originating System fields. |
| `Media.OriginatingSystemMediaKey` | string | Unique identifier from the originating system which is commonly a key to that system. In the case where data is passed through more than one system, this is the originating system key. This is a foreign key relating to the system where this record was originated. |
| `Media.OriginatingSystemName` | string | The name of the originating record provider. Most commonly the name of the MLS. The place where the listing is originally input by the member. The legal name of the company. To be used for display. |
| `Media.Permission` | string | Public, Private, IDX, VOW, Office Only, Firm Only, Agent Only, |
| `Media.PreferredPhotoYN` | boolean | When set to true, the media record in question is the preferred photo. This will typically mean the photo to be shown when only one of the photos is to be displayed. |
| `Media.RAP1_AdditionalDescription` | string | Passthrough field for AdditionalDescription |
| `Media.RAP1_RequiredDoc` | string | Passthrough field for RequiredDoc |
| `Media.RAP1_UploadDateTime` | string | Passthrough field for UploadDateTime |
| `Media.RAP1_Viewable` | string | Passthrough field for Viewable |
| `Media.ResizeMediaURL` | string | The URI to a resizable version of the media file referenced by this record. |
| `Media.ResourceName` | string | The resource or table of the listing or other record the media relates to. i.e. Property, Member, Office, etc. |
| `Media.ResourceRecordID` | string | The well known identifier of the related record from the source resource. The value may be identical to that of the Listing Key, but the Listing ID is intended to be the value used by a human to retrieve the information about a specific listing. In a multiple originating system or a merged system, this value may not be unique and may require the use of the provider system to create a synthetic unique value. |
| `Media.ResourceRecordKey` | string | The primary key of the related record from the source resource. For example the ListingKey, AgentKey, OfficeKey, TeamKey, etc. This is the system you are connecting to and not necessarily the original source of the record. This is a foreign key from the resrouce selected in the ResrouceName field. |
| `Media.ResourceRecordKeyNumeric` | number | The primary key of the related record from the source resource. For example the ListingKey, AgentKey, OfficeKey, TeamKey, etc. This is the system you are connecting to and not necessarily the original source of the record. This is a foreign key from the resource selected in the ResourceName field. This is the numeric only key and used as an alternative to the ResourceRecordKey field. |
| `Media.ShortDescription` | string | The short text given to summarize the object. Commonly used as the short description displayed under a photo. |
| `Media.SourceSystemID` | string | The RESO OUID's OrganizationUniqueId of the Source record provider. The source system is the system from which the record was directly received. In cases where the source system was not where the record originated (the authoritative system), see the Originating System fields. |
| `Media.SourceSystemMediaKey` | string | The system key, a unique record identifier, from the Source System. The Source System is the system from which the record was directly received. In cases where the Source System was not where the record originated (the authoritative system), see the Originating System fields. |
| `Media.SourceSystemName` | string | The name of the immediate record provider. The system from which the record was directly received. The legal name of the company. |
| `ModificationTimestamp` | string | Date/time the roster (member or office) record was last modified. |
| `OfficeAddress1` | string | The street number, direction, name and suffix of the office. |
| `OfficeAddress2` | string | The unit/suite number of the office. |
| `OfficeAlternateId` | string | An alternate ID with no specific use. |
| `OfficeAOR` | string | The Office's Board or Association of REALTORS. |
| `OfficeAORkey` | string | A system unique identifier. Specifically, in aggregation systems, the OfficeAORkey is the system unique identifier from the system that the record was retrieved. This may be identical to the related xxxId. This is a foreign key relating to the AOR's member management system in which the record was originated. |
| `OfficeAORkeyNumeric` | number | A system unique identifier. Specifically, in aggregation systems, the OfficeAORkey is the system unique identifier from the system that the record was retrieved. This may be identical to the related xxxId. This is a foreign key relating to the AOR's member management system in which the record was originated. This is the numeric only key and used as an alternative to the OfficeAORkey field. |
| `OfficeAORMlsId` | string | The local, well-known identifier for the office's Association of REALTORS. This value may not be unique, specifically in the case of aggregation systems, this value should be the identifier from the original system. |
| `OfficeAssociationComments` | string | Notes relating to the office. |
| `OfficeBio` | string | A text field containing biography information for the office record. This may be resume-like information, including experience and qualifications. |
| `OfficeBranchType` | string | The level of the office in the hierarchy of Main, Branch, Stand Alone, etc., |
| `OfficeBrokerKey` | string | The MemberKey of the responsible/owning broker. This is a foreign key relating to the Member resource's MemberKey. |
| `OfficeBrokerKeyNumeric` | number | The MemberKey of the responsible/owning broker. This is a foreign key relating to the Member resource's MemberKey. This is the numeric only key and used as an alternative to the OfficeBrokerKey field. |
| `OfficeBrokerMlsId` | string | The MemberMlsId of the responsible/owning broker. |
| `OfficeBrokerNationalAssociationID` | string | The national association ID of the broker (i.e., the NRDS number in the U.S.). |
| `OfficeCity` | string | The city of the office. |
| `OfficeCorporateLicense` | string | When an office/firm is a corporation, an independent license number is issued. |
| `OfficeCountry` | string | The office's country code for the street address. |
| `OfficeCountyOrParish` | string | The county or parish in which the offices is located. |
| `OfficeEmail` | string | The email address of the office |
| `OfficeFax` | string | North American 10 digit phone numbers should be in the format of ###-###-#### (separated by hyphens). Other conventions should use the common local standard. International numbers should be preceded by a plus symbol. |
| `OfficeKey` | string | A system unique identifier. Specifically, in aggregation systems, the Key is the system unique identifier from the system that the record was just retrieved. This may be identical to the related xxxId identifier, but the key is guaranteed unique for this record set. |
| `OfficeKeyNumeric` | number | A unique identifier for this record from the immediate source. This is the numeric only key and used as an alternative to the OfficeKey fields. This is the local key of the system. When records are received from other systems, a local key is commonly applied. If conveying the original keys from the source or originating systems, see SourceSystemOfficeKey and OriginatingSystemOfficeKey. |
| `OfficeMailAddress1` | string | The street number, direction, name and suffix of the member. |
| `OfficeMailAddress2` | string | The unit/suite number of the member. |
| `OfficeMailCareOf` | string | The care of (c/o) for the office's mailing address. |
| `OfficeMailCity` | string | The office's city for the mailing address. |
| `OfficeMailCountry` | string | The office's country code for the mailling address. |
| `OfficeMailCountyOrParish` | string | The office's county of the mailing address. |
| `OfficeMailPostalCode` | string | The postal code of the office's mailing address. |
| `OfficeMailPostalCodePlus4` | string | The four-digit extension of the U.S. ZIP Code. |
| `OfficeMailStateOrProvince` | string | The office's state or province of the mailing address. |
| `OfficeManagerKey` | string | The lead Office Manager for the given office. This is a foreign key relating to the Member resource's MemberKey. |
| `OfficeManagerKeyNumeric` | number | The lead Office Manager for the given office. This is a foreign key relating to the Member resource's MemberKey. This is the numeric only key and used as an alternative to the OfficeManagerKey field. |
| `OfficeManagerMlsId` | string | The lead Office Manager for the given office. |
| `OfficeMlsId` | string | The local, well-known identifier. This value may not be unique, specifically in the case of aggregation systems, this value should be the identifier from the original system. |
| `OfficeName` | string | The legal name of the brokerage. |
| `OfficeNationalAssociationId` | string | The national association ID of the office. i.e. in the U.S. is the NRDS number. |
| `OfficeNationalAssociationIdInsertDate` | string | The date the office record was initally created in the national association's database (e.g., the date the record was added to NRDS in the U.S.). |
| `OfficePhone` | string | North American 10 digit phone numbers should be in the format of ###-###-#### (separated by hyphens). Other conventions should use the common local standard. International numbers should be preceded by a plus symbol. |
| `OfficePhoneExt` | string | The extension of the given phone number (if applicable). |
| `OfficePostalCode` | string | The postal code of the office. |
| `OfficePostalCodePlus4` | string | The extension of the postal/zip code. i.e. +4 |
| `OfficePreferredMedia` | string | The method the office prefers to receive media. |
| `OfficePrimaryAorId` | string | The primary association of REALTORS® (AOR) associated with the member. This may be another AOR where the member has their primary membership. |
| `OfficePrimaryStateOrProvince` | string | The office's primary state or province. |
| `OfficeStateOrProvince` | string | The state or province in which the office is located. |
| `OfficeStatus` | string | Is the office active, inactive or under disciplinary action. |
| `OfficeType` | string | The type of business conducted by the office. i.e. Real Estate, Appraiser, etc. |
| `OriginalEntryTimestamp` | string | Date/time the roster (member or office) record was originally input into the source system. |
| `OriginatingSystemID` | string | The RESO OUID's OrganizationUniqueId of the Originating record provider. The Originating system is the system with authoritative control over the record. For example; the name of the MLS where the office was input. In cases where the Originating system was not where the record originated (the authoritative system), see the Originating System fields. |
| `OriginatingSystemName` | string | The name of the Originating record provider. Most commonly the name of the MLS. The place where the office is originally input by the member. The legal name of the company. |
| `OriginatingSystemOfficeKey` | string | The system key, a unique record identifier, from the Originating system. The Originating system is the system with authoritative control over the record. For example, the Multiple Listing Service where the office was input. There may be cases where the Source System (how you received the record) is not the Originating System. See Source System Key for more information. |
| `SocialMediaFacebookUrlOrId` | string | The website URL or ID of social media site or account of the member. This is a repeating element. Replace [Type] with any of the options from the SocialMediaType field to create a unique field for that type of social media. For example: SocialMediaFacebookUrlOrID, SocialMediaSkypeUrlOrID, etc. |
| `SocialMediaLinkedInUrlOrId` | string | The website URL or ID of social media site or account of the member. This is a repeating element. Replace [Type] with any of the options from the SocialMediaType field to create a unique field for that type of social media. For example: SocialMediaFacebookUrlOrID, SocialMediaSkypeUrlOrID, etc. |
| `SocialMediaTwitterUrlOrId` | string | The website URL or ID of social media site or account of the member. This is a repeating element. Replace [Type] with any of the options from the SocialMediaType field to create a unique field for that type of social media. For example: SocialMediaFacebookUrlOrID, SocialMediaSkypeUrlOrID, etc. |
| `SocialMediaType` | string | A list of types of sites, blog, social media, the Office URL or ID is referring to. i.e. Website, Blog, Facebook, Twitter, LinkedIn, Skype, etc., This list is used to populate the Type with repeating Social Media URL or ID types. |
| `SocialMediaWebsiteUrlOrId` | string | The website URL or ID of social media site or account of the member. This is a repeating element. Replace [Type] with any of the options from the SocialMediaType field to create a unique field for that type of social media. For example: SocialMediaFacebookUrlOrID, SocialMediaSkypeUrlOrID, etc. |
| `SourceSystemID` | string | The RESO OUID's OrganizationUniqueId of the Source record provider. The source system is the system from which the record was directly received. In cases where the source system was not where the record originated (the authoritative system), see the Originating System fields. |
| `SourceSystemName` | string | The name of the immediate record provider. The system from which the record was directly received. The legal name of the company. |
| `SourceSystemOfficeKey` | string | The system key, a unique record identifier, from the Source System. The Source System is the system from which the record was directly received. In cases where the Source System was not where the record originated (the authoritative system), see the Originating System fields. |
| `SyndicateAgentOption` | string | A list of options allowing the broker to pass the decision of syndication choice down to the listing agents. i.e. No Agent Choice, Allow Agent Choice, Restrict Agent Choice, etc. |
| `SyndicateTo` | string | The principal broker's choice on where they would like their listings syndicated. i.e. Zillow, Trulia, Homes.com, etc. |

## Request Office Information for a Single Office
Returns MLS information about a single Office from UNLOCK MLS.
## Example Code

### Example URL Request
```markdown
https://api.bridgedataoutput.com/api/v2/OData/{dataset_id}/Office({OfficeKey})?access_token={access_token}
```
### Example Response
The same resonse for a list of Office, except you will receive only data from a single Office

### Request Parameters for the URL

| Name | Type | Description |
|------|------|-------------|
| `access_token` | string | Token to identify the user or application. |
| `dataset` | string | Dataset to get the listings from. |
| `OfficeKey` | string | Key to identify a Office |
| `$skip` | integer | Skip the first n items |
| `$select` | string | Select properties that are explicitly specified e.g. OfficeType |
| `$unselect` | string | Filter record properties that are explicitly specified e.g. OfficeFax |
| `$top` | integer | Show only the first n items |
| `$orderby` | string | Order items by specified property value, e.g. ModificationTimestamp asc |
| `$filter` | string | Filter items by certain values |
| `$expand` | array | Expand related entities |