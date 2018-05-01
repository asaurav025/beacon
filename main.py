from flask import Flask, render_template
import paho.mqtt.client as mqtt
from threading import Thread
import recieve1
import recieve2
import alchemy
import psycopg2
import json
import datetime
from flask_cors import CORS, cross_origin
import PrintBar

ServerAddress='192.168.1.110'
app = Flask('iBeacon')
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route('/')
@cross_origin()
def WebPrint():
	result={'val':123,'var':321}

	return render_template('index.html', result = result)

@app.route('/stage1/<Tstamp>/')
@cross_origin()
def Stage1(Tstamp):
	cur=dbconnect()
	Tstamp1="'"+Tstamp+"'"
	Tstamp2="'"+Tstamp+" 23:59:59"+"'"
	print(Tstamp)
	cur.execute("""SELECT * FROM beacon WHERE "UTStamp" >= {} AND "UTStamp" <= {}""".format(Tstamp1,Tstamp2))
	rows=cur.fetchall()
	cur.close()
	query=[]
	column=('MAC','RSSI','Serial','TimeStamp','Flag')
	for row in rows:
		query.append(dict(zip(column,row)))
	return (json.dumps(query, default=DateFormatConvertor))

@app.route('/stage2/')
@cross_origin()
def Stage2():
	print("\nIn stage 2\n\n\n")
	return render_template('stage2.html')

@app.route('/stage2/print/<MAC>/')
@cross_origin()
def Print(MAC):
	print(MAC)
	obj=PrintBar.Printbar(MAC)
	obj.Main()
	return ("success")

# @app.route('/stage3/step1/<MAC>/')
# @cross_origin()
# def AcceptMac(MAC):
# 	arr=list(MAC.split(","))
# 	try:
# 		conn=psycopg2.connect("dbname='beacon' user='postgres' host='{}' port='5433' password='sid555'".format(ServerAddress))
# 	except:
# 		print("Cannot connect to database")
# 	cur=conn.cursor()
# 	for i in arr:
# 		try:
# 			cur.execute("""INSERT INTO beacon ("MAC","RSSI","UTStamp","Flag") VALUES ('{}','{}','{}','0')""".format(json_data['MAC'],json_data['RSSI'],datetime.datetime.now()))
# 			print("Inserted into database")
# 		except:
# 			print("Already in database")
			
# 	conn.commit()
# 	conn.close() 
	

def test1():
	app.run(host = '0.0.0.0', port = 3000)

def test2():
	recieve1.Main()

def test3():
	recieve2.Main()

def dbconnect():
	try:
		conn=psycopg2.connect("dbname='beacon' user='postgres' host='{}' port='5433' password='sid555'".format(ServerAddress))
	except:
		print("Cannot connect to database")
	cur=conn.cursor()
	return cur

def DateFormatConvertor(x):
	if isinstance(x,datetime.datetime):
		return x.__str__()

if __name__ == '__main__':

	t1=Thread(target=test1, args=())
	t2=Thread(target=test2, args=())
	t3=Thread(target=test3, args=())
	t1.start()
	t2.start()
	t3.start()
