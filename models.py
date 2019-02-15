import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Course(db.Model):
    __tablename__ = "courses"
    course_id = db.Column(db.String, primary_key=True)
    name = db.Column(db.String, nullable=False)
    semester = db.Column(db.String, nullable=False)
    category = db.Column(db.String, nullable=False)
    credits = db.Column(db.Integer, nullable=False)
    booked_in = db.relationship("Schedule", backref="course", lazy=True)

    def add_course(self, course_id, name, semester, category, credits):
        c = Course(course_id=course_id, name=name, semester=semester, category=category, credits=credits)
        db.session.add(c)
        db.session.commit()

    def as_dict(self):
       return {c.name: getattr(self, c.name) for c in self.__table__.columns}

class Schedule(db.Model):
    __tablename__ = "schedules"
    id = db.Column(db.Integer, primary_key=True)
    course_id = db.Column(db.String, db.ForeignKey("courses.course_id"), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    semester = db.Column(db.String, nullable=False)
    realm = db.Column(db.String, nullable=False)
    minorMajor = db.Column(db.String, nullable=False)


class requisite(db.Model):
    __tablename__ = "requisites"
    id = db.Column(db.Integer, primary_key=True)
    minorMajor = db.Column(db.String, nullable=False)
    realm = db.Column(db.String, nullable=False)
    min_credits = db.Column(db.String, nullable=True)
    max_credits = db.Column(db.String, nullable=True)