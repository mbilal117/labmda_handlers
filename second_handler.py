import boto3
import psycopg2
import datetime
import pandas as pd

def lambda_handler(event, context):
    s3 = boto3.client('s3')
    list_add = []
    final_df = pd.DataFrame()
    try:
        resp = s3.get_object(Bucket='data-raw-input', Key='pace-data.csv')
        custom_date_parser =  lambda x: datetime.datetime.strptime(x,"%Y-%m-%d %H:%M:%S").isoformat()
        dfs = pd.read_csv(
            resp['Body'],
            usecols=['MovementDateTime', 'Speed', 'CallSign', 'ShipName', 'Beam', 'Length', 'MoveStatus'],
            parse_dates=['MovementDateTime'],
            date_parser=custom_date_parser,
            chunksize=4000
        )
        for df in dfs:
            df.loc[(df.Speed == 0) & (df.MoveStatus == 'Under way using engine'),'Speed'] = df.groupby('CallSign')['Speed'].mean()
            df['Speed'] = df['Speed'].fillna(df.groupby('CallSign')['Speed'].transform('mean'))
            df['BeamRatio'] = df['Beam']/df['Length']
            df['MovementDateTime'] = df['MovementDateTime'].dt.strftime('%Y-%m-%d %H:%M:%S')
            final_df = pd.concat([final_df, df])
    
        data = [tuple(x) for x in final_df[['MovementDateTime', 'Speed', 'CallSign', 'ShipName', 'Beam', 'Length', 'MoveStatus', 'BeamRatio']].to_numpy()]
        excecute_query(data)
    
    except Exception as e:
        return {
            'statusCode': 500,
            'body': f"Upload Failed {e}"
        }
    
    return {
            'statusCode': 200,
            'body': f"Upload succeeded"
        }

def excecute_query(data):
    try:
        con = psycopg2.connect(host='testinstance.cjwq2jodbhft.us-east-1.rds.amazonaws.com', user='postgres', password='testing123', dbname='test', port=5432, connect_timeout=5)
        con.autocommit = True
        cur = con.cursor()
        query = """ INSERT INTO tmc_data(
            "MovementDateTime", "Speed", "CallSign", "ShipName", "Beam", "Length", "MoveStatus", "BeamRatio")
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s); """
        cur.executemany(query, (data))
        cur.close()
    except psycopg2.Error as e:
        return {
            'statusCode': 200,
            'body': f"Upload succeeded {e}"
        }

