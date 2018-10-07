# mobile-inventory
Mobile lab device inventory tracker


## APIs

### GET /api/users
```
curl -X GET \
  http://localhost:8080/api/users \
  -H 'content-type: application/json' \
  -H 'x-api-key: secret_api_key'
```

### GET /api/devices
```
curl -X GET \
  http://localhost:8080/api/devices \
  -H 'content-type: application/json' \
  -H 'x-api-key: secret_api_key'
```

### GET /api/devices/info
```
curl -X GET \
  http://localhost:8080/api/devices/info \
  -H 'content-type: application/json' \
  -H 'x-api-device-id: D123456789' \
  -H 'x-api-key: secret_api_key'
```

### POST /api/devices/register
```
curl -X POST \
  http://localhost:8080/api/devices/register \
  -H 'content-type: application/json' \
  -H 'x-api-device-id: D123456789' \
  -H 'x-api-key: secret_api_key' \
  -d '{
	"inventory_id": "MOB.001",
	"manufacturer": "Samsung",
	"model": "Galaxy 9",
	"os": "Android"
}'
```

### POST /api/devices/alocate 
```
curl -X POST \
  http://localhost:8080/api/devices/alocate \
  -H 'content-type: application/json' \
  -H 'x-api-device-id: D123456789' \
  -H 'x-api-key: secret_api_key' \
  -H 'x-api-user-id: john.doe@somecompany.com'
```
### POST /api/devices/free
```
curl -X POST \
  http://localhost:8080/api/devices/free \
  -H 'content-type: application/json' \
  -H 'x-api-device-id: D123456789' \
  -H 'x-api-key: secret_api_key' \
  -H 'x-api-user-id: john.doe@somecompany.com'
```