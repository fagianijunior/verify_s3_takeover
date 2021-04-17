# Author: fagianijunior <fagianijunior@gmail.com>
# References: https://gupta-bless.medium.com/exploiting-subdomain-takeover-on-s3-6115730d01d7

import sys
import boto3
import re
import CloudFlare

def main():
    accounts = ['tink']

    if not accounts:
        print("Add some account name in account array\nExiting...")
        return 0

    for account in accounts:
        accountBanner(account)
        verify(account)

def listBuckets(session):
    s3        = session.client('s3')
    s3Buckets = s3.list_buckets()
    buckets   = []
    
    for bucket in s3Buckets['Buckets']:
        buckets.append(bucket['Name'])

    return buckets

def listHostedZones(session):
    route53 = session.client('route53')

    hostedZones = route53.list_hosted_zones()

    return hostedZones

def listRecords(session, hostedZone):
    route53 = session.client('route53')
    records = route53.list_resource_record_sets(
            HostedZoneId=hostedZone['Id']
        )
    return records

def verifyRecord(record):
    s3WebsiteRegex  = '(.s3-website-)(us|af|ap|ca|eu|me|sa)(-)(east|west|south|northeast|southeast|central|north)(-[1-3])(.amazonaws.com)?(.)'

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


def accountBanner(account):
    sys.stdout.write("\033[1;36m")
    print('|----------------------------------------------------|')
    print('| CHECKING ACCOUNT: ' + account)
    print('|----------------------------------------------------|')
    sys.stdout.write("\033[0;0m")


def verify(account):
    # define o perfil
    session         = boto3.Session(profile_name=account)
    buckets         = listBuckets(session)
    hostedZones     = listHostedZones(session)

    for hostedZone in hostedZones['HostedZones']:
        print('verificando: ' + hostedZone['Name'])
        records = listRecords(session, hostedZone)
        for record in records['ResourceRecordSets']:
            verifyRecord(record)
    sys.stdout.write("\033[0;0m")


if __name__ == '__main__':
    main()