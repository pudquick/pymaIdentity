import pwd, grp, sys, os
from Collaboration import CBUserIdentity, CBGroupIdentity, CBIdentityAuthority
from SystemConfiguration import SCDynamicStoreCopyConsoleUser
from objc import NULL
from ctypes import *

def CurrentDesktopUser():
    # User account currently logged in locally to the machine, sitting at the Desktop
    # This works even with Fast User Switching
    # http://developer.apple.com/library/mac/#qa/qa1133/_index.html
    current_user = (SCDynamicStoreCopyConsoleUser(NULL, NULL, NULL) or [NULL])[0]
    if (current_user == u'loginwindow') or (current_user == NULL):
        current_user = None
    return User(current_user)

def CurrentEffectiveUser():
    # User account we're currently running this script with
    try:
        return User(os.geteuid())
    except:
        return User(None)

class Group:
    _fields = ('name', 'gid', 'hidden', 'uuid', 'fullname', '_id_obj')
    _gr_map = {'name': 'gr_name', 'gid': 'gr_gid'}
    
    def _init_with_grp(self, grp_entry):
        if isinstance(grp_entry, grp.struct_group):
            for key in self._gr_map.keys():
                setattr(self,key,getattr(grp_entry, self._gr_map[key]))
        if self.gid is not None:
            # Group exists, find extended information
            id_auth = CBIdentityAuthority.defaultIdentityAuthority()
            self._id_obj = CBGroupIdentity.groupIdentityWithPosixGID_authority_(self.gid, id_auth)
            if self._id_obj:
                # Make copies of the data as pure python objects, rather than keep translating
                if self._id_obj.UUIDString() is not None:
                    self.uuid   = str(self._id_obj.UUIDString())
                if self._id_obj.fullName() is not None:
                    self.fullname = str(self._id_obj.fullName())
                self.hidden  = bool(self._id_obj.isHidden())
    
    def __nonzero__(self):
        for i in self._fields:
            if getattr(self,i) is not None:
                return True
        return False
    
    def __str__(self):
        return self.name or ''
    
    def __int__(self):
        if self.gid is None:
            return -(sys.maxint)-1
        return self.gid
    
    def __hash__(self):
        return hash("%s %s" % (int(self),str(self)))
        
    def __eq__(self, other):
        if isinstance(other, Group):
            for i in self._fields:
                if getattr(self,i) != getattr(other,i):
                    return False
            return True
        elif other is None:
            if (self.name is None) and (self.gid is None):
                return True
            return False
        elif isinstance(other, basestring):
            if self.name == other:
                return True
            return False
        elif isinstance(other, (int,long)):
            if self.gid == other:
                return True
            return False
        return False
    
    def __ne__(self, other):
        return not self.__eq__(other)
    
    def __init__(self, name_or_gid = None):
        # If passed a string, assume group name
        # If passed a number, assume gid
        # If None, leave everything with a value of None
        
        # Initialize everything to None
        for i in self._fields:
            setattr(self, i, None)
        
        # Determine whether we were passed a name or a uid
        if isinstance(name_or_gid, (int,long)):
            # Guessing it's a gid
            try:
                gr_info = grp.getgrgid(name_or_gid)
                self._init_with_grp(gr_info)
            except KeyError:
                self.gid = None
        elif isinstance(name_or_gid, basestring):
            # Guessing it's a group name
            try:
                gr_info = grp.getgrnam(name_or_gid)
                self._init_with_grp(gr_info)
            except KeyError:
                self.name = None
    
    def is_member(self, user_info):
        # If we're an invalid group or it's an invalid user, they're not a member of anything
        if not self:
            return False
        if not user_info:
            return False
        
        # If passed a string, assume user name
        # If passed a number, assume uid
        # If passed a User object, use the .uid of it
        if isinstance(user_info, User):
            return user_info.is_member(self)
        elif isinstance(user_info, basestring) or isinstance(user_info, (int,long)):
            return User(user_info).is_member(self)
        else:
            # Not sure what we were passed, fail to False
            return False

