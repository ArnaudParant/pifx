PROJECT_NAME := pifx-api
LOCAL_IMAGE_NAME := $(PROJECT_NAME):latest

all: docker lint

docker:
	git rev-parse HEAD > COMMIT_INFO
	date >> COMMIT_INFO
	echo $(USER) >> COMMIT_INFO
	docker build -t $(LOCAL_IMAGE_NAME) .

lint:
	./run_pylint.sh $(LOCAL_IMAGE_NAME)

run:
	docker run -it -p 9100:9100 --network=host $(LOCAL_IMAGE_NAME)

clean:
	rm -f *.pyc */*.pyc */*/*.pyc
