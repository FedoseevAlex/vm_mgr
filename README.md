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
 "name": "MicroVM", "network_name": "shared"}'
```
Request body could contain up to three parameters: name, flavor and network_name.
- name: string 
User can specify desirable instance name through this parameter. 
If this parameter is absent then random name will be generated.

- flavor: string
This parameter is to specify preset instance configuration.
Default is: m1.nano.

- network_name: string
Specify network to connect instance to.
Default: shared

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


#### Get available networks
```
curl --request GET \
  --url http://<server_ip>:5000/vmmgr/networks
```

**Response example:**
```
{
  "networks": [
    {
      "admin_state_up": true,
      "availability_zone_hints": [],
      "availability_zones": [
        "nova"
      ],
      "created_at": "2020-02-07T12:14:50Z",
      "description": "",
      "id": "dd25cd46-0cc3-4ff7-b420-53febca3128e",
      "ipv4_address_scope": null,
      "ipv6_address_scope": null,
      "mtu": 1450,
      "name": "shared",
      "port_security_enabled": true,
      "project_id": "620cf4fcfbcd4e7495a9664ab253efbd",
      "provider:network_type": "vxlan",
      "provider:physical_network": null,
      "provider:segmentation_id": 13,
      "revision_number": 2,
      "router:external": false,
      "shared": true,
      "status": "ACTIVE",
      "subnets": [
        "0e049711-5a92-49df-b5c2-d77d31438037"
      ],
      "tags": [],
      "tenant_id": "620cf4fcfbcd4e7495a9664ab253efbd",
      "updated_at": "2020-02-07T12:14:52Z"
    }
  ]
}
```
