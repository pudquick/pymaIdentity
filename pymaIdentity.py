import objc
from objc import NULL
from Foundation import NSString

# Generated with: gen_bridge_metadata --64-bit --framework /System/Library/Frameworks/CoreServices.framework/Frameworks/OSServices.framework
# Had to patch around a few things, like
#  - linking to CoreServices.Framework instead of directly to OSServices.framework and clean out a bad line:
#  - remove strange line generated:  printf(((int)') < 0 ? "%s: %d\n" : "%s: %u\n", "'", ');
# Framework documentation:
# https://developer.apple.com/library/mac/#documentation/networking/Reference/IdentityServices_Ref/CSIdentity/index.html

objc.parseBridgeSupport("""<?xml version='1.0'?>
<!DOCTYPE signatures SYSTEM "file://localhost/System/Library/DTDs/BridgeSupport.dtd">
<signatures version='0.9'>
<depends_on path='/System/Library/Frameworks/DiskArbitration.framework'/>
<depends_on path='/System/Library/Frameworks/IOKit.framework'/>
<depends_on path='/System/Library/Frameworks/Security.framework'/>
<depends_on path='/System/Library/Frameworks/SystemConfiguration.framework'/>
<depends_on path='/System/Library/Frameworks/CoreServices.framework/Versions/A/Frameworks/CarbonCore.framework'/>
<depends_on path='/System/Library/Frameworks/CoreServices.framework/Versions/A/Frameworks/CFNetwork.framework'/>
<depends_on path='/System/Library/Frameworks/CoreFoundation.framework'/>
<depends_on path='/System/Library/Frameworks/NetFS.framework'/>
<enum name='kCSIdentityAuthorityNotAccessibleErr' value='-2'/>
<enum name='kCSIdentityClassGroup' value='2'/>
<enum name='kCSIdentityClassUser' value='1'/>
<enum name='kCSIdentityCommitCompleted' value='1'/>
<enum name='kCSIdentityDeletedErr' value='-4'/>
<enum name='kCSIdentityDuplicateFullNameErr' value='-6'/>
<enum name='kCSIdentityDuplicatePosixNameErr' value='-8'/>
<enum name='kCSIdentityFlagHidden' value='1'/>
<enum name='kCSIdentityFlagNone' value='0'/>
<enum name='kCSIdentityInvalidFullNameErr' value='-5'/>
<enum name='kCSIdentityInvalidPosixNameErr' value='-7'/>
<enum name='kCSIdentityPermissionErr' value='-3'/>
<enum name='kCSIdentityQueryEventErrorOccurred' value='5'/>
<enum name='kCSIdentityQueryEventResultsAdded' value='2'/>
<enum name='kCSIdentityQueryEventResultsChanged' value='3'/>
<enum name='kCSIdentityQueryEventResultsRemoved' value='4'/>
<enum name='kCSIdentityQueryEventSearchPhaseFinished' value='1'/>
<enum name='kCSIdentityQueryGenerateUpdateEvents' value='1'/>
<enum name='kCSIdentityQueryIncludeHiddenIdentities' value='2'/>
<enum name='kCSIdentityQueryStringBeginsWith' value='2'/>
<enum name='kCSIdentityQueryStringEquals' value='1'/>
<enum name='kCSIdentityUnknownAuthorityErr' value='-1'/>
<function name='CSIdentityCreateGroupMembershipQuery'>
<arg type='^{__CFAllocator=}'/>
<arg type='^{__CSIdentity=}'/>
<retval type='^{__CSIdentityQuery=}'/>
</function>
<function name='CSIdentityGetClass'>
<arg type='^{__CSIdentity=}'/>
<retval type64='q' type='l'/>
</function>
<function name='CSIdentityGetPosixID'>
<arg type='^{__CSIdentity=}'/>
<retval type='I'/>
</function>
<function name='CSIdentityGetPosixName'>
<arg type='^{__CSIdentity=}'/>
<retval type='^{__CFString=}'/>
</function>
<function name='CSIdentityGetTypeID'>
<retval type64='Q' type='L'/>
</function>
<function name='CSIdentityGetUUID'>
<arg type='^{__CSIdentity=}'/>
<retval type='^{__CFUUID=}'/>
</function>
<function name='CSIdentityIsEnabled'>
<arg type='^{__CSIdentity=}'/>
<retval type='B'/>
</function>
<function name='CSIdentityIsHidden'>
<arg type='^{__CSIdentity=}'/>
<retval type='B'/>
</function>
<function name='CSIdentityIsMemberOfGroup'>
<arg type='^{__CSIdentity=}'/>
<arg type='^{__CSIdentity=}'/>
<retval type='B'/>
</function>
<function name='CSIdentityQueryCopyResults'>
<arg type='^{__CSIdentityQuery=}'/>
<retval already_retained='true' type='^{__CFArray=}'/>
</function>
<function name='CSIdentityQueryCreate'>
<arg type='^{__CFAllocator=}'/>
<arg type64='q' type='l'/>
<arg type='^{__CSIdentityAuthority=}'/>
<retval type='^{__CSIdentityQuery=}'/>
</function>
<function name='CSIdentityQueryCreateForCurrentUser'>
<arg type='^{__CFAllocator=}'/>
<retval type='^{__CSIdentityQuery=}'/>
</function>
<function name='CSIdentityQueryCreateForName'>
<arg type='^{__CFAllocator=}'/>
<arg type='^{__CFString=}'/>
<arg type64='q' type='l'/>
<arg type64='q' type='l'/>
<arg type='^{__CSIdentityAuthority=}'/>
<retval type='^{__CSIdentityQuery=}'/>
</function>
<function name='CSIdentityQueryCreateForPersistentReference'>
<arg type='^{__CFAllocator=}'/>
<arg type='^{__CFData=}'/>
<retval type='^{__CSIdentityQuery=}'/>
</function>
<function name='CSIdentityQueryCreateForPosixID'>
<arg type='^{__CFAllocator=}'/>
<arg type='I'/>
<arg type64='q' type='l'/>
<arg type='^{__CSIdentityAuthority=}'/>
<retval type='^{__CSIdentityQuery=}'/>
</function>
<function name='CSIdentityQueryCreateForUUID'>
<arg type='^{__CFAllocator=}'/>
<arg type='^{__CFUUID=}'/>
<arg type='^{__CSIdentityAuthority=}'/>
<retval type='^{__CSIdentityQuery=}'/>
</function>
<function name='CSIdentityQueryExecute'>
<arg type='^{__CSIdentityQuery=}'/>
<arg type64='Q' type='L'/>
<arg type='^^{__CFError}'/>
<retval type='B'/>
</function>
<function name='CSGetDefaultIdentityAuthority'>
<retval type='^{__CSIdentityAuthority=}'/>
</function>
<function name='CSGetLocalIdentityAuthority'>
<retval type='^{__CSIdentityAuthority=}'/>
</function>
<function name='CSGetManagedIdentityAuthority'>
<retval type='^{__CSIdentityAuthority=}'/>
</function>
</signatures>
""", globals(), '/System/Library/Frameworks/CoreServices.framework/Frameworks/OSServices.framework')

