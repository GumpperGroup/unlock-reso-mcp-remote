# MCP Resources Documentation

## Overview

The UNLOCK MLS MCP Server provides 8 comprehensive resources that offer guidance, documentation, and system information. These resources are designed to help users understand how to effectively use the server's capabilities and provide step-by-step workflows for common real estate tasks.

## Resource Architecture

### Resource System Design

```
MCP Client → Resource Request → Resource Handler → 
Content Generation → Markdown Formatting → MCP Response
```

### Content Types

All resources return markdown-formatted content for optimal readability and structure:
- **Guides**: Step-by-step instructions and best practices
- **References**: Comprehensive lookup tables and examples
- **Workflows**: Complete processes for common tasks
- **Status**: Real-time system information and health checks

## Resources Reference

### 1. Property Search Examples

**URI**: `property://search/examples`  
**MIME Type**: `text/markdown`  
**Description**: Common property search query examples and patterns

#### Content Overview

This resource provides comprehensive examples of how to use the `search_properties` tool effectively, including both natural language and structured query approaches.

#### Key Sections

##### Natural Language Queries
- **Basic Searches**: Simple property searches by type and location
- **Price-Based Searches**: Queries focused on budget constraints
- **Location-Specific Searches**: Area and neighborhood targeting
- **Feature-Based Searches**: Searches by amenities and characteristics
- **Complex Searches**: Multi-criteria advanced searches

##### Search Filters Reference
- **Location Filters**: city, state, zip_code
- **Price Filters**: min_price, max_price with ranges
- **Size Filters**: bedrooms, bathrooms, square footage
- **Property Type Filters**: All supported property types
- **Status Filters**: Active, sold, pending, etc.

##### Optimization Tips
- Specificity guidelines for better results
- Common search patterns and variations
- Troubleshooting for no results or too many results
- Best practices for different user types

#### Example Content Structure

```markdown
# Property Search Examples

## Natural Language Queries
### Basic Searches
- "3 bedroom house in Austin TX"
- "condo under $400k"

### Complex Searches  
- "3+ bedroom house under $450k in Austin TX with pool and 2+ car garage"

## Search Filters
- **Location**: city, state, zip_code
- **Price**: min_price, max_price
- **Property Type**: residential, condo, townhouse, single_family

## Tips for Better Results
1. **Be specific**: Include city and state
2. **Use ranges**: "under", "over", "between"
3. **Combine criteria**: Mix location, price, and features
```

---

### 2. Property Types Reference

**URI**: `property://types/reference`  
**MIME Type**: `text/markdown`  
**Description**: Reference guide for property types and status values

#### Content Overview

Comprehensive guide to understanding property types, status values, and their implications for searches and analysis.

#### Key Sections

##### Property Types
- **Residential Properties**: Single family, condo, townhouse, multi-family
- **Other Property Types**: Land, commercial, business opportunities
- **Type Characteristics**: Typical features and use cases

##### Property Status
- **Active Listings**: Currently available properties
- **Completed Sales**: Sold and closed properties  
- **Inactive Listings**: Expired, withdrawn, cancelled

##### Search Tips by Type
- Specific guidance for each property type
- Best use cases and target audiences
- Common search patterns and examples

#### Example Content Structure

```markdown
# Property Types & Status Reference

## Property Types
### Residential Properties
- **single_family**: Detached single-family homes
- **condo**: Condominiums, condos
- **townhouse**: Townhomes, row houses

## Property Status
### Active Listings
- **active**: Currently for sale and available
- **under_contract**: Sale pending, buyer found

## Search Tips by Property Type
### Single Family Homes
- Best for: Families, first-time buyers
- Typical features: Private yards, garages
- Search examples: "3 bedroom house"
```

---

### 3. Market Analysis Guide  

**URI**: `market://analysis/guide`  
**MIME Type**: `text/markdown`  
**Description**: Guide for understanding market analysis data and insights

#### Content Overview

Detailed explanation of market analysis metrics, interpretation guidelines, and actionable insights for different user types.

