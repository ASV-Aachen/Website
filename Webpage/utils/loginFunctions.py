
'''
Checked if der Nutzer des Request Teil der gegebenen Gruppe ist oder nicht
@param request - Der request der geprüft werden soll
@param groupName {[String]} - Die Namen der zu prüfenden Gruppe
@return True oder false, je nachdem ob der Nutzer zur Gruppe gehört
'''
def isUserPartOfGroup_Editor(user)-> bool:
    # Bist du ein Admin darfst du alles
    if user.groups.filter(name='Admin').exists() or user.groups.filter(name="Editor").exists():
        return True
    return False

def isUserPartOfGroup_Developer(user)-> bool:
    # Bist du ein Admin darfst du alles
    if user.groups.filter(name='Admin').exists() or user.groups.filter(name="Developer").exists():
        return True
    return False

def isUserPartOfGroup_Schriftwart(user)-> bool:
    # Bist du ein Admin darfst du alles
    if user.groups.filter(name='Admin').exists() or user.groups.filter(name="Schriftwart").exists():
        return True
    return False

def isUserPartOfGroup_Seereisenkoordinator(user)-> bool:
    # Bist du ein Admin darfst du alles
    if user.groups.filter(name='Admin').exists() or user.groups.filter(name="Seereisenkoordinator").exists():
        return True
    return False

# @user_passes_test(isUserPartOfGroup_Editor)
# @user_passes_test(isUserPartOfGroup_Developer)
# @user_passes_test(isUserPartOfGroup_Schriftwart)

'''
Beispiele:
@user_passes_test(isUserPartOfGroup(groupNameArray = ['Editor']))
@user_passes_test(isUserPartOfGroup(groupNameArray = ['Developer']))
'''