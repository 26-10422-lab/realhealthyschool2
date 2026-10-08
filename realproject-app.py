import streamlit as st
import pandas as pd
import numpy as np
import requests
import re
from datetime import date
import plotly.express as px
import plotly.graph_objects as go


# =========================================================
# 1. 기본 설정
# =========================================================

st.set_page_config(
    page_title="학교 세균·감염예방 연구소",
    page_icon="🧪",
    layout="wide",
    initial_sidebar_state="expanded",
)


# =========================================================
# 2. 전체 디자인
# =========================================================

st.markdown(
    """
    <style>

    /* 전체 배경 */
    .stApp {
        background: #f4fbf7;
    }

    /* 메인 영역 */
    .main .block-container {
        max-width: 1450px;
        padding-top: 2rem;
        padding-bottom: 3rem;
    }

    /* 사이드바 */
    section[data-testid="stSidebar"] {
        background: linear-gradient(
            180deg,
            #e7f8ef 0%,
            #f4fbf7 100%
        );
        border-right: 1px solid #cce9da;
    }

    section[data-testid="stSidebar"] > div {
        padding-top: 1.5rem;
    }

    /* 기본 글자 */
    html, body, [class*="css"] {
        font-family:
            Pretendard,
            "Noto Sans KR",
            Arial,
            sans-serif;
    }

    /* 제목 */
    h1 {
        color: #164b38 !important;
        font-weight: 800 !important;
        letter-spacing: -1px;
    }

    h2 {
        color: #1e5d46 !important;
        font-weight: 750 !important;
    }

    h3 {
        color: #267057 !important;
        font-weight: 700 !important;
    }

    /* 상단 연구소 헤더 */
    .lab-header {
        background:
            linear-gradient(
                135deg,
                #dff7e9 0%,
                #f7fffa 55%,
                #d9f3e7 100%
            );
        border: 1px solid #c4e7d5;
        border-radius: 24px;
        padding: 28px 32px;
        margin-bottom: 24px;
        box-shadow: 0 8px 25px rgba(40, 110, 78, 0.07);
    }

    .lab-title {
        font-size: 32px;
        font-weight: 850;
        color: #164b38;
        margin-bottom: 6px;
    }

    .lab-subtitle {
        color: #4d7565;
        font-size: 15px;
        line-height: 1.7;
    }

    .tag {
        display: inline-block;
        padding: 6px 12px;
        margin: 4px 5px 0 0;
        border-radius: 999px;
        background: #ffffff;
        border: 1px solid #c5e6d4;
        color: #267057;
        font-size: 12px;
        font-weight: 700;
    }

    /* 섹션 */
    .section-header {
        margin-top: 22px;
        margin-bottom: 14px;
    }

    .section-title {
        font-size: 22px;
        font-weight: 800;
        color: #1b5942;
    }

    .section-subtitle {
        font-size: 13px;
        color: #71887d;
        margin-top: 3px;
    }

    /* 카드 */
    .info-card {
        background: #ffffff;
        border: 1px solid #dceee4;
        border-radius: 18px;
        padding: 20px;
        margin-bottom: 15px;
        box-shadow: 0 5px 18px rgba(36, 98, 70, 0.055);
    }

    .info-card h3 {
        margin-top: 0;
    }

    /* KPI 카드 */
    .metric-card {
        background: #ffffff;
        border: 1px solid #d7ece0;
        border-radius: 18px;
        padding: 20px;
        min-height: 125px;
        box-shadow: 0 5px 18px rgba(36, 98, 70, 0.05);
    }

    .metric-label {
        font-size: 13px;
        color: #71887d;
        font-weight: 650;
        margin-bottom: 9px;
    }

    .metric-value {
        font-size: 30px;
        font-weight: 850;
        color: #18553d;
        line-height: 1.1;
    }

    .metric-caption {
        font-size: 12px;
        color: #8a9c93;
        margin-top: 9px;
    }

    /* 상태 */
    .status {
        display: inline-block;
        padding: 7px 13px;
        border-radius: 999px;
        font-size: 13px;
        font-weight: 800;
    }

    .status-low {
        background: #e5f7eb;
        color: #26704a;
    }

    .status-medium {
        background: #fff6d9;
        color: #8a6910;
    }

    .status-high {
        background: #ffe7e0;
        color: #a64c32;
    }

    /* 연구 포인트 */
    .research-card {
        background: #edf9f2;
        border-left: 5px solid #54ae7e;
        border-radius: 14px;
        padding: 18px 20px;
        margin: 12px 0;
        color: #365b4a;
        line-height: 1.75;
    }

    /* 사이드바 타이틀 */
    .side-title {
        color: #164b38;
        font-size: 22px;
        font-weight: 850;
        margin-bottom: 4px;
    }

    .side-subtitle {
        color: #638073;
        font-size: 12px;
        line-height: 1.5;
        margin-bottom: 18px;
    }

    /* 구분선 */
    hr {
        border: none;
        border-top: 1px solid #d9ece1;
        margin: 25px 0;
    }

    /* 버튼 */
    .stButton > button,
    .stLinkButton > a {
        border-radius: 11px !important;
        font-weight: 700 !important;
        border: 1px solid #b9dfca !important;
    }

    /* 입력창 */
    .stTextInput input,
    .stNumberInput input,
    .stDateInput input {
        border-radius: 10px !important;
    }

    /* 데이터프레임 */
    div[data-testid="stDataFrame"] {
        border: 1px solid #d8ebe0;
        border-radius: 14px;
        overflow: hidden;
    }

    /* 알림 */
    .stAlert {
        border-radius: 14px;
    }

    /* Footer */
    .footer {
        text-align: center;
        color: #8aa097;
        font-size: 12px;
        padding: 35px 0 10px;
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# =========================================================
# 3. NEIS 설정
# =========================================================

NEIS_BASE = "https://open.neis.go.kr/hub"

# NEIS Open API 인증키 발급 페이지
NEIS_KEY_URL = "https://open.neis.go.kr/portal/guide/actKeyPage.do"


# =========================================================
# 4. 공통 함수
# =========================================================

def safe_request(url, params=None, timeout=10):
    """API 요청을 안전하게 처리"""
    try:
        response = requests.get(
            url,
            params=params,
            timeout=timeout
        )

        response.raise_for_status()

        return response.json()

    except requests.exceptions.Timeout:
        return None

    except requests.exceptions.RequestException:
        return None

    except ValueError:
        return None


def clean_html(text):
    """NEIS 급식 데이터의 HTML 태그 제거"""
    if text is None:
        return ""

    text = str(text)

    text = re.sub(r"<br\s*/?>", "\n", text, flags=re.I)
    text = re.sub(r"<[^>]+>", "", text)

    return text.strip()


def section_title(icon, title, subtitle=""):
    st.markdown(
        f"""
        <div class="section-header">
            <div class="section-title">{icon} {title}</div>
            <div class="section-subtitle">{subtitle}</div>
        </div>
        """,
        unsafe_allow_html=True
    )


def metric_card(label, value, caption=""):
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-label">{label}</div>
            <div class="metric-value">{value}</div>
            <div class="metric-caption">{caption}</div>
        </div>
        """,
        unsafe_allow_html=True
    )