#### Key Sections

##### Understanding Market Data
- **Active Listings Statistics**: Inventory and pricing metrics
- **Recently Sold Statistics**: Transaction data and trends
- **Market Insights**: Price trends and inventory levels

##### Market Interpretation
- **Price Trends**: Rising, declining, stable market indicators
- **Inventory Levels**: Buyer's vs seller's market conditions
- **Timing Indicators**: Seasonal and cyclical patterns

##### Actionable Insights
- **For Buyers**: Strategy recommendations by market type
- **For Sellers**: Pricing and timing guidance
- **For Investors**: Market selection and timing criteria

##### Analysis Limitations
- Data scope and coverage limitations
- Seasonal variation considerations
- Local micro-market factors

#### Example Content Structure

```markdown
# Market Analysis Guide

## Understanding Market Data
### Active Listings Statistics
- **Total Active**: Number of properties currently for sale
- **Average Price**: Mean listing price
- **Price per SqFt**: Average cost per square foot

### Market Insights
#### Price Trends
- **Rising**: Active listings priced significantly higher than recent sales
- **Stable**: Active listings within 5% of recent sale prices

## Market Analysis Tips
### For Buyers
- **Rising Market**: Act quickly, expect competition
- **Stable Market**: Normal negotiations, standard timelines
```

---

### 4. Agent Search Guide

**URI**: `agent://search/guide`  
**MIME Type**: `text/markdown`  
**Description**: Guide for finding and working with real estate agents

#### Content Overview

Comprehensive guide to using the `find_agent` tool effectively and working with real estate professionals.

#### Key Sections

##### Finding Real Estate Agents
- **Search by Name**: Finding specific agents
- **Search by Location**: Local market experts
- **Search by Office**: Brokerage-based searches
- **Search by Specialization**: Expertise-based selection

##### Agent Information Available
- **Contact Details**: Phone, email, office information
- **Professional Information**: Licenses, designations, certifications
- **Location Coverage**: Service areas and market expertise

##### Working with Agents
- **Initial Contact**: Best practices for first communication
- **Vetting Questions**: Key questions to ask potential agents
- **Collaboration Tips**: Effective working relationships

##### Agent Selection Criteria
- **For Buyers**: Key qualifications and characteristics
- **For Sellers**: Marketing and pricing expertise
- **For Investors**: Investment-specific knowledge and experience

#### Example Content Structure

```markdown
# Agent Search Guide

## Finding Real Estate Agents
### Search by Name
- Use partial or full agent names
- Example: `find_agent(name="John Smith")`

### Search by Location
- Find agents in specific cities or states
- Example: `find_agent(city="Austin", state="TX")`

## Working with Agents
### Initial Contact
1. Use agent search to find qualified professionals
2. Review location and specialization match
3. Contact via preferred method
4. Discuss specific needs and timeline
```

---

### 5. Common Workflows

**URI**: `workflows://common/patterns`  
**MIME Type**: `text/markdown`  
**Description**: Common real estate data workflows and use cases

#### Content Overview

Step-by-step workflows for common real estate scenarios, combining multiple tools for comprehensive analysis.

#### Key Sections

##### Buyer Workflows
- **First-Time Home Buyer Journey**: Complete process from pre-qualification to closing
- **Investment Property Search**: Systematic approach to finding rental properties

##### Seller Workflows  
- **Property Preparation for Sale**: Market analysis and pricing strategy
- **Pricing Strategy Development**: Comparative market analysis workflow

##### Professional Workflows
- **Agent Market Preparation**: Client consultation preparation
- **Market Research Workflows**: Regular market monitoring and reporting

##### Investor Workflows
- **Portfolio Analysis**: Multi-market comparison and selection
- **Risk Assessment**: Market diversification and timing strategies

##### Integration Patterns
- **Automated Monitoring**: Setting up regular data collection
- **Data Integration**: Connecting with external systems
- **Workflow Automation**: Streamlining repetitive tasks

#### Example Content Structure

