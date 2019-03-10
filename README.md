# twitter

To run the application:
python3 launcher.py

Change the username and password for each request. 
Create a new user:
curl --header "Content-Type: application/json" --request POST   --data '{"username":"xyz", "password":"123", "display_name":"abc"}'   http://localhost:5000/users/register

Update password:
curl --header "Content-Type: application/json" --request POST  --user xyz:121233 --data '{"username":"xyz", "password":"123"}'   http://localhost:5000/users/update

Delete a user:
curl --header "Content-Type: application/json" --request POST  --user xyz:121233 --data '{"username":"xyz"}'   http://localhost:5000/users/delete_user

To tun the test:
py.test test.tavern.yaml