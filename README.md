# streamlit-dashboard
 In this repo, I will show how I created a dashboard webapplication only using python and the streamlit library, without know nothing about django or flask frameworks.
 
 ## Creating the database
 First you need to run the *cria_random_dataset.py* file. It will output a test database, and in my case it is the base_dataset2.csv.
 
 ## Running the streamlit web app in your local machine
First, you need to run the code above in your terminal: 
 <br>
 ```
 streamlit run VIT_BANK.py
 ```
 <br>
Wait a little bit. If everything is ok, your terminal will give you a message saying something like this:

> You can now view your Streamlit app in your browser. <br>
> 
>  Local URL: http://localhost:8501 <br>
>  Network URL: http://XXX.XXX.X.X:YYYY

Probably, your browser will open with the URL http://localhost:8501. But, opening it trought localhost will not apply the page theme that is set in the *.streamlit* directory, inside the *config.toml* file. To do this, copy the network URL that your terminal printed and paste in your browser. When the page open, you will se that it is necessary a password to see something. <br>
The password is **1234**. <br>
Hope you enjoy it!
