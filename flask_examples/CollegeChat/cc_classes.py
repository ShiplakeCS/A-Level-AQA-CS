#from app import get_db
from abc import ABC, abstractmethod
from datetime import datetime
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash


# Comment out when using with flask! ONLY FOR TESTING CLASSES!
def get_db():
    db = sqlite3.connect('CC.db')
    db.row_factory = sqlite3.Row
    return db



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

    @property
    def chatroom_memberships(self):
        return self.__get_chatroom_memberships_for_user()

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

    def __get_chatroom_memberships_for_user(self):

        db = get_db()

        crm_rows = db.execute("SELECT ChatroomID, Owner, Confirmed FROM ChatRoomMembership WHERE UserID=?", [self.id]).fetchall()

        crms = []

        for row in crm_rows:

            crms.append(
                ChatroomMembership(
                    Chatroom(row['ChatroomID']),
                    self,
                    bool(row['Confirmed']),
                    bool(row['Owner'])
                )
            )

        return crms

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

class MessageAttachmentTypeError(Exception):
    pass

class MessageAttachment(DBObject):

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

    @staticmethod
    def add_to_db(message, AttachmentType, OriginalFilePath, ThumbnailPath):

        db = get_db()

        cur = db.cursor()

        attachment_type_id = MessageAttachment.get_attachment_type_id(AttachmentType)

        try:
            cur.execute("INSERT INTO Attachment (MessageID, AttachmentTypeID, OriginalFilePath, ThumbnailFilePath) VALUES (?, ?, ?, ?)", [message.id, attachment_type_id, OriginalFilePath, ThumbnailPath])
            new_attachment_id = cur.lastrowid
            db.commit()

            return MessageAttachment(new_attachment_id)

        except sqlite3.Error as e:
            db.rollback()
            raise e

    @staticmethod
    def get_attachment_type_id(attachment_type):

        db = get_db()

        attachment_type_row = db.execute("SELECT ID FROM AttachmentType WHERE Description=?", [attachment_type]).fetchone()

        if not attachment_type_row:
            raise MessageAttachmentTypeError("{} is not a valid message attachment type!".format(attachment_type))

        return int(attachment_type_row['ID'])

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
        return Chatroom(self.__chatroomID)

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

    def add_attachment(self, attachment_type, original_file_path, thumbnail_file_path):

        a = MessageAttachment.add_to_db(self, attachment_type, original_file_path, thumbnail_file_path)

        return a

    def __get_attachments(self):

        db = get_db()

        attachment_rows = db.execute("SELECT ID FROM Attachment WHERE MessageID=?", [self.id]).fetchall()

        attachment_list = []

        for row in attachment_rows:
            attachment_list.append(MessageAttachment(int(row['ID'])))

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

class ChatroomNotFoundError(Exception):
    pass

class ChatroomConfirmMemberError(Exception):
    pass

class ChatroomRemoveMemberError(Exception):
    pass

class ChatroomAddMemberError(Exception):
    pass

class ChatroomMembership:

    def __init__(self, cr, u, confirmed, owner):

        self.chatroom = cr
        self.member = u
        self.confirmed = confirmed
        self.owner = owner

