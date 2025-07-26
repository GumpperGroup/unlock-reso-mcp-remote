# Property API Endpoint Information

## Request Property Information for a List of Properties
Returns a list of real estate properties (listings) in the MLS from the UNLOCK MLS based on filter parameters in the request.

## Example Code
### Example URL Request
```markdown
https://api.bridgedataoutput.com/api/v2/OData/{dataset_id}/Property?access_token={access_token}
```
### Example Response
```json
{
@odata.context: "https://api.bridgedataoutput.com/api/v2/OData/{dataset_id}/$metadata#Property",
@odata.nextLink: "https://api.bridgedataoutput.com/api/v2/OData/{dataset_id}/",
value: [
{
@odata.context: "https://api.bridgedataoutput.com/api/v2/OData/{dataset_id}/$metadata#Property",
@odata.id: "https://api.bridgedataoutput.com/api/v2/OData/{dataset_id}/Property('P_5af601c3fc76173b348291e9')",
ListingKey: "P_5af601c3fc76173b348291e9",
ListingId: "5af601c3fc76173b348291ea",
OriginatingSystemKey: "{dataset_id}",
LotSizeAcres: 6,
LotSizeSquareFeet: 1746,
LotSizeSource: "Agent",
LotSizeDimensions: "75 x 673 x 114 x 284",
LotSizeDimensionsSource: "Assessor",
AssociationFee: 185,
ListPrice: 518538,
BedroomsPossible: 8,
BathroomsTotalInteger: 13,
BedroomsTotal: 3,
MainLevelBathrooms: 2,
FireplacesTotal: 1,
FireplaceFeatures: [
"One",
"Living Room Fireplace"
],
GarageSpaces: 4,
BathroomsHalf: 2,
Stories: 1,
StoriesTotal: 3,
PublicRemarks: "Nam enim nisi fugit ab. ",
LivingArea: 5211,
LivingAreaUnits: "SquareFeet",
YearBuilt: 1985,
YearBuiltDetails: "Ea pariatur modi debitis sunt nihil provident ut aut.",
YearBuiltSource: "Agent",
StandardStatus: "Active",
MlsStatus: "Active",
PropertyType: "Business",
PropertySubType: "Single Family Residence",
ListingContractDate: "2018-05-11T20:49:07.085Z",
PreviousListPrice: 300393,
OriginalListPrice: 650285,
Contingency: "Quidem mollitia dicta unde perspiciatis laboriosam dolore dolore.",
Disclosures: [
"Bylaw Infractions"
],
NumberOfUnitsTotal: 176,
ListingTerms: [
"Cash"
],
OnMarketDate: "2017-12-04T20:49:07.084Z",
DaysOnMarket: 158,
CloseDate: "2017-08-01T07:24:19.329Z",
StatusChangeTimestamp: "2018-05-11T20:49:07.085Z",
Ownership: "Partnership",
FinancialDataSource: [
"Listing Broker",
"Not Available"
],
Appliances: [
"Dishwasher",
"Disposal"
],
Telephone: [
"Installed"
],
View: [
"View"
],
ViewYN: false,
WaterfrontYN: true,
WaterSource: [
"Municipal"
],
Zoning: "AE",
ZoningDescription: "Agricultural",
AboveGradeFinishedArea: 2221,
BelowGradeFinishedArea: 3513,
RoomsTotal: 15,
ExteriorFeatures: [
"Balcony",
"Fenced Yard",
"Sprinkler"
],
Flooring: [
"Hardwood"
],
FoundationDetails: "Pile",
FrontageType: [
"Golf Course"
],
FrontageLength: 275,
RoadResponsibility: [
"City"
],
Gas: [
"Available"
],
AccessibilityFeatures: [
"Ramp"
],
Heating: [
"Electric",
"Wood"
],
AdditionalParcelsYN: false,
OccupantName: "Albertha Guillermo Wiza",
OccupantPhone: "224-423-6596 x4231",
OccupantType: "Vacant",
PoolPrivateYN: false,
Possession: [
"Close of Escrow"
],
RoadSurfaceType: "Cement",
Roof: [
"Metal"
],
ConstructionMaterials: [
"Wood"
],
Sewer: [
"Yes Connected"
],
CarportSpaces: 2,
OpenParkingYN: true,
LaundryFeatures: [
"In Kitchen",
"Gas Dryer Hookup",
"Washer"
],
PrivateRemarks: "Vero delectus sapiente neque. Quidem debitis libero nulla placeat fuga fugiat consectetur.",
TaxAssessedValue: 856307,
TaxAnnualAmount: 573226,
TaxYear: 2017,
TaxStatusCurrent: [
"Assessed"
],
SubdivisionName: "est",
ModificationTimestamp: "2018-02-04T21:45:33.357Z",
BuyerFinancing: [
"Assumed",
"Cash",
"Contract",
"Conventional",
"FHA",
"FHA 203(b)",
"FHA 203(k)"
],
NewConstructionYN: false,
HomeWarrantyYN: true,
ArchitecturalStyle: [
"distinctio",
"impedit"
],
CommunityFeatures: [
"doloremque"
],
PatioAndPorchFeatures: [
"veritatis",
"pariatur",
"molestias",
"quos",
"provident",
"veniam",
"temporibus",
"totam",
"ut"
],
OtherStructures: [
"laboriosam",
"qui",
"ut",
"illo",
"porro",
"nemo",
"et"
],
ParcelNumber: 1578,
AttachedGarageYN: true,
CarportYN: false,
ContractStatusChangeDate: "2017-10-24T16:44:40.821Z",
ContingentDate: "2017-09-17T09:17:06.633Z",
OriginalEntryTimestamp: "2017-06-02T00:38:48.682Z",
AssociationYN: false,
AssociationName: "voluptatem",
AssociationFeeFrequency: "Monthly",
PhotosCount: 2,
ListingService: "Limited Service",
ListingAggreement: "Exclusive Agency",
LeaseConsideredYN: true,
CopyrightNotice: "Nemo accusantium aliquid eveniet impedit ipsa ut soluta id.",
Disclaimer: "Expedita aperiam placeat eligendi aspernatur sit. Eius sit tenetur sequi sit et.",
PendingTimestamp: "2017-11-08T23:17:50.104Z",
PriceChangeTimestamp: "2017-08-15T03:05:25.153Z",
MajorChangeType: "Price reduction",
MajoreChangeTimestamp: "2017-08-25T19:45:11.311Z",
DualVariableCompensationYN: false,
SignOnPropertyYN: false,
InternetEntireListingDisplayYN: false,
InternetAddressDisplayYN: false,
InternetConsumerCommentYN: true,
InternetAutomatedValuationDisplayYN: true,
SyndicateTo: [
"Zillow",
"Trulia",
"hotspads.com"
],
PrivateOfficeRemarks: "Cupiditate odit beatae sit quis placeat doloremque aut vero. .",
ShowingInstructions: "Esse laborum non consectetur et voluptas quis at.",
ShowingContactPhone: "612-812-6467",
ShowingContactName: "Dameon Howard Schulist",
ShowingContactType: "Agent",
LockBoxLocation: "Recusandae non expedita corrupti officia molestiae fugit.",
LockBoxType: "Rerum sint accusamus aliquid voluptas. Voluptatem sunt et consequatur. Fugit quaerat id temporibus optio ut fugit.",
LockBoxSerialNumber: "uhn4dkn1sj1tx78bkmy81e717",
AccessCode: "9y4x",
Exclusions: "Ut recusandae sunt qui odio quia sit nostrum. Odit maiores voluptates rem modi. Eveniet voluptatem magnam fugiat. Sed maxime et in. Commodi pariatur molestiae facilis architecto.",
Inclusions: "Pariatur vel nisi quo similique dolorem. Porro velit suscipit modi deleniti dolor rem voluptatem.",
SpecialListingConditions: [
"Standard",
"REO",
"Short Sale",
"Probate",
"Auction"
],
ConcessionComments: "Illum enim ipsa ut possimus sit mollitia. Quo autem quo iste quo sit.",
Directions: "Officiis ut alias ex libero. Ea est aperiam qui soluta animi eum ipsam vel.",
ElementarySchool: "Watsica Group",
ElementarySchoolDistrict: "New Hampshire",
MiddleOrJuniorSchool: "Schultz-Rempel",
MiddleOrJuniorSchoolDistrict: "Texas",
HighSchool: "Graham and Sons",
HighSchoolDistrict: "South Carolina",
LandLeaseYN: true,
LandLeaseAmount: 47535197463,
LandLeaseAmountFrequency: "Bi-Weekly",
LandLeaseExpireactionDate: "2018-06-26T11:40:32.694Z",
HorseYN: true,
SeniorCommunityYN: false,
PropertyAttachedYN: true,
GarageYN: true,
Levels: [
"One Level",
"Two Level",
"Split Level"
],
LivingAreaSource: "Estimate",
AboveGradeFinishedAreaSource: "Estimate",
AboveGradeFinishedAreaUnits: "Square Feet",
FoundationArea: 505038,
CoveredSpaces: 4,
ParkingTotal: 1,
EntryLocation: "Top Level",
BuilderName: "Pacocha, Welch and Ziemann",
BuilderModel: "Rustic Steel Computer",
InteriorFeatures: "Atque doloribus qui non mollitia voluptatibus qui nostrum et.",
DirectionFaces: "North-East",
GreenEnergyEfficient: [
"Energy efficient doors",
"Energy efficient windows",
"Energy efficient stove"
],
Walkscore: 78,
TaxLot: "Lot 19 of Block 23 of Tract 2544 of East Jena",
TaxBlock: "Lot 1 of Block 0 of Tract 2270 of Yasmineton",
TaxTract: "Lot 13 of Block 50 of Tract 878 of Schuliststad",
TaxLegalDescription: "Ab eum eos et eligendi et in aut. Enim saepe temporibus sapiente perspiciatis qui est.",
Media: [
{
MediaURL: "https://dvvjkgh94f2v6.cloudfront.net/8v8b238/24i9v02ojs.jpg",
MediaObjectID: "ME_5af601c3fc76173b348291e7",
Order: 1,
MimeType: "image/jpeg",
ShortDescription: "Ventito catena tempus acsi ceno."
},
{
MediaURL: "https://dvvjkgh94f2v6.cloudfront.net/8v8b238/24i9v02oj1.jpg",
MediaObjectID: "ME_5af601c3fc76173b348291e8",
Order: 2,
MimeType: "image/jpeg",
ShortDescription: "Denuo tui clementia quis unde."
}
],
Coordinates: [
-122.4248504,
37.76335862
],
City: "Mission Dolores",
CountyOrParish: "San Francisco Co.",
Country: "US",
PostalCode: "94110",
StateOrProvince: "CA",
Longitude: -122.4248504,
Latitude: 37.76335862,
Elevation: 75573,
ElevationUnits: "Meters",
AnchorsCoTenants: [
"Keebler Group"
],
AssociationFee2: 122,
AssociationFee2Frequency: "One Time",
AssociationFeeIncludes: [
"Water",
"Sewer",
"Security",
"Snow Removal",
"Cable TV",
"Earthquake Insurance",
"Insurance",
"Trash",
"Maintenance Grounds",
"Pest Control",
"Utilities",
"Gas"
],
AssociationName2: "Mosciski-Blick",
AssociationPhone: "1-172-732-9966",
AvailabilityDate: "2018-06-12T23:39:16.548Z",
BathroomsFull: 4,
BathroomsOneQuarter: 2,
BathroomsPartial: 5,
BathroomsThreeQuarter: 1,
BathroomsTotalDecimal: 10.25,
BelowGradeFinishedAreaSource: "Assessor",
BelowGradeFinishedAreaUnits: "Square Meteres",
BuildingAreaSource: "Assessor",
BuildingAreaTotal: 9202119,
BuildingAreaUnits: "Square Feet",
BuildingFeatures: [
"Cafeteria"
],
BuildingName: "Mrs. Haylie Bauch Co",
BusinessName: "Kshlerin-Jaskolski",
BusinessType: "Arts and Entertainment",
CityRegion: "Rathstad",
CommonWalls: [
"End Unit",
"No One Above",
"2+ Common Walls",
"No Common Walls",
"No One Below",
"1 Common Wall"
],
CoolingYN: false,
DocumentsCount: 1,
DoorFeatures: [
"Truck Doors",
"French Doors"
],
ElectricOnPropertyYN: true,
Fencing: [
"Chain Link",
"Wood",
"Block",
"Wrought Iron"
],
FireplaceYN: false,
HeatingYN: true,
ListAgentFirstName: "Cyrus",
ListAgentFullName: "Cyrus Jaren Krajcik",
ListAgentKey: "M_5af601aecd966d3afc88eb0a",
ListAgentLastName: "Krajcik",
ListAgentMiddleName: "Jaren",
ListAgentMlsId: "5af601aecd966d3afc88eb0b",
ListAgentPreferredPhone: "339.831.5242",
ListOfficeKey: "O_5af6019c75f1043ad481d9d8",
ListOfficeMlsId: "5af6019c75f1043ad481d9d9",
ListOfficeName: "Tremblay, Renner and Ullrich Realty",
LotDimensionsSource: "Assessor",
OriginatingSystemID: "{dataset_id}",
OriginatingSystemName: "{dataset_id}",
OtherEquipment: [
"",
"Generator"
],
IDXParticipationYN: false
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

### Response Properties Data Dictionary

| Name | Type | Description |
|------|------|-------------|
| `Name` | Type | Description |
| `@odata.context` | string | Link to the metadata context. |
| `@odata.id` | string | Link to the OData endpoint for the specific record. |
| `AboveGradeFinishedArea` | number | Finished area within the structure that is at or above the surface of the ground. |
| `AboveGradeFinishedAreaSource` | string | The source of the measurements. This is a pick list of options showing the source of the measurement. i.e. Agent, Assessor, Estimate, etc. |
| `AboveGradeFinishedAreaUnits` | string | A pick list of the unit of measurement for the area. i.e. Square Feet, Square Meters, Acres, etc. |
| `AboveGradeUnfinishedArea` | number | The unfinished area within the structure that is at or above the surface of the ground. |
| `AboveGradeUnfinishedAreaSource` | string | The source of the measurements of the unfinished area above grade. This is a pick list of options showing the source of the measurement (e.g., Agent, Assessor, Estimate). |
| `AboveGradeUnfinishedAreaUnits` | string | A pick list of the unit of measurement for the unfinished area above grade (e.g., Square Feet, Square Meters). |
| `AccessCode` | string | If the property is located behind an unmanned security gate such as in a Gated Community, what is the code to gain access through the secured gate. |
| `AccessibilityFeatures` | string | A list or description of the accessibility features included in the sale/lease. |
| `ActivationDate` | string | Indicates when the listing agent intends to change the property to the Active status. |
| `AdditionalParcelsDescription` | string | If additional parcels are included in the sale, a list of those parcel's IDs separated by commas. Do not include the first or primary parcel number, that should be located in the Parcel Number field. |
| `AdditionalParcelsYN` | boolean | Are there more than one parcel or lot included in the sale? |
| `AnchorsCoTenants` | string | The main or most notable tenants as well as other tenants of the shopping center or mall in which the commercial property is located. |
| `Appliances` | string | A list of the appliances that will be included in the sale/lease of the property. |
| `ApprovalStatus` | string | When an MLS has the ability to set a listing to Draft and/or has facility to allow an agent to input, but their manager to approve the listings before publishing, this field is used for such control. |
| `ArchitecturalStyle` | string | A list describing the style of the structure. For example, Victorian, Ranch, Craftsman, etc. |
| `AssociationAmenities` | string | Amenities provided by the Home Owners Association, Mobile Park or Complex. For example Pool, Clubhouse, etc. |
| `AssociationFee` | number | A fee paid by the homeowner to the Home Owners Association which is used for the upkeep of the common area, neighborhood or other association related benefits. |
| `AssociationFee2` | number | A fee paid by the homeowner to the second of two Home Owners Associations, which is used for the upkeep of the common area, neighborhood or other association related benefits. |
| `AssociationFee2Frequency` | string | The frequency the association fee is paid. For example, Weekly, Monthly, Annually, Bi-Monthly, One Time, etc. |
| `AssociationFeeFrequency` | string | The frequency the association fee is paid. For example, Weekly, Monthly, Annually, Bi-Monthly, One Time, etc. |
| `AssociationFeeIncludes` | string | Services included with the association fee. For example Landscaping, Trash, Water, etc. |
| `AssociationName` | string | The name of the Home Owners Association. |
| `AssociationName2` | string | The name of the second of two Home Owners Association. |
| `AssociationPhone` | string | The phone number of the Home Owners Association. North American 10 digit phone numbers should be in the format of ###-###-#### (separated by hyphens). Other conventions should use the common local standard. International numbers should be preceded by a plus symbol. |
| `AssociationPhone2` | string | The phone number of the second of two Home Owners Association. North American 10 digit phone numbers should be in the format of ###-###-#### (separated by hyphens). Other conventions should use the common local standard. International numbers should be preceded by a plus symbol. |
| `AssociationYN` | boolean | Is there a Home Owners Association. A separate Y/N field is needed because not all associations have dues. |
| `AttachedGarageYN` | boolean | A flag indicating that the garage attached to the dwelling. |
| `AttributionContact` | string | A text field to convey a specific contact phone number or email address for the listing firm. |
| `AvailabilityDate` | string | The date the property will be available for possession/occupation. |
| `AvailableLeaseType` | string | Information about the available types of lease for the property (i.e., Net, NNN, NN, Gross, Absolute Net, Escalation Clause, Ground Lease, etc.). |
| `BackOnMarketDate` | string | The date a listing, which had previously gone off market, went back to being on market. This date typically will reflect contractual dates. System timestamp should leverage the term Timestamp rather than Date in the field name. |
| `Basement` | string | A list of information and features about the basement. i.e. None/Slab, Finished, Partially Finished, Crawl Space, Dirt, Outside Entrance, Radon Mitigation |
| `BasementYN` | boolean | Indicates whether or not the property has a basement. |
| `BathroomsFull` | number | A room containing all 4 of the 4 elements constituting a bath, which are; Toilet, Sink, Bathtub or Shower Head. A Full Bath will typically contain four elements; Sink, Toilet, Tub and Shower Head (in tub or stall). However, some may considered a Sink, Toilet and Tub (without a shower) a Full Bath, others consider this to be a Three Quarter Bath. In the event that BathroomsThreeQuarter is not in use, this field may represent the sum of all Full and Three Quarter bathrooms. |
| `BathroomsHalf` | number | A room containing 2 of the 4 elements constituting a bath, which are; Toilet, Sink, Bathtub or Shower Head. A Half Bath will typically contain a Sink and Toilet. |
| `BathroomsOneQuarter` | number | A room containing 1 of the 4 elements constituting a bath which are; Toilet, Sink, Bathtub or Shower Head. Examples are a vanity with a sink or a WC (Water Closet, which is a room with only a toilet). |
| `BathroomsPartial` | number | The number of partial bathrooms in the property being sold/leased. When used in combination with the BathroomsFull field, this replaces (or is the sum of) all Half and One Quarter bathrooms; and in the event BathroomsThreeQuarter is not used, BathroomsFull replaces (or is the sum of) all Full and Three Quarter baths. This field should not be used in combination with the BathroomsOneQuarter or the BathroomsHalf. |
| `BathroomsThreeQuarter` | number | A room containing 3 of the 4 elements constituting a bath, which are; Toilet, Sink, Bathtub or Shower Head. A typical Three Quarter Bath will contain Sink, Toilet and Shower. Some may considered a Sink, Toilet and Tub (without a shower) a Three Quarter Bath, others consider this to be a Full Bath. |
| `BathroomsTotalDecimal` | number | A decimal representation of the total number of bathrooms. |
| `BathroomsTotalInteger` | number | The simple sum of the number of bathrooms. For example for a property with two Full Bathrooms and one Half Bathroom, the Bathrooms Total Integer will be 3. To express this example as 2.5, use the BathroomsTotalDecimal field. To express this example as 2.1, use the BathroomsTotalNotational. |
| `BedroomsPossible` | number | The sum of BedroomsTotal plus other rooms that may be used as a bedroom but are not defined as bedroom per local policy. |
| `BedroomsTotal` | number | The total number of bedrooms in the dwelling. |
| `BelowGradeFinishedArea` | number | Finished area within the structure that is below ground. |
| `BelowGradeFinishedAreaSource` | string | The source of the measurements. This is a pick list of options showing the source of the measurement. i.e. Agent, Assessor, Estimate, etc. |
| `BelowGradeFinishedAreaUnits` | string | A pick list of the unit of measurement for the area. i.e. Square Feet, Square Meters, Acres, etc. |
| `BelowGradeUnfinishedArea` | number | The unfinished area within the structure that is below ground. |
| `BelowGradeUnfinishedAreaSource` | string | The source of the measurements of the unfinished area below grade. This is a pick list of options showing the source of the measurement (e.g., Agent, Assessor, Estimate). |
| `BelowGradeUnfinishedAreaUnits` | string | A pick list of the unit of measurement for the unfinished area below grade (e.g., Square Feet, Square Meters). |
| `BodyType` | string | Type of mobile home. |
| `BridgeModificationTimestamp` | string | A timestamp representing when last this record was modified in the Bridge system. |
| `BuilderModel` | string | The builders model name or number for the property. |
| `BuilderName` | string | Name of the builder of the property or builder's tract. |
| `BuildingAreaSource` | string | The source of the measurements. This is a pick list of options showing the source of the measurement. i.e. Agent, Assessor, Estimate, etc. |
| `BuildingAreaTotal` | number | Total area of the structure. Includes both finished and unfinished areas. |
| `BuildingAreaUnits` | string | A pick list of the unit of measurement for the area. i.e. Square Feet, Square Meters, Acres, etc. |
| `BuildingFeatures` | string | Features or amenities of the building or business park. |
| `BuildingName` | string | Name of the building or business park. |
| `BusinessName` | string | Name of the business being sold. |
| `BusinessType` | string | The type of business being sold. Retail, Wholesale, Grocery, Food & Bev, etc. |
| `BuyerAgencyCompensation` | string | The total commission to be paid for this sale, expressed as either a percentage or a constant currency amount. |
| `BuyerAgencyCompensationType` | string | A list of types to clarify the value entered in the BuyerAgencyCompensation field. For example $, % or some other clarification of the BuyerAgencyCompensation. |
| `BuyerAgentAOR` | string | The Buyer's Agent's Board or Association of REALTORS. |
| `BuyerAgentCellPhone` | string | North American 10 digit phone numbers should be in the format of ###-###-#### (separated by hyphens). Other conventions should use the common local standard. International numbers should be preceded by a plus symbol. |
| `BuyerAgentDesignation` | string | Designations and certifications acknowledging experience and expertise in various real estate sectors are awarded by NAR and each affiliated group upon completion of required courses. |
| `BuyerAgentDirectPhone` | string | North American 10 digit phone numbers should be in the format of ###-###-#### (separated by hyphens). Other conventions should use the common local standard. International numbers should be preceded by a plus symbol. |
| `BuyerAgentEmail` | string | The email address of the Buyer's Agent. |
| `BuyerAgentFax` | string | North American 10 digit phone numbers should be in the format of ###-###-#### (separated by hyphens). Other conventions should use the common local standard. International numbers should be preceded by a plus symbol. |
| `BuyerAgentFirstName` | string | The first name of the buyer's agent. |
| `BuyerAgentFullName` | string | The full name of the buyer's agent. (First Middle Last) |
| `BuyerAgentHomePhone` | string | North American 10 digit phone numbers should be in the format of ###-###-#### (separated by hyphens). Other conventions should use the common local standard. International numbers should be preceded by a plus symbol. |
| `BuyerAgentKey` | string | A system unique identifier. Specifically, in aggregation systems, the Key is the system unique identifier from the system that the record was just retrieved. This may be identical to the related xxxId identifier, but the key is guaranteed unique for this record set. This is a foreign key relating to the Member resource's MemberKey. |
| `BuyerAgentKeyNumeric` | number | A system unique identifier. Specifically, in aggregation systems, the Key is the system unique identifier from the system that the record was just retrieved. This may be identical to the related xxxId identifier, but the key is guaranteed unique for this record set. This is a foreign key relating to the Member resource's MemberKey. This is the numeric only key and used as an alternative to the BuyerAgentKey field. |
| `BuyerAgentLastName` | string | The last name of the buyer's agent. |
| `BuyerAgentMiddleName` | string | The middle name of the buyer's agent. |
| `BuyerAgentMlsId` | string | The local, well-known identifier. This value may not be unique, specifically in the case of aggregation systems, this value should be the identifier from the original system. |
| `BuyerAgentMobilePhone` | string | North American 10 digit phone numbers should be in the format of ###-###-#### (separated by hyphens). Other conventions should use the common local standard. International numbers should be preceded by a plus symbol. |
| `BuyerAgentNamePrefix` | string | Prefix to the name (e.g. Dr. Mr. Ms. etc.) |
| `BuyerAgentNameSuffix` | string | Suffix to the BuyerAgentLastName (e.g. Esq., Jr., III etc.) |
| `BuyerAgentNationalAssociationId` | string | The national association ID of the buyer's agent (e.g., the NRDS number in the U.S.). |
| `BuyerAgentOfficePhone` | string | North American 10 digit phone numbers should be in the format of ###-###-#### (separated by hyphens). Other conventions should use the common local standard. International numbers should be preceded by a plus symbol. |
| `BuyerAgentOfficePhoneExt` | string | The extension of the given phone number (if applicable). |
| `BuyerAgentPager` | string | North American 10 digit phone numbers should be in the format of ###-###-#### (separated by hyphens). Other conventions should use the common local standard. International numbers should be preceded by a plus symbol. |
| `BuyerAgentPreferredPhone` | string | North American 10 digit phone numbers should be in the format of ###-###-#### (separated by hyphens). Other conventions should use the common local standard. International numbers should be preceded by a plus symbol. |
| `BuyerAgentPreferredPhoneExt` | string | The extension of the given phone number (if applicable). |
| `BuyerAgentStateLicense` | string | The license of the buyers agent. Separate multiple licenses with a comma and space. |
| `BuyerAgentTollFreePhone` | string | North American 10 digit phone numbers should be in the format of ###-###-#### (separated by hyphens). Other conventions should use the common local standard. International numbers should be preceded by a plus symbol. |
| `BuyerAgentURL` | string | The website URI of the buyers agent. |
| `BuyerAgentVoiceMail` | string | North American 10 digit phone numbers should be in the format of ###-###-#### (separated by hyphens). Other conventions should use the common local standard. International numbers should be preceded by a plus symbol. |
| `BuyerAgentVoiceMailExt` | string | The extension of the given phone number (if applicable). |
| `BuyerBrokerageCompensation` | string | The total commission to be paid for this sale, expressed as either a percentage or a constant currency amount. |
| `BuyerBrokerageCompensationType` | string | A list of types to clarify the value entered in the BuyerBrokerageCompensation field. For example $, % or some other clarification of the BuyerBrokerageCompensation. |
| `BuyerFinancing` | string | A list of options that describe the type of financing used. This field is used when setting a listing to Closed. i.e. cash, FHA loan, etc. |
| `BuyerOfficeAOR` | string | The Buyer's Office's Board or Association of REALTORS. |
| `BuyerOfficeEmail` | string | The email address of the Buyer's Office. |
| `BuyerOfficeFax` | string | North American 10 digit phone numbers should be in the format of ###-###-#### (separated by hyphens). Other conventions should use the common local standard. International numbers should be preceded by a plus symbol. |
| `BuyerOfficeKey` | string | A system unique identifier. Specifically, in aggregation systems, the Key is the system unique identifier from the system that the record was just retrieved. This may be identical to the related xxxId identifier, but the key is guaranteed unique for this record set. This is a foreign key relating to the Office resource's OfficeKey. |
| `BuyerOfficeKeyNumeric` | number | A system unique identifier. Specifically, in aggregation systems, the Key is the system unique identifier from the system that the record was just retrieved. This may be identical to the related xxxId identifier, but the key is guaranteed unique for this record set. This is a foreign key relating to the Office resource's OfficeKey. This is the numeric only key and used as an alternative to the BuyerOfficeKey field. |
| `BuyerOfficeMlsId` | string | The local, well-known identifier. This value may not be unique, specifically in the case of aggregation systems, this value should be the identifier from the original system. |
| `BuyerOfficeName` | string | The legal name of the brokerage representing the buyer. |
| `BuyerOfficeNationalAssociationId` | string | The national association ID of the buyer's office (e.g., the NRDS number in the U.S.). |
| `BuyerOfficePhone` | string | North American 10 digit phone numbers should be in the format of ###-###-#### (separated by hyphens). Other conventions should use the common local standard. International numbers should be preceded by a plus symbol. |
| `BuyerOfficePhoneExt` | string | The extension of the given phone number (if applicable). |
| `BuyerOfficeURL` | string | The website URI for the buyers office. |
| `BuyerTeamKey` | string | A system unique identifier. Specifically, in aggregation systems, the Key is the system unique identifier from the system that the record was just retrieved. This may be identical to the related xxxId identifier, but the key is guaranteed unique for this record set. This is a foreign key relating to the Teams resource's TeamKey. |
| `BuyerTeamKeyNumeric` | number | A system unique identifier. Specifically, in aggregation systems, the Key is the system unique identifier from the system that the record was just retrieved. This may be identical to the related xxxId identifier, but the key is guaranteed unique for this record set. This is a foreign key relating to the Teams resource's TeamKey. This is the numeric only key and used as an alternative to the BuyerTeamKey field. |
| `BuyerTeamName` | string | The name of the team representing the buyer. |
| `CableTvExpense` | number | The annual expense that is not paid directly by the tenant and is included in the Operating Expense calculations. |
| `CancelationDate` | string | Date the listing contract between the seller and listing agent was cancelled. This is the date entered by the agent reflecting when the change occurred contractually, not a timestamp of when the change was made in the MLS. |
| `CancellationDate` | string | The date that the listing contract between the seller and listing agent was canceled. This is the date entered by the agent reflecting when the change occurred contractually, not a timestamp of when the change was made in the MLS. |
| `CapRate` | number | Cap Rate is equivalent to the return on investment you would receive if you pay cash for a property. The ratio between the net operating income produced by an asset and its capital cost (the original price paid to buy the asset) or alternatively its current market value. |
| `CarportSpaces` | number | The number of carport spaces included in the sale. |
| `CarportYN` | boolean | A flag indicating that the listing has a car port. This flag may be T/F, Y/N or other true, false or unknown indicator. As with all flags, the field may be null. |
| `CarrierRoute` | string | The group of addresses to which the USPS assigns the same code to aid in mail delivery. For the USPS, these codes are 9 digits: 5 numbers for the ZIP Code, one letter for the carrier route type, and 3 numbers for the carrier route number. |
| `City` | string | The city in listing address. |
| `CityRegion` | string | A sub-section or area of a defined city. Examples would be SOHO in New York, NY, Ironbound in Newark, NJ or Inside the Beltway. |
| `CloseDate` | string | With for-sale listings, the date the purchase agreement was fulfilled. With lease listings, the date the requirements were fulfilled, such as contract and/or deposit. This is the date entered by the agent reflecting when the change occurred contractually, not a timestamp of when the change was made in the MLS. |
| `ClosePrice` | number | The amount of money paid by the purchaser to the seller for the property under the agreement. |
| `CoBuyerAgentAOR` | string | The Co Buyer's Agent's Board or Association of REALTORS. |
| `CoBuyerAgentCellPhone` | string | North American 10 digit phone numbers should be in the format of ###-###-#### (separated by hyphens). Other conventions should use the common local standard. International numbers should be preceded by a plus symbol. |
| `CoBuyerAgentDesignation` | string | Designations and certifications acknowledging experience and expertise in various real estate sectors are awarded by NAR and each affiliated group upon completion of required courses. |
| `CoBuyerAgentDirectPhone` | string | North American 10 digit phone numbers should be in the format of ###-###-#### (separated by hyphens). Other conventions should use the common local standard. International numbers should be preceded by a plus symbol. |
| `CoBuyerAgentEmail` | string | The email address of the Buyer's Co Agent. |
| `CoBuyerAgentFax` | string | North American 10 digit phone numbers should be in the format of ###-###-#### (separated by hyphens). Other conventions should use the common local standard. International numbers should be preceded by a plus symbol. |
| `CoBuyerAgentFirstName` | string | The first name of the buyer's co-agent. |
| `CoBuyerAgentFullName` | string | The full name of the buyer's co-agent. (First Middle Last) |
| `CoBuyerAgentHomePhone` | string | North American 10 digit phone numbers should be in the format of ###-###-#### (separated by hyphens). Other conventions should use the common local standard. International numbers should be preceded by a plus symbol. |
| `CoBuyerAgentKey` | string | A system unique identifier. Specifically, in aggregation systems, the Key is the system unique identifier from the system that the record was just retrieved. This may be identical to the related xxxId identifier, but the key is guaranteed unique for this record set. This is a foreign key relating to the Member resource's MemberKey. |
| `CoBuyerAgentKeyNumeric` | number | A system unique identifier. Specifically, in aggregation systems, the Key is the system unique identifier from the system that the record was just retrieved. This may be identical to the related xxxId identifier, but the key is guaranteed unique for this record set. This is a foreign key relating to the Member resource's MemberKey. This is the numeric only key and used as an alternative to the CoBuyerAgentKey field. |
| `CoBuyerAgentLastName` | string | The last name of the buyer's co-agent. |
| `CoBuyerAgentMiddleName` | string | The middle name of the buyer's co-agent. |
| `CoBuyerAgentMlsId` | string | The local, well-known identifier. This value may not be unique, specifically in the case of aggregation systems, this value should be the identifier from the original system. |
| `CoBuyerAgentMobilePhone` | string | North American 10 digit phone numbers should be in the format of ###-###-#### (separated by hyphens). Other conventions should use the common local standard. International numbers should be preceded by a plus symbol. |
| `CoBuyerAgentNamePrefix` | string | Prefix to the name (e.g. Dr. Mr. Ms. etc.) |
| `CoBuyerAgentNameSuffix` | string | Suffix to the CoBuyerAgentLastName (e.g. Esq., Jr., III etc.) |
| `CoBuyerAgentNationalAssociationId` | string | The national association ID of the co-buyer's agent (e.g., the NRDS number in the U.S.). |
| `CoBuyerAgentOfficePhone` | string | North American 10 digit phone numbers should be in the format of ###-###-#### (separated by hyphens). Other conventions should use the common local standard. International numbers should be preceded by a plus symbol. |
| `CoBuyerAgentOfficePhoneExt` | string | The extension of the given phone number (if applicable). |
| `CoBuyerAgentPager` | string | North American 10 digit phone numbers should be in the format of ###-###-#### (separated by hyphens). Other conventions should use the common local standard. International numbers should be preceded by a plus symbol. |
| `CoBuyerAgentPreferredPhone` | string | North American 10 digit phone numbers should be in the format of ###-###-#### (separated by hyphens). Other conventions should use the common local standard. International numbers should be preceded by a plus symbol. |
| `CoBuyerAgentPreferredPhoneExt` | string | The extension of the given phone number (if applicable). |
| `CoBuyerAgentStateLicense` | string | The license of the co-buyers agent. Separate multiple licenses with a comma and space. |
| `CoBuyerAgentTollFreePhone` | string | North American 10 digit phone numbers should be in the format of ###-###-#### (separated by hyphens). Other conventions should use the common local standard. International numbers should be preceded by a plus symbol. |
| `CoBuyerAgentURL` | string | The website URI of the co-buyers agent. |
| `CoBuyerAgentVoiceMail` | string | North American 10 digit phone numbers should be in the format of ###-###-#### (separated by hyphens). Other conventions should use the common local standard. International numbers should be preceded by a plus symbol. |
| `CoBuyerAgentVoiceMailExt` | string | The extension of the given phone number (if applicable). |
| `CoBuyerOfficeAOR` | string | The Co Buyer's Office's Board or Association of REALTORS. |
| `CoBuyerOfficeEmail` | string | The email address of the Buyer's Co Office. |
| `CoBuyerOfficeFax` | string | North American 10 digit phone numbers should be in the format of ###-###-#### (separated by hyphens). Other conventions should use the common local standard. International numbers should be preceded by a plus symbol. |
| `CoBuyerOfficeKey` | string | A system unique identifier. Specifically, in aggregation systems, the Key is the system unique identifier from the system that the record was just retrieved. This may be identical to the related xxxId identifier, but the key is guaranteed unique for this record set. This is a foreign key relating to the Office resource's OfficeKey. |
| `CoBuyerOfficeKeyNumeric` | number | A system unique identifier. Specifically, in aggregation systems, the Key is the system unique identifier from the system that the record was just retrieved. This may be identical to the related xxxId identifier, but the key is guaranteed unique for this record set. This is a foreign key relating to the Office resource's OfficeKey. This is the numeric only key and used as an alternative to the CoBuyerOfficeKey field. |
| `CoBuyerOfficeMlsId` | string | The local, well-known identifier. This value may not be unique, specifically in the case of aggregation systems, this value should be the identifier from the original system. |
| `CoBuyerOfficeName` | string | The legal name of the brokerage co-representing the buyer. |
| `CoBuyerOfficeNationalAssociationId` | string | The national association ID of the co-buyer's office (e.g., the NRDS number in the U.S.). |
| `CoBuyerOfficePhone` | string | North American 10 digit phone numbers should be in the format of ###-###-#### (separated by hyphens). Other conventions should use the common local standard. International numbers should be preceded by a plus symbol. |
| `CoBuyerOfficePhoneExt` | string | The extension of the given phone number (if applicable). |
| `CoBuyerOfficeURL` | string | The website URI for the co-buyers office. |
| `CoListAgentAOR` | string | The Co Listing Agent's Board or Association of REALTORS. |
| `CoListAgentCellPhone` | string | North American 10 digit phone numbers should be in the format of ###-###-#### (separated by hyphens). Other conventions should use the common local standard. International numbers should be preceded by a plus symbol. |
| `CoListAgentDesignation` | string | Designations and certifications acknowledging experience and expertise in various real estate sectors are awarded by NAR and each affiliated group upon completion of required courses. |
| `CoListAgentDirectPhone` | string | North American 10 digit phone numbers should be in the format of ###-###-#### (separated by hyphens). Other conventions should use the common local standard. International numbers should be preceded by a plus symbol. |
| `CoListAgentEmail` | string | The email address of the Co Listing Agent. |
| `CoListAgentFax` | string | North American 10 digit phone numbers should be in the format of ###-###-#### (separated by hyphens). Other conventions should use the common local standard. International numbers should be preceded by a plus symbol. |
| `CoListAgentFirstName` | string | The first name of the co-listing agent. |
| `CoListAgentFullName` | string | The full name of the co-listing agent. (First Middle Last) |
| `CoListAgentHomePhone` | string | North American 10 digit phone numbers should be in the format of ###-###-#### (separated by hyphens). Other conventions should use the common local standard. International numbers should be preceded by a plus symbol. |
| `CoListAgentKey` | string | A system unique identifier. Specifically, in aggregation systems, the Key is the system unique identifier from the system that the record was just retrieved. This may be identical to the related xxxId identifier, but the key is guaranteed unique for this record set. This is a foreign key relating to the Member resource's MemberKey. |
| `CoListAgentKeyNumeric` | number | A system unique identifier. Specifically, in aggregation systems, the Key is the system unique identifier from the system that the record was just retrieved. This may be identical to the related xxxId identifier, but the key is guaranteed unique for this record set. This is a foreign key relating to the Member resource's MemberKey. This is the numeric only key and used as an alternative to the CoListAgentKey field. |
| `CoListAgentLastName` | string | The last name of the co-listing agent. |
| `CoListAgentMiddleName` | string | The middle name of the co-listing agent. |
| `CoListAgentMlsId` | string | The local, well-known identifier. This value may not be unique, specifically in the case of aggregation systems, this value should be the identifier from the original system. |
| `CoListAgentMobilePhone` | string | North American 10 digit phone numbers should be in the format of ###-###-#### (separated by hyphens). Other conventions should use the common local standard. International numbers should be preceded by a plus symbol. |
| `CoListAgentNamePrefix` | string | Prefix to the name (e.g. Dr. Mr. Ms. etc.) |
| `CoListAgentNameSuffix` | string | Suffix to the CoListAgentLastName (e.g. Esq., Jr., III etc.) |
| `CoListAgentNationalAssociationId` | string | The national association ID of the co-listing agent (e.g., the NRDS number in the U.S.). |
| `CoListAgentOfficePhone` | string | North American 10 digit phone numbers should be in the format of ###-###-#### (separated by hyphens). Other conventions should use the common local standard. International numbers should be preceded by a plus symbol. |
| `CoListAgentOfficePhoneExt` | string | The extension of the given phone number (if applicable). |
| `CoListAgentPager` | string | North American 10 digit phone numbers should be in the format of ###-###-#### (separated by hyphens). Other conventions should use the common local standard. International numbers should be preceded by a plus symbol. |
| `CoListAgentPreferredPhone` | string | North American 10 digit phone numbers should be in the format of ###-###-#### (separated by hyphens). Other conventions should use the common local standard. International numbers should be preceded by a plus symbol. |
| `CoListAgentPreferredPhoneExt` | string | The extension of the given phone number (if applicable). |
| `CoListAgentStateLicense` | string | The license of the co-listing agent. Separate multiple licenses with a comma and space. |
| `CoListAgentTollFreePhone` | string | North American 10 digit phone numbers should be in the format of ###-###-#### (separated by hyphens). Other conventions should use the common local standard. International numbers should be preceded by a plus symbol. |
| `CoListAgentURL` | string | The website URI of the co-listing agent. |
| `CoListAgentVoiceMail` | string | North American 10 digit phone numbers should be in the format of ###-###-#### (separated by hyphens). Other conventions should use the common local standard. International numbers should be preceded by a plus symbol. |
| `CoListAgentVoiceMailExt` | string | The extension of the given phone number (if applicable). |
| `CoListOfficeAOR` | string | The Co Listing Office's Board or Association of REALTORS. |
| `CoListOfficeEmail` | string | The email address of the Co Listing Office. |
| `CoListOfficeFax` | string | North American 10 digit phone numbers should be in the format of ###-###-#### (separated by hyphens). Other conventions should use the common local standard. International numbers should be preceded by a plus symbol. |
| `CoListOfficeKey` | string | A system unique identifier. Specifically, in aggregation systems, the Key is the system unique identifier from the system that the record was just retrieved. This may be identical to the related xxxId identifier, but the key is guaranteed unique for this record set. This is a foreign key relating to the Office resource's OfficeKey. |
| `CoListOfficeKeyNumeric` | number | A system unique identifier. Specifically, in aggregation systems, the Key is the system unique identifier from the system that the record was just retrieved. This may be identical to the related xxxId identifier, but the key is guaranteed unique for this record set. This is a foreign key relating to the Office resource's OfficeKey. This is the numeric only key and used as an alternative to the CoListOfficeKey field. |
| `CoListOfficeMlsId` | string | The local, well-known identifier. This value may not be unique, specifically in the case of aggregation systems, this value should be the identifier from the original system. |
| `CoListOfficeName` | string | The legal name of the brokerage co-representing the seller. |
| `CoListOfficeNationalAssociationId` | string | The national association ID of the co-listing office (e.g., the NRDS number in the U.S.). |
| `CoListOfficePhone` | string | North American 10 digit phone numbers should be in the format of ###-###-#### (separated by hyphens). Other conventions should use the common local standard. International numbers should be preceded by a plus symbol. |
| `CoListOfficePhoneExt` | string | The extension of the given phone number (if applicable). |
| `CoListOfficeURL` | string | The website URI for the co-listing office. |
| `CommonInterest` | string | Common Interest is a type of ownership in a property that is composed of an individual lot or unit and a share of the ownership or use of common areas. A Common Interest Development (CID) is usually governed by a recorded set of Covenants, Conditions & Restrictions (CC&Rs). |
| `CommonWalls` | string | A multi select list with options like 1 Common Wall, 2 Common Walls, No Common Walls, No One Above, No One Below. Implementation should include rules preventing illogical selection combinations and to ensure consistency with the Property Attached Y/N field. |
| `CommunityFeatures` | string | A list of features related to, or available within, the community. |
| `CompensationComments` | string | A textual description of the compensation involved in the transaction. |
| `CompSaleYN` | boolean | Indicates whether or not this sale was entered for comparative purposes. |
| `Concessions` | string | Are there concessions included in the sales agreement? Yes, No or Call Listing Agent |
| `ConcessionsAmount` | number | The dollar amount of the concessions. If the concessions are made by the seller, some may subtract this value from the sales price as a means of calculating their own true price. If concessions are made by the buyer, some may add this amount to the sale price to create their own true price. Concessions made by both buyer and seller should be subtracted from each other providing a net value. Details of this calculation should be added to the Concessions Comments field. |
| `ConcessionsComments` | string | Comments describing the concessions made by the buyer or the seller. |
| `ConstructionMaterials` | string | A list of the materials that were used in the construction of the property. |
| `ContinentRegion` | string | A sub-section or area of a continent. Examples would be Southern Europe or Scandinavia. |
| `Contingency` | string | A list of contingencies that must be satisfied in order to complete the transaction. |
| `ContingentDate` | string | The date an offer was made with a contingency. The Listing remains On Market. This is the date entered by the agent reflecting when the change occurred contractually, not a timestamp of when the change was made in the MLS. |
| `ContractStatusChangeDate` | string | The date of the listings contractual status change. This is not necessarily the time the agent made the change in the MLS system, but rather the date of the contractual change. |
| `Cooling` | string | A list describing the cooling or air conditioning features of the property. |
| `CoolingYN` | boolean | The property has cooling or Air Conditioning. |
| `Coordinates` | array | Geographical coordinates (longitude, latitude) |
| `CopyrightNotice` | string | Notice of the legal rights of the owner of the information or data. |
| `Country` | string | The country abbreviation in a postal address. |
| `CountryRegion` | string | A sub-section or area of a defined country. Examples would be Napa Valley in the US, or the Amalfi Coast in Italy. |
| `CountyOrParish` | string | The County, Parish or other regional authority |
| `CoveredSpaces` | number | The total number of garage and carport spaces. |
| `CropsIncludedYN` | boolean | Are crops included in the sale of the property. |
| `CrossStreet` | string | Nearest cross streets to the property. This field is in addition to, and independent of, the driving directions field. |
| `CultivatedArea` | number | Measurement or percentage of the property that has been cultivated. |
| `CumulativeDaysOnMarket` | number | The number of days the property is on market, as defined by the MLS business rules. |
| `CurrentFinancing` | string | A list of options that describe the type of financing that the seller currently has in place for the property being sold. i.e. cash, assumable, FHA loan, etc. |
| `CurrentUse` | string | A list of the type(s) of current use of the property. The current use of the property is an important factor in understanding the overall condition of the land and determining it's appropriateness for intended use. |
| `DaysInMls` | number | The number of days the listing was on market within the MLS system. Like Days on Market, where the calculation can be based on a number of on-market and off-market events, Days in MLS is best defined as being based upon timestamps of when entry or changes were made in the MLS. |
| `DaysOnMarket` | number | The number of days the listing is on market, as defined by the MLS business rules. |
| `DaysOnSite` | number | The number of days the listing appeared on the given site, typically a public portal. |
| `DevelopmentStatus` | string | A list of the Development Status of the property. The developmental status of land is an important factor in selling, purchasing and developing of land properties. |
| `DirectionFaces` | string | The compass direction that the main entrance to the building faces. For example, North, South, East, West, South-West, etc. It may also be known as the building exposure. |
| `Directions` | string | Driving directions to the property. |
| `Disclaimer` | string | Text that serves as the negation or limitation of the rights under a warranty given by a seller to a buyer. |
| `Disclosures` | string | Legal or pertinent information that should be disclosed to potential buyer's agents. |
| `DistanceToBusComments` | string | A textual description of the distance to local bus stops. |
| `DistanceToBusNumeric` | number | Numeric distance from the property to the nearest bus stop. |
| `DistanceToBusUnits` | string | A pick list of the unit linear measurement. i.e. feed, meters, yards, kilometers, miles, etc. |
| `DistanceToElectricComments` | string | If the property does not currently have electrical utility, is service available and if so, what is the distance. |
| `DistanceToElectricNumeric` | number | Numeric distance from the property to the electrical utility. |
| `DistanceToElectricUnits` | string | A pick list of the unit linear measurement. i.e. feed, meters, yards, kilometers, miles, etc. |
| `DistanceToFreewayComments` | string | A textual description of the distance to freeways. |
| `DistanceToFreewayNumeric` | number | Numeric distance from the property to the nearest freeway. |
| `DistanceToFreewayUnits` | string | A pick list of the unit linear measurement. i.e. feed, meters, yards, kilometers, miles, etc. |
| `DistanceToGasComments` | string | If the property does not currently have natural gas utility, is service available and if so, what is the distance. |
| `DistanceToGasNumeric` | number | Numeric distance from the property to the gas utility. |
| `DistanceToGasUnits` | string | A pick list of the unit linear measurement. i.e. feed, meters, yards, kilometers, miles, etc. |
| `DistanceToPhoneServiceComments` | string | If the property does not currently have phone service, is service available and if so, what is the distance. |
| `DistanceToPhoneServiceNumeric` | number | Numeric distance from the property to the phone utility. |
| `DistanceToPhoneServiceUnits` | string | A pick list of the unit linear measurement. i.e. feed, meters, yards, kilometers, miles, etc. |
| `DistanceToPlaceofWorshipComments` | string | A textual description of the distance to local places of worship. |
| `DistanceToPlaceofWorshipNumeric` | number | Numeric distance from the property to the nearest place of worship. |
| `DistanceToPlaceofWorshipUnits` | string | A pick list of the unit linear measurement. i.e. feed, meters, yards, kilometers, miles, etc. |
| `DistanceToSchoolBusComments` | string | Distance from the property to the nearest school bus pickup point. |
| `DistanceToSchoolBusNumeric` | number | Numeric distance from the property to the nearest school bus pickup point. |
| `DistanceToSchoolBusUnits` | string | A pick list of the unit linear measurement. i.e. feed, meters, yards, kilometers, miles, etc. |
| `DistanceToSchoolsComments` | string | A textual description of the distance to local schools. |
| `DistanceToSchoolsNumeric` | number | Numeric distance from the property to the nearest school. |
| `DistanceToSchoolsUnits` | string | A pick list of the unit linear measurement. i.e. feed, meters, yards, kilometers, miles, etc. |
| `DistanceToSewerComments` | string | If the property does not currently have sewer or septic, is sewer service available and if so, what is the distance. |
| `DistanceToSewerNumeric` | number | Numeric distance from the property to the sewer utility. |
| `DistanceToSewerUnits` | string | A pick list of the unit linear measurement. i.e. feed, meters, yards, kilometers, miles, etc. |
| `DistanceToShoppingComments` | string | A description of the distance to primary shopping sources such as groceries, gasoline, clothing or department stores. |
| `DistanceToShoppingNumeric` | number | Numeric distance from the property to the nearest shopping. |
| `DistanceToShoppingUnits` | string | A pick list of the unit linear measurement. i.e. feed, meters, yards, kilometers, miles, etc. |
| `DistanceToStreetComments` | string | If the property does not have a maintained road or street adjacent to the lot, what are the conditions of access and distance to a maintained road. |
| `DistanceToStreetNumeric` | number | Numeric distance from the property to the street. |
| `DistanceToStreetUnits` | string | A pick list of the unit linear measurement. i.e. feed, meters, yards, kilometers, miles, etc. |
| `DistanceToWaterComments` | string | If the property does not currently have water utility, is service available and if so, what is the distance. |
| `DistanceToWaterNumeric` | number | Numeric distance from the property to the water utility. |
| `DistanceToWaterUnits` | string | A pick list of the unit linear measurement. i.e. feed, meters, yards, kilometers, miles, etc. |
| `DocumentsAvailable` | string | A list of the Documents available for the property. Knowing what documents are available for the property is valuable information. |
| `DocumentsChangeTimestamp` | string | System generated timestamp of when the last update or change to the documents for this listing was made. |
| `DocumentsCount` | number | The total number of documents or supplements included with the listings. |
| `DocumentStatus` | string | The statuses a document could be in during a transaction. |
| `DOH1` | string | Department of Housing decal number for the mobile or manufactured home. For the first or only unit/section use DOH 1 over DOH 2 or 3. |
| `DOH2` | string | Department of Housing decal number for the mobile or manufactured home. For two units/sections use DOH 1 and 2 over DOH 3. |
| `DOH3` | string | Department of Housing decal number for the mobile or manufactured home. For two units/sections use DOH 1 and 2 over DOH 3. |
| `DoorFeatures` | string | A list of features or description of the doors included in the sale/lease. |
| `DualOrVariableRateCommissionYN` | boolean | A commission arrangement in which the seller agrees to pay a specified commission to the listing broker if the property is sold through the efforts of a cooperating broker. The seller pays the listing broker a different commission amount if there is no cooperating broker involved in the sale or the sale occurs due to the efforts of the seller directly. |
| `DualVariableCompensationYN` | boolean | A commission arrangement in which the seller agrees to pay a specified commission to the listing broker if the property is sold through the efforts of a cooperating broker, but the seller pays the Listing broker a different commission amount if the sale occurs if:1) there is no cooperating broker involved or 2) due to the efforts of the seller directly. |
| `Electric` | string | A list of electric-service related features of the property (e.g. 110 Volt, 3 Phase, 220 Volt, RV Hookup). Note: the previous "Electric" field was renamed to DistanceToElectricComments |
| `ElectricExpense` | number | The annual expense that is not paid directly by the tenant and is included in the Operating Expense calculations. |
| `ElectricOnPropertyYN` | boolean | Does the property currently have electrical utility available on the property. |
| `ElementarySchool` | string | The name of the primary school having a catchment area that includes the associated property. |
| `ElementarySchoolDistrict` | string | The name of the elementary school district having a catchment area that includes the associated property. |
| `Elevation` | number | The elevation of the property in relation to sea level. Use the Elevation Units field to communicate the unit of measurement. i.e. Feet or Meters. |
| `ElevationUnits` | string | A pick list of the unit of measurement used in the Elevation field. i.e. Feet, Meters. |
| `EntryLevel` | number | A numeric field that describes the level within the structure, SFR or a unit in a building, where the main entry to the dwelling is located. When a unit has one floor it is implicit that this is also the level of the unit itself. |
| `EntryLocation` | string | A description of the main entry way to the property. i.e. Elevator, Ground Level w/ Steps, Ground Level w/o Steps, Mid Level, Top Level, etc. |
| `Exclusions` | string | Elements of the property that will not be included in the sale. i.e. Chandeliers will be removed prior to close. |
| `ExistingLeaseType` | string | Information about the status of the existing lease on the property. i.e. Net, NNN, NN, Gross, Absolute Net, Escalation Clause, Ground Lease, etc. |
| `ExpirationDate` | string | The date when the listing agreement will expire. This is the date entered by the agent reflecting when the change occurred, or will occur, contractually, not a timestamp of when the change was made in the MLS. The expiration date of listings, prior to their expiration, cancellation, sale or lease, is confidential information and should be restricted to the agent and their managers, partners or broker. |
| `ExteriorFeatures` | string | A list of features or description of the exterior of the property included in the sale/lease. |
| `FarmCreditServiceInclYN` | boolean | Specifies whether or not Farm Credit Service shares are included in the price of the property. |
| `FarmLandAreaSource` | string | The source of the measurements. This may be a pick list of options showing the source of the measurement. i.e. Agent, Assessor, Estimate, etc. This field applies to all farm area fields (Cultivated, Pasture, Range, Wooded) |
| `FarmLandAreaUnits` | string | A pick list of the unit of measurement for the area. i.e. Square Feet, Square Meters, Acres, etc. This field applies to all farm area fields (Cultivated, Pasture, Range, Wooded) |
| `Fencing` | string | A list of types of fencing found at the property being sold. |
| `FhaEligibility` | string | The status of the property's FHA eligibility. |
| `FinancialDataSource` | string | The source of the Rental information. For example Accountant, Owner, etc. |
| `FireplaceFeatures` | string | A list of features or description of the fireplace(s) included in the sale/lease. |
| `FireplacesTotal` | number | The total number of fireplaces included in the property. |
| `FireplaceYN` | boolean | Does the property include a fireplace. |
| `Flooring` | string | A list of the type(s) of flooring found within the property. |
| `FoundationArea` | number | The area or dimensions of the footprint of the structure on the lot. |
| `FoundationDetails` | string | A list of the type(s) of foundation on which the property sits. |
| `FrontageLength` | string | Textual description of the length of the frontages selected in the Frontage Type field. |
| `FrontageType` | string | Pick list of types of frontage. i.e. Oceanfront, Lakefront, Golf course, etc. Information about roads or road frontage should be located in the Road Frontage Type and Road Surface Type fields. |
| `FuelExpense` | number | The annual expense that is not paid directly by the tenant and is included in the Operating Expense calculations. |
| `Furnished` | string | The property being leased is furnished, unfurnished or partially furnished. |
| `FurnitureReplacementExpense` | number | The annual expense that is not paid directly by the tenant and is included in the Operating Expense calculations. |
| `GarageSpaces` | number | The number of spaces in the garage(s). |
| `GarageYN` | boolean | A flag indicating that the listing has a garage. This flag may be T/F, Y/N or other true, false or unknown indicator. As with all flags, the field may be null. |
| `GardenerExpense` | number | The annual expense that is not paid directly by the tenant and is included in the Operating Expense calculations. |
| `GardnerExpense` | number | The annual expense that is not paid directly by the tenant and is included in the Operating Expense calculations. |
| `Gas` | string | A list of gas-service related features of the property (e.g. Natural Gas, Private LP Tank, None). Note: the previous "Gas" field was renamed to DistanceToGasComments |
| `GrazingPermitsBlmYN` | boolean | Specifies whether or not the property owner has grazing permits from the Bureau of Land Management. |
| `GrazingPermitsForestServiceYN` | boolean | Specifies whether or not the property owner has grazing permits from the Forestry Service. |
| `GrazingPermitsPrivateYN` | boolean | Specifies whether or not the property owner has private grazing permits. |
| `GreenBuildingVerificationType` | string | The name of the verification or certification awarded to a new or pre-existing residential or commercial structure. For example: LEED, Energy Star, ICC-700. In cases where more than one certification have been awarded, leverage multiple iterations of the green verification fields via the repeating element method. |
| `GreenEnergyEfficient` | string | Pick list of general green attributes such as energy efficient doors, or appliances without naming specific elements with ratings that may wane over time. |
| `GreenEnergyGeneration` | string | Methods of generating power that are included in the sale or lease. |
| `GreenIndoorAirQuality` | string | Pick list of indoor air quality measures without naming specific elements with ratings that may wane over time. |
| `GreenLocation` | string | Pick list describing efficiencies involved with the property's location such as walkability or transportation proximity without naming specific elements with ratings that may wane over time. |
| `GreenSustainability` | string | Pick list of sustainable elements used in the construction of the structure without naming specific elements with ratings that may wane over time. |
| `GreenWaterConservation` | string | Pick list of general water conserving attributes of the property such as landscaping or reclamation without naming specific elements with ratings that may wane over time. |
| `GrossIncome` | number | The actual current income from rent and all other revenue generating sources. |
| `GrossLivingAreaAnsi` | number | The total livable area with the structure as measured using American National Standards Institute (ANSI) measurement guidelines |
| `GrossScheduledIncome` | number | The maximum amount of annual rent collected if the property were 100% occupied all year and all tenants paid their rent. |
| `HabitableResidenceYN` | boolean | Does the property include a structure that can be lived in. |
| `Heating` | string | A list describing the heating features of the property. |
| `HeatingYN` | boolean | The property has heating. |
| `HighSchool` | string | The name of the high school having a catchment area that includes the associated property. |
| `HighSchoolDistrict` | string | The name of the high school district having a catchment area that includes the associated property. When only one school district is used, this field should be used over the Junior or Elementary Districts. |
| `HomeWarrantyYN` | boolean | Is a home warranty included in the sale of the property? Single select. |
| `HorseAmenities` | string | A list of horse amenities on the lot or in the community. |
| `HorseYN` | boolean | The Property is allowed to raise horses. |
| `HoursDaysOfOperation` | string | A simplified enumerated list of the days and hours of operation of the business being sold. i.e. Open 24 Hours or Open 7 Days. For more detailed descriptions use the HoursDaysofOperationDescription field. |
| `HoursDaysofOperationDescription` | string | A detailed description of the hours and days the business being sold is open for business. For a specific list of simplified times the business is open, use the HoursDaysofOperation enumerated field. |
| `HoursDaysOfOperationDescription` | string | A detailed description of the hours and days the business being sold is open for business. For a specific list of simplified times the business is open, use the HoursDaysofOperation enumerated field. |
| `IDXParticipationYN` | boolean | Should this listing participate in IDX. |
| `Inclusions` | string | Portable elements of the property that will be included in the sale. |
| `IncomeIncludes` | string | A list of income sources included in the GrossScheduledIncome and GrossIncome. i.e. Laundry, Parking, Recreation, Storage, etc. |
| `InsuranceExpense` | number | The annual expense that is not paid directly by the tenant and is included in the Operating Expense calculations. |
| `InteriorFeatures` | string | A list of features or description of the interior of the property included in the sale/lease. |
| `InternetAddressDisplayYN` | boolean | A yes/no field that states the seller has allowed the listing address to be displayed on Internet sites. |
| `InternetAutomatedValuationDisplayYN` | boolean | A yes/no field that states the seller allows the listing can be displayed with an AVM on Internet sites. |
| `InternetConsumerCommentYN` | boolean | A yes/no field that states the seller allows a comment or blog system to be attached to the listing on Internet sites. |
| `InternetEntireListingDisplayYN` | boolean | A yes/no field that states the seller has allowed the listing to be displayed on Internet sites. |
| `IrrigationSource` | string | The source which the property receives its water for irrigation. |
| `IrrigationWaterRightsAcres` | number | The number of acres allowed under the property's water rights. |
| `IrrigationWaterRightsYN` | boolean | Does the property include water rights for irrigation? A Boolean or Yes / No field. |
| `LaborInformation` | string | Information about labor laws that are applicable to the business being sold. i.e. Union, Non-Union, Employee License Required. |
| `LandLeaseAmount` | number | When the land is not included in the sale, but is leased, the amount of the lease. This is the Space Rent for Mobile homes in a Park. |
| `LandLeaseAmountFrequency` | string | When the land is not included in the sale, but is leased, the frequency the Land Lease Fee is paid. |
| `LandLeaseExpirationDate` | string | When the land is not included in the sale, but is leased, the expiration date of the Land Lease. |
| `LandLeaseYN` | boolean | The land is not included in the sale and a lease exists. |
| `Latitude` | number | The geographic latitude of some reference point on the property, specified in degrees and decimal parts. Positive numbers must not include the plus symbol. |
| `LaundryFeatures` | string | Add this pick list of features and locations where the laundry is located in the property being sold. i.e. Gas Dryer Hookup, In Kitchen, In Garage, etc. CRMLS sees over 50% utilization of this field which has a dozen enumerations making it too long to fold into other fields such as rooms or Interior Features. |
| `LeasableArea` | number | The area that may be leased within the commercial property. |
| `LeasableAreaUnits` | string | A pick list of the unit of measurement for the area. i.e. Square Feet, Square Meters, Acres, etc. |
| `LeaseAmount` | number | The amount of any lease the business pays for it's current location. |
| `LeaseAmountFrequency` | string | The frequency of the LeaseAmount is paid. Monthly, weekly, annual, etc. |
| `LeaseAssignableYN` | boolean | Can the lease at the business' current location be assigned to another party. |
| `LeaseConsideredYN` | boolean | Will the seller consider leasing the property instead of selling? Single select. |
| `LeaseExpiration` | string | The expiration date of the lease for the business' current location. |
| `LeaseRenewalCompensation` | string | A list of compensations other than the original Selling Office Compensation. i.e. Compensation Paid on Renewal, Compensation Paid on Tennant Purchase, No Renewal Commission, Call Listing Office, etc. |
| `LeaseRenewalOptionYN` | boolean | Is there an option to renew the lease at the business' current location. |
| `LeaseTerm` | string | A pick list of lengths that represent the length of the lease. i.e. Weekly, Month to Month, 6 Month Lease, 12 Month Lease, 24 Month Lease. |
| `Levels` | string | The number of levels in the property being sold. For example, One Level, Two Levels, Split Level, Three or More Levels, Multi Level, Loft. A discreet horizontal plane of interior living space (excluding basements). |
| `License1` | string | License number of the mobile or manufactured home. Also known as the Department of Housing label/insignia number. For the first or only unit/section use License 1 over License 2 or 3. |
| `License2` | string | License number of the mobile or manufactured home. Also known as the Department of Housing label/insignia number. For two units/sections use License 1 and 2 over License 3. |
| `License3` | string | License number of the mobile or manufactured home. Also known as the Department of Housing label/insignia number. For two units/sections use License 1 and 2 over License 3. |
| `LicensesExpense` | number | The annual expense that is not paid directly by the tenant and is included in the Operating Expense calculations. |
| `ListAgentAOR` | string | The Listing Agent's Board or Association of REALTORS. |
| `ListAgentCellPhone` | string | North American 10 digit phone numbers should be in the format of ###-###-#### (separated by hyphens). Other conventions should use the common local standard. International numbers should be preceded by a plus symbol. |
| `ListAgentDesignation` | string | Designations and certifications acknowledging experience and expertise in various real estate sectors are awarded by NAR and each affiliated group upon completion of required courses. |
| `ListAgentDirectPhone` | string | North American 10 digit phone numbers should be in the format of ###-###-#### (separated by hyphens). Other conventions should use the common local standard. International numbers should be preceded by a plus symbol. |
| `ListAgentEmail` | string | The email address of the Listing Agent. |
| `ListAgentFax` | string | North American 10 digit phone numbers should be in the format of ###-###-#### (separated by hyphens). Other conventions should use the common local standard. International numbers should be preceded by a plus symbol. |
| `ListAgentFirstName` | string | The first name of the listing agent. |
| `ListAgentFullName` | string | The full name of the listing agent. (First Middle Last) |
| `ListAgentHomePhone` | string | North American 10 digit phone numbers should be in the format of ###-###-#### (separated by hyphens). Other conventions should use the common local standard. International numbers should be preceded by a plus symbol. |
| `ListAgentKey` | string | A system unique identifier. Specifically, in aggregation systems, the ListAgentKey is the system unique identifier from the system that the record was retrieved. This may be identical to the related xxxId. This is a foreign key relating to the Member resource's MemberKey. |
| `ListAgentKeyNumeric` | number | A system unique identifier. Specifically, in aggregation systems, the ListAgentKey is the system unique identifier from the system that the record was retrieved. This may be identical to the related xxxId. This is a foreign key relating to the Member resource's MemberKey. This is the numeric only key and used as an alternative to the ListAgentKey field. |
| `ListAgentLastName` | string | The last name of the listing agent. |
| `ListAgentMiddleName` | string | The middle name of the listing agent. |
| `ListAgentMlsId` | string | The local, well-known identifier for the member. This value may not be unique, specifically in the case of aggregation systems, this value should be the identifier from the original system. |
| `ListAgentMobilePhone` | string | North American 10 digit phone numbers should be in the format of ###-###-#### (separated by hyphens). Other conventions should use the common local standard. International numbers should be preceded by a plus symbol. |
| `ListAgentNamePrefix` | string | Prefix to the name (e.g. Dr. Mr. Ms. etc.) |
| `ListAgentNameSuffix` | string | Suffix to the ListAgentLastName (e.g. Esq., Jr., III etc.) |
| `ListAgentNationalAssociationId` | string | The national association ID of the franchise (i.e., the NRDS number in the U.S.). |
| `ListAgentOfficePhone` | string | North American 10 digit phone numbers should be in the format of ###-###-#### (separated by hyphens). Other conventions should use the common local standard. International numbers should be preceded by a plus symbol. |
| `ListAgentOfficePhoneExt` | string | The extension of the given phone number (if applicable). |
| `ListAgentPager` | string | North American 10 digit phone numbers should be in the format of ###-###-#### (separated by hyphens). Other conventions should use the common local standard. International numbers should be preceded by a plus symbol. |
| `ListAgentPreferredPhone` | string | North American 10 digit phone numbers should be in the format of ###-###-#### (separated by hyphens). Other conventions should use the common local standard. International numbers should be preceded by a plus symbol. |
| `ListAgentPreferredPhoneExt` | string | The extension of the given phone number (if applicable). |
| `ListAgentStateLicense` | string | The license of the listing agent. Separate multiple licenses with a comma and space. |
| `ListAgentTollFreePhone` | string | North American 10 digit phone numbers should be in the format of ###-###-#### (separated by hyphens). Other conventions should use the common local standard. International numbers should be preceded by a plus symbol. |
| `ListAgentURL` | string | The website URI of the listing agent. |
| `ListAgentVoiceMail` | string | North American 10 digit phone numbers should be in the format of ###-###-#### (separated by hyphens). Other conventions should use the common local standard. International numbers should be preceded by a plus symbol. |
| `ListAgentVoiceMailExt` | string | The extension of the given phone number (if applicable). |
| `ListAOR` | string | The responsible Board or Association of REALTORS for this listing. |
| `ListingAgreement` | string | The nature of the agreement between the seller and the listing agent. Examples are Exclusive Agency, Open Listing, etc. |
| `ListingContractDate` | string | The effective date of the agreement between the seller and the seller's broker. This is the date entered by the agent reflecting when the change occurred contractually, not a timestamp of when the change was made in the MLS. |
| `ListingId` | string | The well known identifier for the listing. The value may be identical to that of the Listing Key, but the Listing ID is intended to be the value used by a human to retrieve the information about a specific listing. In a multiple originating system or a merged system, this value may not be unique and may require the use of the provider system to create a synthetic unique value. |
| `ListingKey` | string | A unique identifier for this record from the immediate source. This is a string that can include URI or other forms. Alternatively use the ListingKeyNumeric for a numeric only key field. This is the local key of the system. When records are received from other systems, a local key is commonly applied. If conveying the original keys from the source or originating systems, see SourceSystemKey and OriginatingSystemKey. |
| `ListingKeyNumeric` | number | A unique identifier for this record from the immediate source. This is the numeric only key and used as an alternative to the ListingKey fields. This is the local key of the system. When records are received from other systems, a local key is commonly applied. If conveying the original keys from the source or originating systems, see SourceSystemKey and OriginatingSystemKey. |
| `ListingService` | string | Defines the type or level of service the listing member will be providing to the selling home owner. This will typically be a single selection. Examples include Full Service, Limited Service or Entry Only. |
| `ListingTerms` | string | Terms of the listing such as Lien Release, Subject to Court Approval or Owner Will Carry. Also may include options that describe the financing terms that are acceptable to the seller, i.e. cash, assumable, FHA loan, etc. |
| `ListingURL` | string | Provides a link to the specific listing on a brokerage website, agent website or other public-facing source. |
| `ListingURLDescription` | string | A pick list of options showing where the listing URL resides (i.e., Brokerage Website, Agent Website, etc.). |
| `ListOfficeAOR` | string | The Listing Office's Board or Association of REALTORS. |
| `ListOfficeEmail` | string | The email address of the Listing Office. |
| `ListOfficeFax` | string | North American 10 digit phone numbers should be in the format of ###-###-#### (separated by hyphens). Other conventions should use the common local standard. International numbers should be preceded by a plus symbol. |
| `ListOfficeKey` | string | A system unique identifier. Specifically, in aggregation systems, the Key is the system unique identifier from the system that the record was just retrieved. This may be identical to the related xxxId identifier, but the key is guaranteed unique for this record set. This is a foreign key relating to the Office resource's OfficeKey. |
| `ListOfficeKeyNumeric` | number | A system unique identifier. Specifically, in aggregation systems, the Key is the system unique identifier from the system that the record was just retrieved. This may be identical to the related xxxId identifier, but the key is guaranteed unique for this record set. This is a foreign key relating to the Office resource's OfficeKey. This is the numeric only key and used as an alternative to the ListOfficeKey field. |
| `ListOfficeMlsId` | string | The local, well-known identifier. This value may not be unique, specifically in the case of aggregation systems, this value should be the identifier from the original system. |
| `ListOfficeName` | string | The legal name of the brokerage representing the seller. |
| `ListOfficeNationalAssociationId` | string | The national association ID of the listing office (e.g., the NRDS number in the U.S.). |
| `ListOfficePhone` | string | North American 10 digit phone numbers should be in the format of ###-###-#### (separated by hyphens). Other conventions should use the common local standard. International numbers should be preceded by a plus symbol. |
| `ListOfficePhoneExt` | string | The extension of the given phone number (if applicable). |
| `ListOfficeURL` | string | The website URI for the listing office. |
| `ListPrice` | number | The current price of the property as determined by the seller and the seller's broker. For auctions this is the minimum or reserve price. |
| `ListPriceLow` | number | The lower price used for Value Range Pricing. The List Price must be greater than or equal to the ListPriceLow. |
| `ListTeamKey` | string | A system unique identifier. Specifically, in aggregation systems, the Key is the system unique identifier from the system that the record was just retrieved. This may be identical to the related xxxId identifier, but the key is guaranteed unique for this record set. This is a foreign key relating to the Teams resource's TeamKey. |
| `ListTeamKeyNumeric` | number | A system unique identifier. Specifically, in aggregation systems, the Key is the system unique identifier from the system that the record was just retrieved. This may be identical to the related xxxId identifier, but the key is guaranteed unique for this record set. This is a foreign key relating to the Teams resource's TeamKey. This is the numeric only key and used as an alternative to the ListTeamKey field. |
| `ListTeamName` | string | The name of the team representing the seller. |
| `LivingArea` | number | The total livable area within the structure. |
| `LivingAreaSource` | string | The source of the measurements. This is a pick list of options showing the source of the measurement. i.e. Agent, Assessor, Estimate, etc. |
| `LivingAreaUnits` | string | A pick list of the unit of measurement for the area. i.e. Square Feet, Square Meters, Acres, etc. |
| `LockBoxLocation` | string | A field describing the location of the lock box. |
| `LockBoxSerialNumber` | string | The serial number of the lockbox placed on the property. |
| `LockBoxType` | string | A field describing the type of lock box. |
| `Longitude` | number | The geographic longitude of some reference point on the property, specified in degrees and decimal parts. Positive numbers must not include the plus symbol. |
| `LotDimensionsSource` | string | The source of the measurements. This may be a pick list of options showing the source of the measurement. i.e. Agent, Assessor, Estimate, etc. |
| `LotFeatures` | string | A list of features or description of the lot included in the sale/lease. |
| `LotSizeAcres` | number | The total Acres of the lot. This field is related to the Lot Size Area and Lot Size Units and must be in sync with the values represented in those fields. Lot Size Source also applies to this field when used. |
| `LotSizeArea` | number | The total area of the lot. See Lot Size Units for the units of measurement (Square Feet, Square Meters, Acres, etc.). |
| `LotSizeDimensions` | string | The dimensions of the lot minimally represented as length and width (i.e. 250 x 180) or a measurement of all sides of the polygon representing the property lines of the property. i.e. 30 x 50 x 120 x 60 x 22. |
| `LotSizeSource` | string | The source of the measurements. This may be a pick list of options showing the source of the measurement. i.e. Agent, Assessor, Estimate, etc. |
| `LotSizeSquareFeet` | number | The total square footage of the lot. This field is related to the Lot Size Area and Lot Size Units and must be in sync with the values represented in those fields. Lot Size Source also applies to this field when used. |
| `LotSizeUnits` | string | A pick list of the unit of measurement for the area. i.e. Square Feet, Square Meters, Acres, etc. |
| `MainLevelBathrooms` | number | The number of bathrooms located on the main or entry level of the property. |
| `MainLevelBedrooms` | number | The number of bedrooms located on the main or entry level of the property. |
| `MaintenanceExpense` | number | The annual expense that is not paid directly by the tenant and is included in the Operating Expense calculations. |
| `MajorChangeTimestamp` | string | Timestamp of the last major change on the listing (see also MajorChangeType). |
| `MajorChangeType` | string | Description of the last major change on the listing, i.e. “price reduction”, “back on market”, etc. May be used to display on a summary view of listing results to quickly identify listings that have had major changes recently. |
| `Make` | string | Make of the mobile or manufactured home. |
| `MaloneId` | number | The malone ID associated with a property listing, given its address information. |
| `ManagerExpense` | number | The annual expense that is not paid directly by the tenant and is included in the Operating Expense calculations. This is for an individual manager. Use ProfessionalManagementExpense for a management company. |
| `MapCoordinate` | string | A map coordinate for the property, as determined by local custom. This is not necessarily the same as the geographic coordinate but may depend on the coordinate system used by whatever mapping service is customarily used by the listing service. |
| `MapCoordinateSource` | string | Name of the map or map book publisher. |
| `MapURL` | string | URI to a map of the property. |
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
| `MiddleOrJuniorSchool` | string | The name of the junior or middle school having a catchment area that includes the associated property. |
| `MiddleOrJuniorSchoolDistrict` | string | The name of the junior or middle school district having a catchment area that includes the associated property. |
| `MLSAreaMajor` | string | The major marketing area name, as defined by the MLS or other non-governmental organization. If there is only one MLS Area in use, it must be the MLSAreaMajor. |
| `MLSAreaMinor` | string | The minor/sub marketing area name, as defined by the MLS or other non-governmental organization. If there is only one MLS Area in use, it must be the MLSAreaMajor. |
| `MlsStatus` | string | Local or regional status that are well known by business users. Each MlsStatus must map to a single StandardStatus. Multiple MlsStatus may map to a single StandardStatus. |
| `MobileDimUnits` | string | A pick list of the unit linear measurement. i.e. feed, meters, yards, kilometers, miles, etc. |
| `MobileHomeRemainsYN` | boolean | Is the mobile home to remain and be included in the sale of the property. |
| `MobileLength` | number | Length of the mobile/manufactured home. |
| `MobileWidth` | number | Width of the mobile/manufactured home. |
| `Model` | string | Model of the mobile or manufactured home. |
| `ModificationTimestamp` | string | The transactional timestamp automatically recorded by the MLS system representing the date/time the listing was last modified. |
| `NetOperatingIncome` | number | Net operating income is the revenue from a property after operating expenses have been deducted, but before deducting income taxes and financing expenses (interest and Principal Payments). For example, Gross Income - Operating Expenses = Net Operating Income (NOI). |
| `NewConstructionYN` | boolean | Is the property newly constructed and has not been previously occupied? |
| `NewTaxesExpense` | number | The annual expense that is not paid directly by the tenant and is included in the Operating Expense calculations. |
| `NumberOfBuildings` | number | Total number of separate buildings included in the income property. |
| `NumberOfFullTimeEmployees` | number | The current number of individuals employed by the business on a full-time basis. |
| `NumberOfLots` | number | Total number of lots on the property or included in the sale. Land properties are often sold with multiple lots. It is important to be able to describe how many lots are in the property and not in all cases do lots have separate Parcel IDs. |
| `NumberOfPads` | number | The number of pads or spaces in the mobile home park. |
| `NumberOfPartTimeEmployees` | number | The current number of individuals employed by the business on a part-time basis. |
| `NumberOfSeparateElectricMeters` | number | Total number of separate meters on the property. |
| `NumberOfSeparateGasMeters` | number | Total number of separate meters on the property. |
| `NumberOfSeparateWaterMeters` | number | Total number of separate meters on the property. |
| `NumberOfUnitsInCommunity` | number | The total number of units in the building, complex or community. This is not the number of units being sold, but rather the size of the community in which the dwelling being sold is located. |
| `NumberOfUnitsLeased` | number | Total number of units currently under a lease agreement. |
| `NumberOfUnitsMoMo` | number | The total number of units leasable month to month. |
| `NumberOfUnitsTotal` | number | Total number of units included in the income property, occupied or unoccupied. |
| `NumberOfUnitsVacant` | number | The number of units currently vacant. |
| `OccupantName` | string | Name of the current occupant, if any, of the property being sold. |
| `OccupantPhone` | string | North American 10 digit phone numbers should be in the format of ###-###-#### (separated by hyphens). Other conventions should use the common local standard. International numbers should be preceded by a plus symbol. |
| `OccupantType` | string | A field that describes the type of occupant, i.e. Owner, Tenant, Vacant. |
| `OffMarketDate` | string | The date the listing was taken off market. Where possible, this date is reflective of the date entered by the agent reflecting when the change occurred contractually, not a timestamp of when the change was made in the MLS. |
| `OffMarketTimestamp` | string | The transactional timestamp automatically recorded by the MLS system representing the most recent date/time the listing's status was set to and off market status (not Active or Backup) |
| `OnMarketDate` | string | The date the listing was placed on market. Where possible, this date is reflective of the date entered by the agent reflecting when the change occurred contractually, not a timestamp of when the change was made in the MLS. |
| `OnMarketTimestamp` | string | The transactional timestamp automatically recorded by the MLS system representing the most recent date/time the listing's status was set to Active or Backup. This also includes initial input of the listing to Active/Backup or from a draft or approval status to Active/Backup. |
| `OpenParkingSpaces` | number | The number of open or uncovered parking spaces included in the sale. |
| `OpenParkingYN` | boolean | A flag indicating that any parking spaces associated with the property are not covered by a roof. |
| `OperatingExpense` | number | The costs associated with the operation and maintenance of an income-producing property. |
| `OperatingExpenseIncludes` | string | When individual expense fields are not used and only a total is entered, this lists the expenses that are included in the OperatingExpense field. |
| `OriginalEntryTimestamp` | string | The transactional timestamp automatically recorded by the MLS system representing the date/time the listing was entered and made visible to members of the MLS. |
| `OriginalListPrice` | number | The original price of the property on the initial agreement between the seller and the seller's broker. |
| `OriginatingSystemID` | string | The RESO OUID's OrganizationUniqueId of the Originating record provider. The Originating system is the system with authoritative control over the record. For example; the name of the MLS where the listing was input. In cases where the Originating system was not where the record originated (the authoritative system), see the Originating System fields. |
| `OriginatingSystemKey` | string | The system key, a unique record identifier, from the Originating system. The Originating system is the system with authoritative control over the record. For example, the Multiple Listing Service where the listing was input. There may be cases where the Source System (how you received the record) is not the Originating System. See Source System Key for more information. |
| `OriginatingSystemName` | string | The name of the Originating record provider. Most commonly the name of the MLS. The place where the listing is originally input by the member. The legal name of the company. |
| `OtherEquipment` | string | A list of other equipment that will be included in the sale of the property. |
| `OtherExpense` | number | The annual expense that is not paid directly by the tenant and is included in the Operating Expense calculations. |
| `OtherParking` | string | Other types of parking available to, or part of, the property. |
| `OtherStructures` | string | A list of structures other than the main dwelling. For example, Guest House, Barn, Shed, etc. |
| `OwnerName` | string | Name of the owner of the property being sold. |
| `OwnerPays` | string | A list of expenses for the property paid for by the owner as opposed to the tenant (e.g. Water, Trash, Electric). |
| `OwnerPhone` | string | North American 10 digit phone numbers should be in the format of ###-###-#### (separated by hyphens). Other conventions should use the common local standard. International numbers should be preceded by a plus symbol. |
| `Ownership` | string | A text description of the manner in which title to a property is held. Trust, Corporation, Joint Tennant, Individual. |
| `OwnershipType` | string | Current type of ownership of the business being sold. i.e. Corporation, LLC, Sole P, Partnership, etc., |
| `ParcelNumber` | string | A number used to uniquely identify a parcel or lot. This number is typically issued by the county or county assessor. The AP number format varies from county to county. It is recommended that all Parcel Numbers be transmitted without dashes or hyphens. |
| `ParkingFeatures` | string | A list of features or description of the parking included in the sale/lease. |
| `ParkingTotal` | number | The total number of parking spaces included in the sale. |
| `ParkManagerName` | string | Name of the manager of the mobile home park. |
| `ParkManagerPhone` | string | North American 10 digit phone numbers should be in the format of ###-###-#### (separated by hyphens). Other conventions should use the common local standard. International numbers should be preceded by a plus symbol. |
| `ParkName` | string | Name of the mobile home park or corporate/commercial park. |
| `PastureArea` | number | Measurement or percentage of the property that has been allocated as pasture or grazing area. |
| `PatioAndPorchFeatures` | string | A list of features or description of the patio or porch included in the sale/lease. |
| `PendingTimestamp` | string | The transactional timestamp automatically recorded by the MLS system representing the most recent date/time the listing's status was set to Pending. |
| `PestControlExpense` | number | The annual expense that is not paid directly by the tenant and is included in the Operating Expense calculations. |
| `PetsAllowed` | string | Are pets allowed at the property being leased? A list of yes, no and more detailed restrictions/allowances. |
| `PhotosChangeTimestamp` | string | System generated timestamp of when the last update or change to the photos for this listing was made. |
| `PhotosCount` | number | The total number of pictures or photos included with the listing. |
| `PoolExpense` | number | The annual expense that is not paid directly by the tenant and is included in the Operating Expense calculations. |
| `PoolFeatures` | string | A list of features or description of the pool included in the sale/lease. |
| `PoolPrivateYN` | boolean | The property has a privately owned pool that is included in the sale/lease. |
| `Possession` | string | A list defining when possession will occur. i.e. COE, COE+1, etc. |
| `PossibleUse` | string | A list of the type(s) of possible or best uses of the property. Probable use gives a good indication of what the best use or potential use of the property could be.i.e. Primary, Vacation, Investment, Rental, Retirement |
| `PostalCity` | string | The official city per the USPS. May be different from the "City". |
| `PostalCode` | string | The postal code portion of a street or mailing address. |
| `PostalCodePlus4` | string | The postal code +4 portion of a street or mailing address. |
| `PowerProductionType` | string | This field is a list of the types of power production system(s) available on the property. The key characteristics of the system are expected to appear as the "[type]" in the related power production fields in a flattened implementation (RETS 1.x only) of the power production fields. A relational implementation of power production must omit the type from the field name and use PowerProductionType to create a vertical representation of the various types of power production available. **Note that PV Solar is the only type of power production currently justified in multiple markets and thus shown. Up and coming renewables that could be added in the future depending on uptake: Wind, Geothermal, Thin Film Solar. |
| `PreviousListPrice` | number | The most recent previous ListPrice of the listing. |
| `PriceChangeTimestamp` | string | The transactional timestamp automatically recorded by the MLS system representing the date/time the listing's price was last changed. |
| `PrivateOfficeRemarks` | string | A remarks field that is only visible to members of the same offices as the listing agent. |
| `PrivateRemarks` | string | Remarks that may contain security or proprietary information and should be restricted from public view. |
| `ProfessionalManagementExpense` | number | The annual expense that is not paid directly by the tenant and is included in the Operating Expense calculations. This is for a management company. Use ManagerExpense for a individual manager. |
| `PropertyAttachedYN` | boolean | A flag indicating that the primary structure is attached to another structure that is not included in the sale. i.e. one unit of a duplex. This flag may be T/F, Y/N or a list of attached or detached. As with all flags, the field may be null. In some systems this information may be part of the Property Sub Type. |
| `PropertyCondition` | string | A list describing the condition of the property and any structures included in the sale. |
| `PropertySubType` | string | A list of types of residential and residential lease properties, i.e. SFR, Condo, etc. Or a list of Sub Types for Mobile, such as Expando, Manufactured, Modular, etc. |
| `PropertyTimeZoneName` | string | The name of the property time zone as provided by the tz database. |
| `PropertyTimeZoneObservesDstYN` | boolean | Indicates whether the property is in a time zone that observes Daylight Savings Time (DST). |
| `PropertyTimeZoneStandardOffset` | number | The time zone offset is the difference, in minutes, between Coordinated Universal Time (UTC) and local time. |
| `PropertyType` | string | A list of types of properties such as Residential, Lease, Income, Land, Mobile, Commercial Sale, etc... |
| `PropertyUniversalID` | string | The PropertyUniversalID is a unique identifier for all properties in the US and Canada based on country and local identification methods with additional handling for special or more granular cases. |
| `PublicRemarks` | string | Text remarks that may be displayed to the public. In an MLS, it is the field where information is entered for the public. This information is intended to be visible on-line. This is typically information that describes the selling points of the building and/or land for sale. Local conditions and rules will determine what such content can contain. Generally, the following information is excluded: any information pertaining to entry to the property, the seller and/or tenant, listing member contact information. In other systems, these remarks will be determined by local business rules. |
| `PublicSurveyRange` | string | This field specifically identifies the Range identified by the Public Land Survey System (PLSS). |
| `PublicSurveySection` | string | This field specifically identifies the Section identified by the Public Land Survey System (PLSS). |
| `PublicSurveyTownship` | string | This field specifically identifies the Township identified by the Public Land Survey System (PLSS). |
| `PurchaseContractDate` | string | With for-sale listings, the date an offer was accepted and the listing was no longer on market. This is the date entered by the agent reflecting when the change occurred contractually, not a timestamp of when the change was made in the MLS. With lease listings this may represent a meeting of the minds to lease, but some contractual requirements are yet to be fulfilled, such as contract signing or receipt of the deposit. |
| `RangeArea` | number | Measurement or percentage of the property that has been allocated as range. |
| `RentControlYN` | boolean | Is the property in a rent control area? |
| `RentIncludes` | string | A list of services or items that the tenant is not responsible to pay. |
| `RoadFrontageType` | string | Pick list of types of Road frontage. i.e. Freeway frontage, No Road Frontage, etc. The road frontage of the property is an important factor in determining value of the property and it’s appropriateness for intended use. |
| `RoadResponsibility` | string | The person or entity responsible for road maintenance (e.g., City, County, Private). |
| `RoadSurfaceType` | string | Pick list of types of surface of the Road to access the property. The surface of the road(s) for access to the property is an important factor in determining value of the property and it’s appropriateness for intended use. |
| `Roof` | string | A list describing the type or style of roof. For example Spanish Tile, Composite, Shake, etc. |
| `RoomBasementArea` | number | [type] This field is a repeating element for each type of room selected in the RoomType field. For every RoomType there are two possible implementations. For a flat implementation (RETS 1.x only), each RoomType used is expected to appear as the "[type]" in the related rooms field name. i.e. RoomKitchenArea. A relational implementation of rooms must omit the type from the field name and use RoomType to create a vertical representation of the various rooms. i.e. RoomArea with Kitchen in the relational table's RoomType field. |
| `RoomBasementDescription` | string | Provides a link to the specific property’s high-performance rating or scoring details directly from and hosted by the sponsoring body of the program. Typically provides thorough details, for example, which points where achieved and how, or in the case of a score what specifically was tested and the results. This is a repeating element. If desired replace [Type] with the name of the certification from the GreenBuildingVerificationType list. |
| `RoomBasementFeatures` | string | [type] This field is a repeating element for each type of room selected in the RoomType field. For every RoomType there are two possible implementations. For a flat implementation (RETS 1.x only), each RoomType used is expected to appear as the "[type]" in the related rooms field name. i.e. RoomKitchenFeatures. A relational implementation of rooms must omit the type from the field name and use RoomType to create a vertical representation of the various rooms. i.e. RoomFeatures with Kitchen in the relational table's RoomType field. |
| `RoomBasementLength` | number | [type] This field is a repeating element for each type of room selected in the RoomType field. For every RoomType there are two possible implementations. For a flat implementation (RETS 1.x only), each RoomType used is expected to appear as the "[type]" in the related rooms field name. i.e. RoomKitchenLength. A relational implementation of rooms must omit the type from the field name and use RoomType to create a vertical representation of the various rooms. i.e. RoomLength with Kitchen in the relational table's RoomType field. |
| `RoomBasementLevel` | string | [type] This field is a repeating element for each type of room selected in the RoomType field. For every RoomType there are two possible implementations. For a flat implementation (RETS 1.x only), each RoomType used is expected to appear as the "[type]" in the related rooms field name. i.e. RoomKitchenLevel. A relational implementation of rooms must omit the type from the field name and use RoomType to create a vertical representation of the various rooms. i.e. RoomLevel with Kitchen in the relational table's RoomType field. |
| `RoomBasementWidth` | number | [type] This field is a repeating element for each type of room selected in the RoomType field. For every RoomType there are two possible implementations. For a flat implementation (RETS 1.x only), each RoomType used is expected to appear as the "[type]" in the related rooms field name. i.e. RoomKitchenWidth. A relational implementation of rooms must omit the type from the field name and use RoomType to create a vertical representation of the various rooms. i.e. RoomWidth with Kitchen in the relational table's RoomType field. |
| `RoomBathroom1Area` | number | [type] This field is a repeating element for each type of room selected in the RoomType field. For every RoomType there are two possible implementations. For a flat implementation (RETS 1.x only), each RoomType used is expected to appear as the "[type]" in the related rooms field name. i.e. RoomKitchenArea. A relational implementation of rooms must omit the type from the field name and use RoomType to create a vertical representation of the various rooms. i.e. RoomArea with Kitchen in the relational table's RoomType field. |
| `RoomBathroom1Description` | string | Provides a link to the specific property’s high-performance rating or scoring details directly from and hosted by the sponsoring body of the program. Typically provides thorough details, for example, which points where achieved and how, or in the case of a score what specifically was tested and the results. This is a repeating element. If desired replace [Type] with the name of the certification from the GreenBuildingVerificationType list. |
| `RoomBathroom1Features` | string | [type] This field is a repeating element for each type of room selected in the RoomType field. For every RoomType there are two possible implementations. For a flat implementation (RETS 1.x only), each RoomType used is expected to appear as the "[type]" in the related rooms field name. i.e. RoomKitchenFeatures. A relational implementation of rooms must omit the type from the field name and use RoomType to create a vertical representation of the various rooms. i.e. RoomFeatures with Kitchen in the relational table's RoomType field. |
| `RoomBathroom1Length` | number | [type] This field is a repeating element for each type of room selected in the RoomType field. For every RoomType there are two possible implementations. For a flat implementation (RETS 1.x only), each RoomType used is expected to appear as the "[type]" in the related rooms field name. i.e. RoomKitchenLength. A relational implementation of rooms must omit the type from the field name and use RoomType to create a vertical representation of the various rooms. i.e. RoomLength with Kitchen in the relational table's RoomType field. |
| `RoomBathroom1Level` | string | [type] This field is a repeating element for each type of room selected in the RoomType field. For every RoomType there are two possible implementations. For a flat implementation (RETS 1.x only), each RoomType used is expected to appear as the "[type]" in the related rooms field name. i.e. RoomKitchenLevel. A relational implementation of rooms must omit the type from the field name and use RoomType to create a vertical representation of the various rooms. i.e. RoomLevel with Kitchen in the relational table's RoomType field. |
| `RoomBathroom1Width` | number | [type] This field is a repeating element for each type of room selected in the RoomType field. For every RoomType there are two possible implementations. For a flat implementation (RETS 1.x only), each RoomType used is expected to appear as the "[type]" in the related rooms field name. i.e. RoomKitchenWidth. A relational implementation of rooms must omit the type from the field name and use RoomType to create a vertical representation of the various rooms. i.e. RoomWidth with Kitchen in the relational table's RoomType field. |
| `RoomBathroom2Area` | number | [type] This field is a repeating element for each type of room selected in the RoomType field. For every RoomType there are two possible implementations. For a flat implementation (RETS 1.x only), each RoomType used is expected to appear as the "[type]" in the related rooms field name. i.e. RoomKitchenArea. A relational implementation of rooms must omit the type from the field name and use RoomType to create a vertical representation of the various rooms. i.e. RoomArea with Kitchen in the relational table's RoomType field. |
| `RoomBathroom2Description` | string | Provides a link to the specific property’s high-performance rating or scoring details directly from and hosted by the sponsoring body of the program. Typically provides thorough details, for example, which points where achieved and how, or in the case of a score what specifically was tested and the results. This is a repeating element. If desired replace [Type] with the name of the certification from the GreenBuildingVerificationType list. |
| `RoomBathroom2Features` | string | [type] This field is a repeating element for each type of room selected in the RoomType field. For every RoomType there are two possible implementations. For a flat implementation (RETS 1.x only), each RoomType used is expected to appear as the "[type]" in the related rooms field name. i.e. RoomKitchenFeatures. A relational implementation of rooms must omit the type from the field name and use RoomType to create a vertical representation of the various rooms. i.e. RoomFeatures with Kitchen in the relational table's RoomType field. |
| `RoomBathroom2Length` | number | [type] This field is a repeating element for each type of room selected in the RoomType field. For every RoomType there are two possible implementations. For a flat implementation (RETS 1.x only), each RoomType used is expected to appear as the "[type]" in the related rooms field name. i.e. RoomKitchenLength. A relational implementation of rooms must omit the type from the field name and use RoomType to create a vertical representation of the various rooms. i.e. RoomLength with Kitchen in the relational table's RoomType field. |
| `RoomBathroom2Level` | string | [type] This field is a repeating element for each type of room selected in the RoomType field. For every RoomType there are two possible implementations. For a flat implementation (RETS 1.x only), each RoomType used is expected to appear as the "[type]" in the related rooms field name. i.e. RoomKitchenLevel. A relational implementation of rooms must omit the type from the field name and use RoomType to create a vertical representation of the various rooms. i.e. RoomLevel with Kitchen in the relational table's RoomType field. |
| `RoomBathroom2Width` | number | [type] This field is a repeating element for each type of room selected in the RoomType field. For every RoomType there are two possible implementations. For a flat implementation (RETS 1.x only), each RoomType used is expected to appear as the "[type]" in the related rooms field name. i.e. RoomKitchenWidth. A relational implementation of rooms must omit the type from the field name and use RoomType to create a vertical representation of the various rooms. i.e. RoomWidth with Kitchen in the relational table's RoomType field. |
| `RoomBathroom3Area` | number | [type] This field is a repeating element for each type of room selected in the RoomType field. For every RoomType there are two possible implementations. For a flat implementation (RETS 1.x only), each RoomType used is expected to appear as the "[type]" in the related rooms field name. i.e. RoomKitchenArea. A relational implementation of rooms must omit the type from the field name and use RoomType to create a vertical representation of the various rooms. i.e. RoomArea with Kitchen in the relational table's RoomType field. |
| `RoomBathroom3Description` | string | Provides a link to the specific property’s high-performance rating or scoring details directly from and hosted by the sponsoring body of the program. Typically provides thorough details, for example, which points where achieved and how, or in the case of a score what specifically was tested and the results. This is a repeating element. If desired replace [Type] with the name of the certification from the GreenBuildingVerificationType list. |
| `RoomBathroom3Features` | string | [type] This field is a repeating element for each type of room selected in the RoomType field. For every RoomType there are two possible implementations. For a flat implementation (RETS 1.x only), each RoomType used is expected to appear as the "[type]" in the related rooms field name. i.e. RoomKitchenFeatures. A relational implementation of rooms must omit the type from the field name and use RoomType to create a vertical representation of the various rooms. i.e. RoomFeatures with Kitchen in the relational table's RoomType field. |
| `RoomBathroom3Length` | number | [type] This field is a repeating element for each type of room selected in the RoomType field. For every RoomType there are two possible implementations. For a flat implementation (RETS 1.x only), each RoomType used is expected to appear as the "[type]" in the related rooms field name. i.e. RoomKitchenLength. A relational implementation of rooms must omit the type from the field name and use RoomType to create a vertical representation of the various rooms. i.e. RoomLength with Kitchen in the relational table's RoomType field. |
| `RoomBathroom3Level` | string | [type] This field is a repeating element for each type of room selected in the RoomType field. For every RoomType there are two possible implementations. For a flat implementation (RETS 1.x only), each RoomType used is expected to appear as the "[type]" in the related rooms field name. i.e. RoomKitchenLevel. A relational implementation of rooms must omit the type from the field name and use RoomType to create a vertical representation of the various rooms. i.e. RoomLevel with Kitchen in the relational table's RoomType field. |
| `RoomBathroom3Width` | number | [type] This field is a repeating element for each type of room selected in the RoomType field. For every RoomType there are two possible implementations. For a flat implementation (RETS 1.x only), each RoomType used is expected to appear as the "[type]" in the related rooms field name. i.e. RoomKitchenWidth. A relational implementation of rooms must omit the type from the field name and use RoomType to create a vertical representation of the various rooms. i.e. RoomWidth with Kitchen in the relational table's RoomType field. |
| `RoomBathroom4Area` | number | [type] This field is a repeating element for each type of room selected in the RoomType field. For every RoomType there are two possible implementations. For a flat implementation (RETS 1.x only), each RoomType used is expected to appear as the "[type]" in the related rooms field name. i.e. RoomKitchenArea. A relational implementation of rooms must omit the type from the field name and use RoomType to create a vertical representation of the various rooms. i.e. RoomArea with Kitchen in the relational table's RoomType field. |
| `RoomBathroom4Description` | string | Provides a link to the specific property’s high-performance rating or scoring details directly from and hosted by the sponsoring body of the program. Typically provides thorough details, for example, which points where achieved and how, or in the case of a score what specifically was tested and the results. This is a repeating element. If desired replace [Type] with the name of the certification from the GreenBuildingVerificationType list. |
| `RoomBathroom4Features` | string | [type] This field is a repeating element for each type of room selected in the RoomType field. For every RoomType there are two possible implementations. For a flat implementation (RETS 1.x only), each RoomType used is expected to appear as the "[type]" in the related rooms field name. i.e. RoomKitchenFeatures. A relational implementation of rooms must omit the type from the field name and use RoomType to create a vertical representation of the various rooms. i.e. RoomFeatures with Kitchen in the relational table's RoomType field. |
| `RoomBathroom4Length` | number | [type] This field is a repeating element for each type of room selected in the RoomType field. For every RoomType there are two possible implementations. For a flat implementation (RETS 1.x only), each RoomType used is expected to appear as the "[type]" in the related rooms field name. i.e. RoomKitchenLength. A relational implementation of rooms must omit the type from the field name and use RoomType to create a vertical representation of the various rooms. i.e. RoomLength with Kitchen in the relational table's RoomType field. |
| `RoomBathroom4Level` | string | [type] This field is a repeating element for each type of room selected in the RoomType field. For every RoomType there are two possible implementations. For a flat implementation (RETS 1.x only), each RoomType used is expected to appear as the "[type]" in the related rooms field name. i.e. RoomKitchenLevel. A relational implementation of rooms must omit the type from the field name and use RoomType to create a vertical representation of the various rooms. i.e. RoomLevel with Kitchen in the relational table's RoomType field. |
| `RoomBathroom4Width` | number | [type] This field is a repeating element for each type of room selected in the RoomType field. For every RoomType there are two possible implementations. For a flat implementation (RETS 1.x only), each RoomType used is expected to appear as the "[type]" in the related rooms field name. i.e. RoomKitchenWidth. A relational implementation of rooms must omit the type from the field name and use RoomType to create a vertical representation of the various rooms. i.e. RoomWidth with Kitchen in the relational table's RoomType field. |
| `RoomBathroom5Area` | number | [type] This field is a repeating element for each type of room selected in the RoomType field. For every RoomType there are two possible implementations. For a flat implementation (RETS 1.x only), each RoomType used is expected to appear as the "[type]" in the related rooms field name. i.e. RoomKitchenArea. A relational implementation of rooms must omit the type from the field name and use RoomType to create a vertical representation of the various rooms. i.e. RoomArea with Kitchen in the relational table's RoomType field. |
| `RoomBathroom5Description` | string | Provides a link to the specific property’s high-performance rating or scoring details directly from and hosted by the sponsoring body of the program. Typically provides thorough details, for example, which points where achieved and how, or in the case of a score what specifically was tested and the results. This is a repeating element. If desired replace [Type] with the name of the certification from the GreenBuildingVerificationType list. |
| `RoomBathroom5Features` | string | [type] This field is a repeating element for each type of room selected in the RoomType field. For every RoomType there are two possible implementations. For a flat implementation (RETS 1.x only), each RoomType used is expected to appear as the "[type]" in the related rooms field name. i.e. RoomKitchenFeatures. A relational implementation of rooms must omit the type from the field name and use RoomType to create a vertical representation of the various rooms. i.e. RoomFeatures with Kitchen in the relational table's RoomType field. |
| `RoomBathroom5Length` | number | [type] This field is a repeating element for each type of room selected in the RoomType field. For every RoomType there are two possible implementations. For a flat implementation (RETS 1.x only), each RoomType used is expected to appear as the "[type]" in the related rooms field name. i.e. RoomKitchenLength. A relational implementation of rooms must omit the type from the field name and use RoomType to create a vertical representation of the various rooms. i.e. RoomLength with Kitchen in the relational table's RoomType field. |
| `RoomBathroom5Level` | string | [type] This field is a repeating element for each type of room selected in the RoomType field. For every RoomType there are two possible implementations. For a flat implementation (RETS 1.x only), each RoomType used is expected to appear as the "[type]" in the related rooms field name. i.e. RoomKitchenLevel. A relational implementation of rooms must omit the type from the field name and use RoomType to create a vertical representation of the various rooms. i.e. RoomLevel with Kitchen in the relational table's RoomType field. |
| `RoomBathroom5Width` | number | [type] This field is a repeating element for each type of room selected in the RoomType field. For every RoomType there are two possible implementations. For a flat implementation (RETS 1.x only), each RoomType used is expected to appear as the "[type]" in the related rooms field name. i.e. RoomKitchenWidth. A relational implementation of rooms must omit the type from the field name and use RoomType to create a vertical representation of the various rooms. i.e. RoomWidth with Kitchen in the relational table's RoomType field. |
| `RoomBathroomArea` | number | [type] This field is a repeating element for each type of room selected in the RoomType field. For every RoomType there are two possible implementations. For a flat implementation (RETS 1.x only), each RoomType used is expected to appear as the "[type]" in the related rooms field name. i.e. RoomKitchenArea. A relational implementation of rooms must omit the type from the field name and use RoomType to create a vertical representation of the various rooms. i.e. RoomArea with Kitchen in the relational table's RoomType field. |
| `RoomBathroomDescription` | string | Provides a link to the specific property’s high-performance rating or scoring details directly from and hosted by the sponsoring body of the program. Typically provides thorough details, for example, which points where achieved and how, or in the case of a score what specifically was tested and the results. This is a repeating element. If desired replace [Type] with the name of the certification from the GreenBuildingVerificationType list. |
| `RoomBathroomFeatures` | string | [type] This field is a repeating element for each type of room selected in the RoomType field. For every RoomType there are two possible implementations. For a flat implementation (RETS 1.x only), each RoomType used is expected to appear as the "[type]" in the related rooms field name. i.e. RoomKitchenFeatures. A relational implementation of rooms must omit the type from the field name and use RoomType to create a vertical representation of the various rooms. i.e. RoomFeatures with Kitchen in the relational table's RoomType field. |
| `RoomBathroomLength` | number | [type] This field is a repeating element for each type of room selected in the RoomType field. For every RoomType there are two possible implementations. For a flat implementation (RETS 1.x only), each RoomType used is expected to appear as the "[type]" in the related rooms field name. i.e. RoomKitchenLength. A relational implementation of rooms must omit the type from the field name and use RoomType to create a vertical representation of the various rooms. i.e. RoomLength with Kitchen in the relational table's RoomType field. |
| `RoomBathroomLevel` | string | [type] This field is a repeating element for each type of room selected in the RoomType field. For every RoomType there are two possible implementations. For a flat implementation (RETS 1.x only), each RoomType used is expected to appear as the "[type]" in the related rooms field name. i.e. RoomKitchenLevel. A relational implementation of rooms must omit the type from the field name and use RoomType to create a vertical representation of the various rooms. i.e. RoomLevel with Kitchen in the relational table's RoomType field. |
| `RoomBathroomWidth` | number | [type] This field is a repeating element for each type of room selected in the RoomType field. For every RoomType there are two possible implementations. For a flat implementation (RETS 1.x only), each RoomType used is expected to appear as the "[type]" in the related rooms field name. i.e. RoomKitchenWidth. A relational implementation of rooms must omit the type from the field name and use RoomType to create a vertical representation of the various rooms. i.e. RoomWidth with Kitchen in the relational table's RoomType field. |
| `RoomBedroom1Area` | number | [type] This field is a repeating element for each type of room selected in the RoomType field. For every RoomType there are two possible implementations. For a flat implementation (RETS 1.x only), each RoomType used is expected to appear as the "[type]" in the related rooms field name. i.e. RoomKitchenArea. A relational implementation of rooms must omit the type from the field name and use RoomType to create a vertical representation of the various rooms. i.e. RoomArea with Kitchen in the relational table's RoomType field. |
| `RoomBedroom1Description` | string | Provides a link to the specific property’s high-performance rating or scoring details directly from and hosted by the sponsoring body of the program. Typically provides thorough details, for example, which points where achieved and how, or in the case of a score what specifically was tested and the results. This is a repeating element. If desired replace [Type] with the name of the certification from the GreenBuildingVerificationType list. |
| `RoomBedroom1Features` | string | [type] This field is a repeating element for each type of room selected in the RoomType field. For every RoomType there are two possible implementations. For a flat implementation (RETS 1.x only), each RoomType used is expected to appear as the "[type]" in the related rooms field name. i.e. RoomKitchenFeatures. A relational implementation of rooms must omit the type from the field name and use RoomType to create a vertical representation of the various rooms. i.e. RoomFeatures with Kitchen in the relational table's RoomType field. |
| `RoomBedroom1Length` | number | [type] This field is a repeating element for each type of room selected in the RoomType field. For every RoomType there are two possible implementations. For a flat implementation (RETS 1.x only), each RoomType used is expected to appear as the "[type]" in the related rooms field name. i.e. RoomKitchenLength. A relational implementation of rooms must omit the type from the field name and use RoomType to create a vertical representation of the various rooms. i.e. RoomLength with Kitchen in the relational table's RoomType field. |
| `RoomBedroom1Level` | string | [type] This field is a repeating element for each type of room selected in the RoomType field. For every RoomType there are two possible implementations. For a flat implementation (RETS 1.x only), each RoomType used is expected to appear as the "[type]" in the related rooms field name. i.e. RoomKitchenLevel. A relational implementation of rooms must omit the type from the field name and use RoomType to create a vertical representation of the various rooms. i.e. RoomLevel with Kitchen in the relational table's RoomType field. |
| `RoomBedroom1Width` | number | [type] This field is a repeating element for each type of room selected in the RoomType field. For every RoomType there are two possible implementations. For a flat implementation (RETS 1.x only), each RoomType used is expected to appear as the "[type]" in the related rooms field name. i.e. RoomKitchenWidth. A relational implementation of rooms must omit the type from the field name and use RoomType to create a vertical representation of the various rooms. i.e. RoomWidth with Kitchen in the relational table's RoomType field. |
| `RoomBedroom2Area` | number | [type] This field is a repeating element for each type of room selected in the RoomType field. For every RoomType there are two possible implementations. For a flat implementation (RETS 1.x only), each RoomType used is expected to appear as the "[type]" in the related rooms field name. i.e. RoomKitchenArea. A relational implementation of rooms must omit the type from the field name and use RoomType to create a vertical representation of the various rooms. i.e. RoomArea with Kitchen in the relational table's RoomType field. |
| `RoomBedroom2Description` | string | Provides a link to the specific property’s high-performance rating or scoring details directly from and hosted by the sponsoring body of the program. Typically provides thorough details, for example, which points where achieved and how, or in the case of a score what specifically was tested and the results. This is a repeating element. If desired replace [Type] with the name of the certification from the GreenBuildingVerificationType list. |
| `RoomBedroom2Features` | string | [type] This field is a repeating element for each type of room selected in the RoomType field. For every RoomType there are two possible implementations. For a flat implementation (RETS 1.x only), each RoomType used is expected to appear as the "[type]" in the related rooms field name. i.e. RoomKitchenFeatures. A relational implementation of rooms must omit the type from the field name and use RoomType to create a vertical representation of the various rooms. i.e. RoomFeatures with Kitchen in the relational table's RoomType field. |
| `RoomBedroom2Length` | number | [type] This field is a repeating element for each type of room selected in the RoomType field. For every RoomType there are two possible implementations. For a flat implementation (RETS 1.x only), each RoomType used is expected to appear as the "[type]" in the related rooms field name. i.e. RoomKitchenLength. A relational implementation of rooms must omit the type from the field name and use RoomType to create a vertical representation of the various rooms. i.e. RoomLength with Kitchen in the relational table's RoomType field. |
| `RoomBedroom2Level` | string | [type] This field is a repeating element for each type of room selected in the RoomType field. For every RoomType there are two possible implementations. For a flat implementation (RETS 1.x only), each RoomType used is expected to appear as the "[type]" in the related rooms field name. i.e. RoomKitchenLevel. A relational implementation of rooms must omit the type from the field name and use RoomType to create a vertical representation of the various rooms. i.e. RoomLevel with Kitchen in the relational table's RoomType field. |
| `RoomBedroom2Width` | number | [type] This field is a repeating element for each type of room selected in the RoomType field. For every RoomType there are two possible implementations. For a flat implementation (RETS 1.x only), each RoomType used is expected to appear as the "[type]" in the related rooms field name. i.e. RoomKitchenWidth. A relational implementation of rooms must omit the type from the field name and use RoomType to create a vertical representation of the various rooms. i.e. RoomWidth with Kitchen in the relational table's RoomType field. |
| `RoomBedroom3Area` | number | [type] This field is a repeating element for each type of room selected in the RoomType field. For every RoomType there are two possible implementations. For a flat implementation (RETS 1.x only), each RoomType used is expected to appear as the "[type]" in the related rooms field name. i.e. RoomKitchenArea. A relational implementation of rooms must omit the type from the field name and use RoomType to create a vertical representation of the various rooms. i.e. RoomArea with Kitchen in the relational table's RoomType field. |
| `RoomBedroom3Description` | string | Provides a link to the specific property’s high-performance rating or scoring details directly from and hosted by the sponsoring body of the program. Typically provides thorough details, for example, which points where achieved and how, or in the case of a score what specifically was tested and the results. This is a repeating element. If desired replace [Type] with the name of the certification from the GreenBuildingVerificationType list. |
| `RoomBedroom3Features` | string | [type] This field is a repeating element for each type of room selected in the RoomType field. For every RoomType there are two possible implementations. For a flat implementation (RETS 1.x only), each RoomType used is expected to appear as the "[type]" in the related rooms field name. i.e. RoomKitchenFeatures. A relational implementation of rooms must omit the type from the field name and use RoomType to create a vertical representation of the various rooms. i.e. RoomFeatures with Kitchen in the relational table's RoomType field. |
| `RoomBedroom3Length` | number | [type] This field is a repeating element for each type of room selected in the RoomType field. For every RoomType there are two possible implementations. For a flat implementation (RETS 1.x only), each RoomType used is expected to appear as the "[type]" in the related rooms field name. i.e. RoomKitchenLength. A relational implementation of rooms must omit the type from the field name and use RoomType to create a vertical representation of the various rooms. i.e. RoomLength with Kitchen in the relational table's RoomType field. |
| `RoomBedroom3Level` | string | [type] This field is a repeating element for each type of room selected in the RoomType field. For every RoomType there are two possible implementations. For a flat implementation (RETS 1.x only), each RoomType used is expected to appear as the "[type]" in the related rooms field name. i.e. RoomKitchenLevel. A relational implementation of rooms must omit the type from the field name and use RoomType to create a vertical representation of the various rooms. i.e. RoomLevel with Kitchen in the relational table's RoomType field. |
| `RoomBedroom3Width` | number | [type] This field is a repeating element for each type of room selected in the RoomType field. For every RoomType there are two possible implementations. For a flat implementation (RETS 1.x only), each RoomType used is expected to appear as the "[type]" in the related rooms field name. i.e. RoomKitchenWidth. A relational implementation of rooms must omit the type from the field name and use RoomType to create a vertical representation of the various rooms. i.e. RoomWidth with Kitchen in the relational table's RoomType field. |
| `RoomBedroom4Area` | number | [type] This field is a repeating element for each type of room selected in the RoomType field. For every RoomType there are two possible implementations. For a flat implementation (RETS 1.x only), each RoomType used is expected to appear as the "[type]" in the related rooms field name. i.e. RoomKitchenArea. A relational implementation of rooms must omit the type from the field name and use RoomType to create a vertical representation of the various rooms. i.e. RoomArea with Kitchen in the relational table's RoomType field. |
| `RoomBedroom4Description` | string | Provides a link to the specific property’s high-performance rating or scoring details directly from and hosted by the sponsoring body of the program. Typically provides thorough details, for example, which points where achieved and how, or in the case of a score what specifically was tested and the results. This is a repeating element. If desired replace [Type] with the name of the certification from the GreenBuildingVerificationType list. |
| `RoomBedroom4Features` | string | [type] This field is a repeating element for each type of room selected in the RoomType field. For every RoomType there are two possible implementations. For a flat implementation (RETS 1.x only), each RoomType used is expected to appear as the "[type]" in the related rooms field name. i.e. RoomKitchenFeatures. A relational implementation of rooms must omit the type from the field name and use RoomType to create a vertical representation of the various rooms. i.e. RoomFeatures with Kitchen in the relational table's RoomType field. |
| `RoomBedroom4Length` | number | [type] This field is a repeating element for each type of room selected in the RoomType field. For every RoomType there are two possible implementations. For a flat implementation (RETS 1.x only), each RoomType used is expected to appear as the "[type]" in the related rooms field name. i.e. RoomKitchenLength. A relational implementation of rooms must omit the type from the field name and use RoomType to create a vertical representation of the various rooms. i.e. RoomLength with Kitchen in the relational table's RoomType field. |
| `RoomBedroom4Level` | string | [type] This field is a repeating element for each type of room selected in the RoomType field. For every RoomType there are two possible implementations. For a flat implementation (RETS 1.x only), each RoomType used is expected to appear as the "[type]" in the related rooms field name. i.e. RoomKitchenLevel. A relational implementation of rooms must omit the type from the field name and use RoomType to create a vertical representation of the various rooms. i.e. RoomLevel with Kitchen in the relational table's RoomType field. |
| `RoomBedroom4Width` | number | [type] This field is a repeating element for each type of room selected in the RoomType field. For every RoomType there are two possible implementations. For a flat implementation (RETS 1.x only), each RoomType used is expected to appear as the "[type]" in the related rooms field name. i.e. RoomKitchenWidth. A relational implementation of rooms must omit the type from the field name and use RoomType to create a vertical representation of the various rooms. i.e. RoomWidth with Kitchen in the relational table's RoomType field. |
| `RoomBedroom5Area` | number | [type] This field is a repeating element for each type of room selected in the RoomType field. For every RoomType there are two possible implementations. For a flat implementation (RETS 1.x only), each RoomType used is expected to appear as the "[type]" in the related rooms field name. i.e. RoomKitchenArea. A relational implementation of rooms must omit the type from the field name and use RoomType to create a vertical representation of the various rooms. i.e. RoomArea with Kitchen in the relational table's RoomType field. |
| `RoomBedroom5Description` | string | Provides a link to the specific property’s high-performance rating or scoring details directly from and hosted by the sponsoring body of the program. Typically provides thorough details, for example, which points where achieved and how, or in the case of a score what specifically was tested and the results. This is a repeating element. If desired replace [Type] with the name of the certification from the GreenBuildingVerificationType list. |
| `RoomBedroom5Features` | string | [type] This field is a repeating element for each type of room selected in the RoomType field. For every RoomType there are two possible implementations. For a flat implementation (RETS 1.x only), each RoomType used is expected to appear as the "[type]" in the related rooms field name. i.e. RoomKitchenFeatures. A relational implementation of rooms must omit the type from the field name and use RoomType to create a vertical representation of the various rooms. i.e. RoomFeatures with Kitchen in the relational table's RoomType field. |
| `RoomBedroom5Length` | number | [type] This field is a repeating element for each type of room selected in the RoomType field. For every RoomType there are two possible implementations. For a flat implementation (RETS 1.x only), each RoomType used is expected to appear as the "[type]" in the related rooms field name. i.e. RoomKitchenLength. A relational implementation of rooms must omit the type from the field name and use RoomType to create a vertical representation of the various rooms. i.e. RoomLength with Kitchen in the relational table's RoomType field. |
| `RoomBedroom5Level` | string | [type] This field is a repeating element for each type of room selected in the RoomType field. For every RoomType there are two possible implementations. For a flat implementation (RETS 1.x only), each RoomType used is expected to appear as the "[type]" in the related rooms field name. i.e. RoomKitchenLevel. A relational implementation of rooms must omit the type from the field name and use RoomType to create a vertical representation of the various rooms. i.e. RoomLevel with Kitchen in the relational table's RoomType field. |
| `RoomBedroom5Width` | number | [type] This field is a repeating element for each type of room selected in the RoomType field. For every RoomType there are two possible implementations. For a flat implementation (RETS 1.x only), each RoomType used is expected to appear as the "[type]" in the related rooms field name. i.e. RoomKitchenWidth. A relational implementation of rooms must omit the type from the field name and use RoomType to create a vertical representation of the various rooms. i.e. RoomWidth with Kitchen in the relational table's RoomType field. |
| `RoomBedroomArea` | number | [type] This field is a repeating element for each type of room selected in the RoomType field. For every RoomType there are two possible implementations. For a flat implementation (RETS 1.x only), each RoomType used is expected to appear as the "[type]" in the related rooms field name. i.e. RoomKitchenArea. A relational implementation of rooms must omit the type from the field name and use RoomType to create a vertical representation of the various rooms. i.e. RoomArea with Kitchen in the relational table's RoomType field. |
| `RoomBedroomDescription` | string | Provides a link to the specific property’s high-performance rating or scoring details directly from and hosted by the sponsoring body of the program. Typically provides thorough details, for example, which points where achieved and how, or in the case of a score what specifically was tested and the results. This is a repeating element. If desired replace [Type] with the name of the certification from the GreenBuildingVerificationType list. |
| `RoomBedroomFeatures` | string | [type] This field is a repeating element for each type of room selected in the RoomType field. For every RoomType there are two possible implementations. For a flat implementation (RETS 1.x only), each RoomType used is expected to appear as the "[type]" in the related rooms field name. i.e. RoomKitchenFeatures. A relational implementation of rooms must omit the type from the field name and use RoomType to create a vertical representation of the various rooms. i.e. RoomFeatures with Kitchen in the relational table's RoomType field. |
| `RoomBedroomLength` | number | [type] This field is a repeating element for each type of room selected in the RoomType field. For every RoomType there are two possible implementations. For a flat implementation (RETS 1.x only), each RoomType used is expected to appear as the "[type]" in the related rooms field name. i.e. RoomKitchenLength. A relational implementation of rooms must omit the type from the field name and use RoomType to create a vertical representation of the various rooms. i.e. RoomLength with Kitchen in the relational table's RoomType field. |
| `RoomBedroomLevel` | string | [type] This field is a repeating element for each type of room selected in the RoomType field. For every RoomType there are two possible implementations. For a flat implementation (RETS 1.x only), each RoomType used is expected to appear as the "[type]" in the related rooms field name. i.e. RoomKitchenLevel. A relational implementation of rooms must omit the type from the field name and use RoomType to create a vertical representation of the various rooms. i.e. RoomLevel with Kitchen in the relational table's RoomType field. |
| `RoomBedroomWidth` | number | [type] This field is a repeating element for each type of room selected in the RoomType field. For every RoomType there are two possible implementations. For a flat implementation (RETS 1.x only), each RoomType used is expected to appear as the "[type]" in the related rooms field name. i.e. RoomKitchenWidth. A relational implementation of rooms must omit the type from the field name and use RoomType to create a vertical representation of the various rooms. i.e. RoomWidth with Kitchen in the relational table's RoomType field. |
| `RoomDiningRoomArea` | number | [type] This field is a repeating element for each type of room selected in the RoomType field. For every RoomType there are two possible implementations. For a flat implementation (RETS 1.x only), each RoomType used is expected to appear as the "[type]" in the related rooms field name. i.e. RoomKitchenArea. A relational implementation of rooms must omit the type from the field name and use RoomType to create a vertical representation of the various rooms. i.e. RoomArea with Kitchen in the relational table's RoomType field. |
| `RoomDiningRoomDescription` | string | Provides a link to the specific property’s high-performance rating or scoring details directly from and hosted by the sponsoring body of the program. Typically provides thorough details, for example, which points where achieved and how, or in the case of a score what specifically was tested and the results. This is a repeating element. If desired replace [Type] with the name of the certification from the GreenBuildingVerificationType list. |
| `RoomDiningRoomFeatures` | string | [type] This field is a repeating element for each type of room selected in the RoomType field. For every RoomType there are two possible implementations. For a flat implementation (RETS 1.x only), each RoomType used is expected to appear as the "[type]" in the related rooms field name. i.e. RoomKitchenFeatures. A relational implementation of rooms must omit the type from the field name and use RoomType to create a vertical representation of the various rooms. i.e. RoomFeatures with Kitchen in the relational table's RoomType field. |
| `RoomDiningRoomLength` | number | [type] This field is a repeating element for each type of room selected in the RoomType field. For every RoomType there are two possible implementations. For a flat implementation (RETS 1.x only), each RoomType used is expected to appear as the "[type]" in the related rooms field name. i.e. RoomKitchenLength. A relational implementation of rooms must omit the type from the field name and use RoomType to create a vertical representation of the various rooms. i.e. RoomLength with Kitchen in the relational table's RoomType field. |
| `RoomDiningRoomLevel` | string | [type] This field is a repeating element for each type of room selected in the RoomType field. For every RoomType there are two possible implementations. For a flat implementation (RETS 1.x only), each RoomType used is expected to appear as the "[type]" in the related rooms field name. i.e. RoomKitchenLevel. A relational implementation of rooms must omit the type from the field name and use RoomType to create a vertical representation of the various rooms. i.e. RoomLevel with Kitchen in the relational table's RoomType field. |
| `RoomDiningRoomWidth` | number | [type] This field is a repeating element for each type of room selected in the RoomType field. For every RoomType there are two possible implementations. For a flat implementation (RETS 1.x only), each RoomType used is expected to appear as the "[type]" in the related rooms field name. i.e. RoomKitchenWidth. A relational implementation of rooms must omit the type from the field name and use RoomType to create a vertical representation of the various rooms. i.e. RoomWidth with Kitchen in the relational table's RoomType field. |
| `RoomFamilyRoomArea` | number | [type] This field is a repeating element for each type of room selected in the RoomType field. For every RoomType there are two possible implementations. For a flat implementation (RETS 1.x only), each RoomType used is expected to appear as the "[type]" in the related rooms field name. i.e. RoomKitchenArea. A relational implementation of rooms must omit the type from the field name and use RoomType to create a vertical representation of the various rooms. i.e. RoomArea with Kitchen in the relational table's RoomType field. |
| `RoomFamilyRoomDescription` | string | Provides a link to the specific property’s high-performance rating or scoring details directly from and hosted by the sponsoring body of the program. Typically provides thorough details, for example, which points where achieved and how, or in the case of a score what specifically was tested and the results. This is a repeating element. If desired replace [Type] with the name of the certification from the GreenBuildingVerificationType list. |
| `RoomFamilyRoomFeatures` | string | [type] This field is a repeating element for each type of room selected in the RoomType field. For every RoomType there are two possible implementations. For a flat implementation (RETS 1.x only), each RoomType used is expected to appear as the "[type]" in the related rooms field name. i.e. RoomKitchenFeatures. A relational implementation of rooms must omit the type from the field name and use RoomType to create a vertical representation of the various rooms. i.e. RoomFeatures with Kitchen in the relational table's RoomType field. |
| `RoomFamilyRoomLength` | number | [type] This field is a repeating element for each type of room selected in the RoomType field. For every RoomType there are two possible implementations. For a flat implementation (RETS 1.x only), each RoomType used is expected to appear as the "[type]" in the related rooms field name. i.e. RoomKitchenLength. A relational implementation of rooms must omit the type from the field name and use RoomType to create a vertical representation of the various rooms. i.e. RoomLength with Kitchen in the relational table's RoomType field. |
| `RoomFamilyRoomLevel` | string | [type] This field is a repeating element for each type of room selected in the RoomType field. For every RoomType there are two possible implementations. For a flat implementation (RETS 1.x only), each RoomType used is expected to appear as the "[type]" in the related rooms field name. i.e. RoomKitchenLevel. A relational implementation of rooms must omit the type from the field name and use RoomType to create a vertical representation of the various rooms. i.e. RoomLevel with Kitchen in the relational table's RoomType field. |
| `RoomFamilyRoomWidth` | number | [type] This field is a repeating element for each type of room selected in the RoomType field. For every RoomType there are two possible implementations. For a flat implementation (RETS 1.x only), each RoomType used is expected to appear as the "[type]" in the related rooms field name. i.e. RoomKitchenWidth. A relational implementation of rooms must omit the type from the field name and use RoomType to create a vertical representation of the various rooms. i.e. RoomWidth with Kitchen in the relational table's RoomType field. |
| `RoomKitchenArea` | number | [type] This field is a repeating element for each type of room selected in the RoomType field. For every RoomType there are two possible implementations. For a flat implementation (RETS 1.x only), each RoomType used is expected to appear as the "[type]" in the related rooms field name. i.e. RoomKitchenArea. A relational implementation of rooms must omit the type from the field name and use RoomType to create a vertical representation of the various rooms. i.e. RoomArea with Kitchen in the relational table's RoomType field. |
| `RoomKitchenDescription` | string | Provides a link to the specific property’s high-performance rating or scoring details directly from and hosted by the sponsoring body of the program. Typically provides thorough details, for example, which points where achieved and how, or in the case of a score what specifically was tested and the results. This is a repeating element. If desired replace [Type] with the name of the certification from the GreenBuildingVerificationType list. |
| `RoomKitchenFeatures` | string | [type] This field is a repeating element for each type of room selected in the RoomType field. For every RoomType there are two possible implementations. For a flat implementation (RETS 1.x only), each RoomType used is expected to appear as the "[type]" in the related rooms field name. i.e. RoomKitchenFeatures. A relational implementation of rooms must omit the type from the field name and use RoomType to create a vertical representation of the various rooms. i.e. RoomFeatures with Kitchen in the relational table's RoomType field. |
| `RoomKitchenLength` | number | [type] This field is a repeating element for each type of room selected in the RoomType field. For every RoomType there are two possible implementations. For a flat implementation (RETS 1.x only), each RoomType used is expected to appear as the "[type]" in the related rooms field name. i.e. RoomKitchenLength. A relational implementation of rooms must omit the type from the field name and use RoomType to create a vertical representation of the various rooms. i.e. RoomLength with Kitchen in the relational table's RoomType field. |
| `RoomKitchenLevel` | string | [type] This field is a repeating element for each type of room selected in the RoomType field. For every RoomType there are two possible implementations. For a flat implementation (RETS 1.x only), each RoomType used is expected to appear as the "[type]" in the related rooms field name. i.e. RoomKitchenLevel. A relational implementation of rooms must omit the type from the field name and use RoomType to create a vertical representation of the various rooms. i.e. RoomLevel with Kitchen in the relational table's RoomType field. |
| `RoomKitchenWidth` | number | [type] This field is a repeating element for each type of room selected in the RoomType field. For every RoomType there are two possible implementations. For a flat implementation (RETS 1.x only), each RoomType used is expected to appear as the "[type]" in the related rooms field name. i.e. RoomKitchenWidth. A relational implementation of rooms must omit the type from the field name and use RoomType to create a vertical representation of the various rooms. i.e. RoomWidth with Kitchen in the relational table's RoomType field. |
| `RoomLivingRoomArea` | number | [type] This field is a repeating element for each type of room selected in the RoomType field. For every RoomType there are two possible implementations. For a flat implementation (RETS 1.x only), each RoomType used is expected to appear as the "[type]" in the related rooms field name. i.e. RoomKitchenArea. A relational implementation of rooms must omit the type from the field name and use RoomType to create a vertical representation of the various rooms. i.e. RoomArea with Kitchen in the relational table's RoomType field. |
| `RoomLivingRoomDescription` | string | Provides a link to the specific property’s high-performance rating or scoring details directly from and hosted by the sponsoring body of the program. Typically provides thorough details, for example, which points where achieved and how, or in the case of a score what specifically was tested and the results. This is a repeating element. If desired replace [Type] with the name of the certification from the GreenBuildingVerificationType list. |
| `RoomLivingRoomFeatures` | string | [type] This field is a repeating element for each type of room selected in the RoomType field. For every RoomType there are two possible implementations. For a flat implementation (RETS 1.x only), each RoomType used is expected to appear as the "[type]" in the related rooms field name. i.e. RoomKitchenFeatures. A relational implementation of rooms must omit the type from the field name and use RoomType to create a vertical representation of the various rooms. i.e. RoomFeatures with Kitchen in the relational table's RoomType field. |
| `RoomLivingRoomLength` | number | [type] This field is a repeating element for each type of room selected in the RoomType field. For every RoomType there are two possible implementations. For a flat implementation (RETS 1.x only), each RoomType used is expected to appear as the "[type]" in the related rooms field name. i.e. RoomKitchenLength. A relational implementation of rooms must omit the type from the field name and use RoomType to create a vertical representation of the various rooms. i.e. RoomLength with Kitchen in the relational table's RoomType field. |
| `RoomLivingRoomLevel` | string | [type] This field is a repeating element for each type of room selected in the RoomType field. For every RoomType there are two possible implementations. For a flat implementation (RETS 1.x only), each RoomType used is expected to appear as the "[type]" in the related rooms field name. i.e. RoomKitchenLevel. A relational implementation of rooms must omit the type from the field name and use RoomType to create a vertical representation of the various rooms. i.e. RoomLevel with Kitchen in the relational table's RoomType field. |
| `RoomLivingRoomWidth` | number | [type] This field is a repeating element for each type of room selected in the RoomType field. For every RoomType there are two possible implementations. For a flat implementation (RETS 1.x only), each RoomType used is expected to appear as the "[type]" in the related rooms field name. i.e. RoomKitchenWidth. A relational implementation of rooms must omit the type from the field name and use RoomType to create a vertical representation of the various rooms. i.e. RoomWidth with Kitchen in the relational table's RoomType field. |
| `RoomMasterBathroomArea` | number | [type] This field is a repeating element for each type of room selected in the RoomType field. For every RoomType there are two possible implementations. For a flat implementation (RETS 1.x only), each RoomType used is expected to appear as the "[type]" in the related rooms field name. i.e. RoomKitchenArea. A relational implementation of rooms must omit the type from the field name and use RoomType to create a vertical representation of the various rooms. i.e. RoomArea with Kitchen in the relational table's RoomType field. |
| `RoomMasterBathroomDescription` | string | Provides a link to the specific property’s high-performance rating or scoring details directly from and hosted by the sponsoring body of the program. Typically provides thorough details, for example, which points where achieved and how, or in the case of a score what specifically was tested and the results. This is a repeating element. If desired replace [Type] with the name of the certification from the GreenBuildingVerificationType list. |
| `RoomMasterBathroomFeatures` | string | [type] This field is a repeating element for each type of room selected in the RoomType field. For every RoomType there are two possible implementations. For a flat implementation (RETS 1.x only), each RoomType used is expected to appear as the "[type]" in the related rooms field name. i.e. RoomKitchenFeatures. A relational implementation of rooms must omit the type from the field name and use RoomType to create a vertical representation of the various rooms. i.e. RoomFeatures with Kitchen in the relational table's RoomType field. |
| `RoomMasterBathroomLength` | number | [type] This field is a repeating element for each type of room selected in the RoomType field. For every RoomType there are two possible implementations. For a flat implementation (RETS 1.x only), each RoomType used is expected to appear as the "[type]" in the related rooms field name. i.e. RoomKitchenLength. A relational implementation of rooms must omit the type from the field name and use RoomType to create a vertical representation of the various rooms. i.e. RoomLength with Kitchen in the relational table's RoomType field. |
| `RoomMasterBathroomLevel` | string | [type] This field is a repeating element for each type of room selected in the RoomType field. For every RoomType there are two possible implementations. For a flat implementation (RETS 1.x only), each RoomType used is expected to appear as the "[type]" in the related rooms field name. i.e. RoomKitchenLevel. A relational implementation of rooms must omit the type from the field name and use RoomType to create a vertical representation of the various rooms. i.e. RoomLevel with Kitchen in the relational table's RoomType field. |
| `RoomMasterBathroomWidth` | number | [type] This field is a repeating element for each type of room selected in the RoomType field. For every RoomType there are two possible implementations. For a flat implementation (RETS 1.x only), each RoomType used is expected to appear as the "[type]" in the related rooms field name. i.e. RoomKitchenWidth. A relational implementation of rooms must omit the type from the field name and use RoomType to create a vertical representation of the various rooms. i.e. RoomWidth with Kitchen in the relational table's RoomType field. |
| `RoomMasterBedroomArea` | number | [type] This field is a repeating element for each type of room selected in the RoomType field. For every RoomType there are two possible implementations. For a flat implementation (RETS 1.x only), each RoomType used is expected to appear as the "[type]" in the related rooms field name. i.e. RoomKitchenArea. A relational implementation of rooms must omit the type from the field name and use RoomType to create a vertical representation of the various rooms. i.e. RoomArea with Kitchen in the relational table's RoomType field. |
| `RoomMasterBedroomDescription` | string | Provides a link to the specific property’s high-performance rating or scoring details directly from and hosted by the sponsoring body of the program. Typically provides thorough details, for example, which points where achieved and how, or in the case of a score what specifically was tested and the results. This is a repeating element. If desired replace [Type] with the name of the certification from the GreenBuildingVerificationType list. |
| `RoomMasterBedroomFeatures` | string | [type] This field is a repeating element for each type of room selected in the RoomType field. For every RoomType there are two possible implementations. For a flat implementation (RETS 1.x only), each RoomType used is expected to appear as the "[type]" in the related rooms field name. i.e. RoomKitchenFeatures. A relational implementation of rooms must omit the type from the field name and use RoomType to create a vertical representation of the various rooms. i.e. RoomFeatures with Kitchen in the relational table's RoomType field. |
| `RoomMasterBedroomLength` | number | [type] This field is a repeating element for each type of room selected in the RoomType field. For every RoomType there are two possible implementations. For a flat implementation (RETS 1.x only), each RoomType used is expected to appear as the "[type]" in the related rooms field name. i.e. RoomKitchenLength. A relational implementation of rooms must omit the type from the field name and use RoomType to create a vertical representation of the various rooms. i.e. RoomLength with Kitchen in the relational table's RoomType field. |
| `RoomMasterBedroomLevel` | string | [type] This field is a repeating element for each type of room selected in the RoomType field. For every RoomType there are two possible implementations. For a flat implementation (RETS 1.x only), each RoomType used is expected to appear as the "[type]" in the related rooms field name. i.e. RoomKitchenLevel. A relational implementation of rooms must omit the type from the field name and use RoomType to create a vertical representation of the various rooms. i.e. RoomLevel with Kitchen in the relational table's RoomType field. |
| `RoomMasterBedroomWidth` | number | [type] This field is a repeating element for each type of room selected in the RoomType field. For every RoomType there are two possible implementations. For a flat implementation (RETS 1.x only), each RoomType used is expected to appear as the "[type]" in the related rooms field name. i.e. RoomKitchenWidth. A relational implementation of rooms must omit the type from the field name and use RoomType to create a vertical representation of the various rooms. i.e. RoomWidth with Kitchen in the relational table's RoomType field. |
| `RoomOfficeArea` | number | [type] This field is a repeating element for each type of room selected in the RoomType field. For every RoomType there are two possible implementations. For a flat implementation (RETS 1.x only), each RoomType used is expected to appear as the "[type]" in the related rooms field name. i.e. RoomKitchenArea. A relational implementation of rooms must omit the type from the field name and use RoomType to create a vertical representation of the various rooms. i.e. RoomArea with Kitchen in the relational table's RoomType field. |
| `RoomOfficeDescription` | string | Provides a link to the specific property’s high-performance rating or scoring details directly from and hosted by the sponsoring body of the program. Typically provides thorough details, for example, which points where achieved and how, or in the case of a score what specifically was tested and the results. This is a repeating element. If desired replace [Type] with the name of the certification from the GreenBuildingVerificationType list. |
| `RoomOfficeFeatures` | string | [type] This field is a repeating element for each type of room selected in the RoomType field. For every RoomType there are two possible implementations. For a flat implementation (RETS 1.x only), each RoomType used is expected to appear as the "[type]" in the related rooms field name. i.e. RoomKitchenFeatures. A relational implementation of rooms must omit the type from the field name and use RoomType to create a vertical representation of the various rooms. i.e. RoomFeatures with Kitchen in the relational table's RoomType field. |
| `RoomOfficeLength` | number | [type] This field is a repeating element for each type of room selected in the RoomType field. For every RoomType there are two possible implementations. For a flat implementation (RETS 1.x only), each RoomType used is expected to appear as the "[type]" in the related rooms field name. i.e. RoomKitchenLength. A relational implementation of rooms must omit the type from the field name and use RoomType to create a vertical representation of the various rooms. i.e. RoomLength with Kitchen in the relational table's RoomType field. |
| `RoomOfficeLevel` | string | [type] This field is a repeating element for each type of room selected in the RoomType field. For every RoomType there are two possible implementations. For a flat implementation (RETS 1.x only), each RoomType used is expected to appear as the "[type]" in the related rooms field name. i.e. RoomKitchenLevel. A relational implementation of rooms must omit the type from the field name and use RoomType to create a vertical representation of the various rooms. i.e. RoomLevel with Kitchen in the relational table's RoomType field. |
| `RoomOfficeWidth` | number | [type] This field is a repeating element for each type of room selected in the RoomType field. For every RoomType there are two possible implementations. For a flat implementation (RETS 1.x only), each RoomType used is expected to appear as the "[type]" in the related rooms field name. i.e. RoomKitchenWidth. A relational implementation of rooms must omit the type from the field name and use RoomType to create a vertical representation of the various rooms. i.e. RoomWidth with Kitchen in the relational table's RoomType field. |
| `RoomsTotal` | number | The number of rooms in the dwelling. |
| `RoomType` | string | This field is a list of the types used in the rooms repeating elements. The Type is a list of possible room types. i.e. Bedroom, Bathroom, Living Room, Workshop, etc. Each selected are expected to appear as the "[type]" in the related rooms fields in a flattened implementation (RETS 1.x only) of the room fields. A relational implementation of rooms must omit the type from the field name and use RoomType to create a vertical representation of the various rooms. **Note that Garage or Basement should not be added as a room type and are represented by the ParkingFeatures and Basement fields respectively. |
| `RVParkingDimensions` | string | The dimensions of the RV parking area minimally represented as length and width (i.e. 25 x 18) or a measurement of all sides of the polygon representing the usable RV parking space. i.e. 33 x 15 x 12 x 60. |
| `SeatingCapacity` | number | The seating capacity of the business being sold. |
| `SecurityFeatures` | string | A list describing the security features included in the sale/lease. |
| `SeniorCommunityYN` | boolean | The community is a senior community. |
| `SerialU` | string | Serial number of the mobile or manufactured home. For the first or only unit/section use Serial U over Serial X or Serial XX. |
| `SerialX` | string | Serial number of the mobile or manufactured home. For two units/sections, Serial U should be used first, Serial X second over or Serial XX. |
| `SerialXX` | string | Serial number of the mobile or manufactured home. For two units/sections, Serial U should be used first, Serial X second over or Serial XX. |
| `Sewer` | string | A list describing the sewer or septic features of the property. |
| `ShowingAdvanceNotice` | number | The hours of advance notice required to schedule a showing. |
| `ShowingAttendedYN` | boolean | Does this home require an attended showing? i.e. Yes = licensed agent representing the seller must be present during showing. |
| `ShowingConsiderations` | string | A pick list of conditions that may require caution or further consideration, such as bringing someone with you, when showing the property (i.e., Electricity Not On, Inconsistent Cell Service, No Exterior Lighting). |
| `ShowingContactName` | string | The name of the contact for the showing of the listed property. |
| `ShowingContactPhone` | string | A telephone number that should be called to arrange showing the property. |
| `ShowingContactPhoneExt` | string | The extension of the given phone number (if applicable). |
| `ShowingContactType` | string | The type of contact for the showing. i.e. Agent, Broker, Seller. |
| `ShowingDays` | string | The days of the week that the property is available for showing. i.e. Sundays, Mondays, Tuesdays, Wednesdays, Thursdays, Fridays, Saturdays |
| `ShowingEndTime` | string | From the days selected in the ShowingDays field, the end time that the property is available for showing. |
| `ShowingInstructions` | string | Remarks that detail the seller's instructions for showing the subject property. Showing instructions may include: contact information, showing times, notice required or other information. These remarks are privileged and are not for public viewing. |
| `ShowingRequirements` | string | A pick list of types of notice required to see the home. i.e. Appointment Required, Courtesy Call Only, Go Direct, etc. |
| `ShowingServiceName` | string | The name of the showing service used to request showings on the listing. |
| `ShowingStartTime` | string | From the days selected in the ShowingDays field, the start time that the property is available for showing. |
| `SignOnPropertyYN` | boolean | Is there a sign on the property. |
| `SimpleDaysOnMarket` | number | A simplified version of days on market (DOM) where the calculation is a simple start and end, such as the difference between the listing input or contract date and the date of sale. |
| `Skirt` | string | A list of types of mobile home skirting. |
| `SourceSystemID` | string | The RESO OUID's OrganizationUniqueId of the Source record provider. The source system is the system from which the record was directly received. In cases where the source system was not where the record originated (the authoritative system), see the Originating System fields. |
| `SourceSystemKey` | string | The system key, a unique record identifier, from the Source System. The Source System is the system from which the record was directly received. In cases where the Source System was not where the record originated (the authoritative system), see the Originating System fields. |
| `SourceSystemName` | string | The name of the immediate record provider. The system from which the record was directly received. The legal name of the company. |
| `SpaFeatures` | string | A list of features or description of the spa included in the sale/lease. |
| `SpaYN` | boolean | The property has a spa. |
| `SpecialLicenses` | string | Special licenses required/used by the business being sold. i.e. Beer/Wine, Class H, Professional, Gambling, None. |
| `SpecialListingConditions` | string | A list of options that describe the type of sale. i.e. Standard, REO, Short Sale, Probate, Auction, NOD, etc., at the time of listing. |
| `StandardStatus` | string | The status of the listing as it reflects the state of the contract between the listing agent and seller or an agreement with a buyer (Active, Active Under Contract, Canceled, Closed, Expired, Pending, Withdrawn). This is a Single Select field. |
| `StartShowingDate` | string | The date the listing agent/broker expects to start showing the property. |
| `StateOrProvince` | string | Text field containing the accepted postal abbreviation for the state or province. |
| `StateRegion` | string | A sub-section or area of a defined state or province. Examples would be the Keys in FL or Hudson Valley in NY. |
| `StatusChangeTimestamp` | string | The transactional timestamp automatically recorded by the MLS system representing the date/time the listing's status was last changed. |
| `Stories` | number | The number of floors in the property being sold. |
| `StoriesTotal` | number | The total number of floors in the building. In the case of multi-dwelling structures, this is the entire structure and not the individual dwelling being sold. |
| `StreetAdditionalInfo` | string | Information other than a prefix or suffix for the street portion of a postal address. |
| `StreetDirPrefix` | string | The direction indicator that precedes the listed property's street name. |
| `StreetDirSuffix` | string | The direction indicator that follows a listed property's street address. |
| `StreetName` | string | The street name portion of a listed property's street address. |
| `StreetNumber` | string | The street number portion of a listed property's street address. In some areas the street number may contain non-numeric characters. This field can also contain extensions and modifiers to the street number, such as "1/2" or "-B". This street number field should not include Prefixes, Direction or Suffixes. |
| `StreetNumberNumeric` | number | The integer portion of the street number. |
| `StreetSuffix` | string | The suffix portion of a listed property's street address. |
| `StreetSuffixModifier` | string | The Street Suffix Modifier allows the member to enter a unique Street Suffix that was not found in the Street Suffix pick list or to extend or prefix the suffix. |
| `StructureType` | string | The type of structure. |
| `SubAgencyCompensation` | string | The total commission to be paid to the Sub Agency, expressed as either a percentage or a constant currency amount. |
| `SubAgencyCompensationType` | string | A list of types to clarify the value entered in the SubAgencyCompensation field. For example $, % or some other clarification of the SubAgencyCompensation. |
| `SubdivisionName` | string | A neighborhood, community, complex or builder tract. |
| `SuppliesExpense` | number | The annual expense that is not paid directly by the tenant and is included in the Operating Expense calculations. |
| `SyndicateTo` | string | When permitted by the broker, the options made by the agent on behalf of the seller, where they would like their listings syndicated. i.e. Zillow, Trulia, Homes.com, etc. |
| `SyndicationRemarks` | string | Becoming more common in the industry, MLS's are hosting a separate "Public Remarks" for syndication purposes. This field should be defaulted to containing the Public Remarks, but upon broker decision, modified to include contact and other information denied by IDX rules, but allowed under local and national regulations. |
| `TaxAnnualAmount` | number | The annual property tax amount as of the last assessment made by the taxing authority. |
| `TaxAnnualAmountPerLivingAreaUnit` | number | The annual property tax amount as of the last assessment made by the taxing authority divided by the property's living area. The LivingAreaUnits field defines the area unit type (e.g., Square Feet or Square Meters). |
| `TaxAnnualAmountPerSquareFoot` | number | The annual property tax amount as of the last assessment made by the taxing authority divided by the property's living area square footage. |
| `TaxAssessedValue` | number | The property value as of the last assessment made by the taxing authority. |
| `TaxBlock` | string | A type of legal description for land in developed areas where streets or other rights-of-ways delineate large parcels of land referred to as divided into lots on which homes or other types of developments are built. An example would read "Lot 12 of Block 45 of Tract 3002 of the City of San Dunes, Desert County." Such a description would also reference an official plat filed with the clerk or recorder for that area which shows the location of the block and often the dimensions of the lots therein. |
| `TaxBookNumber` | string | Some systems of parcel identification incorporate a method which utilizes a county identifier, a tax book number, a tax map number and a parcel identification number. |
| `TaxExemptions` | string | A list of tax exemptions as they relate to the property. |
| `TaxLegalDescription` | string | A type of legal description for land in developed areas where streets or other rights-of-ways delineate large parcels of land referred to as divided into lots on which homes or other types of developments are built. An example would read "Lot 12 of Block 45 of Tract 3002 of the City of San Dunes, Desert County." Such a description would also reference an official plat filed with the clerk or recorder for that area which shows the location of the block and often the dimensions of the lots therein. The text here is also an index into the property as described by the County Recorder. |
| `TaxLot` | string | A type of legal description for land in developed areas where streets or other rights-of-ways delineate large parcels of land referred to as divided into lots on which homes or other types of developments are built. An example would read "Lot 12 of Block 45 of Tract 3002 of the City of San Dunes, Desert County." Such a description would also reference an official plat filed with the clerk or recorder for that area which shows the location of the block and often the dimensions of the lots therein. |
| `TaxMapNumber` | string | Some systems of parcel identification incorporate a method which utilizes a county identifier, a tax book number, a tax map number and a parcel identification number. |
| `TaxOtherAnnualAssessmentAmount` | number | Any other annual taxes, not including the tax reported in the TaxAmount field, as of the last assessment made by the taxing authority. |
| `TaxParcelLetter` | string | Some systems of parcel identification incorporate a method which utilizes a county identifier, a tax book number, a tax map number and a parcel identification number. |
| `TaxStatusCurrent` | string | The current tax status of the mobile home in cases where the land or space is included in the sale. |
| `TaxTract` | string | A type of legal description for land in developed areas where streets or other rights-of-ways delineate large parcels of land referred to as divided into lots on which homes or other types of developments are built. An example would read "Lot 12 of Block 45 of Tract 3002 of the City of San Dunes, Desert County." Such a description would also reference an official plat filed with the clerk or recorder for that area which shows the location of the block and often the dimensions of the lots therein. |
| `TaxYear` | number | The year in with the last assessment of the property value/tax was made. |
| `Telephone` | string | A list of telephone-service related features of the property (e.g. Installed, Public, Available). Note: the previous "Telephone" field was renamed to DistanceToPhoneServiceComments |
| `TenantPays` | string | A list of services or items that the tenant is responsible to pay. |
| `Topography` | string | The state of the surface of the land included with the property. i.e. flat, rolling, etc. |
| `TotalActualRent` | number | Total actual rent currently being collected from tenants of the income property. |
| `Township` | string | A subdivision of the county. |
| `TransactionBrokerCompensation` | string | The total commission to be paid to the transaction facilitator, expressed as either a percentage or a constant currency amount. |
| `TransactionBrokerCompensationType` | string | A list of types to clarify the value entered in the TransactionBrokerCompensation field. For example $, % or some other clarification of the TransactionBrokerCompensation. |
| `TrashExpense` | number | The annual expense that is not paid directly by the tenant and is included in the Operating Expense calculations. |
| `UnitNumber` | string | Text field containing the number or portion of a larger building or complex. Unit Number should appear following the street suffix or, if it exists, the street suffix direction, in the street address. Examples are: "APT G", "55", etc. |
| `UnitsFurnished` | string | Are the units furnished? i.e. All Units, Varies By Unit, None. |
| `UnitType1BedroomBathsTotal` | number | [type] This field is a repeating element for each type of unit selected in the UnitType field. For every UnitType there are two possible implementations. For a flat implementation (RETS 1.x only), each UnitTypeType used is expected to appear as the "[type]" in the related rooms field name. i.e. UnitTypeStudioBathsTotal. A relational implementation of UnitType must omit the type from the field name and use UnitTypeType to create a vertical representation of the various rooms. i.e. UnitTypeBathsTotal with Studio in the relational table's UnitType field. |
| `UnitType1BedroomBedsTotal` | number | [type] This field is a repeating element for each type of unit selected in the UnitType field. For every UnitType there are two possible implementations. For a flat implementation (RETS 1.x only), each UnitTypeType used is expected to appear as the "[type]" in the related rooms field name. i.e. UnitTypeStudioBedsTotal. A relational implementation of UnitType must omit the type from the field name and use UnitTypeType to create a vertical representation of the various rooms. i.e. UnitTypeBedsTotal with Studio in the relational table's UnitType field. |
| `UnitType1BedroomDescription` | string | [type] This field is a repeating element for each type of unit selected in the UnitType field. For every UnitType there are two possible implementations. For a flat implementation (RETS 1.x only), each UnitTypeType used is expected to appear as the "[type]" in the related rooms field name. i.e. UnitTypeStudioDescription. A relational implementation of UnitType must omit the type from the field name and use UnitTypeType to create a vertical representation of the various rooms. i.e. UnitTypeDescription with Studio in the relational table's UnitType field. |
| `UnitType1BedroomFurnished` | string | [type] This field is a repeating element for each type of unit selected in the UnitType field. For every UnitType there are two possible implementations. For a flat implementation (RETS 1.x only), each UnitTypeType used is expected to appear as the "[type]" in the related rooms field name. i.e. UnitTypeStudioFurnished. A relational implementation of UnitType must omit the type from the field name and use UnitTypeType to create a vertical representation of the various rooms. i.e. UnitTypeFurnished with Studio in the relational table's UnitType field. |
| `UnitType1BedroomGarageAttachedYN` | boolean | [type] This field is a repeating element for each type of unit selected in the UnitType field. For every UnitType there are two possible implementations. For a flat implementation (RETS 1.x only), each UnitTypeType used is expected to appear as the "[type]" in the related rooms field name. i.e. UnitTypeStudioGarageAttachedYN. A relational implementation of UnitType must omit the type from the field name and use UnitTypeType to create a vertical representation of the various rooms. i.e. UnitTypeGarageAttachedYN with Studio in the relational table's UnitType field. |
| `UnitType1BedroomGarageSpaces` | number | [type] This field is a repeating element for each type of unit selected in the UnitType field. For every UnitType there are two possible implementations. For a flat implementation (RETS 1.x only), each UnitTypeType used is expected to appear as the "[type]" in the related rooms field name. i.e. UnitTypeStudioGarageSpaces. A relational implementation of UnitType must omit the type from the field name and use UnitTypeType to create a vertical representation of the various rooms. i.e. UnitTypeGarageSpaces with Studio in the relational table's UnitType field. |
| `UnitType1BedroomUnitsTotal` | number | [type] This field is a repeating element for each type of unit selected in the UnitType field. For every UnitType there are two possible implementations. For a flat implementation (RETS 1.x only), each UnitTypeType used is expected to appear as the "[type]" in the related rooms field name. i.e. UnitTypeStudioUnitsTotal. A relational implementation of UnitType must omit the type from the field name and use UnitTypeType to create a vertical representation of the various rooms. i.e. UnitTypeUnitsTotal with Studio in the relational table's UnitType field. |
| `UnitType2BedroomBathsTotal` | number | [type] This field is a repeating element for each type of unit selected in the UnitType field. For every UnitType there are two possible implementations. For a flat implementation (RETS 1.x only), each UnitTypeType used is expected to appear as the "[type]" in the related rooms field name. i.e. UnitTypeStudioBathsTotal. A relational implementation of UnitType must omit the type from the field name and use UnitTypeType to create a vertical representation of the various rooms. i.e. UnitTypeBathsTotal with Studio in the relational table's UnitType field. |
| `UnitType2BedroomBedsTotal` | number | [type] This field is a repeating element for each type of unit selected in the UnitType field. For every UnitType there are two possible implementations. For a flat implementation (RETS 1.x only), each UnitTypeType used is expected to appear as the "[type]" in the related rooms field name. i.e. UnitTypeStudioBedsTotal. A relational implementation of UnitType must omit the type from the field name and use UnitTypeType to create a vertical representation of the various rooms. i.e. UnitTypeBedsTotal with Studio in the relational table's UnitType field. |
| `UnitType2BedroomDescription` | string | [type] This field is a repeating element for each type of unit selected in the UnitType field. For every UnitType there are two possible implementations. For a flat implementation (RETS 1.x only), each UnitTypeType used is expected to appear as the "[type]" in the related rooms field name. i.e. UnitTypeStudioDescription. A relational implementation of UnitType must omit the type from the field name and use UnitTypeType to create a vertical representation of the various rooms. i.e. UnitTypeDescription with Studio in the relational table's UnitType field. |
| `UnitType2BedroomFurnished` | string | [type] This field is a repeating element for each type of unit selected in the UnitType field. For every UnitType there are two possible implementations. For a flat implementation (RETS 1.x only), each UnitTypeType used is expected to appear as the "[type]" in the related rooms field name. i.e. UnitTypeStudioFurnished. A relational implementation of UnitType must omit the type from the field name and use UnitTypeType to create a vertical representation of the various rooms. i.e. UnitTypeFurnished with Studio in the relational table's UnitType field. |
| `UnitType2BedroomGarageAttachedYN` | boolean | [type] This field is a repeating element for each type of unit selected in the UnitType field. For every UnitType there are two possible implementations. For a flat implementation (RETS 1.x only), each UnitTypeType used is expected to appear as the "[type]" in the related rooms field name. i.e. UnitTypeStudioGarageAttachedYN. A relational implementation of UnitType must omit the type from the field name and use UnitTypeType to create a vertical representation of the various rooms. i.e. UnitTypeGarageAttachedYN with Studio in the relational table's UnitType field. |
| `UnitType2BedroomGarageSpaces` | number | [type] This field is a repeating element for each type of unit selected in the UnitType field. For every UnitType there are two possible implementations. For a flat implementation (RETS 1.x only), each UnitTypeType used is expected to appear as the "[type]" in the related rooms field name. i.e. UnitTypeStudioGarageSpaces. A relational implementation of UnitType must omit the type from the field name and use UnitTypeType to create a vertical representation of the various rooms. i.e. UnitTypeGarageSpaces with Studio in the relational table's UnitType field. |
| `UnitType2BedroomUnitsTotal` | number | [type] This field is a repeating element for each type of unit selected in the UnitType field. For every UnitType there are two possible implementations. For a flat implementation (RETS 1.x only), each UnitTypeType used is expected to appear as the "[type]" in the related rooms field name. i.e. UnitTypeStudioUnitsTotal. A relational implementation of UnitType must omit the type from the field name and use UnitTypeType to create a vertical representation of the various rooms. i.e. UnitTypeUnitsTotal with Studio in the relational table's UnitType field. |
| `UnitType3BedroomBathsTotal` | number | [type] This field is a repeating element for each type of unit selected in the UnitType field. For every UnitType there are two possible implementations. For a flat implementation (RETS 1.x only), each UnitTypeType used is expected to appear as the "[type]" in the related rooms field name. i.e. UnitTypeStudioBathsTotal. A relational implementation of UnitType must omit the type from the field name and use UnitTypeType to create a vertical representation of the various rooms. i.e. UnitTypeBathsTotal with Studio in the relational table's UnitType field. |
| `UnitType3BedroomBedsTotal` | number | [type] This field is a repeating element for each type of unit selected in the UnitType field. For every UnitType there are two possible implementations. For a flat implementation (RETS 1.x only), each UnitTypeType used is expected to appear as the "[type]" in the related rooms field name. i.e. UnitTypeStudioBedsTotal. A relational implementation of UnitType must omit the type from the field name and use UnitTypeType to create a vertical representation of the various rooms. i.e. UnitTypeBedsTotal with Studio in the relational table's UnitType field. |
| `UnitType3BedroomDescription` | string | [type] This field is a repeating element for each type of unit selected in the UnitType field. For every UnitType there are two possible implementations. For a flat implementation (RETS 1.x only), each UnitTypeType used is expected to appear as the "[type]" in the related rooms field name. i.e. UnitTypeStudioDescription. A relational implementation of UnitType must omit the type from the field name and use UnitTypeType to create a vertical representation of the various rooms. i.e. UnitTypeDescription with Studio in the relational table's UnitType field. |
| `UnitType3BedroomFurnished` | string | [type] This field is a repeating element for each type of unit selected in the UnitType field. For every UnitType there are two possible implementations. For a flat implementation (RETS 1.x only), each UnitTypeType used is expected to appear as the "[type]" in the related rooms field name. i.e. UnitTypeStudioFurnished. A relational implementation of UnitType must omit the type from the field name and use UnitTypeType to create a vertical representation of the various rooms. i.e. UnitTypeFurnished with Studio in the relational table's UnitType field. |
| `UnitType3BedroomGarageAttachedYN` | boolean | [type] This field is a repeating element for each type of unit selected in the UnitType field. For every UnitType there are two possible implementations. For a flat implementation (RETS 1.x only), each UnitTypeType used is expected to appear as the "[type]" in the related rooms field name. i.e. UnitTypeStudioGarageAttachedYN. A relational implementation of UnitType must omit the type from the field name and use UnitTypeType to create a vertical representation of the various rooms. i.e. UnitTypeGarageAttachedYN with Studio in the relational table's UnitType field. |
| `UnitType3BedroomGarageSpaces` | number | [type] This field is a repeating element for each type of unit selected in the UnitType field. For every UnitType there are two possible implementations. For a flat implementation (RETS 1.x only), each UnitTypeType used is expected to appear as the "[type]" in the related rooms field name. i.e. UnitTypeStudioGarageSpaces. A relational implementation of UnitType must omit the type from the field name and use UnitTypeType to create a vertical representation of the various rooms. i.e. UnitTypeGarageSpaces with Studio in the relational table's UnitType field. |
| `UnitType3BedroomUnitsTotal` | number | [type] This field is a repeating element for each type of unit selected in the UnitType field. For every UnitType there are two possible implementations. For a flat implementation (RETS 1.x only), each UnitTypeType used is expected to appear as the "[type]" in the related rooms field name. i.e. UnitTypeStudioUnitsTotal. A relational implementation of UnitType must omit the type from the field name and use UnitTypeType to create a vertical representation of the various rooms. i.e. UnitTypeUnitsTotal with Studio in the relational table's UnitType field. |
| `UnitType4BedroomOrMoreBathsTotal` | number | [type] This field is a repeating element for each type of unit selected in the UnitType field. For every UnitType there are two possible implementations. For a flat implementation (RETS 1.x only), each UnitTypeType used is expected to appear as the "[type]" in the related rooms field name. i.e. UnitTypeStudioBathsTotal. A relational implementation of UnitType must omit the type from the field name and use UnitTypeType to create a vertical representation of the various rooms. i.e. UnitTypeBathsTotal with Studio in the relational table's UnitType field. |
| `UnitType4BedroomOrMoreBedsTotal` | number | [type] This field is a repeating element for each type of unit selected in the UnitType field. For every UnitType there are two possible implementations. For a flat implementation (RETS 1.x only), each UnitTypeType used is expected to appear as the "[type]" in the related rooms field name. i.e. UnitTypeStudioBedsTotal. A relational implementation of UnitType must omit the type from the field name and use UnitTypeType to create a vertical representation of the various rooms. i.e. UnitTypeBedsTotal with Studio in the relational table's UnitType field. |
| `UnitType4BedroomOrMoreDescription` | string | [type] This field is a repeating element for each type of unit selected in the UnitType field. For every UnitType there are two possible implementations. For a flat implementation (RETS 1.x only), each UnitTypeType used is expected to appear as the "[type]" in the related rooms field name. i.e. UnitTypeStudioDescription. A relational implementation of UnitType must omit the type from the field name and use UnitTypeType to create a vertical representation of the various rooms. i.e. UnitTypeDescription with Studio in the relational table's UnitType field. |
| `UnitType4BedroomOrMoreFurnished` | string | [type] This field is a repeating element for each type of unit selected in the UnitType field. For every UnitType there are two possible implementations. For a flat implementation (RETS 1.x only), each UnitTypeType used is expected to appear as the "[type]" in the related rooms field name. i.e. UnitTypeStudioFurnished. A relational implementation of UnitType must omit the type from the field name and use UnitTypeType to create a vertical representation of the various rooms. i.e. UnitTypeFurnished with Studio in the relational table's UnitType field. |
| `UnitType4BedroomOrMoreGarageAttachedYN` | boolean | [type] This field is a repeating element for each type of unit selected in the UnitType field. For every UnitType there are two possible implementations. For a flat implementation (RETS 1.x only), each UnitTypeType used is expected to appear as the "[type]" in the related rooms field name. i.e. UnitTypeStudioGarageAttachedYN. A relational implementation of UnitType must omit the type from the field name and use UnitTypeType to create a vertical representation of the various rooms. i.e. UnitTypeGarageAttachedYN with Studio in the relational table's UnitType field. |
| `UnitType4BedroomOrMoreGarageSpaces` | number | [type] This field is a repeating element for each type of unit selected in the UnitType field. For every UnitType there are two possible implementations. For a flat implementation (RETS 1.x only), each UnitTypeType used is expected to appear as the "[type]" in the related rooms field name. i.e. UnitTypeStudioGarageSpaces. A relational implementation of UnitType must omit the type from the field name and use UnitTypeType to create a vertical representation of the various rooms. i.e. UnitTypeGarageSpaces with Studio in the relational table's UnitType field. |
| `UnitType4BedroomOrMoreUnitsTotal` | number | [type] This field is a repeating element for each type of unit selected in the UnitType field. For every UnitType there are two possible implementations. For a flat implementation (RETS 1.x only), each UnitTypeType used is expected to appear as the "[type]" in the related rooms field name. i.e. UnitTypeStudioUnitsTotal. A relational implementation of UnitType must omit the type from the field name and use UnitTypeType to create a vertical representation of the various rooms. i.e. UnitTypeUnitsTotal with Studio in the relational table's UnitType field. |
| `UnitTypeLoftBathsTotal` | number | [type] This field is a repeating element for each type of unit selected in the UnitType field. For every UnitType there are two possible implementations. For a flat implementation (RETS 1.x only), each UnitTypeType used is expected to appear as the "[type]" in the related rooms field name. i.e. UnitTypeStudioBathsTotal. A relational implementation of UnitType must omit the type from the field name and use UnitTypeType to create a vertical representation of the various rooms. i.e. UnitTypeBathsTotal with Studio in the relational table's UnitType field. |
| `UnitTypeLoftBedsTotal` | number | [type] This field is a repeating element for each type of unit selected in the UnitType field. For every UnitType there are two possible implementations. For a flat implementation (RETS 1.x only), each UnitTypeType used is expected to appear as the "[type]" in the related rooms field name. i.e. UnitTypeStudioBedsTotal. A relational implementation of UnitType must omit the type from the field name and use UnitTypeType to create a vertical representation of the various rooms. i.e. UnitTypeBedsTotal with Studio in the relational table's UnitType field. |
| `UnitTypeLoftDescription` | string | [type] This field is a repeating element for each type of unit selected in the UnitType field. For every UnitType there are two possible implementations. For a flat implementation (RETS 1.x only), each UnitTypeType used is expected to appear as the "[type]" in the related rooms field name. i.e. UnitTypeStudioDescription. A relational implementation of UnitType must omit the type from the field name and use UnitTypeType to create a vertical representation of the various rooms. i.e. UnitTypeDescription with Studio in the relational table's UnitType field. |
| `UnitTypeLoftFurnished` | string | [type] This field is a repeating element for each type of unit selected in the UnitType field. For every UnitType there are two possible implementations. For a flat implementation (RETS 1.x only), each UnitTypeType used is expected to appear as the "[type]" in the related rooms field name. i.e. UnitTypeStudioFurnished. A relational implementation of UnitType must omit the type from the field name and use UnitTypeType to create a vertical representation of the various rooms. i.e. UnitTypeFurnished with Studio in the relational table's UnitType field. |
| `UnitTypeLoftGarageAttachedYN` | boolean | [type] This field is a repeating element for each type of unit selected in the UnitType field. For every UnitType there are two possible implementations. For a flat implementation (RETS 1.x only), each UnitTypeType used is expected to appear as the "[type]" in the related rooms field name. i.e. UnitTypeStudioGarageAttachedYN. A relational implementation of UnitType must omit the type from the field name and use UnitTypeType to create a vertical representation of the various rooms. i.e. UnitTypeGarageAttachedYN with Studio in the relational table's UnitType field. |
| `UnitTypeLoftGarageSpaces` | number | [type] This field is a repeating element for each type of unit selected in the UnitType field. For every UnitType there are two possible implementations. For a flat implementation (RETS 1.x only), each UnitTypeType used is expected to appear as the "[type]" in the related rooms field name. i.e. UnitTypeStudioGarageSpaces. A relational implementation of UnitType must omit the type from the field name and use UnitTypeType to create a vertical representation of the various rooms. i.e. UnitTypeGarageSpaces with Studio in the relational table's UnitType field. |
| `UnitTypeLoftUnitsTotal` | number | [type] This field is a repeating element for each type of unit selected in the UnitType field. For every UnitType there are two possible implementations. For a flat implementation (RETS 1.x only), each UnitTypeType used is expected to appear as the "[type]" in the related rooms field name. i.e. UnitTypeStudioUnitsTotal. A relational implementation of UnitType must omit the type from the field name and use UnitTypeType to create a vertical representation of the various rooms. i.e. UnitTypeUnitsTotal with Studio in the relational table's UnitType field. |
| `UnitTypeStudioBathsTotal` | number | [type] This field is a repeating element for each type of unit selected in the UnitType field. For every UnitType there are two possible implementations. For a flat implementation (RETS 1.x only), each UnitTypeType used is expected to appear as the "[type]" in the related rooms field name. i.e. UnitTypeStudioBathsTotal. A relational implementation of UnitType must omit the type from the field name and use UnitTypeType to create a vertical representation of the various rooms. i.e. UnitTypeBathsTotal with Studio in the relational table's UnitType field. |
| `UnitTypeStudioBedsTotal` | number | [type] This field is a repeating element for each type of unit selected in the UnitType field. For every UnitType there are two possible implementations. For a flat implementation (RETS 1.x only), each UnitTypeType used is expected to appear as the "[type]" in the related rooms field name. i.e. UnitTypeStudioBedsTotal. A relational implementation of UnitType must omit the type from the field name and use UnitTypeType to create a vertical representation of the various rooms. i.e. UnitTypeBedsTotal with Studio in the relational table's UnitType field. |
| `UnitTypeStudioDescription` | string | [type] This field is a repeating element for each type of unit selected in the UnitType field. For every UnitType there are two possible implementations. For a flat implementation (RETS 1.x only), each UnitTypeType used is expected to appear as the "[type]" in the related rooms field name. i.e. UnitTypeStudioDescription. A relational implementation of UnitType must omit the type from the field name and use UnitTypeType to create a vertical representation of the various rooms. i.e. UnitTypeDescription with Studio in the relational table's UnitType field. |
| `UnitTypeStudioFurnished` | string | [type] This field is a repeating element for each type of unit selected in the UnitType field. For every UnitType there are two possible implementations. For a flat implementation (RETS 1.x only), each UnitTypeType used is expected to appear as the "[type]" in the related rooms field name. i.e. UnitTypeStudioFurnished. A relational implementation of UnitType must omit the type from the field name and use UnitTypeType to create a vertical representation of the various rooms. i.e. UnitTypeFurnished with Studio in the relational table's UnitType field. |
| `UnitTypeStudioGarageAttachedYN` | boolean | [type] This field is a repeating element for each type of unit selected in the UnitType field. For every UnitType there are two possible implementations. For a flat implementation (RETS 1.x only), each UnitTypeType used is expected to appear as the "[type]" in the related rooms field name. i.e. UnitTypeStudioGarageAttachedYN. A relational implementation of UnitType must omit the type from the field name and use UnitTypeType to create a vertical representation of the various rooms. i.e. UnitTypeGarageAttachedYN with Studio in the relational table's UnitType field. |
| `UnitTypeStudioGarageSpaces` | number | [type] This field is a repeating element for each type of unit selected in the UnitType field. For every UnitType there are two possible implementations. For a flat implementation (RETS 1.x only), each UnitTypeType used is expected to appear as the "[type]" in the related rooms field name. i.e. UnitTypeStudioGarageSpaces. A relational implementation of UnitType must omit the type from the field name and use UnitTypeType to create a vertical representation of the various rooms. i.e. UnitTypeGarageSpaces with Studio in the relational table's UnitType field. |
| `UnitTypeStudioUnitsTotal` | number | [type] This field is a repeating element for each type of unit selected in the UnitType field. For every UnitType there are two possible implementations. For a flat implementation (RETS 1.x only), each UnitTypeType used is expected to appear as the "[type]" in the related rooms field name. i.e. UnitTypeStudioUnitsTotal. A relational implementation of UnitType must omit the type from the field name and use UnitTypeType to create a vertical representation of the various rooms. i.e. UnitTypeUnitsTotal with Studio in the relational table's UnitType field. |
| `UnitTypeType` | string | This field is a list of the types used in the Unit Type repeating elements. The Type is a list of possible Unit Types. i.e. 1, 2, 3 or 2 Bed, Studio, Special Loft, etc. Each selected are expected to appear as the "[type]" in the related UnitType fields in a flattened implementation (RETS 1.x only) of the room fields. A relational implementation of UnitTypes must omit the type from the field name and use UnitTypeType to create a vertical representation of the various unit types. The fact that the field repeats the word "type" is intentional. |
| `UniversalPropertyId` | string | The RESO Universal Property Identifier (UPI) is a unique identifier for all real property in the U.S. and Canada. It is based on country and local identification methods and is limited to real property. For cases such as shares of real property, units and other more granular cases, please utilize the UniversalPropertySubId. |
| `UniversalPropertySubId` | string | A unique identifier for all subsets or shares of real property in the U.S. and Canada. This may include Stock Cooperatives, Community Apartment, Units for Rent, etc. Informally abbreviated as UPSI, it is based on country and local identification methods, just as the Universal Property Identifier (UPI), but it is limited to subsets or shares of real property. For cases of complete real property, please utilize the UniversalPropertyId field. |
| `UnparsedAddress` | string | The UnparsedAddress is a text representation of the address with the full civic location as a single entity. It may optionally include any of City, StateOrProvince, PostalCode and Country. |
| `Utilities` | string | A list of the utilities for the property being sold/leased. |
| `VacancyAllowance` | number | An estimate of the amount of rent that may be foregone because of unoccupied units. |
| `VacancyAllowanceRate` | number | An estimate of the percent of rent that may be foregone because of unoccupied units. |
| `Vegetation` | string | A list of the type(s) of vegetation on the property. Note that this is not for farm crops, but more residential type vegetation. |
| `VideosChangeTimestamp` | string | System generated timestamp of when the last update or change to the videos for this listing was made. |
| `VideosCount` | number | The total number of videos or virtual tours included with the listing. |
| `View` | string | A view as seen from the listed property. |
| `ViewYN` | boolean | The property has a view. |
| `VirtualTourURLBranded` | string | A text field that holds the URL for a branded virtual tour of the property. |
| `VirtualTourURLUnbranded` | string | A text field that holds the URL for an unbranded virtual tour of the property. |
| `VirtualTourURLZillow` | string | Zillow 3D virtual tour URL |
| `WalkScore` | number | A walkability index based on the time to walk from a property to near by essentials such as grocery stores, schools, churches, etc. See www.walkscore.com for more information and requirements for using WalkScore. |
| `WaterBodyName` | string | The name, if known, of the body of water on which the property is located. (E.g., lake name, river name, ocean name, sea name, canal name). |
| `WaterfrontFeatures` | string | Features of the waterfront on which the property is located. |
| `WaterfrontYN` | boolean | The property is on the waterfront. |
| `WaterSewerExpense` | number | The annual expense that is not paid directly by the tenant and is included in the Operating Expense calculations. |
| `WaterSource` | string | A list of the source(s) of water for the property |
| `WindowFeatures` | string | A list of features or description of the windows included in the sale/lease. |
| `WithdrawnDate` | string | Date the listing was withdrawn from the market. This is not when a listing contact was cancelled or closed, but a withdrawal from the market while the contract between the seller and listing agent is still in effect and an offer has not been accepted. This is the date entered by the agent reflecting when the change occurred contractually, not a timestamp of when the change was made in the MLS. |
| `WoodedArea` | number | Measurement or percentage of the property that is wooded or forest. |
| `WorkmansCompensationExpense` | number | The annual expense that is not paid directly by the tenant and is included in the Operating Expense calculations. |
| `YearBuilt` | number | The year that an occupancy permit is first granted for the house or other local measure of initial habitability of the build. The type definition permits an empty value with an attribute noting that it is an unknown date or that the building is new construction. While constraints have not been applied, convention at the time of adoption has this as a four (4) digit year value. |
| `YearBuiltDetails` | string | A description of the details behind the year the structure was built. |
| `YearBuiltEffective` | number | The year a major rebuild/renovated of the structure occurred. |
| `YearBuiltSource` | string | Add a list of sources of the year built. i.e. Appraiser, Assessor, Builder, Estimated, etc., |
| `YearEstablished` | number | The year the business being sold was established. |
| `YearsCurrentOwner` | number | The number of years the current owner has had possession of the business. |
| `Zoning` | string | A division of the city or county into areas of different permissible land uses. This Zone field should be used for the short code that is commonly used. For full textual descriptions please use the ZoningDescription field. |
| `ZoningDescription` | string | A list of descriptions of the zoning of the property. The zoning codes are often non-descriptive and variant. Zoning Description is a more descriptive form of the zoning for the property, i.e. Agricultural, Residential, Rezone Possible, etc. Specific zone codes must be added to the Zoning field. |

## Request Property Information for a Single Property (Listing)
Returns MLS information about a single property (listing) from UNLOCK MLS.

## Example Code
### Example URL Request
```markdown
https://api.bridgedataoutput.com/api/v2/OData/{dataset_id}/Property({ListingKey})?access_token={access_token}
```
### Example Response
The same response for a list of properties, except you will receive only data from a single property(Listing)

### Request Parameters for the URL
| Name | Type | Description |
|------|------|-------------|
| `access_token` | string | Token to identify the user or application. |
| `dataset` | string | Dataset to get the listings from. |
| `ListingKey` | string | Key to identify a property |
| `$skip` | integer | Skip the first n items |
| `$select` | string | Select properties that are explicitly specified e.g. OfficeType |
| `$unselect` | string | Filter record properties that are explicitly specified e.g. OfficeFax |
| `$top` | integer | Show only the first n items |
| `$orderby` | string | Order items by specified property value, e.g. ModificationTimestamp asc |
| `$filter` | string | Filter items by certain values |
| `$expand` | array | Expand related entities |