import pandas as pd
import warnings

def get_all_data():
    """
    모든 데이터 파일을 로드하고 필요한 경우 임시 데이터를 반환합니다.
    Returns:
        tuple: (df_reputation, df_research, df_cooperation, df_global)
    """
    # Excel 파일 읽기 시 발생하는 경고 무시
    warnings.simplefilter(action='ignore', category=UserWarning)

    try:
        df_reputation = pd.read_excel('data/reputation.xlsx')
    except FileNotFoundError:
        print("경고: 'data/reputation.xlsx' 파일을 찾을 수 없습니다. 임시 데이터를 사용합니다.")
        df_reputation = pd.DataFrame({
            'Year': [2024, 2025, 2026],
            'QS_Rank': [850, 800, 750],
            'QS_Rank_Domestic': [15, 12, 10],
            'THE_Rank': [900, 850, 800],
            'THE_Rank_Domestic': [20, 18, 16],
            'ARWU_Rank': [700, 650, 600],
            'ARWU_Rank_Domestic': [10, 9, 8],
            'QS_Overall': [16.53, 20.0, 30.8],
            'QS_Academic_Reputation': [4.5, 5.0, 7.9],
            'QS_Citations_Per_Faculty': [18.1, 25.0, 31.0],
            'QS_Faculty_Student_Ratio': [85.0, 90.0, 97.4],
            'QS_Employer_Reputation': [3.2, 4.0, 6.0]
        })

    try:
        df_research = pd.read_excel('data/research.xlsx')
    except FileNotFoundError:
        print("경고: 'data/research.xlsx' 파일을 찾을 수 없습니다. 임시 데이터를 사용합니다.")
        df_research = pd.DataFrame({
            'Year': [2023, 2024, 2025],
            'Funding': [100, 120, 150],
            'Citation': [1500, 1650, 1800]
        })

    try:
        df_cooperation = pd.read_excel('data/cooperation.xlsx')
    except FileNotFoundError:
        print("경고: 'data/cooperation.xlsx' 파일을 찾을 수 없습니다. 임시 데이터를 사용합니다.")
        df_cooperation = pd.DataFrame({
            'Year': [2023, 2024, 2025],
            'Tech_transfer': [5, 8, 12],
            'Patent_application': [50, 60, 70],
            'Patent_registration': [30, 40, 50],
            'Internship_rate': [0.15, 0.18, 0.22]
        })

    try:
        df_global = pd.read_excel('data/global.xlsx')
    except FileNotFoundError:
        print("경고: 'data/global.xlsx' 파일을 찾을 수 없습니다. 임시 데이터를 사용합니다.")
        df_global = pd.DataFrame({
            'Year': [2023, 2024, 2025],
            'Total_students': [500, 600, 750],
            '중국': [200, 250, 300],
            '베트남': [150, 180, 200],
            '말레이시아': [100, 120, 150],
            '기타': [50, 50, 100]
        })
    
    return df_reputation, df_research, df_cooperation, df_global
