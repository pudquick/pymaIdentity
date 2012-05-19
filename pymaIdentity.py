from Collaboration import CBUserIdentity, CBGroupIdentity, CBIdentityAuthority
from SystemConfiguration import SCDynamicStoreCopyConsoleUser
from objc import NULL
import os

# get pseudo authority that represents local + directory services
localAuth = CBIdentityAuthority.localIdentityAuthority()

### Testing group, user, and membership

username, groupname = ("root", "wheel")

print "Test: User: %s, Group: %s" % (username, groupname)

# attempt to find user in question
user = CBUserIdentity.identityWithName_authority_(username, localAuth)
if not user:
    print "Error: Unable to find user:", username
else:
    print "User details:", user

# attempt to find group in question
group = CBGroupIdentity.identityWithName_authority_(groupname, localAuth)
if not group:
    print "Error: Unable to find group:", groupname
else:
    print "Group details:", group

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
    current_gui_user = CBUserIdentity.identityWithName_authority_(current_gui_user, localAuth)

if not current_gui_user:
    print "Error: No one currently logged into workstation physically"
else:
    print "Current GUI user:", current_gui_user

### Get the effective user currently running the process

effective_user = CBUserIdentity.userIdentityWithPosixUID_authority_(os.geteuid(), localAuth)
print "Effective user:", effective_user

