# image_classifier
Webapp developed using Django which classifies images on upload. Uses DeepDetect. Stored in Docker containers.

Welcome to James W.J Ralph's image classification app README.

To begin the app:

###1. Open a terminal and change directory to 'umbo_app'
###2. Run the following commands, sequentially:

docker-compose build

docker-compose run

(If upon running the second command, the output doesn't finish with:
'Starting development server at http://0.0.0.0:8000/
Quit the server with CONTROL-C.',
then just enter ctrl+c into the terminal and re-run 'docker-compose run'.)

###5. Activate the DeepDetect service by running the following in another terminal:

curl -X PUT "http://localhost:8080/services/imageserv" -d "{\"mllib\":\"caffe\",\"description\":\"image classification service\",\"type\":\"supervised\",\"parameters\":{\"input\":{\"connector\":\"image\"},\"mllib\":{\"nclasses\":1000}},\"model\":{\"repository\":\"/opt/models/ggnet/\"}}"

###6. Finally, please run the following commands to initiate the storage of data entered into the app.

docker exec -it umbo_app_web_1 bash

python manage.py migrate


###7.(Optional) Run --> 'sudo chown -R $USER:$USER .'  <-- to give yourself access to the postgresql data and media files stored by the app.


###The setup is now complete. To use the app, access the url http//:localhost/classify/list/ . From there, further instructions for use are provided. Enjoy!


----Overview----
----------------

The app runs with three different docker containers. The web container, based on a python image, the Postgressql container which saves the data of the python models used in the app, and finally the deepdetect container which contains the image classifier.

When an image is uploaded to the app, the Django view 'list' passes a command from the web container to the deepdetect container. It does this by running a series of commands through the Unix socket which the web container is connected to. These commands are saved in the files 'predict.sh', 'execcreate.sh' and 'execstart.sh'. the 'list view alters each of these files each time an image is uploaded to send the correct commands to the deepdetect container. The two containers share the directory they're stored in as a volume and so the deepdetect container is able to access the images stored by the app.

The output of the deepdetect service is then stored and trimmed in the view to produce a useable output for the app.

Ways to improve
---------------

The next thing to add to the app would be an image viewer, so that the picture can be viewed along with the results of the classification.

A flaw in the design of the app is that the container ID of the deepdetect container is required to send the commands via the Unix socket. This creates a slight issue when it comes to the scalability of the app and running multiple containers with the deepdetect server in.

Another flaw is that there is no mechanism in place for the deletion of previous uploads after a certain amount of time which, if the usage was large, creates a backlog of unnecessary memory usage.




