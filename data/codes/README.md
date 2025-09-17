# Procedure Code Database

This folder contains standardized procedure and diagnosis codes used in insurance claims.

## Code Types

### Healthcare Codes
- **CPT (Current Procedural Terminology)**: Medical procedures and services
- **ICD-10**: Diagnosis codes
- **HCPCS**: Healthcare Common Procedure Coding System
- **NDC**: National Drug Codes

### Auto Insurance Codes  
- **Mitchell**: Auto repair procedure codes
- **Labor Operations**: Standard repair labor codes
- **Parts Codes**: OEM and aftermarket parts identification

### Sample Code Structure
```json
{
  "code": "99213",
  "code_type": "CPT",
  "description": "Office/outpatient visit, established patient, 20-29 minutes",
  "category": "Evaluation and Management",
  "typical_cost_range": [150, 300],
  "requirements": [
    "Established patient relationship",
    "Face-to-face encounter",
    "Medical decision making of low complexity"
  ],
  "common_denials": [
    "Insufficient documentation",
    "Frequency limitations exceeded",
    "Not medically necessary"
  ]
}
```

## Files
- `cpt_codes.json` - CPT procedure codes with descriptions
- `icd10_codes.json` - ICD-10 diagnosis codes
- `auto_repair_codes.json` - Auto insurance repair codes  
- `code_mappings.json` - Insurance-specific code mappings
- `denial_patterns.json` - Common denial reasons by code

## Fuzzy Matching Support
- Alternative code descriptions for matching
- Synonym mapping for procedure descriptions
- Insurance-specific code variations
