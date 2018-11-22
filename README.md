# mobile-inventory
Keeping track of your mobile devices

## Setting up the Development Environment

This project is built to run on [Google App Engine](http://appengine.google.com/) Standard Environment.

1. Make sure you have [Python 2.7](https://www.python.org/downloads/) installed

2. Install the [Google App Engine SDK](https://cloud.google.com/appengine/downloads) for Python on your computer.

3. Install the gcloud Python extensions. You can check which componentes are installed with
```
gcloud components list
```

4. Clone this repository
```
git clone https://github.com/i2nes/mobile-inventory.git
```

5. Copy ```config_rename.py``` to ```config.py```. ```config.py``` is used for configurations and secret keys and is not tracked. Change the secrets to be your own.

6. Install needed packages from requirements.txt (make sure your in the same directory as requirements.txt)
```
pip install -r requirements.txt -t lib/
```

7. Startup the app in a development server
```
dev_appserver.py app.yaml
```

8. You should now be able to open the application in your web browser: [http://localhost:8080](http://localhost:8080)

## Deploying to Production

1. Go to your [App Engine Console](https://console.cloud.google.com/appengine) and create a project.

2. Deploy the app with gcloud
```
gcloud app deploy  --project [YOUR_PROJECT_ID] --version [VERSION]
```
- To specify a custom version ID, include the ```--version``` flag. Example: ```live``` for your live version. This can be omitted, but gcloud will create a new version for each deployment and you will end up having several instances running.
- To deploy your app without automatically routing all traffic to that version, include the ```--no-promote``` flag.
- To deploy your app to a specific GCP project, include the ```--project``` flag.

3. The index.yaml file has to be deployed explicitly
```
gcloud app deploy index.yaml --project [YOUR_PROJECT_ID] --version [VERSION]
```

## API Usage Examples

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
  -H 'x-api-device-id: MOB.001' \
  -H 'x-api-key: secret_api_key'
```

### POST /api/devices/register
```
curl -X POST \
  http://localhost:8080/api/devices/register \
  -H 'content-type: application/json' \
  -H 'x-api-device-id: MOB.001' \
  -H 'x-api-key: secret_api_key' \
  -d '{
	"manufacturer": "Samsung",
	"model": "Galaxy 9",
	"os": "Android - 9"
}'
```

### POST /api/devices/alocate 
```
curl -X POST \
  http://localhost:8080/api/devices/alocate \
  -H 'content-type: application/json' \
  -H 'x-api-device-id: MOB.001' \
  -H 'x-api-key: secret_api_key' \
  -H 'x-api-user-id: john.doe@somecompany.com' \
  -d '{
	"manufacturer": "Apple",
	"model": "iPhone 8",
	"os": "iOS - 12.2"
}'
```
### POST /api/devices/free
```
curl -X POST \
  http://localhost:8080/api/devices/free \
  -H 'content-type: application/json' \
  -H 'x-api-device-id: MOB.001' \
  -H 'x-api-key: secret_api_key' \
  -H 'x-api-user-id: john.doe@somecompany.com'
```