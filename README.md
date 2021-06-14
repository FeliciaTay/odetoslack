# odetoslack 
This is a Slack application which will be deployed through Zappa. Zappa is a Python package that bundles up the web application written in Flask and deploys to AWS Lambda. The backend database can be hosted on AWS RDS, using MySQL database.

## Setting up
The below instructions include the setting up of AWS Lambda and AWS RDS. If an AWS group has already been set up, Step 5 can be omitted.

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
    i. Type 'IAM' into the search box and at the left panel, select 'User groups' under 'Access Management'.<br/> 
    ii. Create a new group and give it a name. <br/>
    iii. In the 'Attach Policy' screen, do not check any radio boxes and click on 'Next Step'. At the review screen, check the details and click 'Create Group'.<br/>
    iv. Next, at the 'User groups' main screen, click on the group created and in the 'Permissions' tab, click on'Add permissions' and 'Create Inline Policy'.<br/>
    v. Under the 'JSON' tab, copy and paste the code found in "aws_group" file in the repository.<br/>
    vi.

6.

7.





# Acknowledgements
Credits to:
https://pythonforundergradengineers.com/deploy-serverless-web-app-aws-lambda-zappa.html
