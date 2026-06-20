import streamlit as st

# Cấu hình trang web
st.set_page_config(
    page_title="App Tính Thuế TNCN Việt Nam 2026",
    page_icon="💰",
    layout="centered"
)

# Logo
st.image("logo.jpg.png")

# Thông tin
st.markdown("### 📝 **NGUYỄN HUỲNH NGỌC HÀ**")

st.title("💰 Ứng Dụng Tính Thuế Thu Nhập Cá Nhân")
st.write(
    "Cập nhật đầy đủ Lương, Thưởng, Tăng ca, Phụ cấp theo luật thuế mới nhất năm 2026"
)

st.markdown("---")

# Nhập dữ liệu
st.subheader("📋 Nhập thông tin thu nhập tháng này của bạn")

gross_salary = st.number_input(
    "1. Lương đóng BHXH (VND):",
    min_value=0,
    value=30000000,
    step=500000,
    format="%d"
)

gross_bonus_pay = st.number_input(
    "2. Tiền thưởng / Bonus (VND):",
    min_value=0,
    value=0,
    step=500000,
    format="%d"
)

overtime_pay = st.number_input(
    "3. Tiền lương tăng ca / làm thêm giờ (VND):",
    min_value=0,
    value=0,
    step=500000,
    format="%d"
)

st.markdown("**4. Các khoản phụ cấp nhận bằng tiền mặt:**")

col_sub1, col_sub2 = st.columns(2)

with col_sub1:
    lunch_allowance = st.number_input(
        "Phụ cấp ăn trưa (VND):",
        min_value=0,
        value=0,
        step=50000
    )

with col_sub2:
    other_allowance = st.number_input(
        "Phụ cấp điện thoại, xăng xe (VND):",
        min_value=0,
        value=0,
        step=50000
    )

dependents = int(
    st.number_input(
        "5. Số người phụ thuộc bạn đang nuôi dưỡng (người):",
        min_value=0,
        value=1,
        step=1
    )
)

st.markdown("---")


def tinh_thue_tncn(gross, bonus, overtime, lunch, other, deps):
    total_income = gross + bonus + overtime + lunch + other

    # Bảo hiểm bắt buộc
    bhxh = gross * 0.08
    bhyt = gross * 0.015
    bhtn = gross * 0.01

    total_insurance = bhxh + bhyt + bhtn

    # Giảm trừ gia cảnh
    self_reduction = 15_500_000
    dependent_reduction = deps * 6_200_000

    total_reduction = self_reduction + dependent_reduction

    # Khoản miễn thuế
    exempt_lunch = min(lunch, 730_000)
    exempt_allowance = other

    total_exempt_income = (
        overtime
        + exempt_lunch
        + exempt_allowance
    )

    # Thu nhập tính thuế
    assessable_income = max(
        0,
        total_income
        - total_exempt_income
        - total_insurance
        - total_reduction
    )

    # Biểu thuế lũy tiến
    tax = 0

    brackets = [
        {
            "limit": 10_000_000,
            "rate": 0.05,
            "desc": "Bậc 1: Đến 10 triệu đồng (5%)"
        },
        {
            "limit": 30_000_000,
            "rate": 0.10,
            "desc": "Bậc 2: Trên 10 đến 30 triệu đồng (10%)"
        },
        {
            "limit": 60_000_000,
            "rate": 0.20,
            "desc": "Bậc 3: Trên 30 đến 60 triệu đồng (20%)"
        },
        {
            "limit": 100_000_000,
            "rate": 0.30,
            "desc": "Bậc 4: Trên 60 đến 100 triệu đồng (30%)"
        },
        {
            "limit": float("inf"),
            "rate": 0.35,
            "desc": "Bậc 5: Trên 100 triệu đồng (35%)"
        }
    ]

    temp_income = assessable_income
    previous_limit = 0
    tax_breakdown = []

    for b in brackets:
        range_size = b["limit"] - previous_limit

        if temp_income <= 0:
            break

        taxable_in_bracket = min(temp_income, range_size)
        tax_in_bracket = taxable_in_bracket * b["rate"]

        tax += tax_in_bracket

        tax_breakdown.append({
            "Bậc thuế": b["desc"],
            "Thu nhập tính thuế ở bậc này":
                f"{taxable_in_bracket:,.0f} VND",
            "Tiền thuế phải nộp":
                f"{tax_in_bracket:,.0f} VND"
        })

        temp_income -= taxable_in_bracket
        previous_limit = b["limit"]

    net_salary = total_income - total_insurance - tax

    return {
        "total_income": total_income,
        "bhxh": bhxh,
        "bhyt": bhyt,
        "bhtn": bhtn,
        "total_insurance": total_insurance,
        "dependent_reduction": dependent_reduction,
        "exempt_lunch": exempt_lunch,
        "exempt_allowance": exempt_allowance,
        "assessable_income": assessable_income,
        "tax": tax,
        "net_salary": net_salary,
        "tax_breakdown": tax_breakdown
    }


if st.button("🧮 Tính Thuế & Nhận Kết Quả", type="primary"):

    res = tinh_thue_tncn(
        gross_salary,
        gross_bonus_pay,
        overtime_pay,
        lunch_allowance,
        other_allowance,
        dependents
    )

    st.markdown("---")

    st.subheader("🎯 Kết Quả Tính Toán Tóm Tắt")

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            label="Tổng thu nhập nhận được",
            value=f"{res['total_income']:,.0f} VND"
        )

        st.metric(
            label="Tổng bảo hiểm bắt buộc (10.5%)",
            value=f"{res['total_insurance']:,.0f} VND"
        )

    with col2:
        st.metric(
            label="Thuế TNCN phải nộp",
            value=f"{res['tax']:,.0f} VND"
        )

        st.metric(
            label="THỰC NHẬN VỀ TAY (NET)",
            value=f"{res['net_salary']:,.0f} VND"
        )

    st.markdown("---")

    st.subheader("📜 Giải Trình Chi Tiết Quy Trình Khấu Trừ")

    st.markdown(f"""
- **Tổng thu nhập phát sinh trong tháng:** `{res['total_income']:,.0f} VND`

- **Các khoản được miễn thuế:**
    - Tiền lương tăng ca: `{overtime_pay:,.0f} VND`
    - Tiền ăn trưa được miễn: `{res['exempt_lunch']:,.0f} VND`
    - Phụ cấp công việc: `{res['exempt_allowance']:,.0f} VND`

- **Các khoản bảo hiểm bắt buộc:**
    - BHXH (8%): `{res['bhxh']:,.0f} VND`
    - BHYT (1.5%): `{res['bhyt']:,.0f} VND`
    - BHTN (1%): `{res['bhtn']:,.0f} VND`
    - **Tổng bảo hiểm:** `{res['total_insurance']:,.0f} VND`

- **Giảm trừ gia cảnh:**
    - Bản thân người nộp thuế: `15,500,000 VND`
    - Người phụ thuộc: `{res['dependent_reduction']:,.0f} VND`
      (cho {dependents} người)

- **Thu nhập tính thuế:** `{res['assessable_income']:,.0f} VND`
""")

    if res["tax"] > 0:
        st.write(
            "📊 **Chi tiết số thuế theo biểu thuế lũy tiến từng phần:**"
        )

        st.table(res["tax_breakdown"])

    else:
        st.success(
            "Tuyệt vời! Sau khi áp dụng các khoản miễn trừ và giảm trừ gia cảnh, bạn không phải nộp thuế TNCN."
        )
