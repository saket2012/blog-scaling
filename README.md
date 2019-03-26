# Blog

1) Install the dependencies by using following command
pip3 install -r requirements.txt

2) To install foreman type following command
On MacOS:
npm install foreman
On Ubuntu:
sudo apt install --yes ruby-foreman

3) Start the application by typing following commands
On MacOS:
nf start
On Ubuntu:
foreman start

4)Use the curl commands given in curl_commands.txt

5)To run the tests, type following commands
For users and articles:
py.test test_user.tavern.yaml -v
For tags:
py.test test_tag.tavern.yaml -v
For comments:
py.test test_comments.tavern.yaml -v
