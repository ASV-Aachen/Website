

'''
Checked if der Nutzer des Request Teil der gegebenen Gruppe ist oder nicht
@param request - Der request der geprüft werden soll
@param groupName {[String]} - Die Namen der zu prüfenden Gruppe
@return True oder false, je nachdem ob der Nutzer zur Gruppe gehört
'''
def isUserPartOfGroup(request, groupNameArray)-> bool:
    # Bist du ein Admin darfst du alles
    if request.user.groups.filter(name='Admin').exists() is False:
        return True

    for i in groupNameArray:
        if request.user.groups.filter(name=i).exists() is False:
            return False
    return True

# @user_passes_test(isUserPartOfGroup)

'''
Beispiele:
@user_passes_test(isUserPartOfGroup(groupNameArray = ['Editor']))
@user_passes_test(isUserPartOfGroup(groupNameArray = ['Developer']))
'''