def status_html(text):
    if text in ["낮음", "안전", "양호"]:
        cls = "status-low"
    elif text in ["보통", "주의"]:
        cls = "status-medium"
    else:
        cls = "status-high"

    return f'<span class="status {cls}">{text}</span>'


def plot_style(fig, height=400):
    fig.update_layout(
        height=height,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(255,255,255,0)",
        font=dict(
            family="Noto Sans KR, Arial",
            color="#315848"
        ),
        margin=dict(l=30, r=20, t=50, b=40),
        legend=dict(
            bgcolor="rgba(255,255,255,0.7)"
        ),
    )

    return fig


def render_header():
    with st.container(border=True):
        st.markdown("## 🧪 학교 세균·감염예방 연구소")
        st.write(
            "학교 환경의 미생물 오염과 감염 확산을 데이터로 분석하고 "
            "예방 방법을 탐구하는 학교 연구용 대시보드"
        )

        tag_columns = st.columns(5)
        tags = [
            "🦠 감염예방",
            "🧫 환경오염",
            "🍱 급식위생",
            "📊 데이터분석",
            "🔬 학교연구",
        ]

        for column, tag in zip(tag_columns, tags):
            column.markdown(f"**{tag}**")
# =========================================================
# 5. NEIS 학교 검색
# =========================================================

def search_neis_school(api_key, school_name):
    if not api_key:
        return []

    if not school_name:
        return []

    url = f"{NEIS_BASE}/schoolInfo"

    params = {
        "KEY": api_key,
        "Type": "json",
        "pIndex": 1,
        "pSize": 100,
        "SCHUL_NM": school_name,
    }

    data = safe_request(url, params)

    if not data:
        return []

    result = []

    try:
        rows = data.get("schoolInfo", [])

        for block in rows:
            if not isinstance(block, dict):
                continue

            row_data = block.get("row", [])

            if not isinstance(row_data, list):
                continue

            for row in row_data:

                if not isinstance(row, dict):
                    continue

                if row.get("SCHUL_NM"):
                    result.append(
                        {
                            "학교명": row.get("SCHUL_NM", ""),
                            "교육청코드": row.get(
                                "ATPT_OFCDC_SC_CODE",
                                ""
                            ),
                            "학교코드": row.get(
                                "SD_SCHUL_CODE",
                                ""
                            ),
                            "주소": row.get(
                                "ORG_RDNMA",
                                ""
                            ),
                            "우편번호": row.get(
                                "ORG_RDNZC",
                                ""
                            ),
                        }
                    )

    except Exception:
        return []

    return result


# =========================================================
# 6. NEIS 급식 조회
# =========================================================

def get_neis_meal(
    api_key,
    office_code,
    school_code,
    target_date
):
    if not api_key:
        return None

    if not office_code or not school_code:
        return None

    url = f"{NEIS_BASE}/mealServiceDietInfo"

    ymd = target_date.strftime("%Y%m%d")

    params = {
        "KEY": api_key,
        "Type": "json",
        "pIndex": 1,
        "pSize": 100,
        "ATPT_OFCDC_SC_CODE": office_code,
        "SD_SCHUL_CODE": school_code,
        "MLSV_FROM_YMD": ymd,
        "MLSV_TO_YMD": ymd,
    }

    data = safe_request(url, params)

    if not data:
        return None

    try:
        blocks = data.get("mealServiceDietInfo", [])

        for block in blocks:

            if not isinstance(block, dict):
                continue

            rows = block.get("row", [])

            if not isinstance(rows, list):
                continue

            if len(rows) > 0:
                return rows[0]

    except Exception:
        pass

    return None


# =========================================================
# 7. 알레르기 번호
# =========================================================

ALLERGY_MAP = {
    "1": "난류",
    "2": "우유",
    "3": "메밀",
    "4": "땅콩",
    "5": "대두",
    "6": "밀",
    "7": "고등어",
    "8": "게",
    "9": "새우",
    "10": "돼지고기",
    "11": "복숭아",
    "12": "토마토",
    "13": "아황산류",
    "14": "호두",
    "15": "닭고기",
    "16": "쇠고기",
    "17": "오징어",
    "18": "조개류",
    "19": "잣",
}


def extract_allergy_numbers(text):
    if not text:
        return []

    numbers = re.findall(r"\d+", str(text))

    return sorted(
        set(numbers),
        key=lambda x: int(x)
    )


# =========================================================
# 8. 날씨
# =========================================================

def get_weather():
    """
    기본 위치: 대구
    Open-Meteo 사용
    """

    latitude = 35.8714
    longitude = 128.6014

    url = "https://api.open-meteo.com/v1/forecast"

    params = {
        "latitude": latitude,
        "longitude": longitude,
        "current": "temperature_2m,relative_humidity_2m",
        "timezone": "Asia/Seoul",
    }

    data = safe_request(url, params)

    if not data:
        return None

    try:
        current = data.get("current", {})

        return {
            "temperature": current.get(
                "temperature_2m"
            ),
            "humidity": current.get(
                "relative_humidity_2m"
            ),
            "time": current.get("time"),
        }

    except Exception:
        return None


# =========================================================
# 9. 식중독 위험 계산
# =========================================================

RISKY_FOOD_KEYWORDS = [
    "김밥",
    "샐러드",
    "나물",
    "생채",
    "무침",
    "회",
    "육회",
    "계란",
    "달걀",
    "어묵",
    "두부",
    "햄",
    "마요",
    "냉면",
    "우유",
]


