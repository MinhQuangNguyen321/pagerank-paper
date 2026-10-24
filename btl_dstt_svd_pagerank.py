"""
===============================================================================
BÀI TẬP LỚN ĐẠI SỐ TUYẾN TÍNH - HỌC KỲ 1 NĂM HỌC 2026 - 2027
Đề tài: Phân tích giá trị kỳ dị (SVD) trong Hệ thống gợi ý & Thuật toán Google PageRank
Chuyển đổi mã nguồn từ MATLAB sang Python (NumPy, SciPy, Matplotlib)
===============================================================================
"""

import numpy as np
from fractions import Fraction
import matplotlib.pyplot as plt
from typing import Tuple, List, Dict, Any


def format_fraction(val: float, max_denominator: int = 100000) -> str:
    """
    Chuyển đổi số thực dấu phẩy động sang phân số tối giản (tương tự rats trong MATLAB).
    """
    frac = Fraction(val).limit_denominator(max_denominator)
    return f"{frac.numerator}/{frac.denominator}"


# =============================================================================
# PHẦN 1: HỆ THỐNG GỢI Ý BẰNG SVD VÀ FUNKSVD (MA TRẬN 5 x 5)
# =============================================================================

def run_recommender_svd() -> Dict[str, Any]:
    print("=" * 80)
    print("PHẦN 1: ỨNG DỤNG SVD TRONG HỆ THỐNG GỢI Ý (MA TRẬN 5 USERS x 5 ITEMS)")
    print("=" * 80)

    # 1. Khởi tạo ma trận đánh giá gốc R_raw (0 biểu thị ô khuyết chưa đánh giá)
    # I1, I2, I3: Phim Sci-Fi/Action | I4, I5: Phim Drama/Romance
    R_raw = np.array([
        [5.0, 4.0, 5.0, 1.0, 0.0],  # U1: khuyết I5
        [4.0, 5.0, 4.0, 2.0, 1.0],  # U2: đã đánh giá đủ
        [1.0, 2.0, 1.0, 5.0, 4.0],  # U3: đã đánh giá đủ
        [1.0, 0.0, 2.0, 4.0, 5.0],  # U4: khuyết I2
        [5.0, 4.0, 0.0, 1.0, 2.0]   # U5: khuyết I3
    ], dtype=float)

    m, n = R_raw.shape
    user_means = np.zeros(m)
    R_imputed = R_raw.copy()

    # 2. Tính điểm trung bình từng người dùng và điền khuyết (Baseline Imputation)
    for u in range(m):
        rated_idx = R_raw[u] > 0
        user_means[u] = np.mean(R_raw[u, rated_idx])
        R_imputed[u, ~rated_idx] = user_means[u]

    # 3. Chuẩn hóa tâm (Mean-Centering): A = R_imputed - user_means * ones(1, n)
    A = R_imputed - user_means[:, np.newaxis]

    # 4. Phân tích Giá trị kỳ dị (SVD): A = U * Sigma * V^T
    # Trong NumPy: np.linalg.svd trả về U, s, Vt với Vt = V^T
    U, sigma, Vt = np.linalg.svd(A, full_matrices=False)
    V = Vt.T
    total_energy = np.sum(sigma**2)
    energy_pct = (sigma**2) / total_energy * 100

    print("Điểm trung bình người dùng (bar_r_u):")
    print("  " + "  ".join(f"{x:.2f}" for x in user_means))
    print("\nCác giá trị kỳ dị (sigma_1 -> sigma_5):")
    print("  " + "  ".join(f"{s:.4f}" for s in sigma))
    print("\nTỷ lệ năng lượng chuẩn Frobenius (%):")
    print("  " + "  ".join(f"{p:.3f}%" for p in energy_pct))

    # 5. Xấp xỉ hạng thấp Eckart-Young với k = 1 và k = 2 (Truncated SVD)
    # k = 1
    A_k1 = np.outer(U[:, 0] * sigma[0], Vt[0, :])
    R_pred_k1 = A_k1 + user_means[:, np.newaxis]

    # k = 2
    k = 2
    A_k2 = (U[:, :k] * sigma[:k]) @ Vt[:k, :]
    R_pred_k2 = A_k2 + user_means[:, np.newaxis]

    # 6. Đối chứng với Regularized Matrix Factorization (FunkSVD bằng SGD)
    np.random.seed(42)
    P = 0.1 * np.random.randn(m, k)
    Q = 0.1 * np.random.randn(n, k)
    b_u = np.zeros(m)
    b_i = np.zeros(n)
    
    rated_elements = R_raw[R_raw > 0]
    mu = np.mean(rated_elements)
    lr = 0.02
    reg = 0.02

    # Lấy tọa độ các ô đã đánh giá theo thứ tự cột trước (khớp hoàn toàn với find() của MATLAB)
    col_idx, row_idx = np.where(R_raw.T > 0)
    row_obs, col_obs = row_idx, col_idx

    for epoch in range(2000):
        for u, i in zip(row_obs, col_obs):
            r_ui = R_raw[u, i]
            pred = mu + b_u[u] + b_i[i] + np.dot(P[u, :], Q[i, :])
            err = r_ui - pred
            b_u[u] += lr * (err - reg * b_u[u])
            b_i[i] += lr * (err - reg * b_i[i])
            P_old = P[u, :].copy()
            P[u, :] += lr * (err * Q[i, :] - reg * P[u, :])
            Q[i, :] += lr * (err * P_old - reg * Q[i, :])

    R_pred_funk = mu + b_u[:, np.newaxis] + b_i[np.newaxis, :] + P @ Q.T

    print("\nKết quả dự đoán tại 3 ô khuyết:")
    print(f" + Cặp (U5, I3) [Sci-Fi]: Imputed = {user_means[4]:.2f} | "
          f"SVD(k=1) = {R_pred_k1[4, 2]:.4f} | SVD(k=2) = {R_pred_k2[4, 2]:.4f} | "
          f"FunkSVD = {R_pred_funk[4, 2]:.4f}")
    print(f" + Cặp (U4, I2) [Sci-Fi]: Imputed = {user_means[3]:.2f} | "
          f"SVD(k=1) = {R_pred_k1[3, 1]:.4f} | SVD(k=2) = {R_pred_k2[3, 1]:.4f} | "
          f"FunkSVD = {R_pred_funk[3, 1]:.4f}")
    print(f" + Cặp (U1, I5) [Drama ]: Imputed = {user_means[0]:.2f} | "
          f"SVD(k=1) = {R_pred_k1[0, 4]:.4f} | SVD(k=2) = {R_pred_k2[0, 4]:.4f} | "
          f"FunkSVD = {R_pred_funk[0, 4]:.4f}\n")

    return {
        "R_raw": R_raw,
        "user_means": user_means,
        "sigma": sigma,
        "energy_pct": energy_pct,
        "R_pred_k1": R_pred_k1,
        "R_pred_k2": R_pred_k2,
        "R_pred_funk": R_pred_funk
    }