class User:
    _fields = ('name', 'uid', 'gid', 'home', 'email', 'hidden', 'enabled',
               'uuid', 'fullname', '_id_obj', 'groups')
    _pw_map = {'name': 'pw_name', 'uid': 'pw_uid',
               'gid': 'pw_gid', 'home': 'pw_dir'}
    
    def _init_with_pwd(self, pwd_entry):
        if isinstance(pwd_entry, pwd.struct_passwd):
            for key in self._pw_map.keys():
                setattr(self,key,getattr(pwd_entry, self._pw_map[key]))
        if self.uid is not None:
            # User exists, find extended information
            id_auth = CBIdentityAuthority.defaultIdentityAuthority()
            self._id_obj = CBUserIdentity.userIdentityWithPosixUID_authority_(self.uid, id_auth)
            if self._id_obj:
                # Make copies of the data as pure python objects, rather than keep translating
                if self._id_obj.emailAddress() is not None:
                    self.email  = str(self._id_obj.emailAddress())
                if self._id_obj.UUIDString() is not None:
                    self.uuid   = str(self._id_obj.UUIDString())
                if self._id_obj.fullName() is not None:
                    self.fullname = str(self._id_obj.fullName())
                self.hidden  = bool(self._id_obj.isHidden())
                self.enabled = bool(self._id_obj.isEnabled())
            # Find extended group membership information
            # Load up OS X libc
            libc = CDLL("/usr/lib/libc.dylib")
            # define access to an undocumented Apple function 'getgrouplist_2'
            # Based on the example from:
            # http://opensource.apple.com/source/shell_cmds/shell_cmds-162/id/id.c
            getgrouplist_2 = libc.getgrouplist_2
            # Create the function prototype
            getgrouplist_2.argtypes = [c_char_p, c_uint32, POINTER(POINTER(c_uint32))]
            # Initialize pointer to array of gid information
            groups = POINTER(c_uint32)()
            # Get number of groups and gid list
            ngroups = getgrouplist_2(self.name, self.gid, byref(groups))
            # Make explicit copies prior to freeing the allocated pointer array
            if ngroups > 0:
                self.groups = [Group(int(groups[i])) for i in range(ngroups)]
            # Clean up after ourselves and free up the array, ignoring result
            _ = libc.free(groups)
    
    def __nonzero__(self):
        for i in self._fields:
            if getattr(self,i) is not None:
                return True
        return False
    
    def __str__(self):
        return self.name or ''
    
    def __int__(self):
        if self.uid is None:
            return -(sys.maxint)-1
        return self.uid
    
    def __hash__(self):
        return hash("%s %s" % (int(self),str(self)))
    
    def __eq__(self, other):
        if isinstance(other, User):
            for i in self._fields:
                if getattr(self,i) != getattr(other,i):
                    return False
            return True
        elif other is None:
            if (self.name is None) and (self.uid is None):
                return True
            return False
        elif isinstance(other, basestring):
            if self.name == other:
                return True
            return False
        elif isinstance(other, (int,long)):
            if self.uid == other:
                return True
            return False
        return False
    
    def __ne__(self, other):
        return not self.__eq__(other)
    
    def __init__(self, name_or_uid = None):
        # If passed a string, assume user name
        # If passed a number, assume uid
        # If None, leave everything with a value of None
        
        # Initialize everything to None
        for i in self._fields:
            setattr(self, i, None)
        
        # Determine whether we were passed a name or a uid
        if isinstance(name_or_uid, (int,long)):
            # Guessing it's a uid
            try:
                pw_info = pwd.getpwuid(name_or_uid)
                self._init_with_pwd(pw_info)
            except KeyError:
                self.uid = None
        elif isinstance(name_or_uid, basestring):
            # Guessing it's a user name
            try:
                pw_info = pwd.getpwnam(name_or_uid)
                self._init_with_pwd(pw_info)
            except KeyError:
                self.name = None
    
    def _is_member(self, group_obj):
        if not group_obj:
            return False
        # Try two paths here -
        # 1st check if recursive member, via .groups
        if group_obj in self.groups:
            return True
        else:
            return bool(self._id_obj.isMemberOfGroup_(group_obj._id_obj))
    
    def is_member(self, group_info):
        # If we're an invalid user or it's an invalid group, we're not a member of anything
        if not self:
            return False
        if not group_info:
            return False
        
        # If passed a string, assume group name
        # If passed a number, assume gid
        # If passed a Group object, use the .gid of it
        if isinstance(group_info, Group):
            return self._is_member(group_info)
        elif isinstance(group_info, basestring) or isinstance(group_info, (int,long)):
            return self._is_member(Group(group_info))
        else:
            # Not sure what we were passed, fail to False
            return False
    
    def group_names(self):
        if self.groups:
            return [x.name for x in self.groups]
    
    def group_ids(self):
        if self.groups:
            return [x.gid for x in self.groups]
    
    def group_objs(self):
        # Just for completeness against the other convenience functions
        return self.groups
