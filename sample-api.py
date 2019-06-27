import flask
from flask import request, jsonify
from flask_cors import CORS 
from sample_model import load_model
from new_model import call_from_api
import json
from flask_mysqldb import MySQL 
from fuzzy import output
app = flask.Flask(__name__)
app.config["DEBUG"] = True
CORS(app)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'beproject'

mysql = MySQL(app)

books = [
    {'id': 0,
     'title': 'A Fire Upon the Deep',
     'author': 'Vernor Vinge',
     'first_sentence': 'The coldsleep itself was dreamless.',
     'year_published': '1992'},
    {'id': 1,
     'title': 'The Ones Who Walk Away From Omelas',
     'author': 'Ursula K. Le Guin',
     'first_sentence': 'With a clamor of bells that set the swallows soaring, the Festival of Summer came to the city Omelas, bright-towered by the sea.',
     'published': '1973'},
    {'id': 2,
     'title': 'Dhalgren',
     'author': 'Samuel R. Delany',
     'first_sentence': 'to wound the autumnal city.',
     'published': '1975'}
]


@app.route('/db/save_orders',methods =['POST'])
def index():
    data=request.json
    location=data["location"]
    totalamount=data["totalamount"]
    type=data["type"]
    weight=data["weight"]
    quantity=data["quantity"]
    productName=data["productName"]
    deliveryMode=data["deliveryMode"]

    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO orders (location, totalamount, type, weight, quantity, productName, deliveryMode) VALUES ( %s , %s , %s, %s,%s,%s,%s)", (location,totalamount, type,weight,quantity,productName,deliveryMode))
    mysql.connection.commit()
    cur.close()
    return jsonify('success')
    # return request.data

@app.route('/db/fetch_orders_all',methods=['GET'])
def index1():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM orders o where o.oid NOT IN(SELECT p.oid from order_map_and_status p  )")
    row_headers=[x[0] for x in cur.description] #this will extract row headers
    rv = cur.fetchall()
    json_data=[]
    for result in rv:
        json_data.append(dict(zip(row_headers,result)))
    return json.dumps(json_data)

@app.route('/db/map_order',methods=['POST'])
def index2():
    data=request.json
    oid=data["oid"]
    sid=data["sid"]
    order_status=data["order_status"]
    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO order_map_and_status (oid, sid, order_status) VALUES ( %s , %s , %s)", (oid,sid, order_status))
    mysql.connection.commit()
    cur.close()
    return jsonify('success')

@app.route('/db/trace_order_4pl',methods=['GET'])
def index3():
    cur = mysql.connection.cursor()
    cur.execute("SELECT o.oid, p.sid , o.location, o.totalamount, o.type, o.weight, o.deliveryMode ,p.order_status FROM orders o , order_map_and_status p where o.oid = p.oid ")
    row_headers=[x[0] for x in cur.description] #this will extract row headers
    rv = cur.fetchall()
    json_data=[]
    for result in rv:
        json_data.append(dict(zip(row_headers,result)))
    return json.dumps(json_data)

@app.route('/db/trace_order_customer',methods=['GET'])
def index4():
    cur = mysql.connection.cursor()
    cur.execute("SELECT o.oid , o.location, o.totalamount, o.type, o.weight, o.deliveryMode ,p.order_status FROM orders o , order_map_and_status p where o.oid = p.oid ")
    row_headers=[x[0] for x in cur.description] 
    rv = cur.fetchall()
    # print(rv)
    json_data=[]
    for result in rv:
        json_data.append(dict(zip(row_headers,result)))

    cur = mysql.connection.cursor()
    cur.execute("SELECT o.oid , o.location, o.totalamount, o.type, o.weight, o.deliveryMode  FROM orders o where o.oid NOT IN (SELECT p.oid from order_map_and_status p)")
    row_headers=[x[0] for x in cur.description]
    row_headers.append("order_status")
    row_headers.append("sid")
    rv = cur.fetchall()
    t=()
    # print(type(rv))
    for r in rv:
        print(r)
        r = r + ( 0,)
        t = r + (-1,)
        # print(r)
    print(t)
    for result in rv:
        json_data.append(dict(zip(row_headers,result)))
    
    return json.dumps(json_data)
    # return("success")
    
@app.route('/db/process_order_3pl', methods=['GET','POST'])
def index5():
    data=request.json
    # print(data)
    sid=data["sid"]
    # print(sid)
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM orders o where o.oid IN ( SELECT p.oid from order_map_and_status p where p.sid = %s and order_status=1 )",(sid,))
    row_headers=[x[0] for x in cur.description] #this will extract row headers
    rv = cur.fetchall()
    json_data=[]
    for result in rv:
        json_data.append(dict(zip(row_headers,result)))
    return json.dumps(json_data)

@app.route('/db/order_delivery_complete_3pl', methods=['GET','POST'])
def index20():
    data=request.json
    # print(data)
    sid=data["sid"]
    # print(sid)
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM orders o where o.oid IN ( SELECT p.oid from order_map_and_status p where p.sid = %s and order_status=2 )",(sid,))
    row_headers=[x[0] for x in cur.description] #this will extract row headers
    rv = cur.fetchall()
    json_data=[]
    for result in rv:
        json_data.append(dict(zip(row_headers,result)))
    return json.dumps(json_data)

@app.route('/db/process_to_dispatched',methods=['GET','POST'])
def index8():
    data=request.json
    # print(data)
    oid=data["oid"]
    # print(sid)
    cur = mysql.connection.cursor()
    cur.execute("UPDATE order_map_and_status  SET order_status  = 2 WHERE oid = %s",(oid,))
    mysql.connection.commit()
    cur.close()
    return jsonify("success")

@app.route('/db/dispatched_to_deliver',methods=['GET','POST'])
def index9():
    data=request.json
    # print(data)
    oid=data["oid"]
    # print(sid)
    cur = mysql.connection.cursor()
    cur.execute("UPDATE order_map_and_status  SET order_status  = 3 WHERE oid = %s",(oid,))
    mysql.connection.commit()
    cur.close()
    return jsonify("success")


    

    


@app.route('/', methods=['GET'])
def route():
    return jsonify(books)

# @app.route('/sample_model', methods= ['GET'])
# def bantai():
#     score=load_model()
#     return jsonify(score)

@app.route('/neural',methods= ['GET','POST'])
def abc():
    data=request.data
    dataDict = json.loads(data)
    loc=dataDict["location"]
    truck=dataDict["truck_delivered"]
    hand=dataDict["hand_delivered"]
    l=call_from_api(loc,truck,hand)
    out = l.to_json(orient='records')
    # print(out)
    # print(dataDict["location"])
    return out

@app.route('/fuzzy', methods= ['GET','POST'] )
def index6():
    data=request.json
    print(data)
    experience=data["experience"]
    timeliness=data["timeliness"]
    support=data["support"]
    interaction=data["interaction"]
    quality=data["quality"]
    trouble=data["trouble"]

    l=output(experience,timeliness,support,interaction,quality,trouble)
    return jsonify(l)

if __name__ == '__main__':
    app.run(debug=True)