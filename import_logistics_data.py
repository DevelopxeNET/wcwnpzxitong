import pymysql
from pymysql import Error
from datetime import datetime, date

# 数据库连接信息
DB_CONFIG = {
    'host': '192.168.1.88',
    'port': 3306,
    'user': 'wcwnpz',
    'password': 'm5fApGzkabe4zNFY',
    'database': 'wcwnpz',
    'charset': 'utf8mb4'
}

def normalize_signed_time(value):
    """处理签收时间: 将 'None' 字符串转为 None"""
    if value is None:
        return None
    if isinstance(value, str):
        # 处理 'None', 'null', 空字符串
        if value.lower() in ['none', 'null', '']:
            return None
        # 尝试解析日期字符串 (YYYY-MM-DD)
        try:
            return datetime.strptime(value, '%Y-%m-%d').date()
        except:
            return None
    if isinstance(value, (datetime, date)):
        return value
    return None

def insert_logistics_data(data_list):
    """
    批量插入物流数据
    支持签收时间为 "None" 字符串
    
    参数示例:
    [
        {
            'order_no': 'ORDER001',
            'logistics_channel': '顺丰速运',
            'tracking_no': 'SF123456',
            'query_time': '2026-01-05 10:00:00',
            'logistics_status': '运输中',
            'signed_time': 'None',  # 支持字符串 "None"
            'image_url': 'http://example.com/image.jpg'
        }
    ]
    """
    connection = None
    try:
        connection = pymysql.connect(**DB_CONFIG)
        cursor = connection.cursor()
        
        insert_sql = """
        INSERT INTO logistics_voucher 
        (order_no, logistics_channel, tracking_no, query_time, logistics_status, signed_time, image_url)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        
        success_count = 0
        error_count = 0
        
        for data in data_list:
            try:
                # 处理签收时间
                signed_time = normalize_signed_time(data.get('signed_time'))
                
                cursor.execute(insert_sql, (
                    data.get('order_no'),
                    data.get('logistics_channel'),
                    data.get('tracking_no'),
                    data.get('query_time'),
                    data.get('logistics_status'),
                    signed_time,
                    data.get('image_url')
                ))
                success_count += 1
            except Exception as e:
                print(f"插入失败: {data.get('order_no')} - {e}")
                error_count += 1
        
        connection.commit()
        
        print(f"\n插入结果:")
        print(f"✓ 成功: {success_count} 条")
        if error_count > 0:
            print(f"✗ 失败: {error_count} 条")
        
        # 显示最近插入的数据
        cursor.execute("""
            SELECT id, order_no, logistics_status, signed_time 
            FROM logistics_voucher 
            ORDER BY id DESC 
            LIMIT 10
        """)
        records = cursor.fetchall()
        
        print(f"\n最近插入的数据:")
        print("-" * 80)
        for record in records:
            signed_time_str = record[3] if record[3] else 'None'
            print(f"ID: {record[0]}, 订单号: {record[1]}, 状态: {record[2]}, 签收时间: {signed_time_str}")
        print("-" * 80)
        
    except Error as e:
        print(f"✗ 数据库错误: {e}")
        if connection:
            connection.rollback()
    except Exception as e:
        print(f"✗ 发生错误: {e}")
    finally:
        if connection:
            cursor.close()
            connection.close()
            print("\n数据库连接已关闭")

# 示例用法
if __name__ == "__main__":
    print("="*80)
    print("物流数据导入工具 - 支持签收时间 'None'")
    print("="*80)
    
    # 示例数据
    test_data = [
        {
            'order_no': 'TEST_ORDER_001',
            'logistics_channel': '顺丰速运',
            'tracking_no': 'TEST_SF_001',
            'query_time': '2026-01-05 10:00:00',
            'logistics_status': '已签收',
            'signed_time': '2026-01-05',  # 正常日期
            'image_url': 'http://example.com/test1.jpg'
        },
        {
            'order_no': 'TEST_ORDER_002',
            'logistics_channel': '中通快递',
            'tracking_no': 'TEST_ZTO_002',
            'query_time': '2026-01-05 11:00:00',
            'logistics_status': '运输中',
            'signed_time': 'None',  # 字符串 "None"
            'image_url': 'http://example.com/test2.jpg'
        },
        {
            'order_no': 'TEST_ORDER_003',
            'logistics_channel': '韵达快递',
            'tracking_no': 'TEST_YD_003',
            'query_time': '2026-01-05 12:00:00',
            'logistics_status': '派送中',
            'signed_time': None,  # Python None
            'image_url': 'http://example.com/test3.jpg'
        },
        {
            'order_no': 'TEST_ORDER_004',
            'logistics_channel': '圆通速递',
            'tracking_no': 'TEST_YTO_004',
            'query_time': '2026-01-05 13:00:00',
            'logistics_status': '运输中',
            'signed_time': '',  # 空字符串
            'image_url': 'http://example.com/test4.jpg'
        }
    ]
    
    print(f"\n准备插入 {len(test_data)} 条测试数据...")
    insert_logistics_data(test_data)