def calculate_food_risk(
    temperature,
    humidity,
    menu_text
):
    score = 0

    # 기온
    if temperature >= 30:
        score += 35
    elif temperature >= 25:
        score += 25
    elif temperature >= 20:
        score += 15
    elif temperature >= 15:
        score += 7

    # 습도
    if humidity >= 80:
        score += 25
    elif humidity >= 70:
        score += 18
    elif humidity >= 60:
        score += 10
    elif humidity >= 50:
        score += 5

    # 음식 위험요인
    matched = []

    for keyword in RISKY_FOOD_KEYWORDS:
        if keyword in menu_text:
            matched.append(keyword)

    score += min(len(matched) * 4, 30)

    score = min(int(score), 100)

    if score >= 75:
        level = "높음"
        advice = (
            "온·습도와 메뉴 특성을 고려하면 식중독 예방관리가 "
            "특히 중요한 조건입니다. 조리 후 신속한 배식과 "
            "냉장·보온 관리가 중요합니다."
        )

    elif score >= 50:
        level = "주의"
        advice = (
            "식중독 위험요인이 일부 존재합니다. 조리기구와 "
            "손 위생, 음식의 보관온도를 주의해서 관리하세요."
        )

    elif score >= 25:
        level = "보통"
        advice = (
            "현재 조건은 중간 정도의 위험수준입니다. 기본적인 "
            "손 씻기와 조리환경 위생관리를 유지하세요."
        )

    else:
        level = "낮음"
        advice = (
            "현재 계산된 환경조건에서는 상대적으로 위험도가 낮습니다. "
            "기본적인 위생관리는 계속 유지하세요."
        )

    return score, level, advice, matched


# =========================================================
# 10. 감염확산 시뮬레이션
# =========================================================

def simulate_infection(
    population,
    initial_infected,
    days,
    handwashing,
    mask,
    ventilation
):
    susceptible = population - initial_infected
    infected = float(initial_infected)
    recovered = 0.0

    rows = []

    prevention = (
        handwashing * 0.30
        + mask * 0.30
        + ventilation * 0.40
    )

    beta = 0.32 * (
        1 - prevention * 0.75
    )

    recovery_rate = 0.10

    for day in range(days + 1):

        rows.append(
            {
                "일": day,
                "감수성 인구": susceptible,
                "현재 감염자": infected,
                "누적 회복자": recovered,
            }
        )

        new_infections = (
            beta
            * infected
            * susceptible
            / population
        )

        new_recoveries = (
            recovery_rate
            * infected
        )

        new_infections = min(
            new_infections,
            susceptible
        )

        susceptible -= new_infections

        infected += (
            new_infections
            - new_recoveries
        )

        recovered += new_recoveries

        infected = max(
            0,
            infected
        )

        recovered = min(
            population,
            recovered
        )

    return pd.DataFrame(rows)


# =========================================================
# 11. 학교 환경 오염 데이터
# =========================================================

SURFACE_DATA = pd.DataFrame(
    {
        "장소": [
            "교실 책상",
            "교실 문손잡이",
            "화장실 문손잡이",
            "화장실 세면대",
            "급식실 식탁",
            "급식실 의자",
            "계단 난간",
            "엘리베이터 버튼",
            "컴퓨터 키보드",
            "교무실 문손잡이",
        ],
        "오염지수": [
            52,
            78,
            83,
            71,
            66,
            43,
            76,
            81,
            69,
            58,
        ],
        "위험도": [
            "보통",
            "높음",
            "높음",
            "높음",
            "보통",
            "낮음",
            "높음",
            "높음",
            "보통",
            "보통",
        ],
    }
)


# =========================================================
# 12. 감염병 통계 데이터
# =========================================================

DISEASE_DATA = pd.DataFrame(
    {
        "주차": list(range(1, 13)),
        "인플루엔자": [
            22, 28, 35, 48,
            62, 77, 69, 57,
            43, 31, 25, 19
        ],
        "감염성 장염": [
            15, 18, 20, 25,
            31, 36, 40, 37,
            32, 27, 23, 20
        ],
        "호흡기감염": [
            35, 38, 41, 45,
            49, 54, 57, 55,
            51, 47, 44, 42
        ],
    }
)


# =========================================================
# 13. 병원체 데이터
# =========================================================

PATHOGENS = [
    {
        "이름": "인플루엔자 바이러스",
        "분류": "바이러스",
        "주요감염": "호흡기 감염",
        "전파": "비말·접촉",
        "예방": "손 씻기, 환기, 기침예절, 예방접종",
    },
    {
        "이름": "코로나바이러스",
        "분류": "바이러스",
        "주요감염": "호흡기 감염",
        "전파": "호흡기 분비물",
        "예방": "환기, 손 위생, 기침예절",
    },
    {
        "이름": "노로바이러스",
        "분류": "바이러스",
        "주요감염": "급성 위장관염",
        "전파": "분변-경구·오염된 음식",
        "예방": "손 씻기, 음식 위생",
    },
    {
        "이름": "로타바이러스",
        "분류": "바이러스",
        "주요감염": "장염",
        "전파": "분변-경구",
        "예방": "손 씻기, 위생관리",
    },
    {
        "이름": "아데노바이러스",
        "분류": "바이러스",
        "주요감염": "호흡기·결막염",
        "전파": "비말·접촉",
        "예방": "손 씻기, 환기",
    },
    {
        "이름": "RSV",
        "분류": "바이러스",
        "주요감염": "호흡기 감염",
        "전파": "비말·접촉",
        "예방": "손 위생, 환기",
    },
    {
        "이름": "장출혈성 대장균",
        "분류": "세균",
        "주요감염": "출혈성 장염",
        "전파": "오염된 음식·물",
        "예방": "충분한 가열, 손 씻기",
    },
    {
        "이름": "살모넬라",
        "분류": "세균",
        "주요감염": "식중독",
        "전파": "오염된 음식",
        "예방": "충분한 가열, 교차오염 방지",
    },
    {
        "이름": "황색포도상구균",
        "분류": "세균",
        "주요감염": "식중독·피부감염",
        "전파": "접촉·오염된 음식",
        "예방": "손 위생, 식품 위생",
    },
    {
        "이름": "캄필로박터",
        "분류": "세균",
        "주요감염": "장염",
        "전파": "오염된 육류·물",
        "예방": "충분한 가열",
    },
    {
        "이름": "리스테리아",
        "분류": "세균",
        "주요감염": "식중독",
        "전파": "오염된 식품",
        "예방": "냉장관리, 충분한 가열",
    },
    {
        "이름": "결핵균",
        "분류": "세균",
        "주요감염": "결핵",
        "전파": "공기",
        "예방": "환기, 조기검진",
    },
    {
        "이름": "폐렴구균",
        "분류": "세균",
        "주요감염": "폐렴·중이염",
        "전파": "비말",
        "예방": "손 위생, 예방접종",
    },
    {
        "이름": "연쇄상구균",
        "분류": "세균",
        "주요감염": "인두염 등",
        "전파": "비말·접촉",
        "예방": "손 씻기, 기침예절",
    },
    {
        "이름": "헬리코박터 파일로리",
        "분류": "세균",
        "주요감염": "위장 질환",
        "전파": "구강·분변 경로",
        "예방": "개인위생",
    },
    {
        "이름": "녹농균",
        "분류": "세균",
        "주요감염": "상처·기회감염",
        "전파": "오염된 물·접촉",
        "예방": "환경위생",
    },
    {
        "이름": "바실러스 세레우스",
        "분류": "세균",
        "주요감염": "식중독",
        "전파": "오염된 식품",
        "예방": "조리 후 신속한 냉각·보관",
    },
    {
        "이름": "클로스트리디움 퍼프린젠스",
        "분류": "세균",
        "주요감염": "식중독",
        "전파": "오염된 육류·대량조리식품",
        "예방": "적절한 가열·보관",
    },
    {
        "이름": "장염비브리오",
        "분류": "세균",
        "주요감염": "급성 장염",
        "전파": "어패류",
        "예방": "충분한 가열",
    },
    {
        "이름": "폐렴마이코플라스마",
        "분류": "세균",
        "주요감염": "호흡기 감염",
        "전파": "비말",
        "예방": "환기, 기침예절",
    },
]


