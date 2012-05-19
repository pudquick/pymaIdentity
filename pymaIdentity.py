from Collaboration import CBUserIdentity, CBGroupIdentity, CBIdentityAuthority
from SystemConfiguration import SCDynamicStoreCopyConsoleUser
from objc import NULL
import os

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
