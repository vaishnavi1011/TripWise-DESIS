# TripWise-DESIS



## Installation Guide

Pre-requisites - 

1. Python installed
2. Node installed

Steps 

1. Open 2 terminals

2. Clone the repository at desired location.

git clone https://github.com/ashiya2701/TripWise-DESIS.git

3. Navigate to frontend folder

cd frontend/tripwise

3. Install dependencies

npm i

3.  Inside node_modules>semantic-ui-css folder>semantic.min.css file , ctrl + f and search for ;; and remove 1 semicolon.

4. Run React App

npm start

5. Open another terminal

6. Navigate to backend folder

cd Backend/api

7. Run Flask App

python3 main.py

8. To populate data run these three endpoints

localhost:5000/sample_check_data
localhost:5000/populate_HotelData
localhost:5000/populate_placeData