# =========================================================
# 14. 개인 감염위험도
# =========================================================

def calculate_personal_risk(
    handwash,
    sleep,
    ventilation,
    crowded,
    mask,
    symptoms
):
    score = 0

    # 손 씻기
    if handwash <= 2:
        score += 25
    elif handwash <= 4:
        score += 15
    else:
        score += 5

    # 수면
    if sleep < 5:
        score += 25
    elif sleep < 7:
        score += 15
    elif sleep < 8:
        score += 5

    # 환기
    if ventilation == "거의 안 함":
        score += 20
    elif ventilation == "가끔":
        score += 10

    # 혼잡
    if crowded == "자주":
        score += 15
    elif crowded == "가끔":
        score += 8

    # 마스크
    if mask == "거의 안 씀":
        score += 10
    elif mask == "가끔":
        score += 5

    # 증상
    if symptoms == "있음":
        score += 20

    score = min(score, 100)

    if score >= 70:
        level = "높음"
        advice = (
            "감염 위험요인이 비교적 많이 존재합니다. "
            "손 씻기와 환기, 충분한 수면을 우선적으로 관리하세요."
        )

    elif score >= 40:
        level = "주의"
        advice = (
            "일부 위험요인이 있습니다. 생활습관과 학교 환경에서 "
            "감염예방 행동을 조금 더 강화하는 것이 좋습니다."
        )

    else:
        level = "낮음"
        advice = (
            "현재 입력한 생활습관 기준으로는 상대적으로 위험도가 낮습니다. "
            "현재의 예방습관을 계속 유지하세요."
        )

    return score, level, advice


# =========================================================
# 15. 사이드바
# =========================================================

with st.sidebar:

    st.markdown(
        """
        <div class="side-title">🧪 감염예방 연구소</div>
        <div class="side-subtitle">
            학교 환경과 감염 데이터를 한눈에 분석하는
            연구용 대시보드입니다.
        </div>
        """,
        unsafe_allow_html=True
    )

    st.divider()

    page = st.radio(
        "연구 메뉴",
        [
            "🏠 전체 대시보드",
            "🗺️ 학교 세균 지도",
            "🦠 감염확산 시뮬레이터",
            "📈 감염병 통계",
            "🍱 급식·식중독 위험",
            "🔬 세균·바이러스 도감",
            "🙋 나의 감염위험도",
        ],
    )

    st.divider()

    st.markdown("### 🔐 NEIS 데이터 연결")

    neis_key = st.text_input(
        "NEIS 인증키",
        type="password",
        placeholder="발급받은 인증키 입력",
        help="NEIS Open API에서 발급받은 인증키를 입력하세요."
    )

    st.link_button(
        "🔑 NEIS 인증키 발급",
        NEIS_KEY_URL,
        use_container_width=True
    )

    if neis_key:
        st.success("인증키가 입력되었습니다.")

    else:
        st.caption(
            "학교 검색과 급식 조회를 사용하려면 "
            "NEIS 인증키가 필요합니다."
        )

    st.divider()

    st.caption(
        "학교 세균·감염예방 연구소\n"
        "School Infection Prevention Lab"
    )


# =========================================================
# 16. 상단 헤더
# =========================================================

render_header()


# =========================================================
# PAGE 1. 전체 대시보드
# =========================================================

