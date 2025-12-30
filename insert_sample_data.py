import pymysql
from pymysql import Error
from datetime import date

# 数据库连接信息
DB_CONFIG = {
    'host': '192.168.1.88',
    'port': 3306,
    'user': 'wcwnpz',
    'password': 'm5fApGzkabe4zNFY',
    'database': 'wcwnpz',  # 请根据实际情况修改数据库名
    'charset': 'utf8mb4'
}

def insert_sample_data():
    """插入示例数据"""
    connection = None
    try:
        # 连接数据库
        connection = pymysql.connect(**DB_CONFIG)
        cursor = connection.cursor()
        
        # 先清空现有数据
        cursor.execute("TRUNCATE TABLE logistics_voucher")
        print("✓ 已清空现有数据")
        
        # 示例数据
        sample_data = [
            {
                'order_no': 'ORD20251230001',
                'logistics_channel': '顺丰速运',
                'tracking_no': 'SF1234567890123',
                'query_time': '2025-12-30 10:30:00',
                'logistics_status': '已签收',
                'signed_time': date(2025, 12, 30),
                'image_url': 'https://example.com/voucher/sf_001.jpg'
            },
            {
                'order_no': 'ORD20251230002',
                'logistics_channel': '中通快递',
                'tracking_no': 'ZTO9876543210987',
                'query_time': '2025-12-30 11:15:00',
                'logistics_status': '运输中',
                'signed_time': None,
                'image_url': 'https://example.com/voucher/zto_002.jpg'
            },
            {
                'order_no': 'ORD20251229001',
                'logistics_channel': '韵达快递',
                'tracking_no': 'YD4455667788990',
                'query_time': '2025-12-29 09:20:00',
                'logistics_status': '已签收',
                'signed_time': date(2025, 12, 29),
                'image_url': 'https://example.com/voucher/yd_001.jpg'
            },
            {
                'order_no': 'ORD20251229002',
                'logistics_channel': '圆通速递',
                'tracking_no': 'YTO5566778899001',
                'query_time': '2025-12-29 14:30:00',
                'logistics_status': '派送中',
                'signed_time': None,
                'image_url': 'https://example.com/voucher/yto_002.jpg'
            },
            {
                'order_no': 'ORD20251228001',
                'logistics_channel': '申通快递',
                'tracking_no': 'STO7788990011223',
                'query_time': '2025-12-28 16:45:00',
                'logistics_status': '已签收',
                'signed_time': date(2025, 12, 28),
                'image_url': 'https://example.com/voucher/sto_001.jpg'
            }
        ]
        
        # 插入SQL语句
        insert_sql = """
        INSERT INTO logistics_voucher 
        (order_no, logistics_channel, tracking_no, query_time, logistics_status, signed_time, image_url)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        
        # 批量插入数据
        for data in sample_data:
            cursor.execute(insert_sql, (
                data['order_no'],
                data['logistics_channel'],
                data['tracking_no'],
                data['query_time'],
                data['logistics_status'],
                data['signed_time'],
                data['image_url']
            ))
        
        connection.commit()
        print(f"✓ 成功插入 {len(sample_data)} 条示例数据!")
        
        # 查询并显示插入的数据
        cursor.execute("SELECT * FROM logistics_voucher ORDER BY id ASC")
        records = cursor.fetchall()
        
        print("\n插入的数据:")
        print("=" * 120)
        for record in records:
            print(f"ID: {record[0]}")
            print(f"  订单号: {record[1]}")
            print(f"  物流渠道: {record[2]}")
            print(f"  物流单号: {record[3]}")
            print(f"  查询时间: {record[4]}")
            print(f"  物流状态: {record[5]}")
            print(f"  签收时间: {record[6]}")
            print(f"  图片URL: {record[7]}")
            print(f"  创建时间: {record[8]}")
            print(f"  更新时间: {record[9]}")
            print("-" * 120)
        
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

if __name__ == "__main__":
    print("开始插入示例数据...")
    print(f"连接到数据库: {DB_CONFIG['host']}:{DB_CONFIG['port']}")
    print("=" * 120)
    insert_sample_data()
