package:
	rm -f s2fq.zip
	zip s2fq.zip stream2fifo.js

deploy:
	aws s3 cp s2fq.zip s3://$(DEPLOY_BUCKET)
