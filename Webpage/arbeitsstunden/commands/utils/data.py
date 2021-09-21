
class Nutzer:
    Nachname: str
    Vorname: str
    Eintrittsdatum: str
    Status: str
    E_Mail: str

class user:
    email: str
    password: str
    role: str

class member:
    user_id: user
    first_name: str
    last_name: str
    
class project:
    name: str
    description: str
    first_season: str
    last_season: str
    
class project_item:
    project_id: project
    season: str
    date: str
    title: str
    description: str
    
class project_item_hour:
    project_item_id: project_item
    member_id: member
    duration: int

class season:
    year: int
    obligatory_minutes: int

class reduction: 
    season_id: season
    member_id: member
    status: str
    reduction: int