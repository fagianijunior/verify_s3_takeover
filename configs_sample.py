def accounts():
    accounts = [
        {
            "Aws": {
                "AccountName": '<ACCOUNT_NAME>'
            },
            "CloudFlare": {
                "inUse": True,
                "ZoneId": '<CLOUDFLARE_ZONE_ID>'
            }
        }, {
            "Aws": {
                "AccountName": '<ACCOUNT_NAME>'
            }
        }
    ]
    return accounts

def cloudflare():
    return {"token": '<CLOUDFLARE_API_TOKEN>'}