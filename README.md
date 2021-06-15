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
   pip install PyMySL
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
6. Return to the repository directory and run ```zappa init```. Follow through the configuration process to finish setting up the Zappa project. The below is an example of what could be set:
    ```
   environment: dev
   bucket: zappabucket346
   app's function: app.app
   whether to deploy the application globally: no
   ``` 
   For the app's function, it must end with ```.app```.

7. A *zappa_settings.json* file has been created. Change ```"profile name:"``` to ```"default"``` to correspond to the name defined in the square brackets specified in *.aws/credentials*. <br/>
    Add the following line of code within as well:
    ```
   "aws_region": "ap-southeast-1"
   ```
   The above can differ according to the region you are in.

8. Run the following line of code in command prompt:
    ```
   pip freeze > requirements.txt
   ```

10.






# Acknowledgements
Credits to:
https://pythonforundergradengineers.com/deploy-serverless-web-app-aws-lambda-zappa.html
