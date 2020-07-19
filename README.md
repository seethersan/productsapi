Django 2 project ready to deploy in AWS Lambda/DynamoDB using Zappa library
This serverless project use a DynamoDB table for storing

**Instructions:**
1. Create a virtualenv and activate

```
virtualenv env && source env/bin/activate
```

2. Clone the repository

```
git clone -b lambda https://github.com/seethersan/productsapi.git
cd productsapi
```

3. Install requirements

```
pip install -r requirements.txt
```

5. Initialize Zappa config. 
***You will need to configure awscli with your AWS account's credentials if you haven't done it before.***

```
zappa init

- Enter python3.7 as runtime
- Enter your settings file
- Enter your aws-region
- Enter your project name
```

6. Modify the zappa_settings.json file and add this env variables
***It will configure the lambda function to create the DynamoDB table***

```
"environment_variables": {
    "read_capacity_units": "5",
    "write_capacity_units": "5",
    "region": "us-east-1"
}
```

7. Deploy the Lambda Function

```
zappa deploy dev
```

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
    ```
    If the products pass validation, it will be saved in the database, if not it will response with a report error in JSON format

    You can test it using curl:
    ```
    curl --request GET https://60bqzz9f95.execute-api.us-east-1.amazonaws.com/dev/api/products/ 

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
        https://60bqzz9f95.execute-api.us-east-1.amazonaws.com/dev/api/products/bulk_insert
    ```