if page == "🏠 전체 대시보드":

    section_title(
        "📊",
        "연구 현황 한눈에 보기",
        "학교 환경·감염·급식 데이터를 한 화면에서 확인합니다."
    )

    avg_contamination = SURFACE_DATA["오염지수"].mean()
    max_contamination = SURFACE_DATA["오염지수"].max()
    high_count = (
        SURFACE_DATA["위험도"] == "높음"
    ).sum()

    latest_influenza = DISEASE_DATA[
        "인플루엔자"
    ].iloc[-1]

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        metric_card(
            "평균 환경 오염지수",
            f"{avg_contamination:.1f}",
            "학교 환경 예시 데이터 기준"
        )

    with c2:
        metric_card(
            "최대 오염지수",
            f"{max_contamination}",
            "가장 높은 측정 지점"
        )

    with c3:
        metric_card(
            "고위험 환경",
            f"{high_count}곳",
            "오염 위험도 '높음'"
        )

    with c4:
        metric_card(
            "최근 인플루엔자 지수",
            f"{latest_influenza}",
            "12주차 예시 데이터"
        )

    st.markdown("<br>", unsafe_allow_html=True)

    left, right = st.columns([1.35, 1])

    with left:

        section_title(
            "🗺️",
            "학교 환경 오염도",
            "측정 장소별 오염지수"
        )

        fig = px.bar(
            SURFACE_DATA.sort_values(
                "오염지수",
                ascending=True
            ),
            x="오염지수",
            y="장소",
            orientation="h",
            text="오염지수",
        )

        fig.update_traces(
            marker_color="#63b889",
            textposition="outside"
        )

        fig.update_xaxes(
            range=[0, 100],
            title="오염지수"
        )

        fig.update_yaxes(
            title=""
        )

        fig = plot_style(fig, 480)

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    with right:

        section_title(
            "📈",
            "감염병 추세",
            "12주간 주요 감염 관련 지수"
        )

        fig2 = px.line(
            DISEASE_DATA,
            x="주차",
            y=[
                "인플루엔자",
                "감염성 장염",
                "호흡기감염"
            ],
            markers=True,
        )

        fig2.update_xaxes(
            dtick=1,
            title="주차"
        )

        fig2.update_yaxes(
            title="지수"
        )

        fig2 = plot_style(fig2, 480)

        st.plotly_chart(
            fig2,
            use_container_width=True
        )

    section_title(
        "🔎",
        "오늘의 연구 포인트",
        "데이터를 해석할 때 확인할 핵심 내용"
    )

    st.markdown(
        """
        <div class="research-card">
        <b>① 접촉이 많은 장소를 우선 관리</b><br>
        문손잡이, 난간, 버튼처럼 여러 사람이 반복적으로 접촉하는 장소는
        환경 위생관리의 우선순위를 높게 설정할 수 있습니다.
        </div>

        <div class="research-card">
        <b>② 감염자 수와 회복자 수는 같은 의미가 아님</b><br>
        '현재 감염자'는 특정 시점에 감염 상태인 사람이고,
        '누적 회복자'는 지금까지 감염 후 회복한 사람을 모두 합한 값입니다.
        </div>

        <div class="research-card">
        <b>③ 급식 위험도는 하나의 요인만으로 결정되지 않음</b><br>
        기온, 습도, 메뉴 특성 등을 함께 고려해 위험도를 판단하도록 구성했습니다.
        </div>
        """,
        unsafe_allow_html=True
    )


# =========================================================
# PAGE 2. 학교 세균 지도
# =========================================================

elif page == "🗺️ 학교 세균 지도":

    section_title(
        "🗺️",
        "학교 세균·환경 오염 지도",
        "측정 데이터를 CSV로 직접 업로드해 학교 환경 오염도를 분석할 수 있습니다."
    )

    st.markdown(
        """
        <div class="info-card">
        <b>📁 측정 데이터 업로드</b><br>
        CSV 파일에 장소와 오염지수 데이터를 넣으면
        아래 분석 결과가 자동으로 변경됩니다.
        </div>
        """,
        unsafe_allow_html=True
    )

    uploaded_file = st.file_uploader(
        "학교 세균 측정 CSV 파일",
        type=["csv"],
        help="장소/위치 열과 오염지수/세균수/CFU/측정값 중 하나가 필요합니다."
    )

    if uploaded_file is not None:

        try:
            uploaded_df = pd.read_csv(
                uploaded_file,
                encoding="utf-8-sig"
            )

            location_candidates = [
                "장소",
                "위치",
                "측정장소",
                "측정 장소",
                "구역",
            ]

            value_candidates = [
                "오염지수",
                "세균수",
                "CFU",
                "측정값",
                "오염도",
            ]

            location_col = next(
                (
                    c for c in location_candidates
                    if c in uploaded_df.columns
                ),
                None
            )

            value_col = next(
                (
                    c for c in value_candidates
                    if c in uploaded_df.columns
                ),
                None
            )

            if location_col and value_col:

                new_df = pd.DataFrame(
                    {
                        "장소": uploaded_df[
                            location_col
                        ].astype(str),

                        "오염지수": pd.to_numeric(
                            uploaded_df[value_col],
                            errors="coerce"
                        ),
                    }
                )

                new_df = new_df.dropna(
                    subset=["오염지수"]
                )

                new_df["오염지수"] = new_df[
                    "오염지수"
                ].clip(0, 100)

                new_df["위험도"] = pd.cut(
                    new_df["오염지수"],
                    bins=[
                        -0.01,
                        24.99,
                        49.99,
                        100
                    ],
                    labels=[
                        "낮음",
                        "보통",
                        "높음"
                    ]
                ).astype(str)

                if len(new_df) > 0:
                    surface_df = new_df

                    st.success(
                        f"CSV 데이터 {len(surface_df)}건을 불러왔습니다."
                    )
                else:
                    surface_df = SURFACE_DATA.copy()
                    st.warning(
                        "유효한 측정값이 없어 예시 데이터를 표시합니다."
                    )

            else:

                surface_df = SURFACE_DATA.copy()

                st.warning(
                    "CSV 열 이름을 찾지 못했습니다. "
                    "예시 데이터를 표시합니다."
                )

        except Exception as e:

            surface_df = SURFACE_DATA.copy()

            st.error(
                f"CSV를 읽는 중 문제가 발생했습니다: {e}"
            )

    else:

        surface_df = SURFACE_DATA.copy()

    avg_value = surface_df[
        "오염지수"
    ].mean()

    max_value = surface_df[
        "오염지수"
    ].max()

    high_count = (
        surface_df["위험도"] == "높음"
    ).sum()

    sample_count = len(surface_df)

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        metric_card(
            "평균 오염지수",
            f"{avg_value:.1f}",
            "전체 측정값 평균"
        )

    with c2:
        metric_card(
            "최대 오염지수",
            f"{max_value:.1f}",
            "가장 높은 측정값"
        )

    with c3:
        metric_card(
            "고위험 지점",
            f"{high_count}곳",
            "오염지수 50 이상"
        )

    with c4:
        metric_card(
            "측정 지점",
            f"{sample_count}곳",
            "현재 데이터 기준"
        )

    section_title(
        "📊",
        "장소별 오염도",
        "오염지수가 높을수록 우선적인 위생관리가 필요합니다."
    )

    fig = px.bar(
        surface_df.sort_values(
            "오염지수",
            ascending=True
        ),
        x="오염지수",
        y="장소",
        orientation="h",
        text="오염지수",
    )

    fig.update_traces(
        marker_color="#62b887",
        textposition="outside"
    )

    fig.update_xaxes(
        range=[0, 100],
        title="오염지수"
    )

    fig.update_yaxes(title="")

    fig = plot_style(fig, 500)

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    section_title(
        "📋",
        "측정 데이터",
        "현재 분석에 사용되고 있는 원자료입니다."
    )

    display_df = surface_df.copy()

    display_df["위험도"] = display_df[
        "위험도"
    ].apply(
        lambda x: x
    )

    st.dataframe(
        display_df,
        use_container_width=True,
        hide_index=True
    )

    sample_csv = pd.DataFrame(
        {
            "장소": [
                "교실 책상",
                "문손잡이",
                "화장실 세면대"
            ],
            "오염지수": [
                42,
                78,
                65
            ],
        }
    )

    st.download_button(
        "⬇️ CSV 예시 파일 다운로드",
        data=sample_csv.to_csv(
            index=False
        ).encode("utf-8-sig"),
        file_name="학교_세균측정_예시.csv",
        mime="text/csv",
    )