username,groupname = ("root", "wheel")

print "Getting pseudo central authority ..."
defaultAuthority = CSGetLocalIdentityAuthority()
print "Looking for user:", username
userQuery = CSIdentityQueryCreateForName(NULL, NSString.stringWithString_(username), kCSIdentityQueryStringEquals, kCSIdentityClassUser, defaultAuthority)
result = CSIdentityQueryExecute(userQuery, kCSIdentityQueryIncludeHiddenIdentities, NULL)
print "Search succeeded:", result
users_found = CSIdentityQueryCopyResults(userQuery)
print "Number of users found:", len(users_found)
print users_found
print "Looking for group:", groupname
groupQuery = CSIdentityQueryCreateForName(NULL, NSString.stringWithString_(groupname), kCSIdentityQueryStringEquals, kCSIdentityClassGroup, defaultAuthority)
result = CSIdentityQueryExecute(groupQuery, kCSIdentityQueryIncludeHiddenIdentities, NULL)
print "Search succeeded:", result
groups_found = CSIdentityQueryCopyResults(groupQuery)[:]
print "Number of groups found:", len(groups_found)
print groups_found
print 'Checking group membership for "%s" in "%s"' % (username, groupname)
result = CSIdentityIsMemberOfGroup(users_found[0], groups_found[0])
print "Is member of group:", result
