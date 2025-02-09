import api.domain.company.repository as Repository 
from api.models.index import db, Company, User
import api.domain.users.controller as UserController

def create_company(body):
    cif = body['cif']
    name = body['name']

    existing_cif = Company.query.filter(Company.cif == cif).first()

    existing_name = Company.query.filter(Company.name == name).first()

    if existing_cif: 
        return {'msg': 'Company with the this CIF already exists in database', 'status': 400}

    if existing_name: 
        return {'msg': 'Company with the this name already exists in database', 'status': 400}

    new_user = UserController.create_new_user(body, 'admin')

    if isinstance(new_user, User):
        return Repository.create_company(body, new_user.id)

    return {'msg': new_user['msg'], 'status': new_user['status']}


def get_companies_list():
	all_companies = Repository.get_companies_list()
	return all_companies

def get_company_by_id(company_id):
    company = Repository.get_company_by_id(company_id)
    if company is None:
        return {'msg': 'Company does not exist in this database.', 'status': 404}
    return company

def get_company_by_user_id(user_id):
    user = User.query.get(user_id)
    if user is None: 
        return {'msg': 'User does not exist in this database.', 'status': 404}
    
    company_by_user_id = Repository.get_company_by_user_id(user_id)
    if company_by_user_id == []:
        return {'msg': 'User has no existing companies in this database.', 'status': 404}

    return company_by_user_id

def update_company(update_company, company_id, current_user_id):
    company = Company.query.get(company_id)

    company_user_id = company.user_id
    
    if current_user_id == company_user_id and company.user.role_id == 1:
        updated_company = Repository.update_company(update_company, company)
        return updated_company
    else: 
        return {'msg': 'You do not have rights to update this company!', 'status': 403}  

def delete_company(company_id, current_user_id):
    company = Company.query.get(company_id)
    
    if company is None:
        return {'msg': 'Company does not exist in this database.', 'status': 404}

    if company is None:
        return {'msg': 'Company does not exist in this database.', 'status': 404}

    company_user_id = company.user_id

    if current_user_id == company_user_id:
        deleted_company = Repository.delete_company(company) 
        return deleted_company
    else: 
        if current_user_id == company_user_id:
            deleted_company = Repository.delete_company(company) 
            return deleted_company
        else:
            return {'msg': 'You do not have rights to delete this company', 'status': 403}

    
