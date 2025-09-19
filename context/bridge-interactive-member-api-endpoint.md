# Member API Endpoint Information

## Request Member Information for a List of Members

Returns a list of members of the MLS from the UNLOCK MLS based on the filter parameters included in the request.

## Example Code

### Example URL Request
```markdown
https://api.bridgedataoutput.com/api/v2/OData/{dataset_id}/Member?access_token={access_token}
```
### Example Response
```json
{
{
@odata.context: "https://api.bridgedataoutput.com/api/v2/OData/{dataset_id}/$metadata#Member",
@odata.nextLink: "https://api.bridgedataoutput.com/api/v2/OData/{dataset_id}/",
value: [
{
@odata.context: "https://api.bridgedataoutput.com/api/v2/OData/{dataset_id}/$metadata#Member",
@odata.id: "https://api.bridgedataoutput.com/api/v2/OData/{dataset_id}/Member('M_5af601accd966d3afc88e0e7')",
MemberMlsAccessYN: false,
OfficeKey: "O_5af6019c75f1043ad481d99a",
MemberMlsSecurityClass: [
"Top Secret"
],
OriginatingSystemName: "{dataset_id}",
MemberCountyOrParish: "Schinnerville",
MemberPostalCode: "93470",
MemberMiddleName: "Adeline",
MemberStateLicenceState: "OK",
MemberCity: "Wehnermouth",
ModificationTimestamp: "2017-12-30T17:56:56.031Z",
MemberHomePhone: "423-949-3694",
MemberStateLicense: "5324129684923",
MemberFullName: "Abbigail Adeline Nienow",
MemberDesignation: "Miss",
MemberLoginId: "ANienow",
MemberLanguages: [
"English",
"Spanish",
"French"
],
OriginatingSystemID: "{dataset_id}",
MemberMlsId: "5af601accd966d3afc88e0e8",
SyndicateTo: [
"Zillow"
],
MemberKey: "M_5af601accd966d3afc88e0e7",
OfficeMlsId: "5af6019c75f1043ad481d99b",
OfficeName: "Quigley, Donnelly and Hoeger Realty",
OriginalEntryTimestamp: "2017-08-17T21:10:04.617Z",
JobTitle: "Dynamic Integration Producer",
MemberOfficePhone: "(878) 910-8660 x0908",
MemberMobilePhone: "1-617-918-4804 x6426",
MemberStateOrProvince: "Idaho",
MemberAssociationComments: "Praesentium suscipit deleniti aliquam assumenda beatae aut sapiente.",
MemberFirstName: "Abbigail",
MemberAddress1: "182 Michael Trail",
MemberNationalAssociationId: "5af601accd966d3afc88e0ea",
OriginatingSystemMemberKey: "{dataset_id}",
MemberCountry: "Egypt",
MemberType: "Association Staff",
MemberStatus: "Active",
MemberLastName: "Nienow"
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
| Name | Type | Description |
|------|------|-------------|
| `@odata.context` | string | Link to the metadata context. |
| `@odata.id` | string | Link to the OData endpoint for the specific record. |
| `BridgeModificationTimestamp` | string | A timestamp representing when last this record was modified in the Bridge system. |
| `JobTitle` | string | The title or position of the member within their organization. |
| `LastLoginTimestamp` | string | Date/time the member last logged into the source or other system. |
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
| `MemberAddress1` | string | The street number, direction, name and suffix of the member. |
| `MemberAddress2` | string | The unit/suite number of the member. |
| `MemberAlternateId` | string | This is an alternate ID with no specific use. |
| `MemberAOR` | string | The Member's Primary Board or Association of REALTORS. |
| `MemberAORkey` | string | A system unique identifier. Specifically, in aggregation systems, the MemberAORkey is the system unique identifier from the system that the record was retrieved. This may be identical to the related xxxId. |
| `MemberAORkeyNumeric` | number | A system unique identifier. Specifically, in aggregation systems, the MemberAORkey is the system unique identifier from the system that the record was retrieved. This may be identical to the related xxxId. This is the numeric only key and used as an alternative to the MemberAORkey field. |
| `MemberAORMlsId` | string | The local, well-known identifier for the member's Association of REALTORS. This value may not be unique, specifically in the case of aggregation systems, this value should be the identifier from the original system. |
| `MemberAssociationComments` | string | The association's notes regarding the member. |
| `MemberBillingPreference` | string | The member's preferred method of billing. |
| `MemberBio` | string | A text field containing biography information for the member record. This may be resume-like information, including experience and qualifications. |
| `MemberCarrierRoute` | string | The group of addresses to which the USPS assigns the same code to aid in mail delivery. For the USPS, these codes are 9 digits: 5 numbers for the ZIP Code, one letter for the carrier route type, and 3 numbers for the carrier route number. |
| `MemberCity` | string | The city of the member. |
| `MemberCommitteeCount` | number | The number of current/active committees in which the member belongs. |
| `MemberCountry` | string | The country abbreviation in a postal address. |
| `MemberCountyOrParish` | string | The county or parish in which the member is addressed. |
| `MemberDesignation` | string | Designations and certifications acknowledging experience and expertise in various real estate sectors are awarded by NAR and each affiliated group upon completion of required courses. |
| `MemberDirectPhone` | string | North American 10 digit phone numbers should be in the format of ###-###-#### (separated by hyphens). Other conventions should use the common local standard. International numbers should be preceded by a plus symbol. |
| `MemberEmail` | string | The email address of the Member. |
| `MemberFax` | string | North American 10 digit phone numbers should be in the format of ###-###-#### (separated by hyphens). Other conventions should use the common local standard. International numbers should be preceded by a plus symbol. |
| `MemberFirstName` | string | The first name of the Member. |
| `MemberFullName` | string | The full name of the Member. (First Middle Last) or a alternate full name. |
| `MemberHomePhone` | string | North American 10 digit phone numbers should be in the format of ###-###-#### (separated by hyphens). Other conventions should use the common local standard. International numbers should be preceded by a plus symbol. |
| `MemberIsAssistantTo` | string | The MemberMlsId of the Agent/Broker that this member is an assistant. The typical use will be to add the agent's ID to this field when editing the member record of the assistant. |
| `MemberKey` | string | A unique identifier for this record from the immediate source. This is a string that can include URI or other forms. Alternatively use the MemberKeyNumeric for a numeric only key field. This is the local key of the system. When records are received from other systems, a local key is commonly applied. If conveying the original keys from the source or originating systems, see SourceSystemMemberKey and OriginatingSystemMemberKey. |
| `MemberKeyNumeric` | number | A unique identifier for this record from the immediate source. This is the numeric only key and used as an alternative to the MemberKey fields. This is the local key of the system. When records are received from other systems, a local key is commonly applied. If conveying the original keys from the source or originating systems, see SourceSystemMemberKey and OriginatingSystemMemberKey. |
| `MemberLanguages` | string | The languages the member speaks. |
| `MemberLastName` | string | The last name of the Member. |
| `MemberLoginId` | string | The ID used to logon to the MLS system. |
| `MemberMailOptOutYN` | boolean | Indicates whether or not the member has opted out of receiving solicitation via mail. |
| `MemberMiddleName` | string | The middle name of the Member. |
| `MemberMlsAccessYN` | boolean | Does the member have access to the MLS system. |
| `MemberMlsId` | string | The local, well-known identifier for the member. This value may not be unique, specifically in the case of aggregation systems, this value should be the identifier from the original system. |
| `MemberMlsSecurityClass` | string | The MLS security group or class given to the member. |
| `MemberMobilePhone` | string | North American 10 digit phone numbers should be in the format of ###-###-#### (separated by hyphens). Other conventions should use the common local standard. International numbers should be preceded by a plus symbol. |
| `MemberNamePrefix` | string | Prefix to the name (e.g. Dr. Mr. Ms. etc.) |
| `MemberNameSuffix` | string | Suffix to the surname (e.g. Esq., Jr., III etc.) |
| `MemberNationalAssociationEntryDate` | string | The date that the member's record was entered with the National Association of REALTORS®. |
| `MemberNationalAssociationId` | string | The national association ID of the member. i.e. in the U.S. is the NRDS number. |
| `MemberNickname` | string | An alternate name used by the Member, usually as a substitute for the first name. |
| `MemberOfficePhone` | string | North American 10 digit phone numbers should be in the format of ###-###-#### (separated by hyphens). Other conventions should use the common local standard. International numbers should be preceded by a plus symbol. |
| `MemberOfficePhoneExt` | string | The extension of the given phone number (if applicable). |
| `MemberOtherPhoneType` | string | The type of "other" phone. i.e. Preferred, Office, Mobile, Direct, Home, Fax, Pager, Voicemail, Toll Free, SMS, 1, 2, 3, First, Second, Third, etc.. This is used as the list of options for the Member Other Phone repeating elements. |
| `MemberPager` | string | North American 10 digit phone numbers should be in the format of ###-###-#### (separated by hyphens). Other conventions should use the common local standard. International numbers should be preceded by a plus symbol. |
| `MemberPassword` | string | A password that the member whishes to share with other systems. Normal security considerations apply and are the responsibility of the entity utilizing this field. |
| `MemberPhoneTTYTDD` | string | (Telecommunications Device for the Deaf/TeleTYpewriter) A user terminal with keyboard input and printer or display output used by the hearing and speech impaired. The device contains a modem and is used over a standard analog phone line. If a recipient does not have a corresponding terminal device, TDD/TTY users dial a relay service composed of operators who receive the typed messages, call the recipients and speak the messages to them. The operators also type the responses back to the TDD/TTY user. |
| `MemberPostalCode` | string | The postal code of the member. |
| `MemberPostalCodePlus4` | string | The extension of the postal/zip code. i.e. +4 |
| `MemberPreferredMail` | string | The preferred mailing address for the member. |
| `MemberPreferredMedia` | string | The method the member perfers to receive media by (e.g., Email, Mail, Fax). |
| `MemberPreferredPhone` | string | North American 10 digit phone numbers should be in the format of ###-###-#### (separated by hyphens). Other conventions should use the common local standard. International numbers should be preceded by a plus symbol. |
| `MemberPreferredPhoneExt` | string | The extension of the given phone number (if applicable). |
| `MemberPreferredPublications` | string | Indicates where the member would like to receive any publications from the association. |
| `MemberPrimaryAorId` | string | The primary association of REALTORS® (AOR) associated with the member. This may be another AOR where the member has their primary membership. |
| `MemberStateLicense` | string | The license of the Member. Separate multiple licenses with a comma and space. |
| `MemberStateLicenseExpirationDate` | string | The expiration date for the member's license. |
| `MemberStateLicenseState` | string | The state in which the member is licensed. |
| `MemberStateLicenseType` | string | The license type of the member. |
| `MemberStateOrProvince` | string | The state or province in which the member is addressed. |
| `MemberStatus` | string | Is the account active, inactive or under disciplinary action. |
| `MemberTollFreePhone` | string | North American 10 digit phone numbers should be in the format of ###-###-#### (separated by hyphens). Other conventions should use the common local standard. International numbers should be preceded by a plus symbol. |
| `MemberTransferDate` | string | The date that the member transferred from one member office to another. |
| `MemberType` | string | The type of member. i.e. Agent, Broker, Office Manager, Appraiser, Photographer, Assistants, MLO, Realtor, Association Staff, MLS Staff, etc. |
| `MemberVoiceMail` | string | North American 10 digit phone numbers should be in the format of ###-###-#### (separated by hyphens). Other conventions should use the common local standard. International numbers should be preceded by a plus symbol. |
| `MemberVoiceMailExt` | string | The extension of the given phone number (if applicable). |
| `ModificationTimestamp` | string | Date/time the roster (member or office) record was last modified. |
| `OfficeKey` | string | A system unique identifier. Specifically, in aggregation systems, the Key is the system unique identifier from the system that the record was just retrieved. This may be identical to the related xxxId identifier, but the key is guaranteed unique for this record set. This is a foreign key relating to the Office resource's OfficeKey. |
| `OfficeKeyNumeric` | number | A system unique identifier. Specifically, in aggregation systems, the Key is the system unique identifier from the system that the record was just retrieved. This may be identical to the related xxxId identifier, but the key is guaranteed unique for this record set. This is a foreign key relating to the Office resource's OfficeKey. This is the numeric only key and used as an alternative to the MemberAORkey field. |
| `OfficeMlsId` | string | The local, well-known identifier. This value may not be unique, specifically in the case of aggregation systems, this value should be the identifier from the original system. |
| `OfficeName` | string | The legal name of the brokerage. |
| `OfficeNationalAssociationId` | string | The national association ID of the office (i.e., in the U.S., this is the NRDS number). |
| `OriginalEntryTimestamp` | string | Date/time the roster (member or office) record was originally input into the source system. |
| `OriginatingSystemID` | string | The RESO OUID's OrganizationUniqueId of the Originating record provider. The Originating system is the system with authoritative control over the record. For example; the name of the MLS where the member was input. In cases where the Originating system was not where the record originated (theauthoritative system), see the Originating System fields. |
| `OriginatingSystemMemberKey` | string | The system key, a unique record identifier, from the Originating system. The Originating system is the system with authoritative control over the record. For example, the Multiple Listing Service where the member was input. There may be cases where the Source System (how you received the record) is not the Originating System. See Source System Key for more information. |
| `OriginatingSystemName` | string | The name of the Originating record provider. Most commonly the name of the MLS. The place where the member is originally input by the member. The legal name of the company. |
| `SocialMediaFacebookUrlOrId` | string | The website URL or ID of social media site or account of the member. This is a repeating element. Replace [Type] with any of the options from the SocialMediaType field to create a unique field for that type of social media. For example: SocialMediaFacebookUrlOrID, SocialMediaSkypeUrlOrID, etc. |
| `SocialMediaLinkedInUrlOrId` | string | The website URL or ID of social media site or account of the member. This is a repeating element. Replace [Type] with any of the options from the SocialMediaType field to create a unique field for that type of social media. For example: SocialMediaFacebookUrlOrID, SocialMediaSkypeUrlOrID, etc. |
| `SocialMediaTwitterUrlOrId` | string | The website URL or ID of social media site or account of the member. This is a repeating element. Replace [Type] with any of the options from the SocialMediaType field to create a unique field for that type of social media. For example: SocialMediaFacebookUrlOrID, SocialMediaSkypeUrlOrID, etc. |
| `SocialMediaType` | string | A list of types of sites, blog, social media, the Member URL or ID is referring to. i.e. Website, Blog, Facebook, Twitter, LinkedIn, Skype, etc., This list is used to populate the Type with repeating Social Media URL or ID types. |
| `SocialMediaWebsiteUrlOrId` | string | The website URL or ID of social media site or account of the member. This is a repeating element. Replace [Type] with any of the options from the SocialMediaType field to create a unique field for that type of social media. For example: SocialMediaFacebookUrlOrID, SocialMediaSkypeUrlOrID, etc. |
| `SourceSystemID` | string | The RESO OUID's OrganizationUniqueId of the Source record provider. The source system is the system from which the record was directly received. In cases where the source system was not where the record originated (the authoritative system), see the Originating System fields. |
| `SourceSystemMemberKey` | string | The system key, a unique record identifier, from the Source System. The Source System is the system from which the record was directly received. In cases where the Source System was not where the record originated (the authoritative system), see the Originating System fields. |
| `SourceSystemName` | string | The name of the immediate record provider. The system from which the record was directly received. The legal name of the company. |
| `SyndicateTo` | string | When permitted by the broker, the options made by the individual agent on where they would like their listings syndicated. i.e. Zillow, Trulia, Homes.com, etc. |
| `UniqueLicenseeIdentifier` | string | The Unique Licensee Identifier (ULI) represents a single ID for a licensed real estate agent. It differs from the National Association of REALTORS® NRDS ID in that being a REALTOR is not a requirement. |

## Request Member Information for a Single Member
Returns MLS information about a single Member from UNLOCK MLS.
## Example Code

### Example URL Request
```markdown
https://api.bridgedataoutput.com/api/v2/OData/{dataset_id}/Member({MemberKey})?access_token={access_token}
```
### Example Response
The same response for a list of Member, except you will receive only data from a single Member

### Request Parameters for the URL

| Name | Type | Description |
|------|------|-------------|
| `access_token` | string | Token to identify the user or application. |
| `dataset` | string | Dataset to get the listings from. |
| `MemberKey` | string | Key to identify a member |
| `$skip` | integer | Skip the first n items |
| `$select` | string | Select properties that are explicitly specified e.g. OfficeType |
| `$unselect` | string | Filter record properties that are explicitly specified e.g. OfficeFax |
| `$top` | integer | Show only the first n items |
| `$orderby` | string | Order items by specified property value, e.g. ModificationTimestamp asc |
| `$filter` | string | Filter items by certain values |
| `$expand` | array | Expand related entities |