from sqlalchemy.orm import Session
from database.models import User, RepairPoint
from exceptions import DatabaseError
from security import get_password_hash, verify_password

def create_user(db: Session, name: str, surname: str, email: str, password: str, birth_date: str):
    try:
        hashed_password = get_password_hash(password)
        db_user = User(name=name, surname=surname, email=email, password=hashed_password, birth_date=birth_date)
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
    except Exception as e:
        db.rollback()
        raise DatabaseError(str(e))


def get_user(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()


def update_user(db: Session, user_id: int, name: str, surname: str, email: str, password: str, birth_date: str):
    try:
        db_user = db.query(User).filter(User.id == user_id).first()
        if db_user:
            if name:
                db_user.name = name
            if surname:
                db_user.surname = surname
            if email:
                db_user.email = email
            if password:
                db_user.password = get_password_hash(password)
            if birth_date:
                db_user.birth_date = birth_date
            db.commit()
            return db_user
        else:
            return None
    except Exception as e:
        db.rollback()
        raise DatabaseError(str(e))


def delete_user(db: Session, user_id: int):
    try:
        db_user = db.query(User).filter(User.id == user_id).first()
        if db_user:
            db.delete(db_user)
            db.commit()
            return db_user
        else:
            return None
    except Exception as e:
        db.rollback()
        raise DatabaseError(str(e))


def create_repair_point(db: Session, name: str, email: str, description: str, phone: str, user_id: int):
    try:
        db_repair_point = RepairPoint(name=name, email=email, description=description, phone=phone, user_id=user_id)
        db.add(db_repair_point)
        db.commit()
        db.refresh(db_repair_point)
        return db_repair_point
    except Exception as e:
        db.rollback()
        raise DatabaseError(str(e))


def get_repair_point(db: Session, repair_point_id: int):
    return db.query(RepairPoint).filter(RepairPoint.id == repair_point_id).first()


def get_all_repair_points(db: Session):
    return db.query(RepairPoint).all()


def update_repair_point(db: Session, repair_point_id: int, name: str, email: str, description: str, phone: str):
    try:
        db_repair_point = db.query(RepairPoint).filter(RepairPoint.id == repair_point_id).first()
        if db_repair_point:
            if name:
                db_repair_point.name = name
            if email:
                db_repair_point.email = email
            if description:
                db_repair_point.description = description
            if phone:
                db_repair_point.phone = phone
            db.commit()
            return db_repair_point
        else:
            return None
    except Exception as e:
        db.rollback()
        raise DatabaseError(str(e))


def delete_repair_point(db: Session, repair_point_id: int):
    try:
        db_repair_point = db.query(RepairPoint).filter(RepairPoint.id == repair_point_id).first()
        if db_repair_point:
            db.delete(db_repair_point)
            db.commit()
            return db_repair_point
        else:
            return None
    except Exception as e:
        db.rollback()
        raise DatabaseError(str(e))
