# Run this project
1) Install all dependencies:
    > pip install -r requirements.txt
   - I encourage you install all dependencies in virtual environments.
2) Run server:
    - First, you need set two variable environments, in linux os, type:
    > export FLASK_APP=autoapp.py

    > export FLASK_ENV=development
   
   - Then, make sure you have MongoDB running at *mongodb://localhost:27017* or you must config at DevConfig class at url-tracking/core/settings.py

   - Next, run app:
   > flask run
3) Run consumer:
   - Make sure, you have kafka server running on *localhost:9092*
   > python3 run_consumer.py