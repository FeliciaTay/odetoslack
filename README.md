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
   pip install Flask
   pip install zappa
   pip install slack_sdk
   pip install PyMySL
   ```

5. Log into your AWS account. AWS Access Keys have to be created first. The below steps are referenced from [this link](https://pythonforundergradengineers.com/deploy-serverless-web-app-aws-lambda-zappa.html) under the 'Create AWS Acess Keys' section. More information and pictures can be found at the link. <br/>
    a. Type 'IAM' into the search box and at the left panel, select 'User groups' under 'Access Management'.<br/><br/>
    b. Create a new group and give it a name. <br/><br/>
    c. In the 'Attach Policy' screen, do not check any radio boxes and click on 'Next Step'. At the review screen, check the details and click 'Create Group'.<br/><br/>
    d. Next, at the 'User groups' main screen, click on the group created and in the 'Permissions' tab, click on'Add permissions' and 'Create Inline Policy'.<br/><br/>
    e. Under the 'JSON' tab, copy and paste the code found in *aws_group* file found in the repository. Note to replace the 'XXXXXXXXXXX' within to your own AWS account number.<br/><br/>
    f. Validate the policy and press on 'Apply policy'. <br/><br/>
    g. Head to 'Users' on the left panel and click on 'Add user'. <br/><br/>
    h. Give your new user a name and select the the access type to be 'Programmatic access'. <br/><br/>
    i. Continuing on, add this user to the group just created. <br/><br/>
    j. Tags are optional. Moving on, review the details and click on 'Create user'. <br/><br/>
    k. Upon seeing the green Success screen, copy the access key id and secret access key to ```~/.aws/credentials```. The secret access key will not be shown again. Take caution that ```.aws/``` directory needs to be the home directory and the ```credentials``` file do not have any extensions. <br/>
    DO NOT save the directory under version control. <br/>
    In the ```credentials``` file, copy and paste the text below and modify the XXXXXXXX portions accordingly.<br/>
    ```
    [default]
    aws_access_key_id = XXXXXXXX
    aws_secret_access_key = XXXXXXXX
   ```  
6. Back to the command prompt, run ```zappa init```.

7.





# Acknowledgements
Credits to:
https://pythonforundergradengineers.com/deploy-serverless-web-app-aws-lambda-zappa.html