```markdown
# Common Real Estate Workflows

## Buyer Workflows
### First-Time Home Buyer Journey
1. **Pre-Qualification**
   - Get pre-approved for mortgage
   - Understand budget requirements

2. **Market Research**
   - Use `search_properties` to explore available homes
   - Research neighborhoods and school districts

3. **Property Evaluation**
   - Use `get_property_details` for comprehensive information
   - Research comparable sales

## API Integration Patterns
### Automated Monitoring
- Set up regular market analysis for target areas
- Monitor specific property criteria with alerts
```

---

### 6. API Status & Info

**URI**: `api://status/info`  
**MIME Type**: `text/markdown`  
**Description**: Current API connection status and system information

#### Content Overview

Real-time system status information, configuration details, and health monitoring data.

#### Key Sections

##### Authentication Status
- OAuth2 connection status
- Bridge API connectivity
- MLS ID configuration validation

##### Available Tools
- Tool availability and readiness status
- Feature limitations or issues
- Performance metrics

##### Available Resources
- Resource availability status
- Content freshness and updates
- Access statistics

##### System Configuration
- Logging levels and output
- Rate limiting settings
- Cache configuration
- Performance tuning parameters

##### Data Sources
- Primary API endpoints
- Data coverage and freshness
- Update frequencies
- Compliance standards

##### Support Information
- Server version and framework details
- Transport configuration
- Error handling capabilities
- Performance benchmarks

#### Dynamic Content Generation

This resource generates real-time status information:

```python
async def _get_api_status_info(self) -> str:
    """Get current API status and system information."""
    try:
        # Test authentication
        auth_status = "✅ Connected" if self.settings.bridge_server_token else "❌ Failed"
        
        # Generate status report with current data
        status_content = f"""# API Status & System Information
        
## Authentication Status
- **OAuth2 Connection**: {auth_status}
- **Bridge API**: {self.settings.bridge_api_base_url}
- **MLS ID**: {self.settings.bridge_mls_id}

## Available Tools
- **search_properties**: ✅ Ready
- **get_property_details**: ✅ Ready
- **analyze_market**: ✅ Ready
- **find_agent**: ✅ Ready

## System Configuration
- **Log Level**: {self.settings.log_level}
- **Rate Limiting**: {self.settings.api_rate_limit_per_minute} requests/minute
- **Cache Enabled**: {'Yes' if self.settings.cache_enabled else 'No'}

## Usage Statistics
- **Server Status**: Running and accepting requests
- **Last Health Check**: {self._get_current_timestamp()}
"""
```

---

### 7. Guided Property Search

**URI**: `prompts://guided/search`  
**MIME Type**: `text/markdown`  
**Description**: Step-by-step guided property search workflows

#### Content Overview

Comprehensive step-by-step guides for different property search scenarios, from basic searches to complex investment analysis.

#### Key Sections

##### Quick Start Property Search
- **Step 1**: Define search criteria (natural language vs structured)
- **Step 2**: Review initial results and adjust
- **Step 3**: Get detailed information for properties of interest

##### Guided Search Scenarios
- **First-Time Home Buyer**: Affordable starter homes workflow
- **Investment Property Search**: Rental property analysis process
- **Luxury Home Search**: High-end property search strategy

##### Advanced Search Techniques
- **Comparative Shopping**: Multi-area comparison strategies
- **Search Optimization Tips**: Effective query construction
- **Market Timing**: Using search data for timing decisions

##### Troubleshooting Common Issues
- **No Results Found**: Broadening search criteria
- **Too Many Results**: Narrowing focus techniques
- **Outdated Information**: Data freshness validation

#### Example Content Structure

```markdown
# Guided Property Search Workflows

## Quick Start Property Search
### Step 1: Define Your Search Criteria
**Choose your approach:**

#### For Natural Language Search:
```
Use search_properties with a natural language query:
- "3 bedroom house under $500k in Austin TX"
```

#### For Structured Search:
```
Use search_properties with specific filters:
{
  "filters": {
    "city": "Austin",
    "state": "TX", 
    "min_bedrooms": 3,
    "max_price": 500000
  }
}
```

## Guided Search Scenarios
### Scenario 1: First-Time Home Buyer
**Goal**: Find affordable starter homes

**Step 1**: Start broad
```
Query: "houses under $300k with 2+ bedrooms"
```
```

