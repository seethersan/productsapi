Django 3 project ready to deploy in AWS ElasticBeanstalk (Amazon Linux with python 3.6)

**Instructions:**
1. Create a virtualenv and activate

```
virtualenv env && source env/bin/activate
´´´

2. Clone the repository

```
git clone https://github.com/seethersan/productsapi.git
cd productsapi
´´´

3. Install requirements

```
pip install -r requirements.txt
´´´

4. Install CLI for AWS Elastic Beanstalk

```
pip install awsebcli
´´´

5. Initialize Elastic Beanstalk App. 
***You will need to configure awscli with your AWS account's credentials if you haven't done it before.
Also, at the moment the ebextensions config files are only compatible with Amazon Linux with python 3.6***

```
eb init
´´´

6. Create environment and deploy app
***It will create the RDS Postgres instance, set the RDS env variables and migrate the database***

```
eb create
´´´

7. Open app

```
eb open
´´´

The app has 2 urls:

- /api/products **GET**
    It sends back all the registered products in JSON format
- /api/products/bulk_insert **POST**
    Recieves a JSON in this format
    
    ```
    {
        "products": [
            {
                "id": String
                "name": String
                "value": Float
                "discount_value": Float
                "stock": Int
            },...
        ]
    }
    ´´´
    If the products pass validation, it will be saved in the database, if not it will response with a report error in JSON format

    You can test it using curl:
    ```
    curl --request GET http://productsapi-dev2.us-east-1.elasticbeanstalk.com/api/products/ 

    curl --header "Content-Type: application/json" \
        --request POST \
        --data '{
            "products": [
                {
                    "id": "pollo569",
                    "name": "pollo x1kg",
                    "value": 29.3,
                    "discount_value": 3.2,
                    "stock": 3
                },
                {
                    "id": "pollos965",
                    "name": "pollo x1kg",
                    "value": 29.3,
                    "discount_value": 3.2,
                    "stock": 5
                },
                {
                    "id": "pollo0344",
                    "name": "pollo x1kg",
                    "value": 99.9,
                    "discount_value": 3.2,
                    "stock": 23
                }
            ]
        }' \
        http://productsapi-dev2.us-east-1.elasticbeanstalk.com/api/products/bulk_insert
    ´´´
