import datetime
class Festival:
    def __init__(self):
        
        self.store = {
            "players":{},
            "games":{},
            "events":{},
            "logs":{}
            }
    def log_operation(self,op,by,detail):
        timestamp = datetime.datetime.now().isoformat()
        self.store["logs"][timestamp]= {"op":op,"by":by,"detail":detail}
    def add_player(self,player_id,name,email):
        if player_id in self.store["players"]:
            raise ValueError("Player with this name already exists")
        self.store["players"][player_id] = {"name":name,"email":email,"registered":{}}
        self.log_operation("add_player","system",{"player_id":player_id,"name":name,"email":email})
        return True
    def remove_player(self,player_id,force=False):
        if player_id not in self.store["players"]:
            raise ValueError("Player with this name does not exist")
        player_event = []
        for event_id,event in self.store["events"].items():
            if player_id in event["participants"]:
                player_event.append(event_id)
        if player_event and not force:
            raise ValueError("Player with this name does not exist")
        for event_id in player_event:
            del self.store["events"][event_id]
        del self.store["players"][player_id]
        self.log_operation("remove_player","system",{"player_id":player_id,"force":force,"removed_from_events":player_event})
        return True
    def add_game(self,game_id,title,min_players,max_players,tags):
        if game_id in self.store["games"]:
            raise ValueError("Game with this name already exists")
        tags_dict = {tag:True for tag in tags}
        self.store["games"][game_id] = {"title":title,"min_players":min_players,"max_players":max_players,"tags":tags_dict}
        self.log_operation("add_game","system",{"game_id":game_id,"title":title,"min_players":min_players,"max_players":max_players,"tags":tags})
        return True
    def register_player(self,player_id,event_id,role="player"):
        if player_id not in self.store["players"]:
            raise ValueError("Player with this name does not exist")
        if event_id not in self.store["events"]:
            raise ValueError("Event with this name does not exist")
        event = self.store["events"][event_id]
        game_id = event["game_id"]
        current_player = len(event["participants"])
        max_players = self.store["games"][game_id]["max_players"]
        if current_player >= max_players:
            raise ValueError("Maximum event filled")
        if event["status"] != "scheduled"
            raise ValueError("Player with this name does not exist")
        timestamp = datetime.datetime.now().isoformat()
        event["participants"][player_id] = {"joined_at":timestamp,"result":"pending"}
        self.store["players"][player_id]["registered_games"][event_id] = {"role":role,"score":None}
        self.log_operation("register_player","system",{"player_id":player_id,"event_id":event_id,"role":role)
        return True
    def unregister_player(self,player_id,event_id):
        if player_id not in self.store["players"]:
            raise ValueError("Player with this name does not exist")
        if event_id not in self.store["events"]:
            raise ValueError("Event with this name does not exist")
        event = self.store["events"][event_id]
        if event["status"] != "scheduled":
            raise ValueError("Player with this name does not exist")
        if player_id in event["participants"]:
            del event["participants"][player_id]
        if event_id in self.store["players"][player_id]["registered_games"]:
            del self.store["players"][player_id]["registered_games"][event_id]
        self.log_operation("unregister_player","system",{"player_id":player_id,"event_id":event_id})
        return True
    def record_result(self,event_id,player_id,result):
        if event_id not in self.store["events"]:
            raise ValueError("Event with this name does not exist")
        if player_id not in self.store["players"]:
            raise ValueError("Player with this name does not exist")
        event = self.store["events"][event_id]
        if player_id not in event["participants"]:
            raise ValueError("Player with this name does not exist")
        if result not in ["win","loss","draw"]:
            raise ValueError("Result must be 'win','loss','draw'")
        event["participants"][player_id]["result"] = result
        all_results_recorded = all(participant["result"]!="pending" for participant in event["participants"].values())
        if all_results_recorded:
            event["status"] = "finished"
        self.log_operation("record_result","system",{"event_id":event_id,"player_id":player_id,"result":result})
        return True
    def stats(self):
        ststs = {"total_players":len(self.store["players"]),
                 "total_events":len(self.store["events"]),
                 "total_games":len(self.store["games"]),
                 "games_tags":{},
                 "events_tags":{"scheduled":0,"finished":0,"finished":0}}
        for game in self.store["games"].values():
            for tag in game["tags"]:
                if tag in ststs["games_tags"]:
                    ststs["games_tags"][tag] += 1
                else:
                    ststs["games_tags"][tag] = 1
        for event in self.store["events"].values():
            status=event["status"]
            ststs["events_tags"][status] += 1
        return ststs
    def create_event(self,game_id,time):
        if game_id not in self.store["games"]:
            raise ValueError("Game with this name does not exist")
        event_id = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        self.store["events"][event_id] = {"game_id":game_id,"time":time,"participants":{},"status":"scheduled"}
        self.log_operation("create_event","system",{"game_id":game_id,"time":time,"event_id":event_id})
        return True