---

### 8. Guided Market Analysis

**URI**: `prompts://guided/analysis`  
**MIME Type**: `text/markdown`  
**Description**: Step-by-step guided market analysis workflows

#### Content Overview

Detailed workflows for conducting comprehensive market analysis using the `analyze_market` tool, with specific guidance for different user types and scenarios.

#### Key Sections

##### Quick Start Market Analysis
- **Step 1**: Choose analysis scope (city-wide vs ZIP code)
- **Step 2**: Interpret results and metrics
- **Step 3**: Compare multiple areas for context

##### Guided Analysis Scenarios
- **Home Buyer Market Research**: Understanding market conditions for purchase timing
- **Seller Market Timing**: Optimal listing strategy development
- **Investment Market Selection**: Multi-market comparison for investment decisions

##### Advanced Analysis Techniques
- **Seasonal Trend Analysis**: Comparing different time periods
- **Micro-Market Analysis**: Neighborhood-level insights
- **Market Cycle Analysis**: Understanding market phases

##### Market Analysis Interpretation Guide
- **Price Trend Analysis**: Rising, stable, declining indicators
- **Inventory Level Analysis**: Market balance indicators
- **Actionable Insights**: Strategy recommendations by market type

##### Analysis Validation
- **Cross-Reference Data**: Verification techniques
- **Update Frequency**: When to refresh analysis
- **Quality Checks**: Ensuring reliable insights

#### Example Content Structure

```markdown
# Guided Market Analysis Workflows

## Quick Start Market Analysis
### Step 1: Choose Your Analysis Scope
**Define your target area:**

#### City-Wide Analysis:
```
Use analyze_market with city and state:
{
  "city": "Austin",
  "state": "TX",
  "property_type": "residential",
  "days_back": 90
}
```

## Guided Analysis Scenarios
### Scenario 1: Home Buyer Market Research
**Goal**: Understand if it's a good time to buy

**Step 1**: Analyze your target area
```
{
  "city": "Your Target City",
  "state": "State",
  "property_type": "residential",
  "days_back": 90
}
```

**Questions to answer:**
- Are prices rising or stable?
- How much inventory is available?
- What's the average time on market?
```

## Resource Access Patterns

### Resource Caching

Resources are dynamically generated but can be cached for performance:
- **Static Content**: Guides and references cached for 1 hour
- **Dynamic Content**: Status information regenerated on each request
- **User-Specific**: No user-specific caching implemented

### Resource Updates

Content is updated based on:
- **System Changes**: Configuration and status updates
- **Feature Updates**: New tool capabilities and options
- **Best Practices**: Workflow improvements and optimizations
- **User Feedback**: Common questions and issues

### Performance Optimization

- **Lazy Loading**: Resources generated only when requested
- **Content Compression**: Markdown optimized for size
- **Structured Format**: Consistent formatting for readability
- **Error Handling**: Graceful degradation for resource failures

## Integration with Tools

### Cross-Reference Links

Resources provide context for tool usage:
- Search examples link to `search_properties` tool
- Market guides link to `analyze_market` tool
- Agent guides link to `find_agent` tool
- Workflows combine multiple tools systematically

### Learning Progression

Resources are organized to support progressive learning:
1. **Basic Examples**: Simple tool usage patterns
2. **Reference Guides**: Comprehensive option coverage
3. **Workflows**: Complex multi-tool processes
4. **Advanced Techniques**: Optimization and troubleshooting

### Contextual Help

Resources provide context-sensitive assistance:
- Tool-specific guidance when using each tool
- Scenario-based workflows for common tasks
- Troubleshooting for specific error conditions
- Best practices for different user types

This comprehensive resource system provides users with all the guidance and information needed to effectively use the UNLOCK MLS MCP Server for their real estate data needs.