# =============================================================================
# PHẦN 2: THUẬT TOÁN GOOGLE PAGERANK
# =============================================================================

def solve_pagerank_python(H: np.ndarray, a: np.ndarray, d: float = 0.85, tol: float = 1e-6) \
        -> Tuple[np.ndarray, np.ndarray, np.ndarray, List[float], float]:
    """
    Hàm giải thuật toán Google PageRank bằng cả phương pháp Giải tích và Lặp lũy thừa.
    
    Tham số:
      H   : Ma trận siêu liên kết thô (Hyperlink matrix) cấp n x n
      a   : Vector chỉ thị nút cụt (dangling nodes: a_j = 1 nếu N_j = 0, ngược lại 0)
      d   : Hệ số tắt dần (damping factor, mặc định 0.85)
      tol : Ngưỡng dừng sai số chuẩn L1 (mặc định 1e-6)
      
    Trả về:
      G          : Ma trận Google (n x n)
      pi_exact   : Nghiệm giải tích chính xác từ hệ phương trình tuyến tính
      pi_iter    : Nghiệm xấp xỉ từ phương pháp lặp lũy thừa (Power Iteration)
      err_hist   : Lịch sử sai số chuẩn L1 qua từng bước lặp
      second_eig : Mô-đun trị riêng lớn thứ hai |lambda_2(G)|
    """
    n = H.shape[0]
    e = np.ones((n, 1))
    a_col = a.reshape(n, 1)

    # Bước 1: Vá nút cụt tạo ma trận ngẫu nhiên cột S = H + (1/n) * e * a^T
    S = H + (1.0 / n) * (e @ a_col.T)

    # Bước 2: Tạo ma trận Google G = d * S + ((1 - d) / n) * e * e^T
    G = d * S + ((1.0 - d) / n) * (e @ e.T)

    # Phương pháp 1: Giải tích hệ phương trình tuyến tính (I - G) * pi = 0, sum(pi) = 1
    # Thay hàng cuối cùng bằng điều kiện tổng xác suất = 1
    A_sys = np.eye(n) - G
    A_sys[-1, :] = 1.0
    b_sys = np.zeros(n)
    b_sys[-1] = 1.0
    pi_exact = np.linalg.solve(A_sys, b_sys)

    # Phương pháp 2: Lặp lũy thừa (Power Iteration)
    pi_iter = np.ones(n) / n
    err_hist = []
    for k in range(1, 501):
        pi_next = G @ pi_iter
        l1_err = float(np.sum(np.abs(pi_next - pi_iter)))
        err_hist.append(l1_err)
        pi_iter = pi_next
        if l1_err < tol:
            break

    # Tính trị riêng lớn thứ hai |lambda_2(G)|
    eig_vals = np.sort(np.abs(np.linalg.eigvals(G)))[::-1]
    second_eig = float(eig_vals[1])

    return G, pi_exact, pi_iter, err_hist, second_eig


