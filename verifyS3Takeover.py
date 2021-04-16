# Author: fagianijunior <fagianijunior@gmail.com>
# References: https://gupta-bless.medium.com/exploiting-subdomain-takeover-on-s3-6115730d01d7
# References: 

import sys
import boto3
import re
import cloudflare

accounts = ['tink']
if accounts.count <= 0:
    "Add some account name in account array"
else:
    for account in accounts:
        sys.stdout.write("\033[1;36m")
        print('|----------------------------------------------------|')
        print('| CHECKING ACCOUNT: ' + account)
        print('|----------------------------------------------------|')
        sys.stdout.write("\033[0;0m")

        # define o perfil
        session = boto3.Session(profile_name=account)

        route53 = session.client('route53')
        hostedZones = route53.list_hosted_zones()
        s3WebsiteRegex = '(.s3-website-)(us|af|ap|ca|eu|me|sa)(-)(east|west|south|northeast|southeast|central|north)(-[1-3])(.amazonaws.com)?(.)'

        s3 = session.client('s3')
        s3Buckets = s3.list_buckets()

        buckets = []
        for bucket in s3Buckets['Buckets']:
            buckets.append(bucket['Name'])

        for hostedZone in hostedZones['HostedZones']:
            print('verificando: ' + hostedZone['Name'])
            records = route53.list_resource_record_sets(
                HostedZoneId=hostedZone['Id']
            )
            for record in records['ResourceRecordSets']:
                if record['Type'] in ['CNAME']:
                    if re.search(s3WebsiteRegex, record['ResourceRecords'][0]['Value']):
                        print(record['Name'] + ": " + record['ResourceRecords'][0]['Value'])
                        
                        recordValue = re.sub(s3WebsiteRegex, '', record['ResourceRecords'][0]['Value'])
                        if recordValue in buckets:
                            sys.stdout.write("\033[0;32m")
                            print('OK ' + recordValue)
                        else:
                            sys.stdout.write("\033[1;31m")
                            print('WARNING ' + recordValue)
        sys.stdout.write("\033[0;0m")