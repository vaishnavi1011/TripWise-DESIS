from flask import Blueprint, render_template, request, flash, redirect, url_for, Response
from models import User, Token, Group, UserGroups
from werkzeug.security import generate_password_hash, check_password_hash
from __init__ import db
from flask_login import login_user, login_required, logout_user, current_user
import json
from flask import jsonify, make_response
from flask_cors import CORS, cross_origin
from auth import check_token

group = Blueprint('group', __name__)
CORS(group)


@group.route('/group/list_members', methods=['GET', 'OPTIONS'])
@cross_origin()
def listMembers():
    if request.method == "OPTIONS": # CORS preflight
        return _build_cors_preflight_response()
    headers= request.headers        
    try:
        request_user= check_token(headers.get("access_token"))
        all_users= User.query.all()
        result=[]
        for user in all_users:
            if user.id == request_user:
                continue
            data= {
                "id" : user.id,
                "username" : user.username,
                "phoneNumber" : user.phone_number,
                "email" : user.email
            }
            response = Response(json.dumps(result),status=200)
    except:
        response = Response("could not return all_users",status=404)

    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')

    return _corsify_actual_response(response)  


@group.route('/group/list', methods=['GET', 'OPTIONS'])
@cross_origin()
def listGroups():

    if request.method == "OPTIONS": # CORS preflight
        return _build_cors_preflight_response()
    headers= request.headers        
    try:
        creator= check_token(headers.get("access_token"))
        user_groups_creator= UserGroups.query.filter_by(user= creator).all()
        result=[]
        for user_group in user_groups_creator:
            group= user_group.group
            user_groups_group= UserGroups.query.filter_by(group= group).all()
            group_details= Group.query.filter_by(id= group).first()
            data={
                "name": group_details.name,
                "desc": group_details.description
            }
            members=[]
            for x in user_groups_group:
                member= User.objects.filter_by(id= x.user).first()
                member_details= {
                    "name": member.name,
                    "username": member.username,
                    "email": member.email,
                    "phoneNumber": member.phone_number
                }
                members.append(member_details)
            data["members"]= members
            result.append(data)

        response = Response(json.dumps(result),status=200)
    except:
        response = Response("could not create a group",status=404)

    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')

    return _corsify_actual_response(response)         


@group.route('/group/create', methods=['GET', 'POST', 'OPTIONS'])
@cross_origin()
def createGroup():

    if request.method == "OPTIONS": # CORS preflight
        return _build_cors_preflight_response()    

    data= request.data
    headers= request.headers
        
    try:
        data_dict= json.loads(data.decode('utf-8'))
        group_name= data_dict["groupName"]
        group_description= data_dict["groupDesc"]
        creator= check_token(headers.get("access_token"))
        new_group= Group(name=group_name,description= group_description)
        db.session.add(new_group)
        db.session.commit()
        print(new_group)
        print(new_group.id)
        
        user_groups_creator= UserGroups(group= new_group.id, user=creator)
        db.session.add(user_groups_creator)
        for x in data_dict["Members"]:
            new_user_group= UserGroups(group= new_group.id, user=x)
            db.session.add(new_user_group)
        db.session.commit()
        response = Response("done",status=200)
    except:
        response = Response("could not create a group",status=404)

    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')

    return _corsify_actual_response(response)         

def _build_cors_preflight_response():
    response = make_response()
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add('Access-Control-Allow-Headers', "*")
    response.headers.add('Access-Control-Allow-Methods', "*")
    return response

def _corsify_actual_response(response):
    # response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    response.headers.add("Access-Control-Expose-Headers","Authorization")
    return response
