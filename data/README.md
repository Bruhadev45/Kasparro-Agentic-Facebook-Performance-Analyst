# Data Directory

## Dataset

### Full Dataset
- **File**: `synthetic_fb_ads_undergarments.csv`
- **Size**: ~4,500 rows
- **Date Range**: January 2025
- **Columns**:
  - `campaign_name`: Campaign identifier
  - `adset_name`: Adset identifier
  - `date`: Date of metrics
  - `spend`: Ad spend ($)
  - `impressions`: Number of impressions
  - `clicks`: Number of clicks
  - `ctr`: Click-through rate
  - `purchases`: Number of purchases
  - `revenue`: Revenue generated ($)
  - `roas`: Return on ad spend
  - `creative_type`: Image, Video, Carousel, UGC
  - `creative_message`: Ad copy text
  - `audience_type`: Broad, Lookalike, Retargeting
  - `platform`: Facebook, Instagram
  - `country`: US, UK, IN

### Sample Dataset
To create a sample for faster testing:

```bash
head -100 synthetic_fb_ads_undergarments.csv > sample_fb_ads.csv
```

Then set in `config/config.yaml`:
```yaml
data:
  use_sample_data: true
```

## Data Quality Notes
- Some rows may have missing `spend` values
- Purchases can be 0 for awareness campaigns
- ROAS calculated as revenue/spend
