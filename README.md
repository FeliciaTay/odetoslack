# odetoslack 
This is a Slack application which will be deployed through Zappa. Zappa is a Python package that bundles up the web application written in Flask and deploys to AWS Lambda. The backend database can be hosted on AWS RDS, using MySQL database.

## Setting up
The below instructions include the setting up of AWS Lambda and AWS RDS. If an AWS group has already been set up, Step 5 can be omitted.
Note: Only Python 3.6, 3.7 or 3.8 is supported.

Instructions:
1. Clone this repository. 

2. Using command prompt, navigate to the repository folder.

3. Activate virtual environment using: <br/>
    ```
    python -m venv venv
    venv\Scripts\activate
    ```
4. Run the below commands to install the necessary libraries:
    ```
   pip install Flask==1.1.2
   pip install zappa
   pip install slack_sdk
   pip install PyMySQL
   ```

5. Log into your AWS account. AWS Access Keys have to be created first. The below steps are referenced from [this link](https://docs.aws.amazon.com/IAM/latest/UserGuide/getting-started_create-admin-group.html). <br/>
    a. Type 'IAM' into the search box and at the left panel, select 'User groups' under 'Access Management'.<br/><br/>
    b. Create a new group and give it a name. <br/><br/>
    c. Under the 'Attach permissions policies' section, search for 'AdministratorAccess' and check the box. At the review screen, check the details and click 'Create Group'.<br/><br/>
    d. Head to 'Users' on the left panel and click on 'Add user'. <br/><br/>
    e. Give your new user a name and select the access type to be 'Programmatic access'. <br/><br/>
    f. Continuing on, add this user to the group just created. <br/><br/>
    g. Tags are optional. Moving on, review the details and click on 'Create user'. <br/><br/>
    h. Upon seeing the green Success screen, copy the access key id and secret access key to *~/.aws/credentials* (need to create a new folder and a new file). The secret access key will not be shown again. Take caution that the *.aws/* directory needs to be in the home directory and the *credentials* file do not have any extensions. <br/>
    DO NOT save the directory under version control. <br/>
    In the *credentials* file, copy and paste the text below and modify the XXXXXXXX portions accordingly.<br/>
    ```
    [default]
    aws_access_key_id = XXXXXXXX
    aws_secret_access_key = XXXXXXXX
   ```  
   
6. Create a new file *app.py* in the repository directory. Paste the following code within:
    ```
   from flask import Flask
   app = Flask(__name__)
   
   @app.route('/')
   def hello_world():
    return '<h1>Yeah, that is Zappa! Zappa! Zap! Zap!</h1>'
   
   # We only need this for local development.
   if __name__ == '__main__':
    app.run()
   ```
   The above is an example of a simple Flask application.

7. Next, on the command prompt, run ```zappa init``` in the repository directory. Follow through the configuration process to finish setting up the Zappa project. The below is an example of what could be set:
    ```
   environment: dev
   bucket: zappabucket346
   app's function: app.app
   whether to deploy the application globally: n
   ``` 
   For the app's function, it must end with ```.app```.

8. A *zappa_settings.json* file has been created. Check that```"profile name:"``` is set to ```"default"```, which corresponds to the name defined in the square brackets specified in *.aws/credentials*. <br/>
    Add the following line of code within as well:
    ```
   "aws_region": "ap-southeast-1"
   ```
   The above can differ according to the region you are in.

9. Run the following line of code in command prompt:
    ```
   pip freeze > requirements.txt
   ```

10. Next, run the following command:
    ```
    zappa deploy dev
    ```
    You should see a success message with a URL stated. Take note of this URL. <br/><br/>
    From this point onwards, when changes are made to the *app.py* file, ```zappa update dev``` needs to be run to update the changes. <br/><br/> 
    Note: For the above, ```dev``` is to be replaced with what you named your environment in Step 6.

11. Now, head back to the AWS console and search for 'AWS RDS' in the search box. Click on 'Create database' and follow through the configurations to set up a database. <br/>
    The compulsory settings are: 
    - Engine type: MySQL
    - Enable public access under 'Connectivity'
    
    You will need to take note of the 'Master username' and your 'Master password'.

12. After the creation of the database, click into it and under 'Connectivity & security', note down the endpoint URL.
    
13. Connect to the database using any tool that allows MYSQL access, like MySQL workbench. The host will be the URL obtained from Step 12. <br/>
    Run the code found in *example.txt* in the repository folder.

14. Open up *code.py* in the repository document.





# Acknowledgements
Credits to:
https://pythonforundergradengineers.com/deploy-serverless-web-app-aws-lambda-zappa.html
