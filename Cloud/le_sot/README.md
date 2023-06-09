# Cloud / Le sot

## Challenge
Dans un coin reculé du café est assis Panurge, la mine sombre. Prenant pitié, vous vous donnez pour mission de lui remonter le moral.

« Que diable vous prend-il aujourd'hui ? Il me semblerait rencontrer le désepoir en personne.

— Mes moutons se sont échappés. L'un deux a pris la fuite, et les autres l'ont suivi.

— Comment ? Mais où donc sont-ils allés ?

— Ils sont partis dans les nuages... »

Allons, vous avez bon coeur n'est-ce pas ? Allez donc lui retrouver ses moutons.

## Inputs
- Endpoint S3 : https://s3.gra.io.cloud.ovh.net/
- Bucket : `cloud-intro-challenge`
- Attention, il s'agit d'une vrai infrastructure cloud, le brute-force est particulièrement proscrit


## Solution
We grab the `S3 bucket` content, which references a `JSON` file, which contains the flag:

```console
$ wget https://cloud-intro-challenge.s3.gra.io.cloud.ovh.net/
--2023-05-31 13:07:29--  https://cloud-intro-challenge.s3.gra.io.cloud.ovh.net/
Resolving cloud-intro-challenge.s3.gra.io.cloud.ovh.net (cloud-intro-challenge.s3.gra.io.cloud.ovh.net)... 141.95.161.76
Connecting to cloud-intro-challenge.s3.gra.io.cloud.ovh.net (cloud-intro-challenge.s3.gra.io.cloud.ovh.net)|141.95.161.76|:443... connected.
HTTP request sent, awaiting response... 200 OK
Length: 467 [application/xml]
Saving to: ‘index.html’

index.html                   100%[=============================================>]     467  --.-KB/s    in 0s

2023-05-31 13:07:29 (23.0 MB/s) - ‘index.html’ saved [467/467]


$ cat index.html
<?xml version='1.0' encoding='UTF-8'?>
<ListBucketResult xmlns="http://s3.amazonaws.com/doc/2006-03-01/"><Name>cloud-intro-challenge</Name><Prefix/><Marker/><MaxKeys>1000</MaxKeys><IsTruncated>false</IsTruncated><Contents><Key>les-moutons.json</Key><LastModified>2023-05-12T13:56:48.000Z</LastModified><ETag>"d642390a5d6f695d958015801e585cb1"</ETag><Size>1767</Size><Owner><ID/><DisplayName/></Owner><StorageClass>STANDARD</StorageClass></Contents></ListBucketResult>                                
$ wget https://cloud-intro-challenge.s3.gra.io.cloud.ovh.net/les-moutons.json
--2023-05-31 13:07:49--  https://cloud-intro-challenge.s3.gra.io.cloud.ovh.net/les-moutons.json
Resolving cloud-intro-challenge.s3.gra.io.cloud.ovh.net (cloud-intro-challenge.s3.gra.io.cloud.ovh.net)... 141.95.161.76
Connecting to cloud-intro-challenge.s3.gra.io.cloud.ovh.net (cloud-intro-challenge.s3.gra.io.cloud.ovh.net)|141.95.161.76|:443... connected.
HTTP request sent, awaiting response... 200 OK
Length: 1767 (1.7K) [application/json]
Saving to: ‘les-moutons.json’

les-moutons.json             100%[=============================================>]   1.73K  --.-KB/s    in 0s

2023-05-31 13:07:49 (23.6 MB/s) - ‘les-moutons.json’ saved [1767/1767]


$ cat les-moutons.json | jq
{
  "sheeps": [
    {
      "name": "Ivy",
      "canSwim": false,
      "canFly": false,
      "sex": "male",
      "treat": "follower"
    },
    {
      "name": "Sweetie",
      "canSwim": false,
      "canFly": false,
      "sex": "female",
      "treat": "follower"
    },
    (...)
    {
      "name": "Ruth",
      "canSwim": false,
      "canFly": false,
      "sex": "male",
      "treat": "follower"
    }
  ],
  "flag": "404CTF{D35_m0utOns_D4n5_13s_NU@g3s}"
}
```

## Flag
404CTF{D35_m0utOns_D4n5_13s_NU@g3s}
