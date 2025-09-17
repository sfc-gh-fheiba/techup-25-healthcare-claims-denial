# Claims Data

This folder contains insurance claim data for processing and analysis.

## Data Structure

### Sample Claim Format (JSON/XML)
```json
{
  "claim_id": "CLM-2024-001234",
  "patient_info": {
    "patient_id": "PAT-56789",
    "name": "John Doe",
    "dob": "1985-03-15",
    "insurance_id": "INS-ABC123"
  },
  "provider_info": {
    "provider_id": "PRV-12345",
    "name": "Metro General Hospital",
    "npi": "1234567890"
  },
  "claim_details": {
    "procedure_codes": ["99213", "85025", "36415"],
    "diagnosis_codes": ["Z00.00", "R53.83"],
    "service_date": "2024-01-15",
    "total_amount": 450.00,
    "description": "Office visit with lab work"
  },
  "insurance_info": {
    "primary_insurer": "Blue Cross Blue Shield",
    "policy_number": "BC123456789",
    "group_number": "GRP001"
  }
}
```

## Files
- `sample_claims.json` - Generated sample claims data
- `healthcare_claims.csv` - Structured healthcare claims
- `auto_claims.json` - Auto insurance claim samples
- `homeowners_claims.json` - Property insurance claim samples

## Generation Strategy
- Use AI to generate realistic claim scenarios
- Include various procedure types and complexity levels
- Cover different insurance providers and policy types
