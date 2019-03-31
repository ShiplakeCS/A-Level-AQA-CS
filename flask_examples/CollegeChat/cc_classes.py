from app import get_db
from abc import ABC, abstractmethod
from datetime import datetime
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

class DBObject(ABC):

    @abstractmethod
    def __init__(self, id:int):
        pass

    @abstractmethod
    def add_to_db(self):
        pass

    @abstractmethod
    def update_in_db(self):
        pass

    @abstractmethod
    def delete_from_db(self):
        pass

class UserNotFoundError(Exception):
    pass

class UserNotAdminError(Exception):
    pass

class User(DBObject):

    def __init__(self, id):

        self.__id = id

        db = get_db()

        user_row = db.execute("SELECT User.Username, User.Email, UserType.Description, User.JoinTS, User.LastLoginTS FROM User, UserType WHERE User.UserTypeID = UserType.ID AND User.ID = ?", [id]).fetchone()

        if not user_row:
            raise UserNotFoundError("No User found with ID {}".format(id))

        self.__username = user_row['Username']
        self.__userType = user_row['Description']
        self.__email = user_row['Email']
        self.__joined = datetime.fromtimestamp(user_row['JoinTS'])
        # UPDATED FROM VIDEO - My previous method did NOT work! replace self.__lastLogin = with the code below
        self.__lastLogin = datetime.fromtimestamp(user_row['LastLoginTS']) if user_row['LastLoginTS'] else None
        self.__pendingChanges = False

    @property
    def id(self):
        return self.__id

    @property
    def username(self):
        return self.__username

    @property
    def userType(self):
        return self.__userType

    @userType.setter
    def set_UserType(self, t):

        if t not in User.get_valid_user_types():
            raise ValueError("Invalid UserType specified: {}".format(t))

        self.__userType = t
        self.__pendingChanges = True


    @property
    def email(self):
        return self.__email

    @email.setter
    def set_email(self, email):
        self.__email = email
        self.__pendingChanges = True


    @property
    def joined(self):
        return self.__joined

    @property
    def lastLogin(self):
        return self.__lastLogin

    @lastLogin.setter
    def set_lastLogin(self, ts):
        self.__lastLogin = datetime.fromisoformat(ts)
        self.__pendingChanges = True

    def update_in_db(self):
        if self.__pendingChanges:
            db = get_db()

            userTypeID = User.get_user_type_id_from_description(self.userType)

            try:
                db.execute("UPDATE User SET Email=?, LastLoginTS=?, UserTypeID=? WHERE ID=?", [self.email, self.lastLogin.isoformat(), userTypeID, self.id])
                db.commit()
            except sqlite3.Error as e:
                db.rollback()
                raise e

    def delete_from_db(self, auth_user):

        if auth_user.userType != "Admin":
            raise UserNotAdminError("Only administrator users can delete other users from the database!")

        db = get_db()

        try:
            db.execute("DELETE FROM User WHERE ID=?", [self.id])
            db.commit()
        except sqlite3.Error as e:
            db.rollback()
            raise e

    @staticmethod
    def add_to_db(username, email, password, usertype):

        db = get_db()

        cur = db.cursor()

        try:
            cur.execute("INSERT INTO User (Username, Email, Password, UserTypeID, JoinTS) VALUES (?, ?, ?, ?, ?)",
                    [username, email, generate_password_hash(password), User.get_user_type_id_from_description(usertype), datetime.now().timestamp()])
            new_user_id = cur.lastrowid
            db.commit()

            return User(new_user_id)

        except sqlite3.Error as e:
            db.rollback()
            raise e

    @staticmethod
    def get_user_type_id_from_description(description):
        db = get_db()
        return db.execute("SELECT ID FROM UserType WHERE Description = ?", [description]).fetchone()['ID']

    @staticmethod
    def get_valid_user_types():

        db = get_db()

        user_type_rows = db.execute("SELECT Description FROM UserType").fetchall()

        valid_user_types = []

        for row in user_type_rows:
            valid_user_types.append(row['Description'])

        return valid_user_types