class Chatroom(DBObject):

    def __init__(self, id):

        self.__id = id

        db = get_db()

        chatroom_row = db.execute("SELECT Name, isPrivate, CreatedTS, Disabled FROM ChatRoom WHERE ID=?", [id]).fetchone()

        if not chatroom_row:
            raise ChatroomNotFoundError("No Chatroom with ID {} found in DB".format(self.__id))

        self.__name = chatroom_row['Name']
        self.__private = bool(chatroom_row['isPrivate'])
        self.__disabled = bool(chatroom_row['Disabled'])
        self.__createdTS = datetime.fromtimestamp(float(chatroom_row['CreatedTS']))

        self.__updates_pending = False

    @property
    def id(self):
        return self.__id

    @property
    def name(self):
        return self.__name

    @property
    def private(self):
        return self.__private

    @property
    def disabled(self):
        return self.__disabled

    @property
    def active(self):
        return not self.__disabled

    @property
    def createdTS(self):
        return self.__createdTS

    @property
    def messages(self):
        return self.__get_messages_for_chatroom()

    @property
    def owners(self):
        return self.__get_members_of_chatroom(True)

    @property
    def members(self):
        return self.__get_members_of_chatroom(False, True)

    @property
    def unconfirmed_members(self):

        ms = self.__get_members_of_chatroom(False, False)

        unconfirmed_members = []

        for m in ms:

            if not Chatroom.getMembershipStatus(self, m).confirmed:
                unconfirmed_members.append(m)

        return unconfirmed_members

    def disable(self, u:User):

        if u.userType == "Admin" or self.getMembershipStatus(self, u).owner:

            self.__disabled = True

            self.__updates_pending = True

        else:

            raise UserNotAdminError("Only administrator users or owners of chatrooms can disable the chatroom.")

    def enable(self, u:User):

        if u.userType == "Admin" or self.getMembershipStatus(self, u).owner:

            self.__disabled = False

            self.__updates_pending = True

        else:

            raise UserNotAdminError("Only administrator users or owners of chatrooms can enable the chatroom.")

    def __get_members_of_chatroom(self, get_owners_only=False, get_confirmed_only=False):

        db = get_db()

        members_list = []

        sql = "SELECT UserID FROM ChatRoomMembership WHERE ChatroomID=?"

        if get_owners_only:

            sql += " AND Owner=1"

        if get_confirmed_only:

            sql += " AND Confirmed=1"

        member_rows = db.execute(sql, [self.id]).fetchall()

        for row in member_rows:

            members_list.append(User(int(row['UserID'])))

        return members_list

    def __get_messages_for_chatroom(self, since_id=None):

        db = get_db()

        messages_list = []

        sql = "SELECT Message.ID FROM Message WHERE Message.ChatroomID=?"

        values = [self.id]

        if since_id:
            sql += " AND Message.ID > ?"
            values.append(since_id)

        message_rows = db.execute(sql, values).fetchall()

        for row in message_rows:
            messages_list.append(Message(int(row['ID'])))

        return messages_list

    def get_new_messages(self, since_id):
        return self.__get_messages_for_chatroom(since_id)

    @staticmethod
    def add_to_db(name, private:bool, creator:User):

        db = get_db()

        cur = db.cursor()

        try:
            cur.execute("INSERT INTO ChatRoom (Name, isPrivate, Disabled, CreatedTS) VALUES (?, ?, ?, ?)",
                        [name, int(private), 0, datetime.now().timestamp()])

            new_chatroom_id = cur.lastrowid

            # Add the creator user as the owner of the chatroom by adding a ChatRoomMembership record
            cur.execute("INSERT INTO ChatRoomMembership (UserID, ChatroomID, Owner, Confirmed) VALUES (?, ?, ?, ?)",
                        [creator.id, new_chatroom_id, 1, 1])

            db.commit()

            return Chatroom(new_chatroom_id)

        except sqlite3.Error as e:
            db.rollback()
            raise e

    def update_in_db(self):

        if self.__updates_pending:

            db = get_db()

            try:

                db.execute("UPDATE ChatRoom SET Name = ?, isPrivate = ?, Disabled = ? WHERE ID=?",
                           [self.name, self.private, int(self.disabled), int(self.id)])

                db.commit()

            except sqlite3.Error as e:

                db.rollback()
                raise e

    def delete_from_db(self, auth_user:User):

        if auth_user.userType != "Admin":
            raise UserNotAdminError("Only administrator users can delete chatrooms from the database!")

        db = get_db()

        try:
            db.execute("DELETE FROM ChatRoom WHERE ID=?", [self.id])
            db.execute("DELETE FROM ChatRoomMembership WHERE ChatroomID=?", [self.id])
            db.commit()

        except sqlite3.Error as e:
            db.rollback()
            raise e

    def add_member(self, u: User, is_owner=False, confirmed=False):

        all_members_ids = []

        for m in self.__get_members_of_chatroom(False, False):
            all_members_ids.append(m.id)

        if u.id not in all_members_ids:

            db = get_db()

            try:

                db.execute("INSERT INTO ChatRoomMembership (UserID, ChatroomID, Owner, Confirmed) VALUES (?, ?, ?, ?)", [u.id, self.id, int(is_owner), int(confirmed)])

                db.commit()

            except sqlite3.Error as e:

                db.rollback()
                raise e

    def remove_member(self, u:User):

        # Check user to be removed isn't last owner of group

        owner_ids = [u.id for u in self.owners]

        if len(owner_ids) == 1 and u.id in owner_ids:
            raise ChatroomRemoveMemberError("Cannot remove user {} as they are the only remaining owner for chatroom {}".format(u.username, self.id))

        member_ids = [u.id for u in self.__get_members_of_chatroom(False, False)]

        if u.id not in member_ids:
            raise ChatroomRemoveMemberError("User {} not a member of chatroom {}".format(u.id, self.id))

        db = get_db()

        try:

            db.execute("DELETE FROM ChatRoomMembership WHERE ChatroomID=? AND UserID=?", [self.id, u.id])
            db.commit()

        except sqlite3.Error as e:

            db.rollback()
            raise e

    def confirm_member(self, u: User):

        member_ids = []

        for m in self.__get_members_of_chatroom(False, False):
            member_ids.append(m.id)

        if u.id not in member_ids:
            raise ChatroomConfirmMemberError("User {} not a member of chatroom {}, cannot therefore confirm their membership!".format(u.username, self.id))

        db = get_db()

        try:
            db.execute("UPDATE ChatRoomMembership SET Confirmed = 1 WHERE UserID = ? AND ChatroomID = ?", [u.id, self.id])
            db.commit()

        except sqlite3.Error as e:
            db.rollback()
            raise e

    def set_member_as_owner(self, u: User):

        member_ids = [m.id for m in self.__get_members_of_chatroom(False, True)]

        if u.id not in member_ids:
            raise ChatroomConfirmMemberError("User {} not a member of chatroom {}, cannot therefore make them an owner!".format(u.username, self.id))

        db = get_db()

        try:

            db.execute("UPDATE ChatRoomMembership SET Owner = 1 WHERE ChatroomID = ? and UserID = ?", [self.id, u.id])
            db.commit()

        except sqlite3.Error as e:

            db.rollback()
            raise e

    def add_message(self, contents, sender: User, sender_ip, sender_ua):

        m = Message.add_to_db(contents, sender.id, self.id, sender_ip, sender_ua)

        return m

    @staticmethod
    def getMembershipStatus(cr, u: User):

        db = get_db()

        member_row = db.execute("SELECT Owner, Confirmed FROM ChatRoomMembership WHERE ChatroomID = ? AND UserID = ?", [cr.id, u.id]).fetchone()

        if member_row:

            ms = ChatroomMembership(cr, u, bool(member_row['Confirmed']),
                                    bool(member_row['Owner']))
            return ms

        else:

            return None


if __name__ == '__main__':


    cr = Chatroom(1)

    print(cr.name)
    print("--------")

    cr.add_message("Testing adding a new message via chatroom!", User(2), "192.168.0.1", "Some browser")

    for m in cr.messages:
        print("FROM: {}\t\tDATE: {}".format(m.sender.username, m.ts.isoformat()))
        print(m.contents)
        print("*** END OF MESSAGE ***\n")

    cr.add_member(User(1))
    cr.confirm_member(User(1))
    for member in cr.members:
        print(member.username)

    cr.set_member_as_owner(User(1))


    for member in cr.owners:
        print(member.username)


    u = User(1)

    for crm in u.chatroom_memberships:

        print(crm.chatroom.name)


    m = Message(5)

    m.add_attachment("Video", "video.avi", "video_thumb.jpg")

    for a in m.attachments:
        print("Message attachment found: {}".format(a.id))