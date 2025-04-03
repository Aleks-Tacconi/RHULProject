## Info
- Python version - 3.13.1

## How to run
1. Clone the repository:

    ```sh
    git clone git@github.com:Aleks-Tacconi/RHULProject.git
    ```

2. Navigate to the repository:
    
    ```sh
    cd RHULProject
    ```

3. Create and source a virtual environment:

    ```sh
    python -m venv venv
    source venv/bin/activate # On Linux/MacOS
    .\venv\Scripts\activate  # On Windows
    ```

4. Install dependencies

    ```sh
    pip install -r requirements.txt
    ```

5. Export OPENAI_API_KEY:

    ```sh
    export OPENAI_API_KEY="your_api_key" # On Linux/MacOS
    $env:OPENAI_API_KEY="your_api_key"   # On Windows
    ```

6. Run the program:

    ```sh
    python main.py
    ```

## File Explanations 

### ai/ai.py

- Provides an interface to interact with the openAI api

### entities/abstract/enemy.py

- Abstract base class for representing an general enemy. This provides a template for implementing enemies in the game. Inherits from PhysicsEntity

### entities/abstract/entity.py

- Abstract base class for representing a in game entity. Enforces specific methods which every in game entity should contain. Topmost class in the class hierarchy for entity's

### entities/abstract/physics_entity.py

- Abstract base class for representing a PhysicsEntity. Enforces some methods each physics entity should contain aswell as implementing some methods which can be utilized by any physics entity, such as gravity and checking for collision

### entities/utils/animation.py

- Handles the logic for updating and rendering spritesheets

### entities/utils/playsounds.py

- Simple interface for playing audiofiles. Used for background music, dialog and sfx.

### entities/abyssal_revenant.py

- Handles the AI of then Abyssal Revenant enemy and how it interacts with the player

### entities/attack.py

- Creates a hitbox instance for the attack for each entity. This allows for implementation of different attacks.

### entities/background.py

- Handles rendering the background that has no collisions with player

### entities/block.py

- This allows for the rendering of blocks which can interact with any physics entity. Also provides an implementation of an optimised collision method which checks and handles the collision for the blocks around any provided implementation of a PhysicsEntity.

### entities/cinematic.py

- Handles the rendering of cinematic bars. Used during cutscenes / the tutorial.

### entities/demon_slime_boss.py

- Handles the functions of the final boss enemy.

### entities/evil_hand

- Handles the function of the evil hand enemy

### entities/evil_knight.py

- Handles the function of the evil knight enemy

### entities/fire.py

- Handles creation of vertical fire used by the boss and how they function.

### entities/fireball.py

- Handles horizontal fireballs used by the mage.py

### entities/flying_demon.py

- Handles the flying demon enemy logic

### entities/mage.py

- Handles mage enemy logic

### entities/player.py

- Handles player logic as well as keyboard controls from user.

### entities/player.healthbar.py

- handles the logic and rendering of the player health bar

### entities/teleport.py

- Handles teleport the player to the new coordinates

### entities/trigger.py

- Handles the trigger class with vectors.

### simplegui/components/buffs.py

- Handles the implementation of player buffs which can be chosen on the transition screen. These affect player stats.

### simplegui/components/button.py

- Simple implementation of a Button obj using the CS2PySimpleGUI library. Allows for creating and placing buttons on the screen.

### simplegui/components/cutscene.py

- Handles rendering and dialog for displayed cutscenes.

### simplegui/components/interactables.py

- Implementation of an interactable object in the game. E.g. The portal which takes you to the next level.

### simplegui/components/scoreboard.py

- Handles the logic for calculating the score which the player has gained per level.

### simplegui/components/subtitles.py

- Handles the rendering of the subtitiles for the cutscenes.

### simplegui/components/xp.py

- Implementation of the experience system for the player, rewards the player for killing npcs.

### simplegui/gameloops/abstract/gameloop.py

- Abstract base class which creates a simple template for implementing levels. This enforces functions such as keyhandlers are implemented and creates a mouse instance which can be used for handling mouse inputs. Also enforces a draw handler is provided.

### simplegui/gameloops/cutscene_one.py

- An implementation of a cutscene which plays upon starting the game. This provides some contextual information adding depth to the game.

### simplegui/gameloops/cutscene_screen.py

- Simple interface for creating cutscenes. Implements functionality such as subtitles with text-to-speech, rendering subtitles etc.

### simplegui/gameloops/leaderboard.py

- Displays a list of all users which have created accounts and their score in a sorted order. This adds a level of competitiveness to the game.

### simplegui/gameloops/level_editor.py

- A basic level editor which allows for easy creation of levels that can be played in the game. Provides functionality such as placing/removing block, placing/removing enemies and automatically saves changes made to the level.

### simplegui/gameloops/level_one.py / simplegui/gameloops/level_two.py / simplegui/gameloops/level_three.py

- Implementation of a level, This is the core of the game which encapsulates all the other components of the code. This level implementation creates a player instance, loads the respective level and implements a main gameloop which contains all the necessary interaction to make the game function.

### simplegui/gameloops/login.py

- This is the loginscreen which adds a graphical interface allowing the players to login to their respective accounts or create a new account.

### simplegui/gameloops/titlescreen.py

- This is the title screen which is rendered on launch and provides a way to access the other gameloop implementations 

### simplegui/gameloops/transition_screen.py

- This is the transition screen which gives the user the option to return to main menu or proceed to the next level or reset the level if the player dies. This is rendered when the player dies or successfully completes a level. This also adds the players score to their current score and overwrites their highscore if appropriate.

### simplegui/gameloops/tutorial.py

- This is a gameloop implementation similar to level one/two/three however it also features captions which explain how to play the game to the player, the score gained in this level does not get applied to the users total score.

### simplegui/gui.py

- This defines an easy way to control which gameloop is being rendered. This also sets up the key and mouse handlers for the newly rendered gameloop.

### utils/vector.py

- Class representing Vectors.

### utils/speech.py

- Provides functionality to speak into the microphone to convert voice into text.

### utils/score.py

- Handles login process and updates the score for each user when appropriate.

### utils/mouse.py

- Provides functionality for mouse interaction. Implemented in Abstract Base Class gameloop and can be used in any gameloop implementation in order to handle any mouse related functionality such as the implementation of buttons.
