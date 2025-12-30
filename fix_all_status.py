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

def fix_all_signed_status():
    """统一所有签收状态:成功签收 -> 已签收"""
    connection = None
    try:
        connection = pymysql.connect(**DB_CONFIG)
        cursor = connection.cursor()
        
        # 先查询有多少条"成功签收"记录
        cursor.execute("SELECT COUNT(*) FROM logistics_voucher WHERE logistics_status = '成功签收'")
        count_before = cursor.fetchone()[0]
        
        print("="*80)
        print("开始统一签收状态...")
        print("="*80)
        print(f"查询到 {count_before} 条 '成功签收' 记录")
        
        if count_before > 0:
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
        else:
            print("✓ 没有需要更新的记录,所有状态已正确")
        
        print("\n" + "="*80)
        print("当前数据库中所有物流状态统计:")
        print("="*80)
        
        # 统计所有状态
        cursor.execute("""
            SELECT logistics_status, COUNT(*) as count
            FROM logistics_voucher
            GROUP BY logistics_status
            ORDER BY count DESC
        """)
        
        status_stats = cursor.fetchall()
        
        print(f"{'物流状态':<20} {'数量':<10}")
        print("-"*80)
        for status, count in status_stats:
            status_display = status if status else '(空)'
            print(f"{status_display:<20} {count:<10}")
        
        print("="*80)
        
        # 显示所有记录
        cursor.execute("""
            SELECT id, order_no, logistics_status, signed_time
            FROM logistics_voucher
            ORDER BY id
        """)
        records = cursor.fetchall()
        
        print("\n所有记录详情:")
        print("="*80)
        print(f"{'ID':<5} {'订单号':<30} {'物流状态':<15} {'签收时间'}")
        print("-"*80)
        
        for record in records:
            record_id = record[0]
            order_no = record[1]
            status = record[2] if record[2] else '(空)'
            signed_time = record[3] if record[3] else '(空)'
            print(f"{record_id:<5} {order_no:<30} {status:<15} {signed_time}")
        
        print("="*80)
        
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
    fix_all_signed_status()
