def metrics_doc(content_id, campaign_id, creator_id, company_id, site_id, metrics, content_info, timestamp, updated_at):
    return {
        "content_id": str(content_id),
        "campaign_id": str(campaign_id),
        "creator_id": str(creator_id),
        "company_id": str(company_id),
        "site_id": str(site_id),
        "metrics": metrics,
        "content_info": content_info,
        "timestamp": timestamp,
        "updated_at": updated_at,
    }
