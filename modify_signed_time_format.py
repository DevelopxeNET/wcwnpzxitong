import pymysql
from pymysql import Error

# 数据库连接信息
DB_CONFIG = {
    'host': '192.168.1.88',
    'port': 3306,
    'user': 'wcwnpz',
    'password': 'm5fApGzkabe4zNFY',
    'database': 'wcwnpz',
    'charset': 'utf8mb4'
}

def modify_signed_time_column():
    """修改签收时间列格式为DATE类型"""
    connection = None
    try:
        # 连接数据库
        connection = pymysql.connect(**DB_CONFIG)
        cursor = connection.cursor()
        
        # 修改列类型为DATE
        alter_sql = """
        ALTER TABLE logistics_voucher 
        MODIFY COLUMN signed_time DATE DEFAULT NULL COMMENT '签收时间'
        """
        
        cursor.execute(alter_sql)
        connection.commit()
        
        print("✓ 签收时间列格式已修改为 DATE 类型 (格式: YYYY-MM-DD)")
        
        # 查看修改后的表结构
        cursor.execute("DESCRIBE logistics_voucher")
        columns = cursor.fetchall()
        
        print("\n表结构信息:")
        print("-" * 80)
        for col in columns:
            if col[0] == 'signed_time':
                print(f"字段名: {col[0]}")
                print(f"类型: {col[1]}")
                print(f"允许空值: {col[2]}")
                print(f"说明: 签收时间")
        print("-" * 80)
        
        # 查看数据
        cursor.execute("SELECT id, order_no, signed_time FROM logistics_voucher")
        records = cursor.fetchall()
        
        print("\n当前数据中的签收时间:")
        print("-" * 80)
        for record in records:
            print(f"ID: {record[0]}, 订单号: {record[1]}, 签收时间: {record[2]}")
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

if __name__ == "__main__":
    print("开始修改签收时间列格式...")
    print(f"连接到数据库: {DB_CONFIG['host']}:{DB_CONFIG['port']}")
    print("=" * 80)
    modify_signed_time_column()
