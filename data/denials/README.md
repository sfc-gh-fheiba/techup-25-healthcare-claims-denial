# Denial History and Documents

This folder contains insurance claim denial notices and historical appeal data.

## Denial Document Types

### Denial Notice Structure
- **Claim Information**: Original claim details being denied
- **Denial Reasons**: Specific reasons for denial with policy references
- **Appeal Instructions**: How to appeal the decision
- **Deadline Information**: Time limits for appeals
- **Required Documentation**: Additional materials needed for appeal

### Sample Denial Notice
```json
{
  "denial_id": "DEN-2024-567890",
  "original_claim_id": "CLM-2024-001234",
  "denial_date": "2024-01-25",
  "insurer": "Blue Cross Blue Shield",
  "denial_reasons": [
    {
      "code": "D1",
      "description": "Prior authorization required",
      "policy_reference": "Section 4.2.1",
      "procedure_code": "72148"
    },
    {
      "code": "D5", 
      "description": "Insufficient documentation",
      "policy_reference": "Section 2.3.4",
      "required_docs": ["Physician notes", "Medical necessity statement"]
    }
  ],
  "appeal_deadline": "2024-02-25",
  "total_denied_amount": 1250.00
}
```

## Files
- `denial_notices.pdf` - Sample PDF denial notices
- `denial_letters.json` - Structured denial data
- `appeal_history.json` - Historical appeal outcomes
- `denial_patterns.json` - Analysis of common denial patterns
- `successful_appeals.json` - Examples of successful appeal arguments

## Snowflake AI Extract Processing
- PDF denial notices processed automatically using Snowflake AI Extract
- Text extraction and structure parsing with native Snowflake capabilities
- Denial reason classification using Snowflake Cortex Complete
- Policy reference extraction and linking through Cortex Search

## Analytics Support
- Denial rate tracking by procedure code
- Success rate analysis for different appeal strategies
- Pattern recognition for improving future claims
