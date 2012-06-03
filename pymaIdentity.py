import os, pwd
from Collaboration import CBUserIdentity, CBGroupIdentity, CBIdentityAuthority
from SystemConfiguration import SCDynamicStoreCopyConsoleUser
from objc import NULL
from ctypes import *

def identity_dict(id_obj):
    result = {}
    if (id_obj):
        result['aliases'] = id_obj.aliases()[:]
        result['emailAddress'] = id_obj.emailAddress()
        result['fullName'] = id_obj.fullName()
        result['isHidden'] = id_obj.isHidden()
        result['posixName'] = id_obj.posixName()
        result['UUIDString'] = id_obj.UUIDString()
        if (type(id_obj) == CBUserIdentity):
            result['isEnabled'] = id_obj.isEnabled()
            result['posixUID'] = id_obj.posixUID()
        else:
            result['isEnabled'] = None
            result['posixUID'] = None
        if (type(id_obj) == CBGroupIdentity):
            result['posixGID'] = id_obj.posixGID()
        else:
            result['posixGID'] = None
        if (type(id_obj) == CBUserIdentity):
            result['class'] = "user"
        elif (type(id_obj) == CBGroupIdentity):
            result['class'] = "group"
        else:
            result['class'] = None
    else:
        result = {'aliases': None,'emailAddress': None,'fullName': None,
                  'isHidden': None,'posixName': None,'UUIDString': None,
                  'isEnabled': None,'posixUID': None,'posixGID': None,'class': None}
    return result

def posix_user(username):
    try:
        _ = pwd.getpwnam(username)
    except:
        return {'name': None, 'uid': None, 'gid': None, 'comment': None, 'home': None, 'shell': None}
    return {'name': _.pw_name, 'uid': _.pw_uid, 'gid': _.pw_gid, 'comment': _.pw_gecos, 'home': _.pw_dir, 'shell': _.pw_shell}

def get_groups(username):
    # verify user exists
    defaultAuth = CBIdentityAuthority.defaultIdentityAuthority()
    the_user = CBUserIdentity.identityWithName_authority_(username, defaultAuth)
    if (the_user != None):
        user_details = identity_dict(the_user)
        posix_details = posix_user(user_details['posixName'])
        libc = CDLL("/usr/lib/libSystem.B.dylib")
        # define access to an undocumented Apple function 'getgrouplist_2'
        # Based on the example from:
        # http://opensource.apple.com/source/shell_cmds/shell_cmds-162/id/id.c
        getgrouplist_2 = libc.getgrouplist_2
        getgrouplist_2.argtypes = [c_char_p, c_uint32, POINTER(POINTER(c_uint32))]
        groups = POINTER(c_uint32)()
        ngroups = getgrouplist_2(user_details['posixName'], posix_details['gid'], byref(groups))
        # make explicit copies prior to freeing the allocated pointer array
        group_list = [(0+groups[i]) for i in range(ngroups)]
        # clean up after ourselves
        _ = libc.free(groups)
        for g in group_list:
            full_group = CBGroupIdentity.groupIdentityWithPosixGID_authority_(g, defaultAuth)
            yield identity_dict(full_group)

# get pseudo authority that represents local + directory services
defaultAuth = CBIdentityAuthority.defaultIdentityAuthority()

### Testing group, user, and membership

username, groupname = ("root", "wheel")

print "Test: User: %s, Group: %s" % (username, groupname)

# attempt to find user in question
user = CBUserIdentity.identityWithName_authority_(username, defaultAuth)
if not user:
    print "Error: Unable to find user:", username
else:
    print "User details:", user
    print "User dict:", identity_dict(user)

# attempt to find group in question
group = CBGroupIdentity.identityWithName_authority_(groupname, defaultAuth)
if not group:
    print "Error: Unable to find group:", groupname
else:
    print "Group details:", group
    print "Group dict:", identity_dict(group)

if (user and group):
    # Find out if user is member of group
    member = user.isMemberOfGroup_(group)
    print 'Result: User "%s" membership in group "%s":' % (username, groupname), member
else:
    print "Error: User or group provided did not exist"

### Testing GUI console user information

current_gui_user = (SCDynamicStoreCopyConsoleUser(NULL, NULL, NULL) or [NULL])[0]
if (current_gui_user in [u'loginwindow', NULL]):
    current_gui_user = None

# If is not None, resolve shortname to full account identity
if current_gui_user:
    current_gui_user = CBUserIdentity.identityWithName_authority_(current_gui_user, defaultAuth)

if not current_gui_user:
    print "Error: No one currently logged into workstation physically"
else:
    print "Current GUI user:", current_gui_user

### Get the effective user currently running the process

effective_user = CBUserIdentity.userIdentityWithPosixUID_authority_(os.geteuid(), defaultAuth)
print "Effective user:", effective_user
print "Effective user dict:", identity_dict(effective_user)

### Print out total known group membership for a user

print "Group membership for:", username
for x in get_groups(username):
    print x
