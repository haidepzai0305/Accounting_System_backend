from datetime import datetime
from backend.extension import db
from backend.models.Report import Report
from backend.utils.id_generator import generate_id

def get_income_report_data(period=None):
    """Lấy dữ liệu mock cho Báo cáo kết quả hoạt động kinh doanh."""
    return {
        "period": period or "Tháng 3/2024",
        "rows": [
            {"label": "DOANH THU", "isSection": True},
            {"label": "Doanh thu bán hàng", "isSubItem": True, "amount": "1,200,000,000"},
            {"label": "TỔNG CỘNG DOANH THU", "isTotal": True, "amount": "1,200,000,000"},
            {"label": "CHI PHÍ", "isSection": True},
            {"label": "Chi phí lương", "isSubItem": True, "amount": "800,000,000"},
            {"label": "TỔNG CHI PHÍ", "isTotal": True, "amount": "800,000,000"}
        ],
        "profitAmount": "400,000,000",
        "profitPeriod": "Q1"
    }

def get_balance_sheet_data(date=None):
    """Lấy dữ liệu mock cho Bảng cân đối kế toán."""
    return {
        "date": date or "2024-03-20",
        "rows": [
            {"label": "TÀI SẢN", "isSection": True},
            {"label": "Tiền mặt", "isSubItem": True, "amount": "500,000,000"},
            {"label": "Tiền gửi ngân hàng", "isSubItem": True, "amount": "1,500,000,000"},
            {"label": "TỔNG CỘNG TÀI SẢN", "isTotal": True, "amount": "2,000,000,000"}
        ],
        "isBalanced": True
    }

def get_dashboard_chart_data():
    """Lấy dữ liệu mock cho biểu đồ Dashboard."""
    return {
        "expenseLabels": ["Lương", "Thuê văn phòng", "Marketing", "Điện nước"],
        "expenseValues": [800, 100, 50, 20],
        "trendLabels": ["T1", "T2", "T3"],
        "trendIncome": [1100, 1150, 1200],
        "trendExpense": [750, 780, 800]
    }

def get_all_reports(page=1, limit=20, status=None, report_type=None):
    """Lấy danh sách các báo cáo đã lưu."""
    query = Report.query
    if status:
        query = query.filter_by(status=status)
    if report_type:
        query = query.filter_by(type=report_type)
        
    total = query.count()
    reports = query.order_by(Report.created_at.desc()).offset((page - 1) * limit).limit(limit).all()
    
    return [r.to_dict() for r in reports], total

def get_report_by_id(report_id):
    """Lấy thông tin chi tiết của một báo cáo."""
    report = Report.query.filter_by(report_id=report_id).first()
    if not report:
        raise ValueError("Report not found")
    return report.to_dict()

def create_report(data, user_id):
    """Tạo mới một báo cáo."""
    report = Report(
        report_id=generate_id('RPT'),
        type=data.get('type', 'general'),
        period=data.get('period', ''),
        title=data.get('title', 'New Report'),
        data=data.get('data', {}),
        summary=data.get('summary', {}),
        status=data.get('status', 'draft'),
        generated_by=user_id,
        generated_at=datetime.utcnow()
    )
    db.session.add(report)
    db.session.commit()
    return report.to_dict()

def update_report(report_id, data, user_id):
    """Cập nhật thông tin một báo cáo."""
    report = Report.query.filter_by(report_id=report_id).first()
    if not report:
        raise ValueError("Report not found")
        
    if 'title' in data:
        report.title = data['title']
    if 'data' in data:
        report.data = data['data']
    if 'summary' in data:
        report.summary = data['summary']
    if 'status' in data:
        report.status = data['status']
        if report.status == 'published':
            report.published_by = user_id
            report.published_at = datetime.utcnow()
            
    db.session.commit()
    return report.to_dict()
    
def delete_report(report_id):
    """Xóa một báo cáo."""
    report = Report.query.filter_by(report_id=report_id).first()
    if not report:
        raise ValueError("Report not found")
        
    db.session.delete(report)
    db.session.commit()
    return True
