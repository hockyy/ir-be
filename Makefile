build-docker:
	docker build -t gcr.io/hocky-general/genshin:1.0 .

gcloud-submit:
	gcloud builds submit -t gcr.io/hocky-general/genshin:1.0

run-docker:
	docker run -d --publish 80:80 gcr.io/hocky-general/genshin:1.0