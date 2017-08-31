package:
	rm -f fq2ddb.zip
	zip fq2ddb.zip fq2ddb.js

deploy:
	aws s3 cp fq2ddb.zip s3://$(DEPLOY_BUCKET)
