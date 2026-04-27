import pandas as pd
import numpy as np
import joblib
import time
import glob
import warnings

# Ẩn các cảnh báo lặt vặt của thư viện cho giao diện console đẹp hơn
warnings.filterwarnings('ignore')

print("="*65)
print("🛡️ HỆ THỐNG PHÁT HIỆN XÂM NHẬP MẠNG (IDS) - AI POWERED 🛡️")
print("="*65)
print("[INFO] Đang khởi động hệ thống và nạp mô hình AI...")

# 1. Nạp "Bộ não" đã được huấn luyện (Đã thêm ../ để lùi ra thư mục gốc)
try:
    model = joblib.load('../models/best_rf_model.pkl')
    scaler = joblib.load('../models/standard_scaler.pkl')
    label_encoder = joblib.load('../models/label_encoder.pkl')
    print("[OK] Đã nạp thành công: Mô hình Random Forest, Scaler và Label Encoder.")
except Exception as e:
    print(f"[ERROR] Không tìm thấy file mô hình. Lỗi: {e}")
    print("Vui lòng kiểm tra lại xem bạn đã chạy thành công ô lưu file ở cuối File 02 chưa.")
    exit()

# Danh sách 18 đặc trưng (Bắt buộc phải đúng thứ tự)
FEATURES = [
    'Destination Port', 'Flow Duration', 'Total Fwd Packets', 'Total Backward Packets',
    'Total Length of Fwd Packets', 'Total Length of Bwd Packets', 'Fwd Packet Length Mean',
    'Bwd Packet Length Mean', 'Flow Bytes/s', 'Flow Packets/s',
    'Packet Length Mean', 'Packet Length Std', 'SYN Flag Count',
    'ACK Flag Count', 'FIN Flag Count', 'RST Flag Count',
    'PSH Flag Count', 'URG Flag Count'
]

print("\n[INFO] Đang kết nối với cổng mạng (Giả lập luồng dữ liệu)...")
# Cập nhật đường dẫn data (Thêm ../)
csv_files = glob.glob('../data/*.csv')
if not csv_files:
    print("[ERROR] Không tìm thấy file dữ liệu nào trong thư mục data/.")
    exit()

# Lấy mẫu 30 dòng (có random_state để xáo trộn gói tin bình thường và gói tin tấn công)
df_stream = pd.read_csv(csv_files[0]).sample(30, random_state=100)
df_stream.columns = df_stream.columns.str.strip()

print("[OK] Kết nối thành công! Bắt đầu giám sát lưu lượng thời gian thực...\n")
print("-" * 65)
print(f"{'THỜI GIAN':<12} | {'SỐ HIỆU GÓI TIN':<15} | {'KẾT QUẢ QUÉT CỦA AI':<25}")
print("-" * 65)

# Cập nhật đường dẫn lưu log ra thư mục gốc
log_file = open('../logs/alerts.log', 'a', encoding='utf-8')

# 2. Vòng lặp giám sát thời gian thực
packet_id = 1001 # Đánh số ID giả định cho gói tin
for index, row in df_stream.iterrows():
    # Bước A: Lấy đúng 18 đặc trưng mạng từ gói tin truyền tới
    packet_data = row[FEATURES].to_frame().T
    
    # Bước B: Tiền xử lý nhanh gọn
    packet_data.replace([np.inf, -np.inf], np.nan, inplace=True)
    packet_data.fillna(0, inplace=True)
    
    # Bước C: Chuẩn hóa dữ liệu
    packet_scaled = scaler.transform(packet_data)
    
    # Bước D: AI đưa ra phán đoán
    prediction_encoded = model.predict(packet_scaled)
    
    # Bước E: Dịch con số thành tên loại tấn công
    prediction_label = label_encoder.inverse_transform(prediction_encoded)[0]
    
    current_time = time.strftime("%H:%M:%S")
    
    # Bước F: Phân luồng Cảnh báo
    if prediction_label == 'BENIGN':
        print(f"[{current_time}] | Gói tin #{packet_id:<5} | 🟢 An toàn (BENIGN)")
    else:
        alert_msg = f"[{current_time}] | Gói tin #{packet_id:<5} | 🔴 CẢNH BÁO: Tấn công {prediction_label}!"
        print(alert_msg)
        
        # Ghi sự cố vào sổ nhật ký
        log_file.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')} - Cảnh báo mức Đỏ: Phát hiện {prediction_label} từ gói tin #{packet_id}\n")
        
    # Tạm dừng 1 giây để mô phỏng thời gian chờ gói tin
    time.sleep(1) 
    packet_id += 1

log_file.close()
print("-" * 65)
print("🛡️ Hệ thống đã hoàn tất phiên giám sát. Các cảnh báo đã được tự động lưu vào file 'alerts.log'.")