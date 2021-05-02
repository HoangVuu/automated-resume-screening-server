from app.main.util.response import response_object
from app.main import db
from app.main.model.special_skills_model import SpecialSkillsModel


def get_all_company():
    return SpecialSkillsModel.query.all()

def get_a_skills_by_name(name, page, page_size=5):
    if name == None:
        query = SpecialSkillsModel.query.paginate(page, page_size, error_out=False)
    else:
        query = SpecialSkillsModel.query.filter(SpecialSkillsModel.name.contains(name)).paginate(page, page_size, error_out=False)

    skills = [ com for com in query.items ]
    has_next = query.has_next

    return skills, has_next

def add_new_skill(data):    
    skill = SpecialSkillsModel(
        name=data['name']
    )
    try:
        db.session.add(skill)
        db.session.commit()
        return response_object(200, "Thêm skill thành công", data=skill.to_json())
    except Exception as ex:
        return response_object(200, "Thêm skill thất bại", data=None)