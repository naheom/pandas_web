import json
import pandas as pd
import boto3 as bt3
import re
    
def lambda_handler(event, context):
    
    s3 = bt3.client('s3')
    
    #csv_data_1 = s3.get_object(Bucket='frame-pandas', Key='Pandas_Q1.csv')
    #print('CSV', csv_data_1)
    #contents_1 = csv_data_1['Body'].read()
    #print('Body', contents_1)
    
    method = event.get('httpMethod',{}) 
    
    with open('index.html', 'r') as f:
        indexPage = f.read()
    status_check = [0]*10 
    
    if method == 'GET':
        return {
            "statusCode": 200,
            "headers": {
            'Content-Type': 'text/html',
            },
            "body": indexPage
        }
        
    if method == 'POST':
        bodyContent = event.get('body',{}) 
        parsedBodyContent = json.loads(bodyContent)
        testCases = re.sub('&zwnj;.*&zwnj;','',parsedBodyContent["shown"]["0"], flags=re.DOTALL) 
        userSolution = parsedBodyContent["editable"]["0"] 
        questionName = parsedBodyContent["qname"]["0"]
        original_df = pd.read_csv('https://frame-pandas.s3.amazonaws.com/pandas_data.csv')
        user_output_df = pd.eval(userSolution)
        userHtmlFeedback = user_output_df.to_html()
        
        # Question 1
        isComplete = 0
        right_answer = original_df[original_df['GENDER']=='F']
        right_answer_text = 'original_df[original_df[\'GENDER\']==\'F\']'
        if(right_answer.equals(user_output_df)):
            status_check[0]=1
            isComplete = 1


        progress = len([qn for qn in status_check if qn == 1])
        print(progress)
        return {
            "statusCode": 200,
            "headers": {
            "Content-Type": "application/json",
                },
            "body":  json.dumps({
                "isComplete":isComplete,
                "pythonFeedback": "Hello",
                "htmlFeedback": userHtmlFeedback,
                "textFeedback": right_answer_text,
                "progress": progress,
                "questionStatus":status_check
            })
        }
