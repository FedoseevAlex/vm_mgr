## vm_mgr - Virtual machine manager
This software was written to get along with openstack API.

### Overview
This tool allow you to create and show virtual machine instances.
Also there is a possibility to get information about devstack flavors and images.

### Installation and running
1. Clone the repo  
`https://github.com/FedoseevAlex/vm_mgr.git` 

2. Install package
`pip install --user ./vm_mgr`  

3. Set the environment variables for authentication  
   `AUTH_NAME` - name to authenticate to devstack  
   `AUTH_PASSWORD`- password for devstack authentication  
   `SERVER_IP`- IPv4 address of devstack  
   `FLASK_APP` - Set to `vm_mgr`  
   
4. Run with   
`flask run -h 0.0.0.0`  

### Request examples
  
#### Create virtual machine instance 
```
curl --request POST \
  --url http://<server_ip>:5000/vmmgr/servers \
  --header 'content-type: application/json' \
  --data '{"flavor": "m1.micro",
 "name": "MicroVM"}'
```
**Response example:**
```
{
  "server": {
    "OS-DCF:diskConfig": "MANUAL",
    "adminPass": "dRmhc4B88Ls8",
    "id": "f016783d-aa01-40ba-af3c-fe1a307fd3cb",
    "links": [
      {
        "href": "http://<server_ip>/compute/v2.1/servers/f016783d-aa01-40ba-af3c-fe1a307fd3cb",
        "rel": "self"
      },
      {
        "href": "http://<server_ip>/compute/servers/f016783d-aa01-40ba-af3c-fe1a307fd3cb",
        "rel": "bookmark"
      }
    ],
    "security_groups": [
      {
        "name": "default"
      }
    ]
  }
}
```
 
#### Get available flavors 
```
curl --request GET --url http://<server_ip>:5000/vmmgr/flavors
```

**Response example:**
```

  "flavors": [
    {
      "id": "1",
      "name": "m1.tiny",
      "links": [
        {
          "rel": "self",
          "href": "http://<server_ip>/compute/v2.1/flavors/1"
        },
        {
          "rel": "bookmark",
          "href": "http://<server_ip>/compute/flavors/1"
        }
      ]
    },
    {
      "id": "2",
      "name": "m1.small",
      "links": [
        {
          "rel": "self",
          "href": "http://<server_ip>/compute/v2.1/flavors/2"
        },
        {
          "rel": "bookmark",
          "href": "http://<server_ip>/compute/flavors/2"
        }
      ]
    },
    {
      "id": "42",
      "name": "m1.nano",
      "links": [
        {
          "rel": "self",
          "href": "http://<server_ip>/compute/v2.1/flavors/42"
        },
        {
          "rel": "bookmark",
          "href": "http://<server_ip>/compute/flavors/42"
        }
      ]
    }
  ]
}
```
  
  
#### Get all currently running virtual machines
```
curl --request GET --url http://<server_ip>:5000/vmmgr/servers
```
**Response example:**
```
{
  "servers": [
    {
      "ip_addresses": [
        "192.168.233.82"
      ],
      "name": "MicroVM"
    }
  ]
}
```

#### Getting available images
```
curl --request GET --url http://<server_ip>:5000/vmmgr/images
```
**Response example:**
```
7d3d733d-2b2d-4a8f-a7f6-d607710c9656
```
