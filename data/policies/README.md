# Insurance Policy Documents

This folder contains insurance policy documents for analysis and rule extraction.

## Document Types

### Policy Document Structure
- **Coverage Rules**: What procedures/services are covered
- **Exclusions**: What is explicitly not covered  
- **Prior Authorization Requirements**: Procedures requiring pre-approval
- **Documentation Requirements**: Required supporting materials
- **Cost-sharing**: Deductibles, copays, coinsurance information

### Sample Policy Sections
```text
Section 4.2 - Diagnostic Imaging
- CT scans require prior authorization for non-emergency cases
- MRI limited to 2 per calendar year unless medically necessary
- Ultrasounds covered at 100% for preventive care

Section 6.1 - Laboratory Services  
- Routine blood work covered at 100%
- Genetic testing requires pre-authorization
- Panel tests limited to once per 12 months
```

## Files
- `blue_cross_policy.pdf` - Sample Blue Cross policy document
- `aetna_policy.pdf` - Sample Aetna policy document  
- `auto_insurance_policy.pdf` - Auto insurance policy sample
- `homeowners_policy.pdf` - Property insurance policy sample
- `policy_excerpts.json` - Structured policy rule extracts

## Snowflake AI Extract Integration
- PDF documents processed through Snowflake AI Extract
- Extracted text stored as structured data in Snowflake tables
- Policy rules parsed using Cortex Complete and indexed with Cortex Search
- Vector embeddings generated for semantic policy matching