# =========================================================
# PAGE 3. 감염확산 시뮬레이터
# =========================================================

elif page == "🦠 감염확산 시뮬레이터":

    section_title(
        "🦠",
        "감염확산 시뮬레이터",
        "손 씻기·마스크·환기 수준을 바꾸면서 감염확산 양상이 어떻게 달라지는지 비교합니다."
    )

    control_col, result_col = st.columns(
        [0.85, 1.55]
    )

    with control_col:

        st.markdown(
            '<div class="info-card">',
            unsafe_allow_html=True
        )

        st.markdown("### ⚙️ 시뮬레이션 조건")

        population = st.number_input(
            "전체 인원",
            min_value=10,
            max_value=5000,
            value=500,
            step=10,
        )

        initial_infected = st.number_input(
            "초기 감염자",
            min_value=1,
            max_value=max(
                1,
                population - 1
            ),
            value=min(
                5,
                population - 1
            ),
            step=1,
        )

        days = st.slider(
            "관찰 기간",
            min_value=7,
            max_value=60,
            value=30,
        )

        handwashing = st.slider(
            "손 씻기 실천 수준",
            0.0,
            1.0,
            0.6,
            0.05,
        )

        mask = st.slider(
            "마스크 예방 수준",
            0.0,
            1.0,
            0.4,
            0.05,
        )

        ventilation = st.slider(
            "환기 수준",
            0.0,
            1.0,
            0.6,
            0.05,
        )

        st.markdown(
            "</div>",
            unsafe_allow_html=True
        )

    result_df = simulate_infection(
        population,
        initial_infected,
        days,
        handwashing,
        mask,
        ventilation,
    )

    peak_infected = int(
        np.ceil(
            result_df[
                "현재 감염자"
            ].max()
        )
    )

    final_recovered = int(
        np.ceil(
            result_df[
                "누적 회복자"
            ].iloc[-1]
        )
    )

    final_infected = int(
        np.ceil(
            result_df[
                "현재 감염자"
            ].iloc[-1]
        )
    )

    with result_col:

        r1, r2, r3 = st.columns(3)

        with r1:
            metric_card(
                "🦠 동시에 가장 많았던 감염자",
                f"{peak_infected}명",
                "시뮬레이션 기간 중 최대 현재 감염자"
            )

        with r2:
            metric_card(
                "💚 마지막 날까지 회복한 누적 인원",
                f"{final_recovered}명",
                "시뮬레이션 종료 시 누적 회복자"
            )

        with r3:
            metric_card(
                "현재 감염자",
                f"{final_infected}명",
                "마지막 날의 감염 상태 인원"
            )

        fig = go.Figure()

        fig.add_trace(
            go.Scatter(
                x=result_df["일"],
                y=result_df["현재 감염자"],
                mode="lines+markers",
                name="현재 감염자",
                line=dict(
                    color="#e47c64",
                    width=3
                ),
            )
        )

        fig.add_trace(
            go.Scatter(
                x=result_df["일"],
                y=result_df["누적 회복자"],
                mode="lines+markers",
                name="누적 회복자",
                line=dict(
                    color="#55a978",
                    width=3
                ),
            )
        )

        fig.update_layout(
            title="감염자와 누적 회복자의 변화",
            xaxis_title="일",
            yaxis_title="인원",
        )

        fig = plot_style(
            fig,
            470
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    st.markdown(
        """
        <div class="research-card">
        <b>📌 결과를 읽는 방법</b><br>
        '동시에 가장 많았던 감염자'는 어느 한 시점에 감염 상태였던 사람의
        최대 규모입니다. 반면 '마지막 날까지 회복한 누적 인원'은
        시뮬레이션 동안 감염되었다가 회복한 사람을 누적한 값입니다.
        따라서 두 숫자가 서로 다른 것은 정상입니다.
        </div>
        """,
        unsafe_allow_html=True
    )

    section_title(
        "📋",
        "시뮬레이션 원자료",
        "날짜별 감수성 인구·현재 감염자·누적 회복자"
    )

    st.dataframe(
        result_df.round(2),
        use_container_width=True,
        hide_index=True
    )


# =========================================================
# PAGE 4. 감염병 통계
# =========================================================

elif page == "📈 감염병 통계":

    section_title(
        "📈",
        "감염병 통계 분석",
        "감염병별 추세를 비교하고 직접 CSV 데이터를 넣어 분석할 수도 있습니다."
    )

    uploaded_stats = st.file_uploader(
        "감염병 통계 CSV 업로드",
        type=["csv"],
        key="disease_csv"
    )

    if uploaded_stats:

        try:

            stats_df = pd.read_csv(
                uploaded_stats,
                encoding="utf-8-sig"
            )

            if "주차" not in stats_df.columns:

                st.warning(
                    "'주차' 열이 없어 기본 데이터를 사용합니다."
                )

                stats_df = DISEASE_DATA.copy()

        except Exception:

            st.warning(
                "CSV를 읽지 못해 기본 데이터를 사용합니다."
            )

            stats_df = DISEASE_DATA.copy()

    else:

        stats_df = DISEASE_DATA.copy()

    disease_columns = [
        c for c in stats_df.columns
        if c != "주차"
    ]

    if disease_columns:

        totals = (
            stats_df[disease_columns]
            .sum()
            .sort_values(
                ascending=False
            )
        )

        highest_name = totals.index[0]
        highest_total = totals.iloc[0]

        peak_values = {
            c: stats_df[c].max()
            for c in disease_columns
        }

        peak_name = max(
            peak_values,
            key=peak_values.get
        )

        c1, c2, c3 = st.columns(3)

        with c1:
            metric_card(
                "분석 감염병",
                f"{len(disease_columns)}종",
                "현재 데이터 열 기준"
            )

        with c2:
            metric_card(
                "누적 지수 최고",
                highest_name,
                f"{highest_total:.0f}"
            )

        with c3:
            metric_card(
                "최고 피크",
                peak_name,
                f"{peak_values[peak_name]:.0f}"
            )

        section_title(
            "📉",
            "감염병 추세",
            "주차별 감염 관련 지수 변화"
        )

        fig = px.line(
            stats_df,
            x="주차",
            y=disease_columns,
            markers=True,
        )

        fig.update_xaxes(
            dtick=1,
            title="주차"
        )

        fig.update_yaxes(
            title="감염 지수"
        )

        fig = plot_style(
            fig,
            480
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

        section_title(
            "📋",
            "통계 원자료",
            "연구 분석에 사용되는 데이터"
        )

        st.dataframe(
            stats_df,
            use_container_width=True,
            hide_index=True
        )


# =========================================================
# PAGE 5. 급식·식중독 위험
# =========================================================

elif page == "🍱 급식·식중독 위험":

    section_title(
        "🍱",
        "학교 급식·식중독 위험 분석",
        "NEIS 급식 데이터와 기온·습도를 함께 이용해 위험도를 계산합니다."
    )

    if not neis_key:

        st.markdown(
            """
            <div class="info-card">
            <h3>🔐 먼저 NEIS 인증키를 연결하세요</h3>
            <p>
            학교 검색과 급식 정보를 가져오려면
            NEIS Open API 인증키가 필요합니다.
            </p>
            </div>
            """,
            unsafe_allow_html=True
        )

        st.link_button(
            "🔑 NEIS Open API 인증키 발급 페이지",
            NEIS_KEY_URL,
            use_container_width=False
        )

    else:

        section_title(
            "🏫",
            "학교 검색",
            "학교명을 입력해 NEIS에 등록된 학교를 찾습니다."
        )

        school_query = st.text_input(
            "학교명",
            placeholder="예: ○○고등학교"
        )

        if st.button(
            "🔎 학교 검색",
            use_container_width=False
        ):

            if school_query.strip():

                with st.spinner(
                    "NEIS에서 학교 정보를 검색하고 있습니다..."
                ):

                    schools = search_neis_school(
                        neis_key,
                        school_query.strip()
                    )

                st.session_state[
                    "neis_schools"
                ] = schools

                if schools:
                    st.success(
                        f"{len(schools)}개의 학교를 찾았습니다."
                    )

                else:
                    st.warning(
                        "학교를 찾지 못했습니다. "
                        "학교명을 다시 확인해주세요."
                    )

            else:

                st.warning(
                    "학교명을 입력해주세요."
                )

        schools = st.session_state.get(
            "neis_schools",
            []
        )

        if schools:

            options = [
                f"{s['학교명']} | {s['주소']}"
                for s in schools
            ]

            selected_label = st.selectbox(
                "학교 선택",
                options
            )

            selected_index = options.index(
                selected_label
            )

            selected_school = schools[
                selected_index
            ]

            st.markdown(
                f"""
                <div class="info-card">
                <b>🏫 {selected_school['학교명']}</b><br>
                {selected_school['주소']}<br>
                교육청 코드:
                {selected_school['교육청코드']}
                &nbsp;&nbsp;|&nbsp;&nbsp;
                학교 코드:
                {selected_school['학교코드']}
                </div>
                """,
                unsafe_allow_html=True
            )

            meal_date = st.date_input(
                "급식 날짜",
                value=date.today()
            )

            if st.button(
                "🍱 급식 정보 조회",
                use_container_width=False
            ):

                with st.spinner(
                    "NEIS에서 급식 정보를 가져오는 중..."
                ):

                    meal = get_neis_meal(
                        neis_key,
                        selected_school[
                            "교육청코드"
                        ],
                        selected_school[
                            "학교코드"
                        ],
                        meal_date,
                    )

                st.session_state[
                    "selected_meal"
                ] = meal

            meal = st.session_state.get(
                "selected_meal"
            )

            if meal:

                menu_text = clean_html(
                    meal.get(
                        "DDISH_NM",
                        ""
                    )
                )

                allergy_text = meal.get(
                    "ORPLC_INFO",
                    ""
                )

                allergy_numbers = (
                    extract_allergy_numbers(
                        meal.get(
                            "DDISH_NM",
                            ""
                        )
                    )
                )

                st.markdown(
                    """
                    <div class="info-card">
                    <h3>🍚 오늘의 급식</h3>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

                st.text(
                    menu_text
                )

                if allergy_numbers:

                    allergy_names = [
                        ALLERGY_MAP.get(
                            n,
                            n
                        )
                        for n in allergy_numbers
                    ]

                    st.info(
                        "알레르기 번호: "
                        + ", ".join(
                            allergy_names
                        )
                    )

                weather = get_weather()

                if weather:

                    temperature = float(
                        weather["temperature"]
                    )

                    humidity = float(
                        weather["humidity"]
                    )

                    w1, w2, w3 = st.columns(3)

                    with w1:
                        metric_card(
                            "🌡️ 현재 기온",
                            f"{temperature:.1f}℃",
                            "Open-Meteo 현재값"
                        )

                    with w2:
                        metric_card(
                            "💧 현재 습도",
                            f"{humidity:.0f}%",
                            "Open-Meteo 현재값"
                        )

                    score, level, advice, matched = (
                        calculate_food_risk(
                            temperature,
                            humidity,
                            menu_text
                        )
                    )

                    with w3:
                        metric_card(
                            "⚠️ 식중독 위험지수",
                            f"{score}/100",
                            level
                        )

                    st.markdown(
                        f"""
                        <div class="info-card">
                        <h3>위험 수준: {status_html(level)}</h3>
                        <p>{advice}</p>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

                    if matched:

                        st.markdown(
                            f"""
                            <div class="research-card">
                            <b>🍴 메뉴에서 확인된 위험 관련 키워드</b><br>
                            {", ".join(matched)}
                            </div>
                            """,
                            unsafe_allow_html=True
                        )

                else:

                    st.warning(
                        "날씨 데이터를 가져오지 못했습니다."
                    )

            elif meal is False:

                st.warning(
                    "해당 날짜의 급식 정보가 없습니다."
                )


# =========================================================
# PAGE 6. 세균·바이러스 도감
# =========================================================

elif page == "🔬 세균·바이러스 도감":

    section_title(
        "🔬",
        "세균·바이러스 도감",
        "학교생활과 관련성이 높은 주요 병원체를 찾아보고 예방방법을 학습합니다."
    )

    pathogen_df = pd.DataFrame(
        PATHOGENS
    )

    search_word = st.text_input(
        "🔎 병원체 검색",
        placeholder="예: 노로바이러스, 살모넬라, 호흡기"
    )

    category = st.selectbox(
        "분류",
        [
            "전체",
            "바이러스",
            "세균",
        ]
    )

    filtered = pathogen_df.copy()

    if search_word:

        mask = (
            filtered.astype(str)
            .apply(
                lambda row: row.str.contains(
                    search_word,
                    case=False,
                    na=False
                ).any(),
                axis=1
            )
        )

        filtered = filtered[mask]

    if category != "전체":

        filtered = filtered[
            filtered["분류"] == category
        ]

    st.caption(
        f"검색 결과: {len(filtered)}개"
    )

    for _, row in filtered.iterrows():

        with st.expander(
            f"🦠 {row['이름']} · {row['분류']}"
        ):

            a, b = st.columns(2)

            with a:

                st.markdown(
                    f"""
                    **주요 감염:** {row['주요감염']}

                    **전파 경로:** {row['전파']}
                    """
                )

            with b:

                st.markdown(
                    f"""
                    **예방 방법**

                    {row['예방']}
                    """
                )

    st.divider()

    section_title(
        "🧠",
        "미니 퀴즈",
        "도감에서 배운 감염예방 지식을 확인해보세요."
    )

    quiz_question = st.selectbox(
        "문제",
        [
            "손 씻기가 감염예방에 도움이 되는 이유는?",
            "노로바이러스 예방에 가장 중요한 행동은?",
            "학교에서 호흡기 감염 예방에 도움이 되는 것은?",
        ]
    )

    quiz_options = {
        "손 씻기가 감염예방에 도움이 되는 이유는?": [
            "손에 묻은 병원체를 제거할 수 있기 때문에",
            "키가 커지기 때문에",
            "체온이 낮아지기 때문에",
            "공기가 깨끗해지기 때문에",
        ],
        "노로바이러스 예방에 가장 중요한 행동은?": [
            "손 씻기와 음식 위생관리",
            "운동장 달리기",
            "불을 끄기",
            "창문을 닫기",
        ],
        "학교에서 호흡기 감염 예방에 도움이 되는 것은?": [
            "환기와 기침예절",
            "물을 적게 마시기",
            "교실을 밀폐하기",
            "손을 씻지 않기",
        ],
    }

    correct_answers = {
        "손 씻기가 감염예방에 도움이 되는 이유는?":
            "손에 묻은 병원체를 제거할 수 있기 때문에",

        "노로바이러스 예방에 가장 중요한 행동은?":
            "손 씻기와 음식 위생관리",

        "학교에서 호흡기 감염 예방에 도움이 되는 것은?":
            "환기와 기침예절",
    }

    answer = st.radio(
        "정답을 선택하세요",
        quiz_options[quiz_question]
    )

    if st.button(
        "✅ 정답 확인"
    ):

        if answer == correct_answers[
            quiz_question
        ]:

            st.success(
                "정답입니다! 🎉"
            )

        else:

            st.error(
                "아쉽습니다. 도감 내용을 다시 확인해보세요."
            )


# =========================================================
# PAGE 7. 나의 감염위험도
# =========================================================

elif page == "🙋 나의 감염위험도":

    section_title(
        "🙋",
        "나의 감염위험도 체크",
        "생활습관과 학교생활 조건을 바탕으로 감염예방 위험요인을 확인합니다."
    )

    left, right = st.columns(
        [1, 1.25]
    )

    with left:

        st.markdown(
            '<div class="info-card">',
            unsafe_allow_html=True
        )

        st.markdown(
            "### 📝 생활습관 입력"
        )

        handwash = st.slider(
            "하루 손 씻기 횟수",
            0,
            15,
            5,
        )

        sleep = st.slider(
            "평균 수면시간",
            3.0,
            10.0,
            7.0,
            0.5,
        )

        ventilation = st.selectbox(
            "교실 환기",
            [
                "자주",
                "가끔",
                "거의 안 함",
            ]
        )

        crowded = st.selectbox(
            "사람이 많은 공간 이용",
            [
                "거의 없음",
                "가끔",
                "자주",
            ]
        )

        mask = st.selectbox(
            "마스크 사용",
            [
                "자주 씀",
                "가끔",
                "거의 안 씀",
            ]
        )

        symptoms = st.radio(
            "현재 감염 의심 증상",
            [
                "없음",
                "있음",
            ],
            horizontal=True
        )

        st.markdown(
            '</div>',
            unsafe_allow_html=True
        )

    score, level, advice = (
        calculate_personal_risk(
            handwash,
            sleep,
            ventilation,
            crowded,
            mask,
            symptoms,
        )
    )

    with right:

        metric_card(
            "나의 감염위험도",
            f"{score}/100",
            level
        )

        st.markdown(
            "<br>",
            unsafe_allow_html=True
        )

        fig = go.Figure(
            go.Indicator(
                mode="gauge+number",
                value=score,
                title={
                    "text": "감염위험도"
                },
                gauge={
                    "axis": {
                        "range": [0, 100]
                    },
                    "bar": {
                        "color": "#59ad7d"
                    },
                    "steps": [
                        {
                            "range": [0, 40],
                            "color": "#e6f5eb"
                        },
                        {
                            "range": [40, 70],
                            "color": "#fff4d5"
                        },
                        {
                            "range": [70, 100],
                            "color": "#ffe4dd"
                        },
                    ],
                },
            )
        )

        fig = plot_style(
            fig,
            330
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

        st.markdown(
            f"""
            <div class="info-card">
            <h3>💡 분석 결과</h3>
            <p>
            현재 계산된 위험수준은
            <b>{level}</b>입니다.
            </p>
            <p>{advice}</p>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown(
        """
        <div class="research-card">
        <b>⚠️ 연구용 참고사항</b><br>
        이 결과는 의학적 진단이 아니라 입력한 생활습관을
        비교·분석하기 위한 교육용 지표입니다.
        실제 증상이 있거나 건강상 문제가 의심되면
        보호자 또는 의료전문가에게 상담하세요.
        </div>
        """,
        unsafe_allow_html=True
    )


# =========================================================
# Footer
# =========================================================

st.markdown(
    """
    <div class="footer">
        🧪 학교 세균·감염예방 연구소 · 학교 연구 프로젝트용
    </div>
    """,
    unsafe_allow_html=True
)