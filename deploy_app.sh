

export PROJECT_ID=
export APP_NAME=
export PATH_TO_PRIVATE_KEY=

gcloud config set project ${PROJECT_ID}

gcloud config set run/region REGION

gcloud builds submit --tag gcr.io/${PROJECT_ID}/${APP_NAME}  --project=${PROJECT_ID}
gcloud run deploy --image gcr.io/${PROJECT_ID}/${APP_NAME} --platform managed  --project=${PROJECT_ID} --allow-unauthenticated
