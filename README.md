# BÁO CÁO BÀI TẬP LỚN ĐẠI SỐ TUYẾN TÍNH
## Đề tài: Phân tích Giá trị Kỳ dị (SVD) trong Hệ thống gợi ý & Thuật toán Google PageRank

> **Giảng viên hướng dẫn:** ThS. Đặng Văn Vinh  
> **Đơn vị:** Trường Đại học Bách Khoa – ĐHQG TP. Hồ Chí Minh (Khoa Khoa học Ứng dụng – Bộ môn Toán Ứng dụng)  
> **Lớp môn học:** L01 – Nhóm 15 | Học kỳ 1, Năm học 2026 – 2027  
> **Mã nguồn thực thi:** [btl_dstt_svd_pagerank.py](./btl_dstt_svd_pagerank.py) *(Đã chuyển đổi hoàn chỉnh từ MATLAB sang Python)*

---

## 📌 MỤC LỤC TỔNG QUAN

1. [Tổng quan đề tài & Ý nghĩa thực tiễn](#1-tổng-quan-đề-tài--ý-nghĩa-thực-tiễn)
2. [Chương 1 - Phần A: Phân tích SVD trong Hệ thống gợi ý (Recommender Systems)](#2-chương-1---phần-a-phân-tích-svd-trong-hệ-thống-gợi-ý)
   - [2.1. Ý tưởng cốt lõi bằng trực giác đời sống](#21-ý-tưởng-cốt-lõi-bằng-trực-giác-đời-sống)
   - [2.2. Toán học đằng sau: SVD & Định lý Eckart–Young](#22-toán-học-đằng-sau-svd--định-lý-eckartyoung)
   - [2.3. Quy trình tính toán Truncated SVD](#23-quy-trình-tính-toán-truncated-svd)
   - [2.4. Thuật toán FunkSVD (Giải pháp giải thưởng Netflix 1 triệu USD)](#24-thuật-toán-funksvd-giải-pháp-giải-thưởng-netflix-1-triệu-usd)
   - [2.5. Ví dụ số học chi tiết (5 Người dùng × 5 Bộ phim)](#25-ví-dụ-số-học-chi-tiết-5-người-dùng--5-bộ-phim)
3. [Chương 1 - Phần B: Thuật toán Google PageRank (Đo độ uy tín Web)](#3-chương-1---phần-b-thuật-toán-google-pagerank)
   - [3.1. Ý tưởng cốt lõi: Người lướt web ngẫu nhiên & Bầu cử dân chủ](#31-ý-tưởng-cốt-lõi-người-lướt-web-ngẫu-nhiên--bầu-cử-dân-chủ)
   - [3.2. Căn bệnh 1: Nút cụt (Dangling Nodes) & Cách chữa bằng Ma trận $S$](#32-căn-bệnh-1-nút-cụt-dangling-nodes--cách-chữa-bằng-ma-trận-s)
   - [3.3. Căn bệnh 2: Bẫy liên kết (Spider Traps) & Phép Dịch chuyển tức thời ($d = 0.85$)](#33-căn-bệnh-2-bẫy-liên-kết-spider-traps--phép-dịch-chuyển-tức-thời-d--085)
   - [3.4. Định lý Perron–Frobenius & Phương pháp Lặp lũy thừa (Power Iteration)](#34-định-lý-perronfrobenius--phương-pháp-lặp-lũy-thừa-power-iteration)
   - [3.5. Hai ví dụ thực nghiệm số học chi tiết](#35-hai-ví-dụ-thực-nghiệm-số-học-chi-tiết)
4. [Chương 2: Ứng dụng thực tế & Bộ công cụ đánh giá Web của Google](#4-chương-2-ứng-dụng-thực-tế--bộ-công-cụ-đánh-giá-web-của-google)
   - [4.1. SVD giải quyết 3 điểm nghẽn thương mại điện tử](#41-svd-giải-quyết-3-điểm-nghẽn-thương-mại-điện-tử)
   - [4.2. So sánh Google PageRank vs Thuật toán HITS của Kleinberg](#42-so-sánh-google-pagerank-vs-thuật-toán-hits-của-kleinberg)
   - [4.3. Công cụ Google PageSpeed Insights & Bộ chỉ số Core Web Vitals](#43-công-cụ-google-pagespeed-insights--bộ-chỉ-số-core-web-vitals)
   - [4.4. 4 Lời khuyên chiến lược cho kỹ sư Web](#44-4-lời-khuyên-chiến-lược-cho-kỹ-sư-web)
5. [Chương 3: Hướng dẫn chạy Code Python (Migrate từ MATLAB)](#5-chương-3-hướng-dẫn-chạy-code-python-migrate-từ-matlab)
   - [5.1. Bảng đối chiếu câu lệnh MATLAB $\leftrightarrow$ Python NumPy/SciPy](#51-bảng-đối-chiếu-câu-lệnh-matlab--python-numpyscipy)
   - [5.2. Cách chạy mã nguồn Python](#52-cách-chạy-mã-nguồn-python)
   - [5.3. Bảng đối chiếu kết quả thực nghiệm khớp 100%](#53-bảng-đối-chiếu-kết-quả-thực-nghiệm-khớp-100)
   - [5.4. Đồ thị trực quan hóa sinh ra](#54-đồ-thị-trực-quan-hóa-sinh-ra)

---

## 1. TỔNG QUAN ĐỀ TÀI & Ý NGHĨA THỰC TIỄN

Đề tài kết nối hai ứng dụng đột phá nhất của **Đại số tuyến tính** trong kỷ nguyên Internet:

```
               ┌─────────────────────────────────────────────────────────────┐
               │                ĐẠI SỐ TUYẾN TÍNH HIỆN ĐẠI                  │
               └──────────────┬───────────────────────────────┬──────────────┘
                              │                               │
             (Phân rã ma trận chữ nhật)               (Trị riêng ma trận vuông)
                              │                               │
                              ▼                               ▼
       ┌───────────────────────────────┐     ┌────────────────────────────────┐
       │   PHÂN TÍCH GIÁ TRỊ KỲ DỊ     │     │     THUẬT TOÁN PAGERANK        │
       │             (SVD)             │     │      (GOOGLE SEARCH ENGINE)    │
       └──────────────┬────────────────┘     └────────────────┬───────────────┘
                      │                                       │
                      ▼                                       ▼
       • Hệ thống gợi ý (Netflix, Amazon)      • Đo lường uy tín hàng tỷ trang web
       • Khử nhiễu, đoán sở thích người dùng   • Chuỗi Markov, lặp lũy thừa hội tụ
       • Không gian nhân tố ẩn (Latent Space)  • Tối ưu cấu trúc liên kết Web thực tế
```

- **SVD (Singular Value Decomposition):** Thuật toán đứng sau giải thưởng Netflix Prize 1 triệu USD, giúp các nền tảng như Netflix, Spotify, Shopee hiểu được "gu ngầm" của người dùng để gợi ý chính xác những gì họ thích dù họ chưa từng xem qua.
- **PageRank:** Thuật toán nền tảng đưa Google trở thành công cụ tìm kiếm số 1 hành tinh, mô hình hóa toàn bộ mạng Internet thành một đồ thị toán học để tìm ra các trang web uy tín nhất.

---

## 2. CHƯƠNG 1 - PHẦN A: PHÂN TÍCH SVD TRONG HỆ THỐNG GỢI Ý

### 2.1. Ý tưởng cốt lõi bằng trực giác đời sống
Hãy tưởng tượng một bảng đánh giá phim với hàng triệu người dùng và hàng triệu bộ phim:
- **Vấn đề:** Mỗi người dùng bình thường chỉ xem và chấm điểm khoảng 10–20 bộ phim. Bảng dữ liệu có tới **99% ô trống (khuyết điểm)**! Làm sao Netflix biết bạn sẽ thích bộ phim mới ra mắt để gợi ý?
- **Giải pháp trực giác:** Đằng sau hàng triệu bộ phim thực ra chỉ có một số ít **"chủ đề ẩn" (Latent Concepts)** chi phối: ví dụ *Mức độ Hành động/Viễn tưởng* và *Mức độ Tình cảm/Lãng mạn*.
  - Người dùng $A$ thích xem bom tấn hành động.
  - Phim $B$ là một bộ phim thuần hành động bom tấn.
  - Dù $A$ chưa từng xem $B$, ta vẫn suy ra được $A$ sẽ chấm điểm rất cao cho $B$!
- **SVD chính là công cụ toán học tự động bóc tách các "chủ đề ẩn" này** từ một bảng số liệu thô sơ.

---

### 2.2. Toán học đằng sau: SVD & Định lý Eckart–Young

Với mọi ma trận bảng đánh giá đã chuẩn hóa $A \in \mathbb{R}^{m \times n}$ (gồm $m$ người dùng và $n$ sản phẩm), SVD phân tích $A$ thành tích 3 ma trận:

$$A = U \cdot \Sigma \cdot V^T$$

Trong đó:
- **$U \in \mathbb{R}^{m \times m}$ (Ma trận người dùng - chủ đề):** Hàng thứ $u$ cho biết mức độ người dùng $u$ đam mê từng chủ đề ẩn.
- **$\Sigma \in \mathbb{R}^{m \times n}$ (Ma trận độ quan trọng của chủ đề):** Là ma trận đường chéo chứa các giá trị kỳ dị $\sigma_1 \ge \sigma_2 \ge \dots \ge \sigma_r > 0$. $\sigma_k$ càng lớn thì chủ đề thứ $k$ càng quan trọng trong việc quyết định điểm số.
- **$V \in \mathbb{R}^{n \times n}$ (Ma trận sản phẩm - chủ đề):** Hàng thứ $i$ cho biết bộ phim $i$ mang bao nhiêu phần trăm đặc tính của từng chủ đề.

```
       Ma trận gốc A             U (User - Concept)     Σ (Trọng số)    V^T (Item - Concept)
    ┌                 ┐        ┌                 ┐    ┌             ┐    ┌                 ┐
    │  r_11  ...  r_1n│        │  u_11  ...  u_1k│    │ σ_1         │    │  v_11  ...  v_1n│
    │   ...  ...   ...│   ≈    │   ...  ...   ...│  · │      ...    │  · │   ...  ...   ...│
    │  r_m1  ...  r_mn│        │  u_m1  ...  u_mk│    │         σ_k │    │  v_k1  ...  v_kn│
    └                 ┘        └                 ┘    └             ┘    └                 ┘
         (m x n)                    (m x k)               (k x k)             (k x n)
```

> **Định lý Xấp xỉ Hạng Thấp Eckart–Young (1936):**  
> Nếu ta chỉ giữ lại $k$ giá trị kỳ dị lớn nhất ($k \ll \min(m, n)$) và bỏ đi các giá trị nhỏ còn lại:
> $$A_k = \sum_{j=1}^k \sigma_j u_j v_j^T$$
> Thì $A_k$ chính là ma trận hạng $k$ **xấp xỉ tốt nhất** cho ma trận ban đầu $A$ theo cả chuẩn Frobenius (tổng bình phương sai số nhỏ nhất) lẫn chuẩn phổ L2! Việc cắt bỏ các giá trị kỳ dị đuôi chính là **khử nhiễu dữ liệu**.

---

### 2.3. Quy trình tính toán Truncated SVD

Để điền vào các ô trống chưa có đánh giá, thuật toán SVD cổ điển thực hiện 4 bước:

1. **Tính điểm trung bình mỗi người dùng ($\bar{r}_u$):** Do có người rất dễ tính (toàn chấm 4-5 sao), có người rất khó tính (toàn chấm 1-2 sao).
2. **Điền khuyết tạm thời (Baseline Imputation):** Tạm thời điền $\bar{r}_u$ vào các ô người dùng chưa đánh giá.
3. **Chuẩn hóa tâm (Mean-Centering):** Trừ mỗi hàng đi $\bar{r}_u$ để tạo ra ma trận độ lệch $A$: $a_{ui} = r_{ui} - \bar{r}_u$. Khi đó ô chưa đánh giá sẽ mang giá trị độ lệch bằng $0.00$.
4. **Phân rã SVD & Tái tạo điểm số:**
   - Phân tích $A = U \Sigma V^T$.
   - Giữ lại $k$ thành phần lớn nhất tạo thành $A_k = U_k \Sigma_k V_k^T$.
   - Cộng lại điểm trung bình ban đầu: $\hat{R}_k = A_k + \bar{r}_u$.
   - Giá trị tại các ô trống lúc này chính là **điểm dự đoán**!

---

### 2.4. Thuật toán FunkSVD (Giải pháp giải thưởng Netflix 1 triệu USD)

- **Nhược điểm của Truncated SVD cổ điển:** Việc điền trước số trung bình vào các ô trống đã vô tình đưa thông tin giả vào dữ liệu, khiến SVD cố gắng khớp cả những số giả đó.
- **Giải pháp của Simon Funk (FunkSVD):** Không điền số giả! Chỉ tính toán trực tiếp trên **những ô thực sự đã được người dùng đánh giá** bằng thuật toán Tối ưu hóa suy giảm độ dốc ngẫu nhiên (SGD) kết hợp điều chuẩn L2 để chống hiện tượng quá khớp (Overfitting):
  
  $$\min_{P, Q, b} \sum_{(u, i) \in \text{Observed}} \left( r_{ui} - (\mu + b_u + b_i + p_u \cdot q_i^T) \right)^2 + \lambda (\|p_u\|_2^2 + \|q_i\|_2^2 + b_u^2 + b_i^2)$$

---

### 2.5. Ví dụ số học chi tiết (5 Người dùng × 5 Bộ phim)

Xét 5 người dùng và 5 bộ phim:
- $I_1, I_2, I_3$: Thể loại **Hành động / Viễn tưởng (Sci-Fi)**.
- $I_4, I_5$: Thể loại **Tình cảm / Tâm lý (Drama)**.
- Người dùng $U_1, U_2, U_5$ là tín đồ phim Sci-Fi.
- Người dùng $U_3, U_4$ là tín đồ phim Drama.

Bảng điểm gốc $R_{\text{raw}}$:
| Người dùng | $I_1$ (Sci-Fi) | $I_2$ (Sci-Fi) | $I_3$ (Sci-Fi) | $I_4$ (Drama) | $I_5$ (Drama) | Trung bình $\bar{r}_u$ |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **$U_1$** | 5.0 | 4.0 | 5.0 | 1.0 | **? (Khuyết)** | **3.75** |
| **$U_2$** | 4.0 | 5.0 | 4.0 | 2.0 | 1.0 | **3.20** |
| **$U_3$** | 1.0 | 2.0 | 1.0 | 5.0 | 4.0 | **2.60** |
| **$U_4$** | 1.0 | **? (Khuyết)** | 2.0 | 4.0 | 5.0 | **3.00** |
| **$U_5$** | 5.0 | 4.0 | **? (Khuyết)** | 1.0 | 2.0 | **3.00** |

#### Kết quả phân rã SVD:
- Các giá trị kỳ dị: $\sigma_1 = 6.7324$ (chiếm **82.79%** năng lượng), $\sigma_2 = 2.3483$ (**10.07%**), $\sigma_3 = 1.5063$, $\sigma_4 = 1.2810$, $\sigma_5 = 0$.
- Chỉ cần chọn $k = 2$ nhân tố ẩn đầu tiên đã giữ lại được **92.86%** toàn bộ thông tin của ma trận!

#### Kết quả dự đoán tại 3 ô khuyết:
1. **Cặp ($U_5, I_3$) [Người thích Sci-Fi – Phim Sci-Fi]:**
   - Điểm trung bình: 3.00 sao.
   - SVD ($k=1$): **3.93 sao**, SVD ($k=2$): **3.94 sao**, FunkSVD: **5.16 sao** (quy tròn 5.0 sao).
   - 👉 **Quyết định hệ thống:** **GỢI Ý NGAY** (Dự đoán điểm xuất sắc vì bắt đúng sở thích Sci-Fi).
2. **Cặp ($U_4, I_2$) [Người thích Drama – Phim Sci-Fi]:**
   - Điểm trung bình: 3.00 sao.
   - SVD ($k=1$): **2.32 sao**, SVD ($k=2$): **2.07 sao**, FunkSVD: **0.66 sao** (quy tròn 1.0 sao).
   - 👉 **Quyết định hệ thống:** **KHÔNG GỢI Ý** (Hệ thống nhận ra $U_4$ ghét phim Sci-Fi).
3. **Cặp ($U_1, I_5$) [Người thích Sci-Fi – Phim Drama]:**
   - FunkSVD dự đoán **1.90 sao** (chính xác với gu ghét Drama của $U_1$).

---

## 3. CHƯƠNG 1 - PHẦN B: THUẬT TOÁN GOOGLE PAGERANK

### 3.1. Ý tưởng cốt lõi: Người lướt web ngẫu nhiên & Bầu cử dân chủ

Thuật toán PageRank do Sergey Brin và Larry Page sáng lập năm 1998 tại Stanford dựa trên hai nguyên tắc trực giác:
1. **Liên kết là một lá phiếu bầu uy tín:** Nếu trang $A$ gắn link trỏ tới trang $B$, nghĩa là trang $A$ đánh giá trang $B$ có nội dung hữu ích.
2. **Không phải mọi lá phiếu đều có giá trị như nhau:** Lá phiếu từ một trang lớn (như Báo Tuổi Trẻ, Wikipedia) có giá trị cao hơn hàng nghìn lá phiếu từ các blog cá nhân vô danh.
3. **Người lướt web ngẫu nhiên (Random Surfer):** Một người ngồi lướt web nhấp chuột ngẫu nhiên vào các liên kết trên màn hình. Trang web nào người này ghé thăm với tần suất cao nhất chính là trang có **PageRank cao nhất**.

Công thức đệ quy cơ bản:
$$\text{PR}(i) = \sum_{j \in B_i} \frac{\text{PR}(j)}{N_j} \iff \pi = H \pi$$

Trong đó:
- $B_i$ là tập các trang trỏ tới trang $i$.
- $N_j$ là số liên kết đi ra từ trang $j$.
- $H$ là **Ma trận siêu liên kết thô (Hyperlink Matrix)**.
- $\pi$ là vector điểm số PageRank (tổng điểm bằng 1).

---

### 3.2. Căn bệnh 1: Nút cụt (Dangling Nodes) & Cách chữa bằng Ma trận $S$

```
          [Trang A] ───► [Trang B] ───► [Tệp PDF cụt] (Không có link ra)
                                            │
                                            ▼
                                  (Điểm số biến mất!)
```

- **Hiện tượng:** Những trang web không có liên kết đi ra (như tệp PDF, ảnh, hoặc trang không có link). Cột tương ứng trong ma trận $H$ toàn số 0.
- **Hậu quả (Rank Leak):** Khi lướt đến trang này, người dùng bị kẹt. Sau vài bước nhân ma trận, toàn bộ điểm số của cả hệ thống mạng bị **rò rỉ về 0** ($\sum \pi_i \to 0$)!
- **Cách chữa (Ma trận ngẫu nhiên cột $S$):** Giả định khi người dùng gặp nút cụt, họ sẽ gõ ngẫu nhiên một địa chỉ bất kỳ trong toàn bộ $n$ trang web với xác suất đều $1/n$:
  
  $$S = H + \frac{1}{n} e \cdot a^T$$
  
  *(Trong đó $a_j = 1$ nếu trang $j$ là nút cụt, ngược lại $a_j = 0$). Lúc này $S$ trở thành ma trận có tổng mỗi cột bằng đúng 1.*

---

### 3.3. Căn bệnh 2: Bẫy liên kết (Spider Traps) & Phép Dịch chuyển tức thời ($d = 0.85$)

```
   [Trang chủ] ──► [Trang B] ──► [Trang C] ◄──────┐
                                    │             │  BẪY LIÊN KẾT:
                                    └────────► [Trang D]  Hai trang chỉ trỏ qua lại,
                                                          hút sạch 100% điểm của site!
```

- **Hiện tượng:** Một nhóm trang web chỉ trỏ lòng vòng cho nhau mà không có đường liên kết thoát ra ngoài (hoặc trang web tự trỏ vào chính nó).
- **Hậu quả (Rank Sink):** Giống như một "hố đen vũ trụ", bẫy liên kết sẽ **hút cạn 100% điểm số** của toàn bộ website. Điểm của Trang chủ và các trang quan trọng khác đều bị tụt về 0.
- **Cách chữa thần kỳ của Google (Ma trận Google $G$):** Đưa vào cơ chế **Dịch chuyển tức thời (Teleportation)** với hệ số tắt dần $d = 0.85$:
  - Với xác suất $d = 85\%$: Người dùng tiếp tục click vào các link trên trang.
  - Với xác suất $1 - d = 15\%$: Người dùng cảm thấy chán nản, bèn gõ trực tiếp một URL mới trên thanh địa chỉ để nhảy ngẫu nhiên tới bất kỳ trang nào trên toàn cầu.
  
  $$G = d \cdot S + \frac{1 - d}{n} e \cdot e^T$$

---

### 3.4. Định lý Perron–Frobenius & Phương pháp Lặp lũy thừa (Power Iteration)

- **Định lý Perron–Frobenius:** Vì mọi phần tử của ma trận Google $G$ đều thực sự dương ($G_{ij} > 0$), $G$ là một ma trận ngẫu nhiên nguyên thủy (primitive stochastic matrix). Định lý toán học bảo đảm rằng:
  1. $G$ luôn có trị riêng lớn nhất duy nhất $\lambda_1 = 1$.
  2. Tồn tại duy nhất một vector riêng dừng $\pi > 0$ thỏa mãn $G\pi = \pi$ và $\sum \pi_i = 1$.
- **Phương pháp Lặp lũy thừa (Power Iteration):** Bắt đầu từ vector khởi tạo đều $\pi^{(0)} = [1/n, \dots, 1/n]^T$, ta liên tục nhân:
  
  $$\pi^{(k+1)} = G \pi^{(k)}$$
  
- **Tốc độ hội tụ:** Tốc độ hội tụ của thuật toán phụ thuộc trực tiếp vào mô-đun của **trị riêng lớn thứ hai $|\lambda_2(G)|$**:
  
  $$\|\pi^{(k)} - \pi^*\|_1 \le C \cdot |\lambda_2(G)|^k \le C \cdot d^k$$
  
  Với $d = 0.85$, thuật toán hội tụ cực nhanh (thường chỉ mất 20 – 80 bước lặp cho mạng hàng triệu trang)!

---

### 3.5. Hai ví dụ thực nghiệm số học chi tiết

#### Ví dụ 1: Mạng 4 trang Web liên thông mạnh (A, B, C, D)
- Cấu trúc: Không có nút cụt ($a = [0, 0, 0, 0]^T$).
- Trị riêng thứ hai: $|\lambda_2(G_1)| = 0.464749$ (rất nhỏ $\to$ hội tụ thần tốc).
- **Số bước lặp hội tụ ($\epsilon < 10^{-6}$):** Chỉ **19 bước lặp**!
- Điểm PageRank giải tích chính xác:
  - $\text{PR}(A) = \frac{215}{584} \approx 36.82\%$ (Trang chủ có PageRank cao nhất).
  - $\text{PR}(C) \approx 28.80\%$.
  - $\text{PR}(D) \approx 20.21\%$.
  - $\text{PR}(B) \approx 14.18\%$.

#### Ví dụ 2: Mạng 5 trang Web có Nút cụt $P_4$ và Bẫy liên kết $\{P_3, P_5\}$
- $P_4$ là tệp PDF không có link ra ($N_{P_4} = 0$).
- Cụm $\{P_3, P_5\}$ tạo thành bẫy liên kết khép kín ($P_3 \leftrightarrow P_5$).
- **Đối chứng thực nghiệm kinh điển:**
  - Nếu **không có $d$** ($d = 1.0$): Cụm bẫy $\{P_3, P_5\}$ hút sạch **100% điểm** ($P_3: 50\%, P_5: 50\%$). Trang chủ $P_1$ và Danh mục $P_2$ **bị xóa sổ về 0%**!
  - Khi áp dụng **Ma trận Google ($d = 0.85$)**:
    - $P_3 = 41.04\%$ và $P_5 = 39.20\%$ (vẫn giữ điểm cao xứng đáng).
    - Trang chủ $P_1 = 6.02\%$, Danh mục $P_2 = 6.02\%$, Tệp PDF $P_4 = 7.72\%$ **vẫn giữ được điểm số dương hợp lý**!

---

## 4. CHƯƠNG 2: ỨNG DỤNG THỰC TẾ & BỘ CÔNG CỤ ĐÁNH GIÁ WEB CỦA GOOGLE

### 4.1. SVD giải quyết 3 điểm nghẽn thương mại điện tử
1. **Khắc phục độ thưa dữ liệu và tính bắc cầu láng giềng:** Trên Amazon, 99.9% người dùng không mua cùng một sản phẩm cụ thể. SVD chiếu họ vào không gian nhân tố ẩn nên vẫn nhận diện được những người có chung sở thích.
2. **Khả năng mở rộng quy mô (Scalability):** SVD tính toán ngoại tuyến (offline). Khi phục vụ thời gian thực (online), việc gợi ý chỉ là một phép nhân vô hướng của 2 vector độ dài $k$ ($p_u \cdot q_i^T$) với độ trễ dưới 1 phần nghìn giây.
3. **Hiện tượng từ đồng nghĩa (Synonymy):** Giúp nhận diện "sổ ghi chép tái chế" và "vở viết sinh thái" có cùng bản chất dù khác tên gọi văn bản.

---

### 4.2. So sánh Google PageRank vs Thuật toán HITS của Kleinberg

| Tiêu chí | Thuật toán Google PageRank | Thuật toán HITS (Kleinberg) |
| :--- | :--- | :--- |
| **Bản chất Đại số** | Trị riêng & Vector riêng của chuỗi Markov | Phân tích SVD của ma trận kề $A$ |
| **Phân loại trang** | Một điểm số uy tín duy nhất ($PR$) | Tách làm 2 điểm: **Authority** (uy tín) và **Hub** (tổng hợp) |
| **Thời điểm tính toán** | Tính toán trước ngoại tuyến (Query-independent) | Tính toán theo từng từ khóa tìm kiếm (Query-dependent) |
| **Khả năng chống spam** | Rất cao nhờ hệ số dịch chuyển $d=0.85$ | Dễ bị thao túng bởi các trang liên kết tương hỗ (Mutually reinforcing) |

---

### 4.3. Công cụ Google PageSpeed Insights & Bộ chỉ số Core Web Vitals

Google không chỉ chấm điểm dựa trên liên kết (PageRank) mà còn đánh giá **tốc độ trải nghiệm thực tế**:

#### 1. Bộ ba chỉ số Core Web Vitals (Dữ liệu người dùng thật - CrUX):
- **LCP (Largest Contentful Paint - Tốc độ hiển thị nội dung chính):** $\le 2.5\text{s}$ (Tốt). Đo thời gian bức ảnh banner hoặc tiêu đề chính hiện lên.
- **INP (Interaction to Next Paint - Độ nhạy tương tác):** $\le 200\text{ms}$ (Tốt). Thay thế FID từ tháng 3/2024, đo độ trễ khi click chuột, gõ phím.
- **CLS (Cumulative Layout Shift - Độ ổn định giao diện):** $\le 0.10$ (Tốt). Tránh hiện tượng các nút bấm bị giật nhảy khiến người dùng bấm nhầm.

#### 2. Công thức Điểm hiệu năng Google Lighthouse (v10 - v13):
$$\text{Score} = 30\% \cdot S_{\text{TBT}} + 25\% \cdot S_{\text{LCP}} + 25\% \cdot S_{\text{CLS}} + 10\% \cdot S_{\text{FCP}} + 10\% \cdot S_{\text{SI}}$$
*(Trong đó Total Blocking Time - TBT chiếm tỷ trọng cao nhất 30% nhằm chống nghẽn CPU do JavaScript).*

---

### 4.4. 4 Lời khuyên chiến lược cho kỹ sư Web

1. **Thiết kế liên kết nội bộ liên thông mạnh (Tránh Nút cụt & Bẫy liên kết):** Mọi trang bài viết, trang sản phẩm đều phải có menu điều hướng, thanh đường dẫn (breadcrumbs) trỏ về Trang chủ và Danh mục chính để dòng chảy PageRank lưu thông đều đặn.
2. **Kiểm soát số lượng liên kết đi ra ($N_j$):** Vì giá trị uy tín chia đều cho các link ra ($PR(j)/N_j$), hãy loại bỏ các liên kết rác để không làm phân tán điểm uy tín.
3. **Tích hợp khối gợi ý cá nhân hóa bằng SVD:** Gợi ý các sản phẩm phù hợp ở chân trang giúp giữ chân khách hàng, tăng số trang xem/phiên và tăng chỉ số Engaged Sessions trên GA4.
4. **Tối ưu hình ảnh và luồng JavaScript:** Khai báo sẵn thuộc tính `width`, `height` cho ảnh để triệt tiêu lỗi giật khung hình CLS; dùng định dạng ảnh hiện đại WebP/AVIF và chia nhỏ các hàm JavaScript dài quá 50ms để tối ưu điểm Lighthouse.

---

## 5. CHƯƠNG 3: HƯỚNG DẪN CHẠY CODE PYTHON (MIGRATE TỪ MATLAB)

Toàn bộ mã nguồn MATLAB gốc trong báo cáo đã được chuyển đổi sang tệp Python duy nhất:
👉 **[`btl_dstt_svd_pagerank.py`](./btl_dstt_svd_pagerank.py)**

### 5.1. Bảng đối chiếu câu lệnh MATLAB $\leftrightarrow$ Python NumPy/SciPy

| STT | Thao tác giải thuật | Lệnh trong MATLAB | Cú pháp tương đương trong Python |
| :---: | :--- | :--- | :--- |
| **1** | Phân tích SVD rút gọn | `[U, S, V] = svd(A, 'econ')` | `U, s, Vt = np.linalg.svd(A, full_matrices=False)` |
| **2** | Giải hệ phương trình tuyến tính | `pi_exact = A_sys \ b_sys` | `pi_exact = np.linalg.solve(A_sys, b_sys)` |
| **3** | Tìm trị riêng ma trận | `eig_vals = eig(G)` | `eig_vals = np.linalg.eigvals(G)` |
| **4** | Tính chuẩn L1 vector | `norm(v1 - v2, 1)` | `np.sum(np.abs(v1 - v2))` |
| **5** | Đổi số thực sang phân số | `rats(x)` | `Fraction(x).limit_denominator()` |
| **6** | Lũy thừa ma trận cấp cao | `S^100` | `np.linalg.matrix_power(S, 100)` |
| **7** | Vẽ đồ thị thang Logarit | `semilogy(x, y)` | `plt.semilogy(x, y)` |
| **8** | Vẽ biểu đồ cột nhóm | `bar(data, 'grouped')` | `ax.bar(x - width/2, ...); ax.bar(x + width/2, ...)` |

---

### 5.2. Cách chạy mã nguồn Python

Chạy trực tiếp bằng môi trường ảo đã cài sẵn các thư viện:

```bash
# Thực thi toàn bộ chương trình và xuất kết quả + đồ thị
./.venv/bin/python btl_dstt_svd_pagerank.py
```

*(Chương trình sẽ tự động in bảng phân tích số liệu ra Terminal và lưu đồ thị chất lượng cao tại tệp `btl_dstt_visualizations.png`).*

---

### 5.3. Bảng đối chiếu kết quả thực nghiệm khớp 100%

| Hạng mục kiểm tra | Giá trị tính trong Báo cáo (MATLAB) | Kết quả mã Python chạy thực tế | Đánh giá |
| :--- | :---: | :---: | :---: |
| **SVD $\sigma_1$** (Năng lượng) | $6.7324$ ($82.786\%$) | $6.7324$ ($82.786\%$) | Khớp tuyệt đối |
| **SVD $\sigma_2$** (Năng lượng) | $2.3483$ ($10.072\%$) | $2.3483$ ($10.072\%$) | Khớp tuyệt đối |
| **Dự đoán ($U_5, I_3$)** | $3.9316$ (k=1) \| $3.9432$ (k=2) | $3.9316$ (k=1) \| $3.9432$ (k=2) | Khớp tuyệt đối |
| **FunkSVD ($U_5, I_3$)** | $5.1579$ | $5.1579$ | Khớp tuyệt đối |
| **FunkSVD ($U_4, I_2$)** | $0.6557$ | $0.6557$ | Khớp tuyệt đối |
| **Ví dụ 1 $|\lambda_2(G_1)|$** | $0.464749$ | $0.464749$ | Khớp tuyệt đối |
| **Ví dụ 1 Số bước lặp** | $19$ bước ($\epsilon < 10^{-6}$) | $19$ bước ($\epsilon < 10^{-6}$) | Khớp tuyệt đối |
| **Ví dụ 1 Điểm $PR(A)$** | $0.368151$ ($215/584$) | $0.368151$ ($215/584$) | Khớp tuyệt đối |
| **Ví dụ 2 $|\lambda_2(G_2)|$** | $0.850000$ | $0.850000$ | Khớp tuyệt đối |
| **Ví dụ 2 Số bước lặp** | $75$ bước ($\epsilon < 10^{-6}$) | $75$ bước ($\epsilon < 10^{-6}$) | Khớp tuyệt đối |
| **Ví dụ 2 Điểm $PR(P_3)$** | $0.410420$ ($15140/36889$) | $0.410420$ ($15140/36889$) | Khớp tuyệt đối |
| **Ví dụ 2 Điểm $PR(P_1)$** | $0.060181$ ($60/997$) | $0.060181$ ($60/997$) | Khớp tuyệt đối |

---

### 5.4. Đồ thị trực quan hóa sinh ra

Khi chạy lệnh, tệp hình ảnh [`btl_dstt_visualizations.png`](./btl_dstt_visualizations.png) được sinh ra với 3 khung biểu đồ:

1. **Biểu đồ 1 (Phổ SVD & Năng lượng tích lũy):** Minh họa trực quan giá trị kỳ dị giảm nhanh và cho thấy chỉ cần $k=2$ thành phần đã gom được $92.86\%$ năng lượng ma trận.
2. **Biểu đồ 2 (Tốc độ hội tụ Power Iteration):** Đồ thị đường cong logarit biểu diễn tốc độ giảm sai số; Ví dụ 1 dốc đứng và chạm ngưỡng sau 19 bước, Ví dụ 2 chạm ngưỡng sau 75 bước.
3. **Biểu đồ 3 (Triệt tiêu Bẫy liên kết tại Ví dụ 2):** So sánh trực tiếp giữa trường hợp $d=1.0$ (bị hút sạch điểm) và $d=0.85$ (phân phối đều đặn và hợp lý).

---

## 🎯 LỜI KẾT
Tài liệu và mã nguồn Python này được cấu trúc toàn diện, chuẩn mực và trực quan, giúp người đọc nắm bắt bản chất của **Đại số tuyến tính ứng dụng** mà không bị choáng ngợp bởi công thức hàn lâm. Chúc bạn học tập và đạt điểm tuyệt đối trong môn Đại số Tuyến Tính!