class MessageAttachmentNotFoundError(Exception):
    pass

class MessageAttachement(DBObject):

    def __init__(self, id):

        self.__id = id

        db = get_db()

        attachment_row = db.execute("SELECT MessageID, AttachmentType.Description, OriginalFilePath, ThumbnailFilePath FROM Attachment, AttachmentType WHERE Attachment.AttachmentTypeID = AttachmentType.ID AND Attachment.ID = ?", [id]).fetchone()

        if not attachment_row:
            raise MessageAttachmentNotFoundError("No attachment with ID {} found in DB".format(self.__id))

        self.__parentMessageId = attachment_row['MessageID']
        self.__type = attachment_row['Description']
        self.__filepath = attachment_row['OriginalFilePath']
        self.__thumbnail_filepath = attachment_row['ThumbnailFilePath']

    @property
    def id(self):
        return self.__id

    @property
    def type(self):
        return self.__type

    @property
    def parent_message(self):
        return Message(self.__parentMessageId)

    @property
    def parent_message_id(self):
        return self.__parentMessageId

    @property
    def filepath(self):
        return self.__filepath

    @property
    def thumbnail(self):
        return self.__thumbnail_filepath

    def add_to_db(self):
        #TODO: Add ability to add attachments to DB. Check that parent message ID is valid first
        pass

    def update_in_db(self):
        pass

    def delete_from_db(self):
        pass

class MessageNotFoundError(Exception):
    pass

class Message(DBObject):
    
    def __init__(self, id):
        
        self.__id = id

        db = get_db()

        message_row = db.execute("SELECT Contents, SenderID, ChatroomID, TS, SenderIP, SenderUA FROM Message WHERE ID=?",[id]).fetchone()

        if not message_row:
            raise MessageNotFoundError("No Message found with ID {}".format(id))

        self.__contents = message_row['Contents']
        self.__senderID = message_row['SenderID']
        self.__chatroomID = message_row['ChatroomID']
        self.__ts = datetime.fromtimestamp(message_row['TS'])
        self.__senderIP = message_row['SenderIP']
        self.__senderUserAgent = message_row['SenderUA']

    @property
    def id(self):
        return self.__id

    @property
    def contents(self):
        return self.__contents

    @property
    def sender(self):
        return User(self.__senderID)

    @property
    def senderID(self):
        return self.__senderID

    @property
    def chatroomID(self):
        return self.__chatroomID

    @property
    def chatroom(self):
        return None # TODO: Return chatroom object when implemented

    @property
    def ts(self):
        return self.__ts

    @property
    def senderIP(self):
        return self.__senderIP

    @property
    def senderUA(self):
        return self.__senderUserAgent

    @property
    def attachments(self):
        return self.__get_attachments()

    def __get_attachments(self):

        db = get_db()

        attachment_rows = db.execute("SELECT ID FROM Attachment WHERE MessageID=?", [self.id]).fetchall()

        attachment_list = []

        for row in attachment_rows:
            attachment_list.append(MessageAttachement(int(attachment_rows['ID'])))

        return attachment_list

    @staticmethod
    def add_to_db(contents, senderID, chatroomID, senderIP, senderUA):

        db = get_db()

        cur = db.cursor()

        try:
            cur.execute("INSERT INTO Message (Contents, SenderID, ChatroomID, SenderIP, SenderUA, TS) VALUES (?, ?, ?, ?, ?, ?)",
                    [contents, senderID, chatroomID, senderIP, senderUA, datetime.now().timestamp()])
            new_message_id = cur.lastrowid
            db.commit()

            return Message(new_message_id)

        except sqlite3.Error as e:
            db.rollback()
            raise e

    def delete_from_db(self):
        pass

    def update_in_db(self):
        pass