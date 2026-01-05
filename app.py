from flask import Flask, render_template, request, jsonify
import pymysql
from pymysql import Error
import os
from config import config

app = Flask(__name__)

# 加载配置
env = os.environ.get('FLASK_ENV', 'development')
app.config.from_object(config[env])

# 数据库连接信息
DB_CONFIG = {
    'host': app.config['DB_HOST'],
    'port': app.config['DB_PORT'],
    'user': app.config['DB_USER'],
    'password': app.config['DB_PASSWORD'],
    'database': app.config['DB_NAME'],
    'charset': app.config['DB_CHARSET']
}

def normalize_status(status):
    """统一物流状态: 成功签收 -> 已签收"""
    if status and '成功签收' in status:
        return '已签收'
    return status

def normalize_signed_time(signed_time):
    """处理签收时间: 将 'None' 字符串转为 None"""
    if signed_time is None:
        return None
    if isinstance(signed_time, str) and signed_time.lower() in ['none', 'null', '']:
        return None
    return signed_time

def get_logistics_data(order_no=None, tracking_no=None):
    """获取物流凭证数据"""
    connection = None
    try:
        connection = pymysql.connect(**DB_CONFIG)
        cursor = connection.cursor(pymysql.cursors.DictCursor)
        
        # 构建查询SQL
        sql = """
            SELECT id, order_no, logistics_channel, tracking_no, 
                   query_time, logistics_status, signed_time, image_url,
                   created_at, updated_at
            FROM logistics_voucher 
        """
        
        conditions = []
        params = []
        
        if order_no:
            conditions.append("order_no LIKE %s")
            params.append(f"%{order_no}%")
        
        if tracking_no:
            conditions.append("tracking_no LIKE %s")
            params.append(f"%{tracking_no}%")
        
        if conditions:
            sql += " WHERE " + " AND ".join(conditions)
        
        sql += " ORDER BY id DESC"
        
        cursor.execute(sql, params if params else None)
        
        records = cursor.fetchall()
        
        # 统一物流状态
        for record in records:
            if record.get('logistics_status'):
                record['logistics_status'] = normalize_status(record['logistics_status'])
        
        return records
        
    except Error as e:
        print(f"数据库错误: {e}")
        return []
    finally:
        if connection:
            cursor.close()
            connection.close()

@app.route('/')
def index():
    """首页展示物流凭证数据"""
    # 获取查询参数
    order_no = request.args.get('order_no', '').strip()
    tracking_no = request.args.get('tracking_no', '').strip()
    
    error_message = None
    data = []
    
    try:
        # 查询数据
        data = get_logistics_data(order_no=order_no, tracking_no=tracking_no)
    except Exception as e:
        error_message = str(e)
        print(f"查询错误: {e}")
    
    return render_template('index.html', 
                         records=data, 
                         order_no=order_no, 
                         tracking_no=tracking_no,
                         error_message=error_message)

@app.route('/api-docs')
def api_docs():
    """API文档页面"""
    return render_template('api_docs.html')

@app.route('/api/tracking/<tracking_no>', methods=['GET'])
def api_get_tracking(tracking_no):
    """API接口: 通过物流单号查询签收状态、签收时间和凭证"""
    connection = None
    try:
        connection = pymysql.connect(**DB_CONFIG)
        cursor = connection.cursor(pymysql.cursors.DictCursor)
        
        # 查询物流单号信息
        cursor.execute("""
            SELECT order_no, logistics_channel, tracking_no, 
                   query_time, logistics_status, signed_time, image_url
            FROM logistics_voucher 
            WHERE tracking_no = %s
        """, (tracking_no,))
        
        result = cursor.fetchone()
        
        if result:
            # 统一物流状态
            if result.get('logistics_status'):
                result['logistics_status'] = normalize_status(result['logistics_status'])
            
            # 格式化日期
            response_data = {
                'code': 200,
                'message': '查询成功',
                'data': {
                    'order_no': result['order_no'],
                    'logistics_channel': result['logistics_channel'],
                    'tracking_no': result['tracking_no'],
                    'query_time': result['query_time'].strftime('%Y-%m-%d %H:%M:%S') if result['query_time'] else None,
                    'logistics_status': result['logistics_status'],
                    'signed_time': result['signed_time'].strftime('%Y-%m-%d') if result['signed_time'] else None,
                    'image_url': result['image_url']
                }
            }
            return jsonify(response_data)
        else:
            return jsonify({
                'code': 404,
                'message': '未找到该物流单号的信息',
                'data': None
            }), 404
            
    except Error as e:
        return jsonify({
            'code': 500,
            'message': f'数据库错误: {str(e)}',
            'data': None
        }), 500
    except Exception as e:
        return jsonify({
            'code': 500,
            'message': f'服务器错误: {str(e)}',
            'data': None
        }), 500
    finally:
        if connection:
            cursor.close()
            connection.close()

if __name__ == '__main__':
    print("启动Flask服务...")
    print("访问地址: http://0.0.0.0:5000")
    # Windows 环境使用 Flask 开发服务器
    app.run(host='0.0.0.0', port=5000, debug=False)
