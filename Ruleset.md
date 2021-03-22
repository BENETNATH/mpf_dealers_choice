Dealer's choive 2.0 Ruleset
---------------------------

Version : 0.1

Author : Benoit Petit-Demouliere

Source : https://github.com/BENETNATH/mpf_dealers_choice

Topic : https://pinside.com/pinball/forum/topic/trying-to-revive-an-old-em-dealer-s-choice-with-opp-and-mpf

Pinball : Dealer's Choice, Williams 1973

        4 players EM, 4 flippers, 3 bumpers
        10 rollovers, 8 standup targets
        a row of 10 lights playfield-centered between flippers

Comments: this is a first draft, need to be coded and adjusted !

---------------------------
I. CLASSICAL RULES
---------------------------
This ruleset is active by default and corresponds mostly to the initial rules, except the skill shot and ball save
3 balls played by each player

**BALL SERVE**

On ball serve, the 10 bonus lights are pulsating from 1 to 10 (Value written on playfield = 1000 to 10000)

***Skill shots*** :
* Simple skill shot:

        One random light is blinking among Top lane left, Top lane right, Top rollover, one of the 3 bumpers
        Value is 0.5 * the value of the light when the shot is made => up to 5000 Pts

* Hidden skill shot 1:

        Press left flipper button for 1 sec to discard skill shot lights, then shoot top right lane then directly "advance bonus" target
        Value is 1 * the value of the light when the shot is made => up to 10000 Pts

* Hidden skill shot 2:

        Press right flipper button for 1 sec to discard skill shot lights, then shoot top left lane then directly "SPECIAL" lane switch
        Value is 1 * the value of the light when the shot is made => up to 10000 Pts

***Ball save*** :
        During 8 sec, ball is given back as a ball saver

**INGAME**

***Single shots values*** :
- Rollover, bumper, top lanes : 100
- Outlanes : 		1000
- Right inlane : 	1000
- Special lane : 	1000
- Cards targets : 	200
- Advance Bonus targets : 150 + 1 bonus counter (add 1 light in bonus row)
- Top Rollover 		1000

***Group shot completion*** :
- Rollover :
    1. First times : 	2000 + lights Bonus double (x2 End Bonus)
	2. Second time : 	3500 + lights Bonus triple (x3 End bonus)
	3. Again : 			5000
- Target Cards (10, J, Q, K, A) :
	1. First time -> lights Extraball (right inlane)
	2. Second time -> lights Special (right top lane (Special)

***Extraball***:
- Shoot Right inlane when lit

***Special***: 
- Shoot Special lane when lit
	    Brings frenzy mode during 30 sec
	    All switches worth 10x
	    Chimes go crazy (TBD)
	
---------------------------
II. MODERN RULES
---------------------------
This ruleset is activated by keeping left flipper button when pressing start for the first player (mode is active for all players)

Unlimited balls played by each player for a duration of 2 min 30 per ball per player.
Timer starts on ball served and at the end of the timer, coils are turned off
9 missions to complete. They are off by default and represented by the lights in frontbox used for bonus lottery.
On ball serve, you choose the mission, once it's validated, it remains lit.
You need to complete all missions.
Each completed mission give you +30 sec on the Game timer.

***Ball serve*** :

    Flipper buttons navigate between each mission. 
    The mission is displayed via frontbox light (bonus lights 10 to 90)
    Mission start on first switch activated.
    Mission is lost after 3 ball drain and considered as completed (stays lit in frontbox)

***Missions*** :
* 10 - Bumper mania :
        you need to do 10 shot on each bumper to complete the mission
        When 10 shots are made on one bumper, this bumper is turned off
        Each bumper shot = 100
        Mission completed = 5000 and drain

* 20 - Cards by order :
        You need to shoot 10, then Jasper, then Queen, King and finally Ace, in the correct order.
        Other shoots are doing nothing
        Each card shot = 500
        Mission completed = 5000 and drain

* 30 - Reversed flippers :
        Left button activates Right flippers, and vice-versa
        You need to do all Card targets shots
        Each card shot = 100
        Mission completed = 5000 and drain

* 40 - Upside down :
        Left button activates Upper flippers
        Right button activates Lower flippers
        You need to do all Card targets shots
        Each card shot = 100
        Mission completed = 5000 and drain

* 50 - No Hold :
        You need to do all rollover (1-9)
        Flippers do not hold
        Each rollover shot = 100
        Mission completed = 5000 and drain

* 60 - Lanes :
        You need to do all lanes (yep, even outlanes)
        Each lane shot on the first time = 500
        Mission completed = 5000 and drain

* 70 -  Shooting range :
        Shoot the lit shot among targetrs and rollover. Complete once 10 shots are made
        Each card shot = 100
        Mission completed = 5000 and drain

* 80 - Tic Tac Toe :
        Shoot Rollover to lit a line of 3. 
        Rollin on a rollover switches between On and OFF
        Each rollover shot = 100
        Mission completed = 5000 and drain

* 90 - Slingshot contest :
        You need to activate 40 times slingshots
        Each slingshot shot = 100
        Mission completed = 5000 and drain


Once all missions are completed, you reach the Wizard mode

**WIZARD MODE !!**

Still to be considered..