def run_pagerank_examples() -> Dict[str, Any]:
    print("=" * 80)
    print("PHẦN 2: KIỂM CHỨNG 2 VÍ DỤ THUẬT TOÁN GOOGLE PAGERANK (d = 0.85)")
    print("=" * 80)

    d = 0.85
    tol = 1e-6

    # --- VÍ DỤ 1: Mạng lưới 4 trang Web liên thông mạnh (A, B, C, D) ---
    H1 = np.array([
        [0.0,   0.0, 1.0, 0.5],
        [1/3.0, 0.0, 0.0, 0.0],
        [1/3.0, 0.5, 0.0, 0.5],
        [1/3.0, 0.5, 0.0, 0.0]
    ], dtype=float)
    a1 = np.zeros(4)  # Không có nút cụt

    G1, pi_exact1, pi_iter1, err_hist1, lam2_1 = solve_pagerank_python(H1, a1, d, tol)

    print("--- KẾT QUẢ VÍ DỤ 1 (4 trang liên thông mạnh A, B, C, D) ---")
    print(f"Mô-đun trị riêng lớn thứ hai |lambda_2(G1)| = {lam2_1:.6f}")
    print(f"Số bước lặp Power Iteration để đạt sai số L1 < 1e-6: k = {len(err_hist1)} bước")
    names1 = ['A', 'B', 'C', 'D']
    for i, name in enumerate(names1):
        print(f"  PR({name}): Nghiệm lặp = {pi_iter1[i]:.6f} | "
              f"Nghiệm giải tích = {pi_exact1[i]:.6f} | "
              f"Phân số = {format_fraction(pi_exact1[i])}")

    # --- VÍ DỤ 2: Mạng lưới 5 trang Web có Nút cụt (P4) và Bẫy liên kết {P3, P5} ---
    H2 = np.array([
        [0.0,   1/3.0, 0.0, 0.0, 0.0],
        [1/3.0, 0.0,   0.0, 0.0, 0.0],
        [1/3.0, 1/3.0, 0.0, 0.0, 1.0],
        [1/3.0, 1/3.0, 0.0, 0.0, 0.0],
        [0.0,   0.0,   1.0, 0.0, 0.0]
    ], dtype=float)
    a2 = np.array([0, 0, 0, 1, 0], dtype=float)  # P4 là nút cụt (Dangling Node)

    G2, pi_exact2, pi_iter2, err_hist2, lam2_2 = solve_pagerank_python(H2, a2, d, tol)

    print("\n--- KẾT QUẢ VÍ DỤ 2 (5 trang có Nút cụt P4 và Bẫy liên kết {P3, P5}) ---")
    print(f"Mô-đun trị riêng lớn thứ hai |lambda_2(G2)| = {lam2_2:.6f}")
    print(f"Số bước lặp Power Iteration để đạt sai số L1 < 1e-6: k = {len(err_hist2)} bước")
    for i in range(5):
        print(f"  PR(P{i+1}): Nghiệm lặp = {pi_iter2[i]:.6f} | "
              f"Nghiệm giải tích = {pi_exact2[i]:.6f} | "
              f"Phân số = {format_fraction(pi_exact2[i])}")

    return {
        "H1": H1, "G1": G1, "pi_exact1": pi_exact1, "err_hist1": err_hist1, "lam2_1": lam2_1,
        "H2": H2, "G2": G2, "pi_exact2": pi_exact2, "err_hist2": err_hist2, "lam2_2": lam2_2,
        "a2": a2
    }


