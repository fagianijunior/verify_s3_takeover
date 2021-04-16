# Verify Exploiting Subdomain Takeover on S3

Vulnerability references: `https://gupta-bless.medium.com/exploiting-subdomain-takeover-on-s3-6115730d01d7` 



## What this script does ###

Checks domains on route53 and cloudflare that point to a bucket that does not exist anymore.

### Usage

- Install the dependencies

    ```$ pip3 install -r requirements.txt```

- This script uses your credentials in ~ /.aws/credentials

    Reference: `https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-files.html`

- Edit the script and add to the array (accounts = []), which profiles you want to check for vulnerability

- Those who return WARNING, manual check in S3 if the bucket exists, if it does not exist anymore, remove the dns registration

### TO DO

- Use cloudflare API

- Refactor the code

- Create functions

- Learn more about python :)
