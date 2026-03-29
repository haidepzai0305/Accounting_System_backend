from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity

from backend.services.report_service import (
    get_income_report_data,
    get_balance_sheet_data,
    get_dashboard_chart_data,
    get_all_reports,
    get_report_by_id,
    create_report,
    update_report,
    delete_report
)

report_bp = Blueprint('reports', __name__, url_prefix='/api/reports')

# --- Analytics Mock Data Endpoints ---

@report_bp.route('/income', methods=['GET'])
@jwt_required()
def get_report_income():
    try:
        data = get_income_report_data()
        return jsonify(data), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@report_bp.route('/balance', methods=['GET'])
@jwt_required()
def get_report_balance():
    try:
        data = get_balance_sheet_data()
        return jsonify(data), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@report_bp.route('/chart', methods=['GET'])
@jwt_required()
def get_report_chart():
    try:
        data = get_dashboard_chart_data()
        return jsonify(data), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400


# --- CRUD Endpoints for Report Model ---

@report_bp.route('', methods=['GET'])
@jwt_required()
def list_reports():
    try:
        page = int(request.args.get('page', 1))
        limit = int(request.args.get('limit', 20))
        status = request.args.get('status')
        report_type = request.args.get('type')
        
        reports, total = get_all_reports(page=page, limit=limit, status=status, report_type=report_type)
        return jsonify({
            'data': reports,
            'total': total,
            'page': page,
            'limit': limit
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@report_bp.route('/<report_id>', methods=['GET'])
@jwt_required()
def get_report(report_id):
    try:
        report = get_report_by_id(report_id)
        return jsonify(report), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@report_bp.route('', methods=['POST'])
@jwt_required()
def create_new_report():
    try:
        data = request.json
        user_identity = get_jwt_identity()
        user_id = user_identity.get('id') if isinstance(user_identity, dict) else user_identity
            
        report = create_report(data, user_id)
        return jsonify(report), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@report_bp.route('/<report_id>', methods=['PUT'])
@jwt_required()
def update_existing_report(report_id):
    try:
        data = request.json
        user_identity = get_jwt_identity()
        user_id = user_identity.get('id') if isinstance(user_identity, dict) else user_identity
            
        report = update_report(report_id, data, user_id)
        return jsonify(report), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@report_bp.route('/<report_id>', methods=['DELETE'])
@jwt_required()
def delete_existing_report(report_id):
    try:
        delete_report(report_id)
        return jsonify({'message': 'Report deleted successfully'}), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 400
