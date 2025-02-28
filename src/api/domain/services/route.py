from flask import Blueprint, request
import api.domain.services.controller as Controller
from flask_jwt_extended import jwt_required, get_jwt_identity
from api.models.index import Services
import api.utilities.handle_response as Response

api = Blueprint('api/services', __name__)

@api.route('/<int:company_id>', methods=["POST"])
@jwt_required()
def create_new_service(company_id):
    current_user = get_jwt_identity()
    current_user_id = current_user['id']
    
    body = request.get_json()

    new_service = Controller.create_new_service(company_id, current_user_id, body)

    if isinstance(new_service, Services):
        return Response.response_ok('New service created successfully!', new_service.serialize())
    else:
        return Response.response_error(new_service['msg'], new_service['status'])

@api.route('/company/<int:company_id>', methods=['GET'])
def get_services_by_company(company_id):
    services_by_company = Controller.get_services_by_company(company_id)

    if isinstance(services_by_company, list):
        serialized_services = list(map(lambda service: service.serialize(), services_by_company))
        return Response.response_ok('List of all services of the company', serialized_services)
    else:
        return Response.response_error(services_by_company['msg'], services_by_company['status'])

@api.route('/<int:service_id>', methods=['GET'])
def get_single_service(service_id):
    service = Controller.get_single_service(service_id)

    if isinstance(service, Services):
        return Response.response_ok('Service was found in database.', service.serialize())
    else:
        return Response.response_error(service['msg'], service['status'])

@api.route('/<int:service_id>', methods=['PUT'])
@jwt_required()
def update_service(service_id):
    current_user = get_jwt_identity()
    current_user_id = current_user["id"]
    update_service = request.get_json()

    service = Controller.update_service(service_id, update_service,  current_user_id )
    if isinstance(service, Services):
        return Response.response_ok('Service has been updated in database.', service.serialize())
    else:
        return Response.response_error(service["msg"], service['status'])

@api.route('/<int:service_id>', methods=['PATCH'])
@jwt_required()
def delete_service(service_id):
    current_user = get_jwt_identity()
    current_user_id = current_user['id']

    service = Controller.delete_service(service_id, current_user_id)

    if isinstance(service, Services):
        return Response.response_ok('Service was deleted from database.', service.serialize())
    else:
        return Response.response_error(service['msg'], service['status'])
