# Hệ Thống Phát Hiện Xâm Nhập Mạng (IDS) - Machine Learning

## Giới Thiệu
Dự án: **Hệ Thống Phát Hiện Xâm Nhập Mạng (IDS) - Machine Learning**. Dự án sử dụng bộ dữ liệu **CIC-IDS2017** để phát hiện các luồng tấn công mạng phổ biến như **DDoS**, **DoS**, **PortScan** và các loại tấn công khác.

## Mục Tiêu Lab
- Tiền xử lý tập dữ liệu mạng quy mô lớn (làm sạch, mã hóa, chuẩn hóa).
- Lọc đặc trưng (Feature Selection) — giữ lại **18 đặc trưng** cốt lõi.
- Cân bằng dữ liệu bằng **SMOTE** và **RandomUnderSampler**.
- Huấn luyện và so sánh 5 thuật toán: **Logistic Regression**, **SVM**, **Naive Bayes**, **KNN**, **Random Forest**.
- Xây dựng mô-đun mô phỏng phát hiện tấn công **thời gian thực** (Real-time).

## Cấu Trúc Thư Mục
Sơ đồ cây thư mục:
```text
.
├── data/
│   ├── *.csv
│   └── processed/processed_data.npz
├── logs/
│   └── alerts.log
├── models/
│   └── *.pkl
├── notebooks/
│   ├── 01_EDA_and_Preprocessing.ipynb
│   └── 02_Model_Training.ipynb
├── src/
│   └── realtime_detector.py
├── requirements.txt
└── README.md
```

Tệp/Thư mục quan trọng:
- Dữ liệu: [data/](data/)
- Log cảnh báo: [logs/alerts.log](logs/alerts.log)
- Mô hình đã lưu (.pkl): [models/](models/)
- Notebook EDA & tiền xử lý: [notebooks/01_EDA_and_Preprocessing.ipynb](notebooks/01_EDA_and_Preprocessing.ipynb)
- Notebook huấn luyện: [notebooks/02_Model_Training.ipynb](notebooks/02_Model_Training.ipynb)
- Script real-time: [src/realtime_detector.py](src/realtime_detector.py)
- Yêu cầu phụ thuộc: [requirements.txt](requirements.txt)

## Hướng Dẫn Cài Đặt & Chạy

1. Tạo và kích hoạt môi trường ảo (Windows PowerShell):
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

2. Cài đặt dependencies:
```powershell
pip install -r requirements.txt
```

3. Chạy mô phỏng phát hiện thời gian thực:
```powershell
cd src
python realtime_detector.py
```

## Quy Trình & Kết Quả

### Quy trình chính (tóm tắt 3 bước)
- **Tiền xử lý:** Làm sạch dữ liệu, mã hoá biến categorical, chuẩn hoá, xử lý thiếu và lưu tập đã xử lý vào `data/processed/processed_data.npz`.
- **Huấn luyện mô hình:** Thực hiện feature selection (giữ 18 đặc trưng), cân bằng dữ liệu với `SMOTE` + `RandomUnderSampler`, huấn luyện và đánh giá 5 mô hình.
- **Giám sát thời gian thực:** `realtime_detector.py` mô phỏng nhận luồng, dự đoán và ghi cảnh báo vào `logs/alerts.log`.

### Kết quả chính
- **Naive Bayes:** Chạy nhanh nhưng có sai số cao (độ chính xác thấp, nhiều false positive/false negative).
- **Logistic Regression:** Gặp khó khăn hội tụ do dữ liệu phức tạp; cần tuning và feature engineering.
- **Random Forest:** Đạt ma trận nhầm lẫn và các chỉ số tốt nhất trong thí nghiệm — được chọn làm **mô hình chiến thắng** (độ chính xác và recall tốt trên các lớp tấn công quan trọng).

> Mọi cảnh báo tấn công phát hiện được sẽ được ghi tự động vào [logs/alerts.log](logs/alerts.log).

## Ghi Chú Thực Thi & Tuning
- Nên thử thêm feature engineering, ensemble hoặc hyperparameter tuning để cải thiện Logistic Regression và SVM.
- Lưu metadata (phiên bản dataset, hyperparameters) cùng mô hình trong `models/` để phục vụ tái tạo.
- Với môi trường production, chuyển mô phỏng sang pipeline stream thực tế (ví dụ Kafka/Socket) và dùng hàng đợi/batching để tránh quá tải.

## Thông Tin Tác Giả
- Sinh viên thực hiện: **Nguyễn Lê Gia Bảo - N23DCCN074**
- Đơn vị: **Học viện Công nghệ Bưu chính Viễn thông (PTIT)**

---