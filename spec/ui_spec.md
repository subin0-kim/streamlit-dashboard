# Performance Measurement Data Analysis Dashboard UI Specification

## 1. Navigation
- 상단에 탭 형태로 페이지 전환 가능
  - 📊 Dashboard: 성능 분석 대시보드
  - 📁 File Management: 파일 관리 페이지

## 2. Dashboard Page

### 2.1 Sidebar Layout
좌측 패널은 다음과 같은 순서로 구성되며, 각 섹션은 접을 수 있는 형태로 제공:

1. **Available Files** (기본 펼침)
   - 파일 목록 표시
   - 각 파일은 Alias로 표시
   - 마우스 오버 시 Description 툴팁으로 표시
   - 체크박스로 파일 선택
   - File Search에서 선택한 파일과 체크박스 상태 공유

2. **File Search**
   - 검색어 입력 필드
   - 실시간 검색 결과 표시
   - 검색된 파일도 체크박스로 선택 가능
   - Available Files와 체크박스 상태 동기화
   - 새로운 검색을 해도 이전 선택 상태 유지
   - 체크박스 상태는 세션 전체에서 유지

3. **Goodput Settings** (기본 접힘)
   - TTFT 설정 (기본값: 3.0)
   - TPOT 설정 (기본값: 0.2)

4. **File Upload** (기본 접힘)
   - CSV 파일 업로드 기능
   - 드래그 앤 드롭 지원

### 2.2 Main Content Area

#### 2.2.1 Performance Metrics Selection
- 체크박스 형태로 성능 지표 선택
- 선택된 지표는 즉시 화면에 표시
- 선택 가능한 지표:
  - TPM
  - TPM Trend
  - RPM
  - RPM Trend

#### 2.2.2 Visualization Area
- 선택된 지표에 따라 차트 자동 표시
- 각 차트는 전체 너비 사용
- 차트 아래에 Raw Data 섹션 (접을 수 있음)

## 3. File Management Page

### 3.1 File Upload Section
- 드래그 앤 드롭으로 여러 파일 동시 업로드 가능
- 각 파일에 대한 메타데이터 입력:
  - Alias (기본값: 파일명에서 .csv 제외)
  - Description
  - 기본값일 경우 연한 회색으로 표시
  - 클릭 시 전체 텍스트 선택되어 바로 수정 가능

### 3.2 File Listing Section
- 업로드된 파일 목록을 테이블 형태로 표시
- 컬럼:
  - Alias
  - Description
  - Upload Date
  - File Size

### 3.3 File Deletion Section
- 다중 선택 가능한 체크박스 제공
- 선택된 파일들을 한 번에 삭제 가능
- 삭제 전 확인 대화상자 표시

## 4. Color Scheme
- Primary: #1E88E5 (Blue)
- Secondary: #43A047 (Green)
- Background: #FFFFFF (White)
- Text: #333333 (Dark Gray)
- Default Value Text: #999999 (Light Gray)
- Hover: #F5F5F5 (Light Gray)

## 5. Responsive Design
- 모든 요소는 화면 크기에 따라 자동 조정
- 모바일 환경에서도 사용 가능하도록 최적화
- 사이드바는 화면이 좁을 때 자동으로 접힘

## 6. User Experience
- 모든 작업에 대한 즉각적인 피드백 제공
- 로딩 상태 표시
- 에러 메시지는 명확하고 해결 방법 제시
- 툴팁을 통한 추가 정보 제공

## 7. 성능 지표 시각화
- **TPM Bar Chart**:
  - Goodput 조건 만족 시 최대 TPM 표시
  - 각 bar 위에 TPM 값 오버레이로 표시
    - 1000 미만: 정수로 표시 (예: 856)
    - 1000 이상: K 단위로 표시 (예: 356K)
  - Raw Data 섹션 (접기 가능)
- **TPM Trend Line Chart**:
  - 배치 크기별 TPM 추이
  - Raw Data 섹션 (접기 가능)
- **RPM Bar Chart**:
  - Goodput 조건 만족 시 최대 RPM 표시
  - 각 bar 위에 RPM 값 오버레이로 표시
    - 1000 미만: 정수로 표시 (예: 856)
    - 1000 이상: K 단위로 표시 (예: 356K)
  - Raw Data 섹션 (접기 가능)
- **RPM Trend Line Chart**:
  - 배치 크기별 RPM 추이
  - Raw Data 섹션 (접기 가능)
- **Latency Line Chart**:
  - 배치 크기별 Latency 추이
  - Raw Data 섹션 (접기 가능)
- **First Token Line Chart**:
  - 배치 크기별 First Token 추이
  - Raw Data 섹션 (접기 가능)
- **decode Line Chart**:
  - 배치 크기별 decode 추이
  - Raw Data 섹션 (접기 가능)
- **Error Ratio Line Chart**:
  - 배치 크기별 Error Ratio 추이
  - Raw Data 섹션 (접기 가능)
- **Requests Line Chart**:
  - 배치 크기별 Requests 추이
  - Raw Data 섹션 (접기 가능)
- **AVG Output Tokens Bar Chart**:
  - 각 파일별 평균 AVG Output Tokens 표시
  - 각 bar 위에 평균값 오버레이로 표시
  - Raw Data 섹션 (접기 가능)

## 8. 데이터 표시 규칙
- **Goodput 조건**:
  - TTFT <= 설정값
  - TPOT <= 설정값
- **파일 선택에 따른 동작**:
  - 단일 파일: 개별 성능 지표 표시
  - 다중 파일: 비교 분석 그래프 표시
- **Raw Data 표시**:
  - 각 그래프 하단에 "Performance Summary - {지표명}" 섹션
  - 기본적으로 접힌 상태
  - 클릭 시 데이터 테이블 표시

## 9. 추가 기능 화면
- **데이터 관리 확장**:
  - 파일 그룹화 및 태그 관리
  - 고급 검색 및 필터링
  - 데이터 백업/복원

- **분석 기능**:
  - 성능 지표 상관관계 분석
  - 성능 한계점 시각화
  - 커스텀 지표 계산
  - 추세 분석 및 예측

- **사용자 인터페이스**:
  - 커스터마이징 가능한 대시보드
  - 그래프 스타일 설정
  - 리포트 생성
  - 상태 저장/불러오기 
