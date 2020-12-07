from flask import Flask, request, json, jsonify
from sqlalchemy import create_engine
from sqlalchemy.sql import text

app = Flask(__name__)

@app.route('/total_cuti', methods = ['GET'])
def get_total_cuti_by_date():
    body = request.json
    tbstart_date = body.get('start_date')
    tbend_date = body.get('end_date')
    conn_str = 'postgresql://postgres:parallelepiped@localhost:5432/employee'
    engine = create_engine(conn_str, echo=False)
    with engine.connect() as connection:
        qry = text("select sum(lama_cuti) as total_lama_cuti from (select *, (DATE_PART('day', leave.end_date - leave.start_date))+1 as lama_cuti from employee inner join leave on employee.nik = leave.employee_nik) as c where start_date >= :start_date and end_date <= :end_date")
        result = connection.execute(qry, start_date= tbstart_date, end_date=tbend_date)
        for row in result:
            return jsonify(total_hari_lama_cuti = row['total_lama_cuti'])

if __name__=="__main__":
    app.run(debug=True)