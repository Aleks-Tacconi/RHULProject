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

4. Export OPENAI_API_KEY:

    ```sh
    export OPENAI_API_KEY="your_api_key" # On Linux/MacOS
    $env:OPENAI_API_KEY="your_api_key"   # On Windows
    ```

5. Run the program:

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

### simplegui/components/buffs.py

- Handles the implementation of player buffs which can be chosen on the transition screen. These affect player stats

### simplegui/components/button.py

- Simple implementation of a Button obj using the CS2PySimpleGUI library. Allows for creating and placing buttons on the screen.

### simplegui/components/cutscene.py

- Handles rendering and dialog for displayed cutscenes 

### simplegui/components/interactables.py

- Implementation of an interactable object in the game. E.g. The portal which takes you to the next level

### simplegui/components/scoreboard.py

- Handles the logic for calculating the score which the player has gained per level.

### simplegui/components/subtitles.py

- Handles the rendering of the subtitiles for the cutscenes

### simplegui/components/xp.py

- Implementation of the experience system for the player, rewards the player for killing npcs

### simplegui/gameloops/gameloop.py

- Abstract base class which creates a simple template for implementing levels. This enforces functions such as keyhandlers are implemented and creates a mouse instance which can be used for handling mouse inputs. Also enforces a draw handler is provided.