# =============================================================================
# PHẦN 3: VẼ ĐỒ THỊ TRỰC QUAN HÓA BẰNG MATPLOTLIB
# =============================================================================

def plot_visualizations(ex1_data: Dict[str, Any], svd_data: Dict[str, Any], save_path: str = "btl_dstt_visualizations.png"):
    print("\n" + "=" * 80)
    print("PHẦN 3: XUẤT ĐỒ THỊ TRỰC QUAN HÓA DỮ LIỆU")
    print("=" * 80)

    # Cấu hình giao diện đồ thị phong cách khoa học
    plt.rcParams.update({'font.size': 11, 'figure.autolayout': True})
    fig = plt.figure(figsize=(16, 5))

    # --- Đồ thị 1: Phổ giá trị kỳ dị SVD & Năng lượng tích lũy Frobenius ---
    ax1 = fig.add_subplot(1, 3, 1)
    sigma = svd_data["sigma"]
    k_indices = np.arange(1, len(sigma) + 1)
    energy_cum = np.cumsum(svd_data["energy_pct"])
    
    ax1.bar(k_indices, sigma, color='#3498db', alpha=0.8, edgecolor='black', label=r'Giá trị kỳ dị $\sigma_k$')
    ax1.set_xlabel('Chỉ số giá trị kỳ dị (k)')
    ax1.set_ylabel(r'Giá trị $\sigma_k$', color='#2980b9')
    ax1.set_title('Phổ SVD & Năng lượng Frobenius\n(Ma trận 5x5)', fontweight='bold')
    ax1.set_xticks(k_indices)
    ax1.grid(True, linestyle='--', alpha=0.6)

    # Trục phụ biểu diễn phần trăm năng lượng tích lũy
    ax1_twin = ax1.twinx()
    ax1_twin.plot(k_indices, energy_cum, color='#e74c3c', marker='o', linewidth=2, label=r'Năng lượng tích lũy (%)')
    ax1_twin.set_ylabel('Năng lượng tích lũy (%)', color='#c0392b')
    ax1_twin.set_ylim(0, 105)
    ax1_twin.axhline(92.86, color='#27ae60', linestyle=':', label='k=2 (92.86%)')

    # --- Đồ thị 2: Tốc độ hội tụ sai số chuẩn L1 của Power Iteration ---
    ax2 = fig.add_subplot(1, 3, 2)
    err1 = ex1_data["err_hist1"]
    err2 = ex1_data["err_hist2"]

    ax2.semilogy(range(1, len(err1) + 1), err1, '-o', markersize=4, color='#2980b9',
                 linewidth=1.8, label=r'Ví dụ 1 (4 trang, $|\lambda_2|=0.465$)')
    ax2.semilogy(range(1, len(err2) + 1), err2, '-s', markersize=3, color='#e67e22',
                 linewidth=1.8, label=r'Ví dụ 2 (5 trang, $|\lambda_2|=0.850$)')
    ax2.axhline(1e-6, color='red', linestyle='--', linewidth=1.2, label=r'Ngưỡng dừng $\epsilon = 10^{-6}$')

    ax2.set_xlabel('Bước lặp (k)')
    ax2.set_ylabel(r'Sai số chuẩn $L_1$: $||\pi^{(k)} - \pi^{(k-1)}||_1$')
    ax2.set_title('Tốc độ hội tụ Power Iteration\n(Thang đo Logarit cơ số 10)', fontweight='bold')
    ax2.grid(True, which="both", linestyle='--', alpha=0.5)
    ax2.legend(loc='upper right', fontsize=9)

    # --- Đồ thị 3: So sánh phân phối điểm PageRank Ví dụ 2 (Khi d=1.0 và d=0.85) ---
    ax3 = fig.add_subplot(1, 3, 3)
    H2 = ex1_data["H2"]
    a2 = ex1_data["a2"]
    pi_exact2 = ex1_data["pi_exact2"]
    
    # Ma trận ngẫu nhiên S2 khi d = 1.0
    S2 = H2 + (1.0 / 5.0) * np.outer(np.ones(5), a2)
    # Lũy thừa ma trận S2^100 để mô phỏng bẫy liên kết
    S2_power = np.linalg.matrix_power(S2, 100)
    pi_trap = (S2_power @ (np.ones(5) / 5.0)) * 100
    pi_google = pi_exact2 * 100

    labels = ['P1\n(Home)', 'P2\n(Category)', 'P3\n(Spider Trap)', 'P4\n(PDF cụt)', 'P5\n(Spider Trap)']
    x = np.arange(len(labels))
    width = 0.35

    ax3.bar(x - width/2, pi_trap, width, label=r'$d = 1.0$ (Bẫy hút cạn điểm)', color='#e74c3c', alpha=0.85)
    ax3.bar(x + width/2, pi_google, width, label=r'$d = 0.85$ (Ma trận Google $G_2$)', color='#2ecc71', alpha=0.85)

    ax3.set_ylabel('Điểm PageRank (%)')
    ax3.set_title('Hiệu quả triệt tiêu Bẫy liên kết\n(Ví dụ 2)', fontweight='bold')
    ax3.set_xticks(x)
    ax3.set_xticklabels(labels, fontsize=9)
    ax3.grid(True, axis='y', linestyle='--', alpha=0.6)
    ax3.legend(loc='upper left', fontsize=9)

    plt.tight_layout()
    plt.savefig(save_path, dpi=300)
    print(f"Đã xuất hình ảnh trực quan hóa đồ thị thành công tại: {save_path}")


# =============================================================================
# CHƯƠNG TRÌNH CHÍNH (MAIN ENTRY POINT)
# =============================================================================

if __name__ == "__main__":
    svd_res = run_recommender_svd()
    pr_res = run_pagerank_examples()
    plot_visualizations(pr_res, svd_res, save_path="btl_dstt_visualizations.png")
    print("\nHoàn tất thực thi toàn bộ chương trình Python!")
