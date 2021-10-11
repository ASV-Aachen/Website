
class Nutzer:
    Nachname: str
    Vorname: str
    Eintrittsdatum: str
    Status: str
    E_Mail: str

class user:
    id: str
    member_id: str
    email: str
    password: str
    role: str

class member:
    id: str
    user_id: user
    first_name: str
    last_name: str
    
class project:
    id: str
    name: str
    description: str
    first_season: str
    last_season: str
    
class project_item:
    id: str
    project_id: project
    season: str
    date: str
    title: str
    description: str
    
class project_item_hour:
    id: str
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