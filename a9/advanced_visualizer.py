from Tkinter import *
import random
from sets import Set
import operator
import time

strategies =  ['Greed','No Bidding','Item Pickup','NanoBidding','Bidvasion','Bidding Salesman','Gravity Bidding','Bidforce','RandomBid','Simulated Bidding','K-Bids']


class visualizer():
    
    class Player():
        def __init__(self, teamid, teamname, money, time, strategy = ""):
            self.teamid = teamid
            self.teamname = teamname
            self.money = money
            self.time = time
            self.strategy = strategy
            if self.strategy=="":
                random.shuffle(strategies)
                self.strategy = strategies.pop(0)
        
            self.current_bid = 0
        
            self.items = {}
    
        def update(self, bid, time_used, item_won=-1):
            if item_won != -1:
                self.money = max(self.money - self.current_bid, 0)
                if item_won in self.items:
                    self.items[item_won] = self.items.get(item_won) + 1
                else:
                    self.items[item_won] = 1
        
            self.time = max(self.time - time_used, 0)
            self.current_bid = bid
     
    # The Player Class
                      
    def __init__(self, goal, team_list, itemlist, init_money=100):
        self.goal = goal
        self.players = []
        self.pot_item_names = ['Balisto', 'Daim', 'Excellence', 'Flake', 'Godiva',
                               'Hay Hay', 'Idaho Spud', 'KitKat', 'Lion', 'Mars',
                               'Noisette', 'Oreo', 'Penguin', 'Rolo', 'Snickers',
                               'Twix', 'UnoBar', 'Valomilk', 'WunderBar', 'Yorkie',
                               'Zero Bar']
        
        self.item_names = ['Almond Joy', 'Caramello Koala']
        self.item_colors = ['red', 'blue', 'magenta', 'purple', 'grey', 'darkblue', 'brown',
                            'violet', 'darkgreen', 'orange']
        
        random.shuffle(self.item_colors)
        
        
        self.itemlist = itemlist[:]
        random.shuffle(self.pot_item_names)
            # Create all Player instances
        for i in range(0, len(team_list)):
            teamid = i
            name = team_list[i][0]
            money = init_money
            time = int(team_list[i][1])
            
            new_player = self.Player(teamid, name, money, time)
            self.players.append(new_player)
          
        # Create item names
        self.diff_items = len(Set(itemlist))
        for i in range(int(self.diff_items) - 2):  # -2 because almond and caramel are always in
            self.item_names.append(self.pot_item_names.pop())
          
        self.item_names.sort()
    
        print self.item_names
        
        
        # Current item
        self.current_item = self.itemlist.pop(0)
        self.last_item = -1
        self.last_winner = -1
        
        self.bidqueue = []

        self.master = Tk()
        
        self.labelList = []
        
        self.tkimage = []
        for i in range(11):
            str_num = str(i+1)
            self.tkimage.append(PhotoImage(file="images/picture"+str_num+".gif"))
                     
        random.shuffle(self.tkimage)
        
        self.numimage = []
        for i in range(10):
            str_num = str(i)
            self.numimage.append(PhotoImage(file="images/"+str_num+".gif"))
        
        self.numimage.append(PhotoImage(file="images/number_template.gif"))
        self.numimage.append(PhotoImage(file="images/x_1.gif"))
        self.podium = PhotoImage(file="images/podium2.gif")
        self.shasha= PhotoImage(file="images/shasha.gif")
        
        # Height is dependent on number of players
        self.width = 1200
        self.height = 1000
        
        self.w = Canvas(self.master, width=self.width, height=self.height)
        self.w.pack()
        
        self.draw_scoreboard(-1)
        
        
    def set_podiums(self, state, pid=-1):
    
        no_players = len(self.players)
        width = self.width
        height = self.height
        
        if(no_players<=4):
            player_box_upper_y = height/3
            player_box_y_offset = height - player_box_upper_y
            player_box_left_x = 0
            player_box_x_offset = width/no_players
            
            for player in self.players:
                self.labelList.append(self.tkimage[player.teamid])
                center_x = player_box_left_x + (player_box_x_offset/2)
                center_y = player_box_upper_y + (player_box_y_offset/2)
                self.w.create_image((center_x,center_y-95),image=self.tkimage[player.teamid],anchor='s')
                #self.w.create_rectangle(center_x-75,center_y-100,center_x+75,center_y+100,fill="brown")
                self.w.create_image((center_x,center_y-10),image=self.podium,anchor='center')
                player_box_left_x += player_box_x_offset
                self.w.create_text((center_x,center_y-73),text=player.teamname,font=("Purisa",11),anchor='center')
                self.w.create_text((center_x,center_y-53),text=player.strategy,font=("Purisa",12),anchor='center')
                if(state==-1):
                    if((player.teamid == pid) or ((player.teamid in self.bidqueue) and (self.bidqueue.index(player.teamid)<self.bidqueue.index(pid)))):
                        if player.current_bid < 10:
                            self.w.create_image((center_x-37,center_y-8),image=self.numimage[0],anchor='center')
                            self.w.create_image((center_x,center_y-8),image=self.numimage[0],anchor='center')
                            self.w.create_image((center_x+37,center_y-8),image=self.numimage[int(str(player.current_bid)[0])],anchor='center')
                        elif player.current_bid < 100:
                            self.w.create_image((center_x-37,center_y-8),image=self.numimage[0],anchor='center')
                            self.w.create_image((center_x,center_y-8),image=self.numimage[int(str(player.current_bid)[0])],anchor='center')
                            self.w.create_image((center_x+37,center_y-8),image=self.numimage[int(str(player.current_bid)[1])],anchor='center')
                        else:
                            self.w.create_image((center_x-37,center_y-8),image=self.numimage[int(str(player.current_bid)[0])],anchor='center')
                            self.w.create_image((center_x,center_y-8),image=self.numimage[int(str(player.current_bid)[1])],anchor='center')
                            self.w.create_image((center_x+37,center_y-8),image=self.numimage[int(str(player.current_bid)[2])],anchor='center')
                    else:
                        self.w.create_image((center_x-37,center_y-8),image=self.numimage[-1],anchor='center')
                        self.w.create_image((center_x,center_y-8),image=self.numimage[-1],anchor='center')
                        self.w.create_image((center_x+37,center_y-8),image=self.numimage[-1],anchor='center')
                    if self.current_item in player.items:
                        (key,value) = (self.current_item,player.items[self.current_item])
                    else:
                        (key,value) = (self.current_item,0)
                    text_in = str(value) + "* "
                    self.w.create_text((center_x-35, center_y+36), text=text_in, font=("Purisa",15), justify='left', anchor='nw')
                    item = self.item_names[key]
                    self.w.create_oval((center_x-16, center_y +26, center_x + 16, center_y+36 + 20 + 3), fill=self.item_colors[key])
                    self.w.create_text((center_x + 1, center_y+40), text=item[0], justify='left', anchor='center')
                        
                elif state == 0:
                    if player.teamid in self.bidqueue:
                        self.w.create_image((center_x-37,center_y-8),image=self.numimage[-1],anchor='center')
                        self.w.create_image((center_x,center_y-8),image=self.numimage[-1],anchor='center')
                        self.w.create_image((center_x+37,center_y-8),image=self.numimage[-1],anchor='center')
                    else:        
                        self.w.create_image((center_x-37,center_y-8),image=self.numimage[10],anchor='center')
                        self.w.create_image((center_x,center_y-8),image=self.numimage[10],anchor='center')
                        self.w.create_image((center_x+37,center_y-8),image=self.numimage[10],anchor='center')
                    if self.current_item in player.items:
                        (key,value) = (self.current_item,player.items[self.current_item])
                    else:
                        (key,value) = (self.current_item,0)
                    text_in = str(value) + "* "
                    self.w.create_text((center_x-35, center_y+36), text=text_in, font=("Purisa",15), justify='left', anchor='nw')
                    item = self.item_names[key]
                    self.w.create_oval((center_x-16, center_y +26, center_x + 16, center_y+36 + 20 + 3), fill=self.item_colors[key])
                    self.w.create_text((center_x + 1, center_y+40), text=item[0], justify='left', anchor='center')
                        
                else:
                    self.w.create_image((center_x-37,center_y-8),image=self.numimage[10],anchor='center')
                    self.w.create_image((center_x,center_y-8),image=self.numimage[10],anchor='center')
                    self.w.create_image((center_x+37,center_y-8),image=self.numimage[10],anchor='center')
                    for (key, value) in sorted(player.items.iteritems(), key=operator.itemgetter(1), reverse=True)[:1]:
                        text_in = str(value) + "* "
                        self.w.create_text((center_x-35, center_y+36), text=text_in, font=("Purisa",15), justify='left', anchor='nw')
                        item = self.item_names[key]
                        self.w.create_oval((center_x-16, center_y +26, center_x + 16, center_y+36 + 20 + 3), fill=self.item_colors[key])
                        self.w.create_text((center_x + 1, center_y+40), text=item[0], justify='left', anchor='center')
                
                self.w.create_text((center_x,center_y+75),text="Time left:  " + str(player.time),font=("Purisa",11),anchor='center')
                       
        if(no_players>4):  
            if(no_players%2):
                upper = (no_players/2)+1 
            else:
                upper = no_players/2
            i=0    
    
    
            player_box_upper_y = height/3
            player_box_y_offset = height - player_box_upper_y
            player_box_left_x = 0
            player_box_x_offset = width/upper
            
            while i<upper:
                self.labelList.append(self.tkimage[self.players[i].teamid])
                center_x = player_box_left_x + (player_box_x_offset/2)
                center_y = player_box_upper_y + (player_box_y_offset/2)/2 + 75 + 36
                self.w.create_image((center_x,center_y-95),image=self.tkimage[self.players[i].teamid],anchor='s')
                #self.w.create_rectangle(center_x-75,center_y-100,center_x+75,center_y+100,fill="brown")
                self.w.create_image((center_x,center_y-10),image=self.podium,anchor='center')
                player_box_left_x += player_box_x_offset
                self.w.create_text((center_x,center_y-73),text=self.players[i].teamname,font=("Purisa",11),anchor='center')
                self.w.create_text((center_x,center_y-53),text=self.players[i].strategy,font=("Purisa",12),anchor='center')
                
                player = self.players[i]
                if(state==-1):
                    if((player.teamid == pid) or ((player.teamid in self.bidqueue) and (self.bidqueue.index(player.teamid)<self.bidqueue.index(pid)))):
                        if player.current_bid < 10:
                            self.w.create_image((center_x-37,center_y-8),image=self.numimage[0],anchor='center')
                            self.w.create_image((center_x,center_y-8),image=self.numimage[0],anchor='center')
                            self.w.create_image((center_x+37,center_y-8),image=self.numimage[int(str(player.current_bid)[0])],anchor='center')
                        elif player.current_bid < 100:
                            self.w.create_image((center_x-37,center_y-8),image=self.numimage[0],anchor='center')
                            self.w.create_image((center_x,center_y-8),image=self.numimage[int(str(player.current_bid)[0])],anchor='center')
                            self.w.create_image((center_x+37,center_y-8),image=self.numimage[int(str(player.current_bid)[1])],anchor='center')
                        else:
                            self.w.create_image((center_x-37,center_y-8),image=self.numimage[int(str(player.current_bid)[0])],anchor='center')
                            self.w.create_image((center_x,center_y-8),image=self.numimage[int(str(player.current_bid)[1])],anchor='center')
                            self.w.create_image((center_x+37,center_y-8),image=self.numimage[int(str(player.current_bid)[2])],anchor='center')
                    else:
                        self.w.create_image((center_x-37,center_y-8),image=self.numimage[-1],anchor='center')
                        self.w.create_image((center_x,center_y-8),image=self.numimage[-1],anchor='center')
                        self.w.create_image((center_x+37,center_y-8),image=self.numimage[-1],anchor='center')
                    if self.current_item in player.items:
                        (key,value) = (self.current_item,player.items[self.current_item])
                    else:
                        (key,value) = (self.current_item,0)
                    text_in = str(value) + "* "
                    self.w.create_text((center_x-35, center_y+36), text=text_in, font=("Purisa",15), justify='left', anchor='nw')
                    item = self.item_names[key]
                    self.w.create_oval((center_x-16, center_y +26, center_x + 16, center_y+36 + 20 + 3), fill=self.item_colors[key])
                    self.w.create_text((center_x + 1, center_y+40), text=item[0], justify='left', anchor='center')
                        
                elif state == 0:
                    if player.teamid in self.bidqueue:
                        self.w.create_image((center_x-37,center_y-8),image=self.numimage[-1],anchor='center')
                        self.w.create_image((center_x,center_y-8),image=self.numimage[-1],anchor='center')
                        self.w.create_image((center_x+37,center_y-8),image=self.numimage[-1],anchor='center')
                    else:        
                        self.w.create_image((center_x-37,center_y-8),image=self.numimage[10],anchor='center')
                        self.w.create_image((center_x,center_y-8),image=self.numimage[10],anchor='center')
                        self.w.create_image((center_x+37,center_y-8),image=self.numimage[10],anchor='center')
                    if self.current_item in player.items:
                        (key,value) = (self.current_item,player.items[self.current_item])
                    else:
                        (key,value) = (self.current_item,0)
                    text_in = str(value) + "* "
                    self.w.create_text((center_x-35, center_y+36), text=text_in, font=("Purisa",15), justify='left', anchor='nw')
                    item = self.item_names[key]
                    self.w.create_oval((center_x-16, center_y +26, center_x + 16, center_y+36 + 20 + 3), fill=self.item_colors[key])
                    self.w.create_text((center_x + 1, center_y+40), text=item[0], justify='left', anchor='center')
                        
                else:
                    self.w.create_image((center_x-37,center_y-8),image=self.numimage[10],anchor='center')
                    self.w.create_image((center_x,center_y-8),image=self.numimage[10],anchor='center')
                    self.w.create_image((center_x+37,center_y-8),image=self.numimage[10],anchor='center')
                    for (key, value) in sorted(player.items.iteritems(), key=operator.itemgetter(1), reverse=True)[:1]:
                        text_in = str(value) + "* "
                        self.w.create_text((center_x-35, center_y+36), text=text_in, font=("Purisa",15), justify='left', anchor='nw')
                        item = self.item_names[key]
                        self.w.create_oval((center_x-16, center_y +26, center_x + 16, center_y+36 + 20 + 3), fill=self.item_colors[key])
                        self.w.create_text((center_x + 1, center_y+40), text=item[0], justify='left', anchor='center')
                
                self.w.create_text((center_x,center_y+75),text="Time left:  " + str(player.time),font=("Purisa",11),anchor='center')
                
                i+=1
    
            player_box_upper_y = height/3
            player_box_y_offset = height - player_box_upper_y
            player_box_left_x = 0
            player_box_x_offset = width/(no_players-upper)
            
            while(i<no_players):
                print i
                self.labelList.append(self.tkimage[self.players[i].teamid])
                center_x = player_box_left_x + (player_box_x_offset/2)
                center_y = player_box_upper_y + (player_box_y_offset/2) + (player_box_y_offset/2)/2 + 75
                self.w.create_image((center_x,center_y-95),image=self.tkimage[self.players[i].teamid],anchor='s')
                #self.w.create_rectangle(center_x-75,center_y-100,center_x+75,center_y+100,fill="brown")
                self.w.create_image((center_x,center_y-10),image=self.podium,anchor='center')
                player_box_left_x += player_box_x_offset
                self.w.create_text((center_x,center_y-73),text=self.players[i].teamname,font=("Purisa",11),anchor='center')
                self.w.create_text((center_x,center_y-53),text=self.players[i].strategy,font=("Purisa",12),anchor='center')
                
                player = self.players[i]
                if(state==-1):
                    if((player.teamid == pid) or ((player.teamid in self.bidqueue) and (self.bidqueue.index(player.teamid)<self.bidqueue.index(pid)))):
                        if player.current_bid < 10:
                            self.w.create_image((center_x-37,center_y-8),image=self.numimage[0],anchor='center')
                            self.w.create_image((center_x,center_y-8),image=self.numimage[0],anchor='center')
                            self.w.create_image((center_x+37,center_y-8),image=self.numimage[int(str(player.current_bid)[0])],anchor='center')
                        elif player.current_bid < 100:
                            self.w.create_image((center_x-37,center_y-8),image=self.numimage[0],anchor='center')
                            self.w.create_image((center_x,center_y-8),image=self.numimage[int(str(player.current_bid)[0])],anchor='center')
                            self.w.create_image((center_x+37,center_y-8),image=self.numimage[int(str(player.current_bid)[1])],anchor='center')
                        else:
                            self.w.create_image((center_x-37,center_y-8),image=self.numimage[int(str(player.current_bid)[0])],anchor='center')
                            self.w.create_image((center_x,center_y-8),image=self.numimage[int(str(player.current_bid)[1])],anchor='center')
                            self.w.create_image((center_x+37,center_y-8),image=self.numimage[int(str(player.current_bid)[2])],anchor='center')
                    else:
                        self.w.create_image((center_x-37,center_y-8),image=self.numimage[-1],anchor='center')
                        self.w.create_image((center_x,center_y-8),image=self.numimage[-1],anchor='center')
                        self.w.create_image((center_x+37,center_y-8),image=self.numimage[-1],anchor='center')
                    if self.current_item in player.items:
                        (key,value) = (self.current_item,player.items[self.current_item])
                    else:
                        (key,value) = (self.current_item,0)
                    text_in = str(value) + "* "
                    self.w.create_text((center_x-35, center_y+36), text=text_in, font=("Purisa",15), justify='left', anchor='nw')
                    item = self.item_names[key]
                    self.w.create_oval((center_x-16, center_y +26, center_x + 16, center_y+36 + 20 + 3), fill=self.item_colors[key])
                    self.w.create_text((center_x + 1, center_y+40), text=item[0], justify='left', anchor='center')
                        
                elif state == 0:
                    if player.teamid in self.bidqueue:
                        self.w.create_image((center_x-37,center_y-8),image=self.numimage[-1],anchor='center')
                        self.w.create_image((center_x,center_y-8),image=self.numimage[-1],anchor='center')
                        self.w.create_image((center_x+37,center_y-8),image=self.numimage[-1],anchor='center')
                    else:        
                        self.w.create_image((center_x-37,center_y-8),image=self.numimage[10],anchor='center')
                        self.w.create_image((center_x,center_y-8),image=self.numimage[10],anchor='center')
                        self.w.create_image((center_x+37,center_y-8),image=self.numimage[10],anchor='center')
                    if self.current_item in player.items:
                        (key,value) = (self.current_item,player.items[self.current_item])
                    else:
                        (key,value) = (self.current_item,0)
                    text_in = str(value) + "* "
                    self.w.create_text((center_x-35, center_y+36), text=text_in, font=("Purisa",15), justify='left', anchor='nw')
                    item = self.item_names[key]
                    self.w.create_oval((center_x-16, center_y +26, center_x + 16, center_y+36 + 20 + 3), fill=self.item_colors[key])
                    self.w.create_text((center_x + 1, center_y+40), text=item[0], justify='left', anchor='center')
                        
                else:
                    self.w.create_image((center_x-37,center_y-8),image=self.numimage[10],anchor='center')
                    self.w.create_image((center_x,center_y-8),image=self.numimage[10],anchor='center')
                    self.w.create_image((center_x+37,center_y-8),image=self.numimage[10],anchor='center')
                    for (key, value) in sorted(player.items.iteritems(), key=operator.itemgetter(1), reverse=True)[:1]:
                        text_in = str(value) + "* "
                        self.w.create_text((center_x-35, center_y+36), text=text_in, font=("Purisa",15), justify='left', anchor='nw')
                        item = self.item_names[key]
                        self.w.create_oval((center_x-16, center_y +26, center_x + 16, center_y+36 + 20 + 3), fill=self.item_colors[key])
                        self.w.create_text((center_x + 1, center_y+40), text=item[0], justify='left', anchor='center')
                
                self.w.create_text((center_x,center_y+75),text="Time left:  " + str(player.time),font=("Purisa",11),anchor='center')
                
                i+=1
        
        
    def draw_scoreboard(self,end, pid=-1):
        self.w.create_line(5, 5, 600, 5)

        x_offset = 10
        y_offset = 10
        
        self.w.create_image(((self.width*3/4)+100,(self.height/6)+100),image=self.shasha,anchor='center')
          
        if(end==-1):
            # draw status
            text_in = 'Last item:'
            self.w.create_text((x_offset, y_offset), text=text_in, justify='left', anchor='nw')
            x_offset += len(text_in) * 6 + 5
            if(self.last_item > -1):
                item = self.item_names[self.last_item]
                self.w.create_oval((x_offset, y_offset + 1, x_offset + 12, y_offset + 3 + 10), fill=self.item_colors[self.last_item])
                self.w.create_text((x_offset + 2, y_offset), text=item[0], justify='left', anchor='nw')
                x_offset += 15
                self.w.create_text((x_offset, y_offset), text=item, justify='left', anchor='nw', fill=self.item_colors[self.last_item])
                x_offset += len(item) * 6 + 20  
            text_in = 'Last Winner:'
            self.w.create_text((x_offset, y_offset), text=text_in, justify='left', anchor='nw')
            x_offset += len(text_in) * 6 + 10
            if(self.last_winner > -1):
                self.w.create_text((x_offset, y_offset), text=self.last_winner, justify='left', anchor='nw')
            x_offset = 10
            y_offset += 30
            text_in = 'Next ' + str(min(int(self.goal), len(self.itemlist))) + ' items:'
            self.w.create_text((x_offset, y_offset), text=text_in, justify='left', anchor='nw')
            x_offset += len(text_in) * 6 + 20
            for i in range(min(int(self.goal), len(self.itemlist))):
                item = self.item_names[self.itemlist[i]]
                self.w.create_oval((x_offset, y_offset + 1, x_offset + 12, y_offset + 10 + 3), fill=self.item_colors[self.itemlist[i]])
                self.w.create_text((x_offset + 2, y_offset), text=item[0], justify='left', anchor='nw')
                x_offset += 15
                self.w.create_text((x_offset, y_offset), text=item, justify='left', anchor='nw', fill=self.item_colors[self.itemlist[i]])
                x_offset += len(item) * 6 + 20  

            y_offset += 27
            
            self.w.create_line(10, y_offset, 600, y_offset)
            
            y_offset += 27
            
            x_offset = 20
            text_in = 'Current item:'
            self.w.create_text((x_offset, y_offset), text=text_in, justify='left', anchor='nw')
            x_offset += len(text_in) * 6 + 20
            item = self.item_names[self.current_item]
            self.w.create_oval((x_offset, y_offset + 1, x_offset + 150, y_offset +150), fill=self.item_colors[self.current_item])
            self.w.create_text((x_offset + 75, y_offset +75), text=item[0], font=("Purisa",90), justify='left', anchor='center')
            x_offset += 170
            self.w.create_text((x_offset, y_offset+75), text=item, justify='left', font=("Purisa",30), anchor='w', fill=self.item_colors[self.current_item]) 
            y_offset += 150
        else:
            ranking = self.players[:]
            ranking.sort(key = lambda x: max(x.items.values(),0),reverse=True)
            for player in ranking:
                x_offset = 30
                text_in = player.teamname + ":"
                if(player.teamid == end):
                    text_in += 'WINNER'
                self.w.create_text((x_offset, y_offset), text=text_in, justify='left', anchor='nw', fill='red')
                x_offset = 230
                text_in = 'Items:'
                self.w.create_text((x_offset, y_offset), text=text_in, justify='left', anchor='nw')
                x_offset += len(text_in) * 6 + 20
                for (key, value) in sorted(player.items.iteritems(), key=operator.itemgetter(1), reverse=True)[:4]:
                    text_in = str(value) + "* "
                    self.w.create_text((x_offset, y_offset), text=text_in, justify='left', anchor='nw')
                    x_offset += len(text_in) * 6
                    item = self.item_names[key]
                    self.w.create_oval((x_offset, y_offset + 1, x_offset + 12, y_offset + 10 + 3), fill=self.item_colors[key])
                    self.w.create_text((x_offset + 1, y_offset), text=item[0], justify='left', anchor='nw')
                    x_offset += 15
                    self.w.create_text((x_offset, y_offset), text=item, justify='left', anchor='nw')
                    x_offset += len(item) * 6 + 20  
                x_offset = 100
                y_offset += 35
            
            self.w.create_line(10, y_offset, 600, y_offset)
            x_offset = 10
            y_offset += 5
            # draself.w.head
            x_offset += 400
            text_in = 'Goal: ' + str(self.goal) + ' similar items'
            self.w.create_text((x_offset, y_offset), text=text_in, justify='left', anchor='nw')
            y_offset += 20
        
        final_y = self.height/3 + (self.height - self.height/3)/4 - 83
        
        self.w.create_line(5, 5, 5, final_y)
        self.w.create_line(600, 5, 600, final_y)
        self.w.create_line(5, final_y, 600, final_y)
        self.w.update()
        
        
    #TODO: COMMUNICATION WITH SERVER - MAIN SCRIPT IS HERE
    #TODO: DISPLAY WINNER OF THE GAME
    #Overloaded function:
    #for every given bid: id,bid,time_used (for every team)
    #if item is won: id,-1 (only once for the winner)
    #if game is won: id only for the winner
    def update(self, pid, bid=-2, time_used=0):
        if bid >=0:
            self.bidqueue.append(pid)
            self.players[pid].update(bid,time_used)
            self.w.delete("all")
            self.set_podiums(0,pid)
            self.draw_scoreboard(-1,pid)
            self.w.update()
        elif bid==-1:
            for i in self.bidqueue:
                self.w.delete("all")
                self.set_podiums(-1,i)
                self.draw_scoreboard(-1,i)
                self.w.update()
                time.sleep(2)
            for i in range(len(self.players)):
                if i == pid:
                    self.players[i].update(0,0,self.current_item)
                    self.last_winner = self.players[i].teamname
                    self.last_item = self.current_item
                    self.current_item = self.itemlist.pop(0)
                else:
                    self.players[i].update(0,0)
            self.bidqueue = []
            self.w.delete("all")
            self.set_podiums(-2)
            self.draw_scoreboard(-2)
            self.w.update()
        elif bid == -2:
            self.w.delete("all")
            self.set_podiums(pid)
            self.draw_scoreboard(pid)
            self.w.update()

'''EXAMPLE'''
#Visualizer is created with goal of 3, 2 players and an itemlist
v = visualizer(3,[('Shrivelled Turtleman',120),('White Truffle',150),("john",120),("joe",120),("anna",120),('mark',120),('tom',150),("john",120),("joe",120),("anna",120),("anna",120)],[4,3,3,3,2,1,2,0,3,4])
#v = visualizer(3,[('Shrivelled Turtleman',120),('White Truffle',150)],[4,3,3,3,2,1,2,0,3,4])


v.update(0,10,15) #Player 0, Bid 10, Time used 15
time.sleep(2)
v.update(1,10,20) #Player 1, Bid 10, Time used 20
time.sleep(2)
v.update(0,-1) # Player 0 wins the item
time.sleep(2)
v.update(0,10,15) 
time.sleep(2)
v.update(1,15,20)
time.sleep(2)
v.update(1,-1)
time.sleep(2)
v.update(0,10,21)
time.sleep(2)
v.update(1,10,20)
time.sleep(2)
v.update(1,-1)
time.sleep(2)
v.update(0,10,15)
time.sleep(2)
v.update(1,10,10)
time.sleep(2)
v.update(1,-1)
v.update(1) #Player 0 wins the game
v.w.mainloop()