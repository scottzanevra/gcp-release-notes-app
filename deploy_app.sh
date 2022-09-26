

export PROJECT_ID=dataplex-demo-342803
export APP_NAME=dataplex-demo-342803
export PATH_TO_PRIVATE_KEY="/Users/szanevra/Downloads/dataplex-demo-342803-e2b0cc499e2a.json"

gcloud config set project ${PROJECT_ID}

gcloud config set run/region REGION

gcloud builds submit --tag gcr.io/${PROJECT_ID}/${APP_NAME}  --project=${PROJECT_ID}
gcloud run deploy --image gcr.io/${PROJECT_ID}/${APP_NAME} --platform managed  --project=${PROJECT_ID} --allow-unauthenticated
