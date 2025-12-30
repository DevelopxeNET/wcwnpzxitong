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

def create_logistics_table():
    """创建物流凭证表"""
    connection = None
    try:
        # 连接数据库
        connection = pymysql.connect(**DB_CONFIG)
        cursor = connection.cursor()
        
        # 创建表的SQL语句
        create_table_sql = """
        CREATE TABLE IF NOT EXISTS logistics_voucher (
            id INT AUTO_INCREMENT PRIMARY KEY COMMENT '自增ID',
            order_no VARCHAR(100) NOT NULL COMMENT '订单号',
            logistics_channel VARCHAR(100) DEFAULT NULL COMMENT '物流渠道',
            tracking_no VARCHAR(100) DEFAULT NULL COMMENT '物流单号',
            query_time DATETIME DEFAULT NULL COMMENT '查询时间',
            logistics_status VARCHAR(50) DEFAULT NULL COMMENT '物流状态',
            signed_time DATETIME DEFAULT NULL COMMENT '签收时间',
            image_url TEXT DEFAULT NULL COMMENT '图片URL',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
            INDEX idx_order_no (order_no),
            INDEX idx_tracking_no (tracking_no),
            INDEX idx_query_time (query_time)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='物流凭证表';
        """
        
        # 执行创建表
        cursor.execute(create_table_sql)
        connection.commit()
        
        print("✓ 表 'logistics_voucher' 创建成功!")
        
        # 查看表结构
        cursor.execute("DESCRIBE logistics_voucher")
        columns = cursor.fetchall()
        
        print("\n表结构信息:")
        print("-" * 80)
        print(f"{'字段名':<20} {'类型':<20} {'允许空值':<10} {'说明'}")
        print("-" * 80)
        for col in columns:
            print(f"{col[0]:<20} {col[1]:<20} {col[2]:<10} {col[5] if col[5] else ''}")
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
    print("开始创建物流凭证表...")
    print(f"连接到数据库: {DB_CONFIG['host']}:{DB_CONFIG['port']}")
    print("-" * 80)
    create_logistics_table()
