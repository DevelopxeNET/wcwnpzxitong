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

def update_status():
    """更新物流状态:成功签收 -> 已签收"""
    connection = None
    try:
        connection = pymysql.connect(**DB_CONFIG)
        cursor = connection.cursor()
        
        # 更新所有"成功签收"为"已签收"
        update_sql = """
        UPDATE logistics_voucher 
        SET logistics_status = '已签收'
        WHERE logistics_status = '成功签收'
        """
        
        cursor.execute(update_sql)
        affected_rows = cursor.rowcount
        connection.commit()
        
        print(f"✓ 成功更新 {affected_rows} 条记录: '成功签收' -> '已签收'")
        
        # 查看更新后的数据
        cursor.execute("SELECT id, order_no, logistics_status FROM logistics_voucher")
        records = cursor.fetchall()
        
        print("\n当前所有记录的物流状态:")
        print("-" * 80)
        for record in records:
            print(f"ID: {record[0]}, 订单号: {record[1]}, 物流状态: {record[2]}")
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
    print("开始更新物流状态...")
    print("=" * 80)
    update_status()
