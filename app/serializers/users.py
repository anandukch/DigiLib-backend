from app.common import UserRoleEnum, UserRoles


def userEntity(user) -> dict:
    return {
        "id": str(user["_id"]),
        "name": user["name"],
        "email": user["email"],
        "role": user["role"],
        "verified": user["verified"],
        "password": user["password"],
        "created_at": user["created_at"],
        "updated_at": user["updated_at"],
    }


def userResponseEntity(user, role: UserRoleEnum = UserRoles.STUDENT) -> dict:
    res={
        "id": str(user["_id"]),
        "name": user["name"],
        "email": user["email"],
        "role": user["role"],
        "created_at": user["created_at"],
        "updated_at": user["updated_at"],
    }
    
    if role == UserRoles.STUDENT:
        res["semester"] = user["semester"]
        res["department"] = user["department"]
        res["reg_no"] = user["reg_no"]
    return res


def embeddedUserResponse(user) -> dict:
    return {
        "id": str(user["_id"]),
        "name": user["name"],
        "email": user["email"],
    }


def userListEntity(users) -> list:
    return [userEntity(user) for user in users]

def userResponsesEntity(users, role: UserRoleEnum = UserRoles.STUDENT) -> list:
    return [userResponseEntity(user, role) for user in users]
